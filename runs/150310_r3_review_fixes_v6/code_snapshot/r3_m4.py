"""Robustness v3, M4: kept versus dropped markets (prereg_review_fixes.md section 4).

Descriptive table of all in-scope markets by group (kept and each drop_reason). Main contrast: kept against the
eligible-but-dropped (no_price, stale_price, below_min_trades). Calibration rows for the dropped markets that have a price.
No p-value except the Q1 row on stale_price, which carries Cohen's w.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from common import md_table, run_stage, write_json, write_manifest
from r3_common import flat, load_main_q1, main_net_gap, q1_row, row_line, stage_args, t_interval

STAGE = "r3_m4"
NUMERIC = ["volume_usdc", "volume_before_T1d", "duration_days", "n_trades", "n_trades_before_T1d"]


def iqr_cols(g: pd.DataFrame) -> dict:
    out = {}
    for c in NUMERIC:
        q = g[c].quantile([0.25, 0.5, 0.75])
        out |= {f"{c}_q25": float(q[0.25]), f"{c}_median": float(q[0.5]), f"{c}_q75": float(q[0.75])}
    return out


def group_row(name: str, g: pd.DataFrame, total: int, cat_levels: list[str]) -> dict:
    shares = g["cat8"].value_counts(normalize=True)
    row = {"group": name, "n": len(g), "share_of_total": len(g) / total}
    row |= {f"cat_{c}": float(shares.get(c, 0.0)) for c in cat_levels}
    row |= iqr_cols(g)
    row["outcome1_rate"] = float(g["y"].mean()) if g["y"].notna().any() else None
    return row


def calibration(g: pd.DataFrame, alpha: float) -> dict:
    d = g.dropna(subset=["p_1d", "y"])
    t = t_interval((d["y"] - d["p_1d"]).to_numpy(), alpha)
    return {"n": t["n"], "net_gap": t["mean"], "net_gap_ci_low": t["ci_low"], "net_gap_ci_high": t["ci_high"],
            "mean_sq_residual": float(((d["y"] - d["p_1d"]) ** 2).mean())}


def draw(table: pd.DataFrame, out) -> None:
    fig, ax = plt.subplots(figsize=(7, 4), layout="constrained")
    ax.bar(table["group"], table["share_of_total"], color="#555555", label="Share of 688,131 in-scope markets")
    ax.set(ylabel="Share of markets", xlabel="Group (kept or first failing rule)")
    ax.tick_params(axis="x", rotation=30)
    ax.grid(axis="y", alpha=0.3)
    fig.legend(loc="outside upper center", ncol=1)
    fig.savefig(out / "fig_r3_m4_kept_vs_dropped.png", dpi=150)
    plt.close(fig)


def main() -> None:
    _, out, src, params = stage_args()
    alpha, n_bins = float(params["alpha"]), int(params["n_bins"])

    def work() -> dict[str, str]:
        m = pd.read_parquet(out / "r3_markets.parquet")
        total = len(m)
        m["group"] = np.where(m["kept"], "kept", m["drop_reason"])
        m["duration_days"] = (pd.to_datetime(m["close_at"]) - pd.to_datetime(m["opens_at"])).dt.total_seconds() / 86400
        cat = m["category_refined"].fillna("Unknown").astype(str)
        top = cat[m["kept"]].value_counts().head(int(params["m4_top_categories"])).index
        m["cat8"] = cat.where(cat.isin(top), "Other")
        levels = [*top, "Other"]
        order = ["kept", "updown", "non_binary", "no_outcome", "no_price", "stale_price", "below_min_trades"]
        eligible = m[m["group"].isin(params["m4_eligible_dropped"])]
        rows = [group_row(g, m[m["group"] == g], total, levels) for g in order if (m["group"] == g).any()]
        rows.append(group_row("eligible_dropped_pooled", eligible, total, levels))
        table = pd.DataFrame(rows)
        table.to_csv(out / "m4_kept_vs_dropped.csv", index=False)

        main_res = load_main_q1(src)
        kept = m[m["kept"]].assign(y=lambda d: d["y"].astype(int))
        gap0 = main_net_gap(kept)
        calib = {g: calibration(m[m["group"] == g], alpha) for g in ["stale_price", "below_min_trades"] if (m["group"] == g).any()}
        stale = m[(m["group"] == "stale_price") & m["y"].notna() & m["p_1d"].notna()].assign(y=lambda d: d["y"].astype(int))
        stale_row, _ = q1_row(stale, "p_1d", alpha, n_bins, main_res, gap0)
        results = {"n_in_scope": total, "category_levels": levels, "groups": rows, "calibration": calib, "stale_price_q1": stale_row}
        for r in rows:
            results |= {f"{r['group']}_{k}": v for k, v in r.items() if k != "group" and not k.startswith("cat_")}
        for g, c in calib.items():
            results |= flat(f"calib_{g}", c)
        results |= flat("stale_q1", stale_row)
        write_json(out / "m4_results.json", results)
        draw(table, out)
        write_manifest(out, params, {k: v for k, v in results.items() if k not in ("groups",)}, __file__, STAGE)
        short = table[["group", "n", "share_of_total", "volume_before_T1d_median", "duration_days_median", "n_trades_median",
                       "outcome1_rate"]]
        calib_tab = pd.DataFrame([{"group": g, **c} for g, c in calib.items()])
        return {
            "Why": "M4: only 47,948 of 688,131 markets stay. Does the kept set differ from the markets that were dropped?",
            "Input data": f"{total} in-scope markets (r3_markets.parquet, drop_reason). Volume before T - 1 day from the raw pass. Real data.",
            "Output data": "m4_kept_vs_dropped.csv, m4_results.json, fig_r3_m4_kept_vs_dropped.png",
            "Result": md_table(short) + "\n\nCalibration of dropped markets that have a price (net gap with t interval, mean squared residual):\n\n"
                      + md_table(calib_tab) + "\n\nQ1 analysis on stale_price (w next to p):\n\n" + md_table(pd.DataFrame([row_line("stale_price", stale_row)]))
                      + "\n\nDescriptive. Medians and interquartile ranges carry the comparison (all columns in the CSV).",
            "Figure": "![m4](fig_r3_m4_kept_vs_dropped.png)  Caption: share of in-scope markets by group. "
                      "Why: it shows how much of the market set each drop rule removes. Source: this run folder.",
        }

    run_stage(out, STAGE, "M4: kept versus dropped markets.", work)


if __name__ == "__main__":
    main()
