"""Robustness R1 (D-013): split payouts. Join the kept markets to CTF/resolutions.parquet, classify the payout,
check our Yes label against the resolutions winner, and re-run the Q1 analysis without the unclear markets.

Descriptive. The sensitivity row sits next to the Q1 row and never replaces it. Criteria: analysis/prereg_robustness.md.
"""
import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from common import DATA_ROOT, connect, load_params, md_table, run_stage, write_json, write_manifest
from q1_calibration import analyze, wilson
from verdicts import q1 as q1_rule

STAGE = "r1_split_payout"
CLASSES = ["clean", "split", "other", "missing"]


def parse_vector(raw: object) -> tuple[float, ...]:
    """Payout strings to floats. A failed cast gives NaN, which makes the market class 'other'."""
    if raw is None:
        return ()
    out = []
    for x in raw:
        try:
            out.append(float(x))
        except (TypeError, ValueError):
            out.append(float("nan"))
    return tuple(out)


def classify(vectors: set[tuple[float, ...]]) -> tuple[str, int | None]:
    """Class and winner index (clean only) from the DISTINCT payout vectors of one condition_id."""
    if not vectors:
        return "missing", None
    if len(vectors) > 1:
        return "other", None   # duplicate rows disagree
    vec = next(iter(vectors))
    if any(x != x for x in vec) or len(vec) < 2:
        return "other", None
    if len(vec) == 2 and sorted(vec) == [0.0, 1.0]:
        return "clean", vec.index(1.0)
    if vec[0] > 0 and len(set(vec)) == 1:
        return "split", None
    return "other", None


def load_resolutions(con, kept_ids: pd.DataFrame) -> tuple[dict[str, set], dict[str, int], dict]:
    """Payout vectors per kept market, and the duplicate counts. Join key: lower(condition_id)."""
    path = DATA_ROOT / "CTF" / "resolutions.parquet"
    con.register("kept_ids", kept_ids)
    total, distinct = con.execute(
        f"SELECT count(*), count(DISTINCT lower(condition_id)) FROM read_parquet('{path}')").fetchone()
    rows = con.execute(f"""
        SELECT lower(r.condition_id) AS cid, r.payout_numerators AS pn
        FROM read_parquet('{path}') r SEMI JOIN kept_ids k ON lower(r.condition_id) = lower(k.market_id)""").fetchall()
    vectors: dict[str, set] = {}
    n_rows: dict[str, int] = {}
    for cid, pn in rows:
        vectors.setdefault(cid, set()).add(parse_vector(pn))
        n_rows[cid] = n_rows.get(cid, 0) + 1
    dup_ids = [c for c, n in n_rows.items() if n > 1]
    dups = {"resolutions_rows": int(total), "resolutions_distinct_ids": int(distinct),
            "kept_ids_with_rows": len(n_rows), "kept_ids_with_duplicate_rows": len(dup_ids),
            "kept_duplicates_identical": sum(len(vectors[c]) == 1 for c in dup_ids),
            "kept_duplicates_conflicting": sum(len(vectors[c]) > 1 for c in dup_ids)}
    return vectors, n_rows, dups


def choose_mapping(agree_index0: float, yes_index: int, agree_min: float) -> int | None:
    """Prereg rule: keep the primary index if agreement >= agree_min, flip it if agreement <= 1 - agree_min, else none."""
    if agree_index0 >= agree_min:
        return yes_index
    if 1 - agree_index0 >= agree_min:
        return 1 - yes_index
    return None


def draw_figure(counts: dict, orig_bins: pd.DataFrame, sens_bins: pd.DataFrame, out: Path) -> None:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5), layout="constrained")
    ax1.bar(CLASSES, [counts.get(c, 0) for c in CLASSES], color="#555555")
    ax1.set_yscale("log")
    ax1.set(xlabel="Payout class of the kept market", ylabel="Markets (count, log scale)")
    ax1.grid(axis="y", alpha=0.3)
    ax2.plot([0, 1], [0, 1], color="#888888", ls="--", label="Perfect calibration")
    for name, b, color, dx in [("Q1 original (all kept)", orig_bins, "#222222", 0.0),
                               ("Sensitivity (minus split, other, mismatch)", sens_bins, "#aa5500", 0.006)]:
        ax2.plot(b["mean_price"] + dx, b["observed_rate"], "o", ms=4, color=color, label=name)
    ax2.set(xlabel="Mean price p_1d in bin (USDC per share)", ylabel="Observed Yes rate", xlim=(0, 1), ylim=(0, 1))
    ax2.grid(alpha=0.3)
    fig.legend(loc="outside upper center", ncol=3)
    fig.savefig(out / "fig_r1_split_payout.png", dpi=150)
    plt.close(fig)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--params", required=True)
    ap.add_argument("--out", default=".")
    args = ap.parse_args()
    out, params = Path(args.out), load_params(args.params)
    n_bins, alpha = int(params["n_bins"]), float(params["alpha"])
    agree_min, yes_index = float(params["robust_agree_min"]), int(params["robust_yes_payout_index"])

    def work() -> dict[str, str]:
        m = pd.read_parquet(out / "markets.parquet")
        kept = m[m["kept"]][["market_id", "p_1d", "y"]].sort_values("market_id").reset_index(drop=True)
        kept["y"] = kept["y"].astype(int)
        con = connect()
        vectors, n_rows, info = load_resolutions(con, kept[["market_id"]])
        cls = [classify(vectors.get(i.lower(), set())) for i in kept["market_id"]]
        kept["res_class"] = [c for c, _ in cls]
        kept["res_winner_index"] = pd.array([w for _, w in cls], dtype="Int64")
        kept["res_rows"] = [n_rows.get(i.lower(), 0) for i in kept["market_id"]]
        counts = kept["res_class"].value_counts().to_dict()

        clean = kept[kept["res_class"] == "clean"]
        n_clean = len(clean)
        agree0 = float(((clean["res_winner_index"] == yes_index) == (clean["y"] == 1)).mean()) if n_clean else float("nan")
        used = choose_mapping(agree0, yes_index, agree_min) if n_clean else None
        kept["y_resolutions"] = pd.array([int(w == used) if used is not None and pd.notna(w) else pd.NA
                                          for w in kept["res_winner_index"]], dtype="Int64")
        kept["mismatch"] = (kept["y_resolutions"].notna() & (kept["y_resolutions"] != kept["y"])).fillna(False).astype(bool)
        n_agree = int(round(agree0 * n_clean)) if n_clean else 0
        lo, hi = wilson(n_agree, n_clean, alpha) if n_clean else (float("nan"), float("nan"))
        kept["excluded"] = kept["res_class"].isin(["split", "other"]) | kept["mismatch"]

        sub = kept[~kept["excluded"]]
        if len(sub) < 20:
            raise ValueError(f"only {len(sub)} markets left for the sensitivity row")
        res_sens, bins_sens, _ = analyze(sub[["market_id", "p_1d", "y"]], n_bins, alpha)
        res_orig = json.loads((out / "q1_results.json").read_text())["main_with_min_filter"]
        if res_orig["n_markets"] != len(kept):
            raise ValueError(f"q1_results.json has {res_orig['n_markets']} markets, markets.parquet has {len(kept)} kept")
        rule_orig = q1_rule({"main_with_min_filter": res_orig}, alpha)["verdict"]
        rule_sens = q1_rule({"main_with_min_filter": res_sens}, alpha)["verdict"]
        same = rule_orig == rule_sens

        kept[["market_id", "p_1d", "y", "res_class", "res_rows", "res_winner_index", "y_resolutions", "mismatch",
              "excluded"]].to_csv(out / "r1_markets.csv", index=False)   # one row per kept market, sorted by market_id
        split_y = kept[kept["res_class"] == "split"]["y"].value_counts().to_dict()
        results = {
            "n_kept": len(kept), "class_counts": {c: int(counts.get(c, 0)) for c in CLASSES},
            "class_shares": {c: counts.get(c, 0) / len(kept) for c in CLASSES}, "duplicates": info,
            "our_y_on_split_markets": {"y1": int(split_y.get(1, 0)), "y0": int(split_y.get(0, 0))},
            "mapping": {"yes_index_primary": yes_index, "n_clean": n_clean, "agreement_index_primary": agree0,
                        "agreement_index_other": 1 - agree0 if n_clean else None, "agreement_ci95": [lo, hi],
                        "index_used": used, "validated": used is not None, "agree_min": agree_min,
                        "n_mismatch": int(kept["mismatch"].sum())},
            "sensitivity": {"n_excluded": int(kept["excluded"].sum()), "n_markets": len(sub),
                            "q1_original": res_orig, "q1_sensitivity": res_sens,
                            "rule_result_original": rule_orig, "rule_result_sensitivity": rule_sens,
                            "rule_results_same": same,
                            "delta_effect_w": res_sens["chi2_gof"]["effect_w"] - res_orig["chi2_gof"]["effect_w"]},
        }
        write_json(out / "r1_results.json", results)
        draw_figure(results["class_counts"], pd.read_csv(out / "q1_bins.csv"), bins_sens, out)
        write_manifest(out, params, {k: v for k, v in results.items() if k != "sensitivity"}
                       | {"sensitivity_rule_results_same": same}, __file__, STAGE)
        tab = pd.DataFrame({"class": CLASSES, "markets": [results["class_counts"][c] for c in CLASSES],
                            "share": [results["class_shares"][c] for c in CLASSES]})
        c_o, c_s = res_orig["chi2_gof"], res_sens["chi2_gof"]
        sens = pd.DataFrame({"metric": ["n markets", "chi2 (df)", "p", "Cohen's w", "Brier", "bins off (BH)", "Q1 rule result"],
                             "Q1 original": [res_orig["n_markets"], f"{c_o['chi2']:.1f} ({c_o['df']})", c_o["p"], c_o["effect_w"],
                                             res_orig["brier"], res_orig["bins_reject_bh"], rule_orig],
                             "sensitivity": [res_sens["n_markets"], f"{c_s['chi2']:.1f} ({c_s['df']})", c_s["p"], c_s["effect_w"],
                                             res_sens["brier"], res_sens["bins_reject_bh"], rule_sens]})
        return {
            "Why": "D-013: does the Q1 result hold when split, other and mismatching payouts are removed?",
            "Input data": f"markets.parquet: {len(kept)} kept markets. {DATA_ROOT / 'CTF' / 'resolutions.parquet'}: "
                          f"{info['resolutions_rows']} rows. Real data.",
            "Output data": "r1_markets.csv (one row per kept market), r1_results.json, fig_r1_split_payout.png",
            "Result": md_table(tab) + f"\n\nDuplicates among kept ids: {info['kept_ids_with_duplicate_rows']} "
                      f"({info['kept_duplicates_identical']} identical, {info['kept_duplicates_conflicting']} conflicting).\n\n"
                      f"Agreement of our y with the resolutions winner (index {yes_index}): {agree0:.4f} on {n_clean} clean markets "
                      f"(95% Wilson CI {lo:.4f} to {hi:.4f}). Index used: {used}. Mismatches: {int(kept['mismatch'].sum())}.\n\n"
                      + md_table(sens) + f"\n\nQ1 rule results the same: {same}. Change in w: {results['sensitivity']['delta_effect_w']:.4g}.",
            "Figure": "![r1](fig_r1_split_payout.png)  Caption: kept markets by payout class (log scale), and the Q1 "
                      "calibration points with and without the unclear markets. Why: points that overlap mean the "
                      "unclear markets do not move the result. Source: this run folder.",
        }

    run_stage(out, STAGE, "R1: split payouts and a Q1 sensitivity row.", work)


if __name__ == "__main__":
    main()
