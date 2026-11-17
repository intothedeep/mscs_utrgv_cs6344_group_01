"""Robustness v3, peer asks (prereg_review_fixes.md section 7): (a) volume tercile, (b) close period.

Descriptive, no verdict. Volume = sum of usdc_amount with ts <= T - 1 day (no look-ahead), from r3_markets.parquet.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests

from common import md_table, run_stage, write_json, write_manifest
from r3_common import bin_gaps, flat, load_kept, load_main_q1, main_net_gap, q1_row, row_line, stage_args

STAGE = "r3_peer"
TERCILES = ["low", "mid", "high"]


def assign_terciles(v: pd.Series) -> tuple[pd.Series, float, float]:
    """Cut points at the 1/3 and 2/3 quantiles. Ties go to the lower tercile: low v <= q1, mid q1 < v <= q2, high v > q2."""
    q1, q2 = float(v.quantile(1 / 3)), float(v.quantile(2 / 3))
    return pd.Series(np.where(v <= q1, "low", np.where(v <= q2, "mid", "high")), index=v.index), q1, q2


def merge_years(counts: pd.Series, min_n: int) -> dict[int, str]:
    """A year below min_n merges into the next later year until the group has min_n. The last group merges backward."""
    groups: list[list[int]] = []
    cur: list[int] = []
    total = 0
    for year, n in counts.sort_index().items():
        cur.append(int(year))
        total += int(n)
        if total >= min_n:
            groups.append(cur)
            cur, total = [], 0
    if cur:
        if groups:
            groups[-1] += cur
        else:
            groups.append(cur)
    return {y: (str(g[0]) if len(g) == 1 else f"{g[0]}-{g[-1]}") for g in groups for y in g}


def welch(a: np.ndarray, b: np.ndarray, alpha: float) -> dict:
    res = stats.ttest_ind(a, b, equal_var=False)
    ci = res.confidence_interval(1 - alpha)
    pooled = np.sqrt((a.var(ddof=1) + b.var(ddof=1)) / 2)
    return {"diff": float(a.mean() - b.mean()), "ci_low": float(ci.low), "ci_high": float(ci.high), "t": float(res.statistic),
            "p": float(res.pvalue), "cohens_d": float((a.mean() - b.mean()) / pooled)}


def draw(rows: dict[str, dict], title_x: str, file: str, out) -> None:
    fig, ax = plt.subplots(figsize=(7, 3.6), layout="constrained")
    for i, (nm, r) in enumerate(rows.items()):
        ax.errorbar(r["net_gap"], i, xerr=[[r["net_gap"] - r["net_gap_ci_low"]], [r["net_gap_ci_high"] - r["net_gap"]]],
                    fmt="o", color="#222222", capsize=3, label="Net gap with 95% t interval" if i == 0 else None)
    ax.axvline(0, color="#888888", ls="--", label="No gap")
    ax.set(yticks=range(len(rows)), yticklabels=[f"{n} (n={r['n']})" for n, r in rows.items()], xlabel="Net gap mean(y - p_1d) (USDC per share)",
           ylabel=title_x)
    ax.invert_yaxis()
    ax.grid(alpha=0.3)
    fig.legend(loc="outside upper center", ncol=2)
    fig.savefig(out / file, dpi=150)
    plt.close(fig)


def volume_part(kept: pd.DataFrame, out, alpha: float, n_bins: int, main_res: dict, gap0: float, small_n: int) -> tuple[dict, dict, str]:
    kept = kept.dropna(subset=["volume_before_T1d"]).copy()
    kept["tercile"], q1, q2 = assign_terciles(kept["volume_before_T1d"])
    rows, cells = {}, []
    for t in TERCILES:
        g = kept[kept["tercile"] == t]
        rows[t], bins = q1_row(g, "p_1d", alpha, n_bins, main_res, gap0)
        gaps = bin_gaps(bins, alpha)
        cells.append(gaps.assign(tercile=t, small=gaps["n"] < small_n))
    pd.concat(cells).to_csv(out / "peer_a_volume_x_odds.csv", index=False)
    bh = multipletests([rows[t]["p"] for t in TERCILES], alpha=alpha, method="fdr_bh")[1]
    for t, p_bh in zip(TERCILES, bh):
        rows[t]["p_bh"] = float(p_bh)
    resid = (kept["y"] - kept["p_1d"]).to_numpy(float)
    hl = welch(resid[(kept["tercile"] == "high").to_numpy()], resid[(kept["tercile"] == "low").to_numpy()], alpha)
    res = {"cut_low_mid": q1, "cut_mid_high": q2, "n_with_volume": len(kept), "high_vs_low": hl} | flat("high_vs_low", hl)
    for t in TERCILES:
        res |= flat(f"tercile_{t}", rows[t])
    tab = md_table(pd.DataFrame([row_line(t, rows[t]) | {"p_bh": rows[t]["p_bh"]} for t in TERCILES]))
    return rows, res, tab + f"\n\nCut points (USDC before T - 1 day): {q1:.2f}, {q2:.2f}. High minus low net gap (Welch): {hl}."


def period_part(kept: pd.DataFrame, alpha: float, n_bins: int, main_res: dict, gap0: float, min_n: int) -> tuple[dict, dict, str]:
    kept = kept.copy()
    kept["year"] = pd.to_datetime(kept["close_at"]).dt.year
    mapping = merge_years(kept["year"].value_counts(), min_n)
    kept["period"] = kept["year"].map(mapping)
    rows = {}
    for per in sorted(kept["period"].unique()):
        rows[per], _ = q1_row(kept[kept["period"] == per], "p_1d", alpha, n_bins, main_res, gap0)
    bh = multipletests([r["p"] for r in rows.values()], alpha=alpha, method="fdr_bh")[1] if len(rows) > 1 else [rows[next(iter(rows))]["p"]]
    for r, p_bh in zip(rows.values(), bh):
        r["p_bh"] = float(p_bh)
    res: dict = {"year_to_period": {str(k): v for k, v in mapping.items()}, "n_periods": len(rows)}
    for per, r in rows.items():
        res |= flat(f"period_{per}", r)
    tab = md_table(pd.DataFrame([row_line(per, r) | {"p_bh": r["p_bh"]} for per, r in rows.items()]))
    return rows, res, tab + f"\n\nYear to period: {res['year_to_period']}."


def main() -> None:
    _, out, src, params = stage_args()
    alpha, n_bins = float(params["alpha"]), int(params["n_bins"])

    def work() -> dict[str, str]:
        kept = load_kept(out)
        main_res = load_main_q1(src)
        gap0 = main_net_gap(kept)
        rows_a, res_a, tab_a = volume_part(kept, out, alpha, n_bins, main_res, gap0, int(params["peer_a_small_cell_n"]))
        rows_b, res_b, tab_b = period_part(kept, alpha, n_bins, main_res, gap0, int(params["peer_b_min_group_n"]))
        write_json(out / "peer_a_results.json", res_a)
        write_json(out / "peer_b_results.json", res_b)
        draw(rows_a, "Volume tercile before T - 1 day", "fig_r3_peer_a_volume.png", out)
        draw(rows_b, "Calendar year of close_at (UTC)", "fig_r3_peer_b_period.png", out)
        write_manifest(out, params, {"peer_a": res_a, "peer_b": res_b}, __file__, STAGE)
        return {
            "Why": "Peer asks: does the gap depend on volume (Gorabi) or on the period (Molina)?",
            "Input data": f"{len(kept)} kept markets. Volume before T - 1 day from the raw pass. Real data.",
            "Output data": "peer_a_results.json, peer_a_volume_x_odds.csv (3 terciles x 10 bins, cells with n < 30 marked small), "
                           "peer_b_results.json, fig_r3_peer_a_volume.png, fig_r3_peer_b_period.png",
            "Result": "(a) Volume tercile (BH over 3 chi-square p-values):\n\n" + tab_a + "\n\n(b) Close period (BH over the period p-values):\n\n"
                      + tab_b + "\n\nDescriptive, no verdict.",
            "Figure": "![peer a](fig_r3_peer_a_volume.png) ![peer b](fig_r3_peer_b_period.png)  Caption: net gap with 95% t interval "
                      "per volume tercile and per close period. Why: intervals that overlap mean no sign that the gap changes. "
                      "Source: this run folder.",
        }

    run_stage(out, STAGE, "Peer asks: volume tercile and close period.", work)


if __name__ == "__main__":
    main()
