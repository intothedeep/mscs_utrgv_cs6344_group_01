"""MVP2 Q1c: are busier markets more accurate? Spearman of log volume and log trade count against per-market Brier error.

Population = markets kept WITH the min_trades filter. volume_usdc and n_trades count the whole life of the market
(all trades in scope, also those after T - 1 day), so they are not known at evaluation time.
"""
import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd
from scipy import stats

from common import load_params, md_table, run_stage, write_json, write_manifest

STAGE = "q1c_volume"
N_BINS = 10   # quantile bins of x for the mean line
PREDICTORS = {"volume_usdc": "Volume (USDC)", "n_trades": "Trades (count)"}


def spearman(x: np.ndarray, err: np.ndarray, alpha: float) -> dict:
    """Spearman rho (the effect size) with p and an approximate (1 - alpha) CI by Fisher z."""
    r = stats.spearmanr(x, err)
    n, rho = len(x), float(r.statistic)
    half = stats.norm.ppf(1 - alpha / 2) * np.sqrt(1.06 / (n - 3))  # Fieller variance 1.06 / (n - 3) for Spearman
    lo, hi = np.tanh(np.arctanh(rho) - half), np.tanh(np.arctanh(rho) + half)
    return {"n": n, "rho": rho, "p": float(r.pvalue), "ci_low": float(lo), "ci_high": float(hi)}


def add_scaled(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    """z-score (mean, sd) and robust scaling (median, IQR) for each column. A zero spread gives NaN."""
    out = df.copy()
    for c in cols:
        sd = df[c].std(ddof=1)
        iqr = df[c].quantile(0.75) - df[c].quantile(0.25)
        out[f"z_{c}"] = (df[c] - df[c].mean()) / sd if sd > 0 else np.nan
        out[f"robust_{c}"] = (df[c] - df[c].median()) / iqr if iqr > 0 else np.nan
    return out


def binned_mean(x: pd.Series, err: pd.Series) -> pd.DataFrame:
    bins = pd.qcut(np.log1p(x), N_BINS, duplicates="drop")
    g = pd.DataFrame({"x": x, "err": err, "bin": bins}).groupby("bin", observed=True)
    return pd.DataFrame({"x_median": g["x"].median(), "mean_error": g["err"].mean(), "n": g.size()})


def draw_scatter(df: pd.DataFrame, out: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(9, 4.2), sharey=True, layout="constrained")
    for ax, (col, label) in zip(axes, PREDICTORS.items()):
        pos = df[df[col] > 0]   # log axis cannot show 0
        ax.scatter(pos[col], pos["brier"], s=6, alpha=0.3, color="#555555", rasterized=True)
        line = binned_mean(df[col], df["brier"])
        ax.plot(line["x_median"].clip(lower=pos[col].min()), line["mean_error"], color="#aa5500", marker="o", ms=4)
        ax.set_xscale("log")
        ax.set_xlabel(f"{label}, log scale")
        ax.grid(alpha=0.3)
    axes[0].set_ylabel("Per-market Brier error (squared error, unitless)")
    handles = [Line2D([], [], color="#555555", marker="o", ls="", ms=3, alpha=0.5, label="Market"),
               Line2D([], [], color="#aa5500", marker="o", ms=4, label="Mean error per decile of x")]
    fig.legend(handles=handles, loc="outside upper center", ncol=2)
    fig.savefig(out / "fig11_volume_vs_error.png", dpi=150)
    plt.close(fig)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--params", required=True)
    ap.add_argument("--out", default=".")
    args = ap.parse_args()
    out, params = Path(args.out), load_params(args.params)
    alpha = float(params["alpha"])

    def work() -> dict[str, str]:
        m = pd.read_parquet(out / "markets.parquet")
        df = m[m["kept"]][["market_id", "volume_usdc", "n_trades", "p_1d", "y"]].dropna().copy()
        if len(df) < 20:
            raise ValueError(f"only {len(df)} kept markets: too few for Q1c")
        df["brier"] = (df["p_1d"] - df["y"]) ** 2
        df["log1p_volume_usdc"] = np.log1p(df["volume_usdc"])
        df["log1p_n_trades"] = np.log1p(df["n_trades"])
        res = {"n_markets": len(df),
               "spearman_log_volume_vs_error": spearman(df["log1p_volume_usdc"].to_numpy(), df["brier"].to_numpy(), alpha),
               "spearman_log_trades_vs_error": spearman(df["log1p_n_trades"].to_numpy(), df["brier"].to_numpy(), alpha),
               "scaling": "z = (x - mean) / sd; robust = (x - median) / IQR; columns in q1c_scaled.csv"}
        scaled = add_scaled(df, ["volume_usdc", "n_trades", "brier", "log1p_volume_usdc", "log1p_n_trades"])
        # Individual-level output (measurement.md §3): every market with raw, log and scaled values.
        scaled.to_csv(out / "q1c_scaled.csv", index=False)
        binned = pd.concat({col: binned_mean(df[col], df["brier"]) for col in PREDICTORS}, names=["predictor", "bin"])
        binned.reset_index().astype({"bin": str}).to_csv(out / "q1c_binned.csv", index=False)
        write_json(out / "q1c_results.json", res)
        draw_scatter(df, out)
        write_manifest(out, params, res, __file__, STAGE)
        s = json.loads((out / "q1c_results.json").read_text())  # report numbers come from the saved JSON
        rows = [("log1p(volume_usdc)", s["spearman_log_volume_vs_error"]), ("log1p(n_trades)", s["spearman_log_trades_vs_error"])]
        tab = pd.DataFrame({"x": [r[0] for r in rows], "n": [r[1]["n"] for r in rows],
                            "rho (effect size)": [r[1]["rho"] for r in rows],
                            "95% CI": [f"[{r[1]['ci_low']:.3f}, {r[1]['ci_high']:.3f}]" for r in rows],
                            "p": [f"{r[1]['p']:.3g}" for r in rows]})
        tab.to_csv(out / "q1c_table.csv", index=False)
        return {
            "Why": "Q1c: do markets with more volume or more trades have a price closer to the outcome?",
            "Input data": f"markets.parquet: {s['n_markets']} kept markets (with min_trades filter), real data. "
                          "Volume and trade count cover all trades of the market in scope, not only those before T - 1 day.",
            "Output data": "q1c_scaled.csv, q1c_binned.csv, q1c_table.csv, q1c_results.json, fig11_volume_vs_error.png",
            "Result": ("Primary: Spearman rho of log volume vs Brier error. Negative rho with p < 0.05 = busier is more "
                       f"accurate.\n\n{md_table(tab)}"),
            "Figure": "![volume vs error](fig11_volume_vs_error.png)  Caption: per-market Brier error against volume and "
                      "trade count (log x) with the mean error per decile of x. "
                      "Why: a falling line means busier markets have smaller errors. Source: this run folder.",
        }

    run_stage(out, STAGE, "Q1c: are busier markets more accurate?", work)


if __name__ == "__main__":
    main()
