"""Robustness v3, M2: Yes-oriented calibration (prereg_review_fixes.md section 2).

Splits the kept markets into Yes/No markets (Y) and all other markets (N) and runs the Q1 analysis on each, with the price
and outcome oriented on the "Yes" side. A sensitivity row only: it makes a wording proposal and never changes D-037.
Label 1 comes from the saved label check (runs/150296_v1label), label 2 from r3_markets.parquet.
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from common import md_table, run_stage, write_json, write_manifest
from r3_common import bin_gaps, bin_of, flat, load_kept, load_main_q1, main_net_gap, q1_row, row_line, stage_args

STAGE = "r3_m2"


def normalize(label: pd.Series) -> pd.Series:
    """lower(trim()), inner whitespace collapsed (prereg_v1_label_check.md 2.2). NULL stays NULL."""
    return label.str.strip().str.lower().str.replace(r"\s+", " ", regex=True)


def draw_reliability(bins: pd.DataFrame, n: int, out: Path) -> None:
    fig, ax = plt.subplots(figsize=(6, 6), layout="constrained")
    ax.plot([0, 1], [0, 1], color="#888888", ls="--", label="Perfect calibration")
    err = np.clip(np.vstack([bins["observed_rate"] - bins["ci_low"], bins["ci_high"] - bins["observed_rate"]]), 0, None)
    ax.errorbar(bins["mean_price"], bins["observed_rate"], yerr=err, fmt="o", ms=4, capsize=3, color="#222222",
                label=f"Yes/No markets (n={n}), 95% Wilson interval")
    ax.set(xlabel="Mean Yes price in bin (USDC per share)", ylabel="Observed Yes rate", xlim=(0, 1), ylim=(0, 1))
    ax.grid(alpha=0.3)
    fig.legend(loc="outside upper center", ncol=1)
    fig.savefig(out / "fig_r3_m2_yes_reliability.png", dpi=150)
    plt.close(fig)


def main() -> None:
    args, out, src, params = stage_args()
    alpha, n_bins = float(params["alpha"]), int(params["n_bins"])
    label_dir = Path(args.label_run)

    def work() -> dict[str, str]:
        kept = load_kept(out)
        main_res = load_main_q1(src)
        gap0 = main_net_gap(kept)
        saved = pd.read_csv(label_dir / "label1_by_market.csv", usecols=["market_id", "label_norm"])
        counts = json.loads((label_dir / "label1_counts.json").read_text())
        df = kept.merge(saved, on="market_id", how="left", validate="one_to_one")
        df["label1_norm"] = df["label_norm"]
        df["label2_norm"] = normalize(df["label2"])
        n_label_mismatch = int((df["label1_norm"].fillna("") != normalize(df["label1"]).fillna("")).sum())
        yes1, yes2 = df["label1_norm"].eq("yes"), df["label2_norm"].eq("yes")
        df["is_yes_no"] = (yes1 & df["label2_norm"].eq("no")) | (yes2 & df["label1_norm"].eq("no"))
        df["p_yes"] = np.where(yes1, df["p_1d"], np.where(yes2, 1 - df["p_1d"], np.nan))
        df["y_yes"] = np.where(yes1, df["y"], np.where(yes2, 1 - df["y"], -1)).astype(int)
        df["bin_yes"] = np.where(df["is_yes_no"], bin_of(df["p_yes"].fillna(0).to_numpy(), n_bins), -1)
        df[["market_id", "label1_norm", "label2_norm", "is_yes_no", "p_yes", "y_yes", "bin_yes"]].to_csv(
            out / "m2_yes_by_market.csv", index=False)

        yset = df[df["is_yes_no"]].assign(y=lambda d: d["y_yes"])
        nset = df[~df["is_yes_no"]]
        row_y, bins_y = q1_row(yset, "p_yes", alpha, n_bins, main_res, gap0)
        row_n, bins_n = q1_row(nset, "p_1d", alpha, n_bins, main_res, gap0)
        gaps_y, gaps_n = bin_gaps(bins_y, alpha), bin_gaps(bins_n, alpha)
        gaps_y.to_csv(out / "m2_bins_yes_no.csv", index=False)
        gaps_n.to_csv(out / "m2_bins_other.csv", index=False)

        n_yes_like = int(counts["overall"]["n_yes_like"])
        l2_for_yes = df.loc[yes1, "label2_norm"].fillna("(null)").value_counts().to_dict()
        n_label2_not_no = int(yes1.sum() - l2_for_yes.get("no", 0))
        scaled = yset["p_yes"] * n_bins
        n_inner = int(((scaled == scaled.round()) & (scaled.round() >= 1) & (scaled.round() <= n_bins - 1)).sum())
        yes_bias = bool(row_y["p"] < alpha and row_y["net_gap_ci_high"] < 0)
        results = {"n_yes_no": len(yset), "n_other": len(nset), "n_label1_yes": int(yes1.sum()), "n_label2_yes": int(yes2.sum()),
                   "n_yes_like_label_check": n_yes_like, "n_label2_not_no_for_label1_yes": n_label2_not_no,
                   "check_n_yes_no_ge_expected": len(yset) >= n_yes_like - n_label2_not_no,
                   "label2_values_for_label1_yes": l2_for_yes, "n_label1_mismatch_vs_label_check": n_label_mismatch,
                   "n_p1d_on_inner_edge_yes_no": n_inner, "yes_bias": yes_bias,
                   "wording": ("In Yes/No markets, Yes is priced above its observed rate (proposal only, D-037 stays)"
                               if yes_bias else "keep 'outcome 1' only")} | flat("yes_no", row_y) | flat("other", row_n)
        results["bins_yes_no"] = gaps_y.to_dict("records")
        results["bins_other"] = gaps_n.to_dict("records")
        write_json(out / "m2_results.json", results)
        draw_reliability(bins_y, len(yset), out)
        write_manifest(out, params, {k: v for k, v in results.items() if not k.startswith("bins_")}, __file__, STAGE)
        tab = pd.DataFrame([row_line("Yes/No markets", row_y), row_line("Other markets", row_n)])
        return {
            "Why": "M2: 'outcome 1 is priced too high' mixes Yes/No markets with team-name markets. Is there a Yes-bias in Yes/No markets?",
            "Input data": f"{len(kept)} kept markets. Label 1 from {label_dir.name}/label1_by_market.csv, label 2 rebuilt from raw. Real data.",
            "Output data": "m2_yes_by_market.csv, m2_bins_yes_no.csv, m2_bins_other.csv, m2_results.json, fig_r3_m2_yes_reliability.png",
            "Result": md_table(tab) + f"\n\nReading: {results['wording']}. Label 2 values where label 1 is yes: {l2_for_yes}. "
                      f"n(Y) {len(yset)} against the check bound {n_yes_like - n_label2_not_no}. Wilson intervals are "
                      f"{'outside the lectures (D-039)'}; the z interval sits next to them in m2_bins_*.csv.\n\n"
                      + md_table(gaps_y.round(4)),
            "Figure": "![m2](fig_r3_m2_yes_reliability.png)  Caption: observed Yes rate against mean Yes price in Yes/No markets. "
                      "Why: points below the diagonal mean Yes is priced above its observed rate. Source: this run folder.",
        }

    run_stage(out, STAGE, "M2: Yes-oriented calibration.", work)


if __name__ == "__main__":
    main()
