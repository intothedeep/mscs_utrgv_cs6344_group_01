"""Job B stage 3 (Q1): is the crowd right? Calibration of p_1d against the outcome y.

Main result = markets kept WITH the min_trades filter. The no-filter run is reported next to it.
"""
import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests
from statsmodels.stats.proportion import proportion_confint

from common import load_params, md_table, run_stage, write_json, write_manifest

STAGE = "q1_calibration"
LOG_CLIP = 1e-6


def wilson(k: int, n: int, alpha: float) -> tuple[float, float]:
    lo, hi = proportion_confint(k, n, alpha=alpha, method="wilson")
    return float(lo), float(hi)


def bin_table(df: pd.DataFrame, bin_col: str, alpha: float) -> pd.DataFrame:
    rows = []
    for b, g in df.groupby(bin_col, observed=True):
        n, k, mean_p = len(g), int(g["y"].sum()), float(g["p_1d"].mean())
        lo, hi = wilson(k, n, alpha)
        rows.append({"bin": b, "n": n, "n_yes": k, "mean_price": mean_p, "observed_rate": k / n,
                     "diff_obs_minus_price": k / n - mean_p, "ci_low": lo, "ci_high": hi,
                     "binom_p": float(stats.binomtest(k, n, min(max(mean_p, 0.0), 1.0)).pvalue)})
    return pd.DataFrame(rows)


def analyze(df: pd.DataFrame, n_bins: int, alpha: float) -> tuple[dict, pd.DataFrame, pd.DataFrame]:
    df = df.copy()
    df["bin"] = np.minimum((df["p_1d"] * n_bins).astype(int), n_bins - 1)  # equal-width bins, p=1 in last bin
    bins = bin_table(df, "bin", alpha)
    bins["p_bonferroni"] = multipletests(bins["binom_p"], alpha=alpha, method="bonferroni")[1]
    bins["p_bh"] = multipletests(bins["binom_p"], alpha=alpha, method="fdr_bh")[1]
    bins["reject_bonferroni"] = bins["p_bonferroni"] < alpha
    bins["reject_bh"] = bins["p_bh"] < alpha
    # Equal-frequency check: same table on quantile bins (ties dropped).
    df["bin_eqf"] = pd.qcut(df["p_1d"], n_bins, duplicates="drop").astype(str)
    eqf = bin_table(df, "bin_eqf", alpha)

    p, y = df["p_1d"].to_numpy(), df["y"].to_numpy()
    # Chi-square GoF on the bin x {Yes, No} table: expected Yes = n * mean price. No fitted parameters, so df = bins.
    exp_yes, exp_no = bins["n"] * bins["mean_price"], bins["n"] * (1 - bins["mean_price"])
    ok_yes, ok_no = exp_yes > 0, exp_no > 0
    chi2 = float((((bins["n_yes"] - exp_yes) ** 2 / exp_yes.where(ok_yes))[ok_yes]).sum()
                 + (((bins["n"] - bins["n_yes"] - exp_no) ** 2 / exp_no.where(ok_no))[ok_no]).sum())
    dof = len(bins)
    pc = np.clip(p, LOG_CLIP, 1 - LOG_CLIP)
    pred = p > 0.5
    tp, fp = int((pred & (y == 1)).sum()), int((pred & (y == 0)).sum())
    fn, tn = int((~pred & (y == 1)).sum()), int((~pred & (y == 0)).sum())
    ks = stats.ks_2samp(p[y == 1], p[y == 0])
    longshot = {}
    for lo_e, hi_e in [(0.0, 0.1), (0.1, 0.2)]:
        g = df[(df["p_1d"] >= lo_e) & (df["p_1d"] < hi_e)]
        if len(g):
            k, n, mean_p = int(g["y"].sum()), len(g), float(g["p_1d"].mean())
            lo, hi = wilson(k, n, alpha)
            longshot[f"{lo_e}-{hi_e}"] = {"n": n, "mean_price": mean_p, "observed_rate": k / n,
                                          "obs_minus_expected": k / n - mean_p,
                                          "ci_low_diff": lo - mean_p, "ci_high_diff": hi - mean_p}
    res = {
        "n_markets": len(df), "class_balance_yes": float(y.mean()),
        "brier": float(np.mean((p - y) ** 2)),
        "log_loss": float(-np.mean(y * np.log(pc) + (1 - y) * np.log(1 - pc))),
        "mean_entropy_bits": float(np.mean(-(pc * np.log2(pc) + (1 - pc) * np.log2(1 - pc)))),
        "chi2_gof": {"chi2": chi2, "df": dof, "p": float(stats.chi2.sf(chi2, dof)),
                     "effect_w": float(np.sqrt(chi2 / len(df)))},  # Cohen's w = sqrt(chi2 / N)
        "confusion_at_0.5": {"tp": tp, "fp": fp, "fn": fn, "tn": tn,
                             "accuracy": (tp + tn) / len(df),
                             "precision": tp / (tp + fp) if tp + fp else None,
                             "recall": tp / (tp + fn) if tp + fn else None},
        "ks_yes_vs_no": {"D": float(ks.statistic), "p": float(ks.pvalue),
                         "n_yes": int((y == 1).sum()), "n_no": int((y == 0).sum())},
        "longshot": longshot,
        "bins_reject_bonferroni": int(bins["reject_bonferroni"].sum()),
        "bins_reject_bh": int(bins["reject_bh"].sum()),
    }
    return res, bins, eqf


def draw_calibration(main: pd.DataFrame, nomin: pd.DataFrame, out: Path) -> None:
    fig, ax = plt.subplots(figsize=(6, 6), layout="constrained")
    ax.plot([0, 1], [0, 1], color="#888888", ls="--", label="Perfect calibration")
    for name, b, color, dx in [("With min_trades filter (main)", main, "#222222", 0.0),
                               ("Without filter", nomin, "#aa5500", 0.006)]:
        err = np.clip(np.vstack([b["observed_rate"] - b["ci_low"], b["ci_high"] - b["observed_rate"]]), 0, None)  # float rounding can give -1e-17 at rate 0 or 1; plot only
        ax.errorbar(b["mean_price"] + dx, b["observed_rate"], yerr=err, fmt="o", ms=4, capsize=3, color=color, label=name)
    ax.set(xlabel="Mean price p_1d in bin (USDC per share)", ylabel="Observed Yes rate", xlim=(0, 1), ylim=(0, 1))
    ax.grid(alpha=0.3)
    fig.legend(loc="outside upper center", ncol=3)
    fig.savefig(out / "fig4_calibration.png", dpi=150)
    plt.close(fig)


def draw_ecdfs(df: pd.DataFrame, out: Path) -> None:
    fig, ax = plt.subplots(figsize=(6, 4), layout="constrained")
    for label, g, color in [("Resolved Yes", df[df["y"] == 1], "#222222"), ("Resolved No", df[df["y"] == 0], "#aa5500")]:
        x = np.sort(g["p_1d"].to_numpy())
        ax.step(x, np.arange(1, len(x) + 1) / len(x), where="post", label=f"{label} (n={len(x)})", color=color)
    ax.set(xlabel="p_1d (price, USDC per share)", ylabel="ECDF (share of markets)")
    ax.grid(alpha=0.3)
    fig.legend(loc="outside upper center", ncol=2)
    fig.savefig(out / "fig5_ecdf_yes_no.png", dpi=150)
    plt.close(fig)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--params", required=True)
    ap.add_argument("--out", default=".")
    args = ap.parse_args()
    out, params = Path(args.out), load_params(args.params)
    n_bins, alpha = int(params["n_bins"]), float(params["alpha"])

    def work() -> dict[str, str]:
        m = pd.read_parquet(out / "markets.parquet")
        main_df = m[m["kept"]][["market_id", "p_1d", "y"]]
        nomin_df = m[m["kept_no_min"]][["market_id", "p_1d", "y"]]
        if len(main_df) < 20:
            raise ValueError(f"only {len(main_df)} kept markets: too few for Q1")
        res_main, bins_main, eqf = analyze(main_df, n_bins, alpha)
        res_nomin, bins_nomin, _ = analyze(nomin_df, n_bins, alpha)
        bins_main.to_csv(out / "q1_bins.csv", index=False)
        bins_nomin.to_csv(out / "q1_bins_no_min.csv", index=False)
        eqf.to_csv(out / "q1_bins_eqfreq.csv", index=False)
        # Individual-level output (measurement.md §3): every market in the larger set, with the bin and both flags.
        ind = m[m["kept_no_min"]][["market_id", "p_1d", "y", "kept"]].copy()
        ind["bin"] = np.minimum((ind["p_1d"] * n_bins).astype(int), n_bins - 1)
        ind.rename(columns={"kept": "kept_with_min_filter"}).to_csv(out / "q1_markets.csv", index=False)
        write_json(out / "q1_results.json", {"main_with_min_filter": res_main, "no_min_filter": res_nomin,
                                              "t_rule": params["t_rule"], "min_trades": params["min_trades"]})
        draw_calibration(bins_main, bins_nomin, out)
        draw_ecdfs(main_df, out)
        write_manifest(out, params, {"main": res_main, "no_min_filter": res_nomin}, __file__, STAGE)
        keys = ["n_markets", "class_balance_yes", "brier", "log_loss", "mean_entropy_bits"]
        tab = pd.DataFrame({"metric": keys + ["chi2 (df)", "chi2 effect w", "KS D (Yes vs No)"],
                            "with min filter": [res_main[k] for k in keys] + [
                                f"{res_main['chi2_gof']['chi2']:.1f} ({res_main['chi2_gof']['df']}), p={res_main['chi2_gof']['p']:.3g}",
                                res_main["chi2_gof"]["effect_w"], res_main["ks_yes_vs_no"]["D"]],
                            "without filter": [res_nomin[k] for k in keys] + [
                                f"{res_nomin['chi2_gof']['chi2']:.1f} ({res_nomin['chi2_gof']['df']}), p={res_nomin['chi2_gof']['p']:.3g}",
                                res_nomin["chi2_gof"]["effect_w"], res_nomin["ks_yes_vs_no"]["D"]]})
        bin_tab = md_table(bins_main[["bin", "n", "mean_price", "observed_rate", "ci_low", "ci_high", "binom_p", "p_bonferroni", "p_bh"]])
        return {
            "Why": "Q1: does the price 1 day before T match how often the outcome is Yes?",
            "Input data": f"markets.parquet: {len(main_df)} kept markets (with filter), {len(nomin_df)} without the filter. "
                          f"T rule={params['t_rule']}, min_trades={params['min_trades']}. Real data.",
            "Output data": "q1_bins.csv, q1_bins_no_min.csv, q1_bins_eqfreq.csv, q1_results.json, q1_markets.csv, "
                           "fig4_calibration.png, fig5_ecdf_yes_no.png",
            "Result": md_table(tab) + f"\n\nBins rejected: Bonferroni {res_main['bins_reject_bonferroni']}, "
                      f"BH {res_main['bins_reject_bh']} of {len(bins_main)} (main).\n\n" + bin_tab,
            "Figure": "![calibration](fig4_calibration.png) ![ecdf](fig5_ecdf_yes_no.png)  Caption: observed Yes rate "
                      "against mean price per bin with 95% Wilson CI, and ECDFs of p_1d by outcome. "
                      "Why: points on the diagonal mean the price matches the outcome rate. Source: this run folder.",
        }

    run_stage(out, STAGE, "Q1: calibration of the price 1 day before T.", work)


if __name__ == "__main__":
    main()
