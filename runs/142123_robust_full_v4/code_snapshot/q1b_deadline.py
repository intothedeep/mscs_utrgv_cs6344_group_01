"""MVP2 Q1b: does the market get smarter near the deadline? Price at T - 7 d against price at T - 1 d.

Population = kept markets (min_trades filter) that opened at least 7 days before T and have a fresh p_7d.
Same markets at both horizons, so the comparison is paired.
"""
import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

from common import load_params, md_table, run_stage, write_json, write_manifest
from q1_calibration import LOG_CLIP

STAGE = "q1b_deadline"
COLORS = {"Resolved Yes": "#222222", "Resolved No": "#aa5500"}


def entropy_bits(p: np.ndarray) -> np.ndarray:
    pc = np.clip(p, LOG_CLIP, 1 - LOG_CLIP)
    return -(pc * np.log2(pc) + (1 - pc) * np.log2(1 - pc))


def one_sample_t(diff: np.ndarray, alpha: float) -> dict:
    """One-sample t-test of diff against 0, mean with (1 - alpha) CI, Cohen's d = mean / sd."""
    n, mean, sd = len(diff), float(diff.mean()), float(diff.std(ddof=1))
    t = stats.ttest_1samp(diff, 0.0)
    half = float(stats.t.ppf(1 - alpha / 2, n - 1) * sd / np.sqrt(n))
    return {"n": n, "mean_diff": mean, "ci_low": mean - half, "ci_high": mean + half, "t": float(t.statistic),
            "df": n - 1, "p": float(t.pvalue), "cohens_d": mean / sd if sd > 0 else None}


def ks_yes_no(p: np.ndarray, y: np.ndarray) -> dict:
    ks = stats.ks_2samp(p[y == 1], p[y == 0])
    return {"D": float(ks.statistic), "p": float(ks.pvalue), "n_yes": int((y == 1).sum()), "n_no": int((y == 0).sum())}


def analyze(df: pd.DataFrame, alpha: float) -> dict:
    p7, p1, y = df["p_7d"].to_numpy(), df["p_1d"].to_numpy(), df["y"].to_numpy()
    h7, h1 = entropy_bits(p7), entropy_bits(p1)
    return {
        "n_markets": len(df),
        # Positive mean = the error at 7 d is larger than at 1 d = better near the deadline.
        "brier_diff_7d_minus_1d": one_sample_t((p7 - y) ** 2 - (p1 - y) ** 2, alpha),
        "abs_error_diff_7d_minus_1d": one_sample_t(np.abs(p7 - y) - np.abs(p1 - y), alpha),
        "brier": {"7d": float(np.mean((p7 - y) ** 2)), "1d": float(np.mean((p1 - y) ** 2))},
        "ks_yes_vs_no": {"7d": ks_yes_no(p7, y), "1d": ks_yes_no(p1, y)},
        "mean_entropy_bits": {"7d": float(h7.mean()), "1d": float(h1.mean()), "diff_7d_minus_1d": float((h7 - h1).mean())},
    }


def draw_ecdfs(df: pd.DataFrame, out: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(9, 4.2), sharex=True, sharey=True, layout="constrained")
    for ax, (col, title) in zip(axes, [("p_7d", "7 days before T"), ("p_1d", "1 day before T")]):
        for label, g in [("Resolved Yes", df[df["y"] == 1]), ("Resolved No", df[df["y"] == 0])]:
            x = np.sort(g[col].to_numpy())
            ax.step(x, np.arange(1, len(x) + 1) / len(x), where="post", color=COLORS[label],
                    label=f"{label} (n={len(x)})")
        ax.set_title(title, fontsize=10)
        ax.set_xlabel(f"{col} (price, USDC per share)")
        ax.grid(alpha=0.3)
    axes[0].set_ylabel("ECDF (share of markets)")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="outside upper center", ncol=2)
    fig.savefig(out / "fig10_ecdf_7d_vs_1d.png", dpi=150)
    plt.close(fig)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--params", required=True)
    ap.add_argument("--out", default=".")
    args = ap.parse_args()
    out, params = Path(args.out), load_params(args.params)
    alpha, stale = float(params["alpha"]), float(params["max_staleness_h"])

    def work() -> dict[str, str]:
        m = pd.read_parquet(out / "markets.parquet")
        sel = m["kept"] & m["open_ge_7d"] & m["p_7d"].notna() & m["p_1d"].notna() & (m["p_age_7d_h"] <= stale)
        df = m[sel][["market_id", "p_7d", "p_age_7d_h", "p_1d", "p_age_h", "y"]]
        if len(df) < 20:
            raise ValueError(f"only {len(df)} markets with both prices: too few for Q1b")
        res = analyze(df, alpha)
        res["selection"] = {"n_kept": int(m["kept"].sum()), "n_kept_open_ge_7d": int((m["kept"] & m["open_ge_7d"]).sum()),
                            "n_used": len(df), "max_staleness_h": stale}
        sq = ((df["p_7d"] - df["y"]) ** 2 - (df["p_1d"] - df["y"]) ** 2)
        # Individual-level output (measurement.md §3): both prices and both errors for every market used.
        df.assign(brier_7d=(df["p_7d"] - df["y"]) ** 2, brier_1d=(df["p_1d"] - df["y"]) ** 2,
                  brier_diff_7d_minus_1d=sq).to_csv(out / "q1b_markets.csv", index=False)
        write_json(out / "q1b_results.json", res)
        draw_ecdfs(df, out)
        write_manifest(out, params, res, __file__, STAGE)
        s = json.loads((out / "q1b_results.json").read_text())  # report numbers come from the saved JSON
        tt, ae, ent, ks = s["brier_diff_7d_minus_1d"], s["abs_error_diff_7d_minus_1d"], s["mean_entropy_bits"], s["ks_yes_vs_no"]
        tab = pd.DataFrame({
            "quantity": ["Brier (7 d)", "Brier (1 d)", "mean H(p) bits (7 d)", "mean H(p) bits (1 d)",
                         "mean H(p) change (7 d - 1 d)", "KS D Yes vs No (7 d)", "KS D Yes vs No (1 d)"],
            "value": [s["brier"]["7d"], s["brier"]["1d"], ent["7d"], ent["1d"], ent["diff_7d_minus_1d"],
                      ks["7d"]["D"], ks["1d"]["D"]],
            "p": ["", "", "", "", "", f"{ks['7d']['p']:.3g}", f"{ks['1d']['p']:.3g}"]})
        tab.to_csv(out / "q1b_table.csv", index=False)
        return {
            "Why": "Q1b: is the price closer to the outcome 1 day before T than 7 days before T?",
            "Input data": f"markets.parquet: {s['selection']['n_used']} markets of {s['selection']['n_kept']} kept "
                          f"({s['selection']['n_kept_open_ge_7d']} opened >= 7 d before T). Both prices at most "
                          f"{stale:g} h old. Real data.",
            "Output data": "q1b_markets.csv, q1b_table.csv, q1b_results.json, fig10_ecdf_7d_vs_1d.png",
            "Result": (f"Primary: one-sample t-test of Brier difference (7 d - 1 d): mean={tt['mean_diff']:.4g}, "
                       f"95% CI [{tt['ci_low']:.4g}, {tt['ci_high']:.4g}], t={tt['t']:.4g} (df {tt['df']}), "
                       f"p={tt['p']:.3g}, Cohen's d={tt['cohens_d']}. Positive mean = better near the deadline.\n\n"
                       f"Absolute error difference (7 d - 1 d): mean={ae['mean_diff']:.4g}, "
                       f"95% CI [{ae['ci_low']:.4g}, {ae['ci_high']:.4g}], p={ae['p']:.3g}, Cohen's d={ae['cohens_d']}.\n\n"
                       f"The entropy drop is expected by construction: prices move toward 0 or 1 near the deadline. "
                       f"The error change is the real test.\n\n{md_table(tab)}"),
            "Figure": "![ecdf 7d vs 1d](fig10_ecdf_7d_vs_1d.png)  Caption: ECDFs of the price for Yes-resolved and "
                      "No-resolved markets, at 7 days and at 1 day before T. "
                      "Why: the further apart the two curves, the better the price separates the outcomes. "
                      "Source: this run folder.",
        }

    run_stage(out, STAGE, "Q1b: does the market get smarter near the deadline?", work)


if __name__ == "__main__":
    main()
