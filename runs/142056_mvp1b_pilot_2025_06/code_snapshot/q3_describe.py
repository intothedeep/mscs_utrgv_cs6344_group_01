"""Job B stage 2 (Q3): what does the data look like? Summary stats, histograms, ECDF, fits, QQ, KS."""
import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

from common import load_params, md_table, run_stage, write_json, write_manifest

STAGE = "q3_describe"
POWER_LAW_XMIN_QUANTILE = 0.90  # fixed: power law is a tail model, so fit only the top 10%
QQ_POINTS = 5000                # QQ plots draw a fixed-seed subsample
SEED = 42


def summarize(x: np.ndarray) -> dict:
    counts, edges = np.histogram(x, bins=50)
    mode_bin = int(counts.argmax())  # continuous data: mode = midpoint of the fullest of 50 bins
    q = np.quantile(x, [0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99])
    return {"n": int(len(x)), "mean": float(x.mean()), "median": float(np.median(x)),
            "mode_50bin_mid": float((edges[mode_bin] + edges[mode_bin + 1]) / 2),
            "min": float(x.min()), "max": float(x.max()), "range": float(x.max() - x.min()),
            "variance": float(x.var(ddof=1)),
            **{f"q{p}": float(v) for p, v in zip([1, 5, 25, 50, 75, 95, 99], q)}}


def fit_and_ks(x: np.ndarray) -> dict:
    """Normal, exponential, power law fits, each with a KS test (D = effect size).

    The KS p-values are optimistic because parameters are estimated from the same data.
    """
    mu, sd = x.mean(), x.std(ddof=1)
    ks_norm = stats.kstest(x, "norm", args=(mu, sd))
    ks_exp = stats.kstest(x, "expon", args=(0, x.mean()))
    xmin = float(np.quantile(x, POWER_LAW_XMIN_QUANTILE))
    tail = x[x >= xmin]
    alpha = 1 + len(tail) / np.log(tail / xmin).sum()  # continuous MLE (Clauset et al. 2009)
    ks_pl = stats.kstest(tail, lambda v: 1 - (v / xmin) ** (1 - alpha))
    return {
        "normal": {"mu": float(mu), "sigma": float(sd), "D": float(ks_norm.statistic), "p": float(ks_norm.pvalue)},
        "exponential": {"scale": float(x.mean()), "D": float(ks_exp.statistic), "p": float(ks_exp.pvalue)},
        "power_law": {"alpha": float(alpha), "xmin": xmin, "xmin_quantile": POWER_LAW_XMIN_QUANTILE,
                      "n_tail": int(len(tail)), "D": float(ks_pl.statistic), "p": float(ks_pl.pvalue)},
    }


def draw_hist(price: np.ndarray, size: np.ndarray, out: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(9, 4), layout="constrained")
    axes[0].hist(price, bins=50, range=(0, 1), color="#555555")
    axes[0].set(xlabel="p_1d (price, USDC per share)", ylabel="Markets (count)", title="Price 1 day before T")
    axes[1].hist(size, bins=np.logspace(np.log10(max(size.min(), 1e-6)), np.log10(size.max()), 60), color="#555555")
    axes[1].set(xscale="log", xlabel="Trade size (USDC)", ylabel="Trades (count)", title="Trade size")
    for ax in axes:
        ax.grid(alpha=0.3)
    fig.savefig(out / "fig1_fig2_hist.png", dpi=150)
    plt.close(fig)


def draw_ecdf(size: np.ndarray, vol: np.ndarray, out: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 4), layout="constrained")
    for name, x, color in [("Trade size (USDC)", size, "#222222"), ("Wallet volume (USDC)", vol, "#aa5500")]:
        xs = np.sort(x)
        idx = np.linspace(0, len(xs) - 1, min(len(xs), 5000)).astype(int)  # thin the line, ECDF shape is kept
        ax.plot(xs[idx], (idx + 1) / len(xs), label=name, color=color)
    ax.set(xscale="log", xlabel="Value (USDC)", ylabel="ECDF (share of rows at or below)")
    ax.grid(alpha=0.3)
    fig.legend(loc="outside upper center", ncol=2)
    fig.savefig(out / "ecdf.png", dpi=150)
    plt.close(fig)


def draw_qq(size: np.ndarray, vol: np.ndarray, out: Path) -> None:
    rng = np.random.default_rng(SEED)
    fig, axes = plt.subplots(2, 2, figsize=(8, 7), layout="constrained")
    for row, (name, x) in enumerate([("Trade size", size), ("Wallet volume", vol)]):
        s = rng.choice(x, min(QQ_POINTS, len(x)), replace=False)
        for col, (tag, v) in enumerate([("raw", s), ("log", np.log(s))]):
            stats.probplot(v, dist="norm", plot=axes[row, col])
            axes[row, col].set_title(f"{name}, {tag}")
            axes[row, col].set_xlabel("Normal theoretical quantile (z)")
            axes[row, col].set_ylabel("Ordered values" + (" (log USDC)" if tag == "log" else " (USDC)"))
            axes[row, col].grid(alpha=0.3)
    fig.savefig(out / "fig3_qq.png", dpi=150)
    plt.close(fig)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--params", required=True)
    ap.add_argument("--out", default=".")
    args = ap.parse_args()
    out, params = Path(args.out), load_params(args.params)

    def work() -> dict[str, str]:
        markets = pd.read_parquet(out / "markets.parquet")
        price = markets.loc[markets["kept"], "p_1d"].dropna().to_numpy(float)
        size = pd.read_parquet(out / "trade_sizes_sample.parquet")["usdc_amount"].to_numpy(float)
        size = size[size > 0]  # log and power-law need positive values
        vol = pd.read_parquet(out / "wallets.parquet")["volume_usdc"].to_numpy(float)
        vol = vol[vol > 0]
        variables = {"p_1d": price, "trade_size_usdc": size, "wallet_volume_usdc": vol}
        results = {"summary": {k: summarize(v) for k, v in variables.items()},
                   "fits": {"trade_size_usdc": fit_and_ks(size), "wallet_volume_usdc": fit_and_ks(vol)},
                   "notes": {"trade_size_sample_rows": int(len(size)),
                             "wallet_volume": "wallet x role rows pooled (maker and taker rows)"}}
        write_json(out / "q3_results.json", results)
        pd.DataFrame(results["summary"]).T.to_csv(out / "q3_summary.csv")
        draw_hist(price, size, out)
        draw_ecdf(size, vol, out)
        draw_qq(size, vol, out)
        write_manifest(out, params, {"n_price": len(price), "n_size": len(size), "n_wallet_rows": len(vol)}, __file__, STAGE)
        tab = pd.DataFrame(results["summary"]).T[["n", "mean", "median", "mode_50bin_mid", "range", "variance"]].reset_index()
        fit_rows = [[v, m, f["D"], f["p"]] for v, d in results["fits"].items() for m, f in d.items()]
        tab_fit = md_table(pd.DataFrame(fit_rows, columns=["variable", "model", "KS D", "KS p"]))
        return {
            "Why": "Q3: describe price, trade size and wallet volume before Q1 and Q2 use them.",
            "Input data": f"markets.parquet kept markets ({len(price)}), trade_sizes_sample.parquet ({len(size)} trades, "
                          f"fixed-seed sample), wallets.parquet ({len(vol)} wallet x role rows).",
            "Output data": "q3_results.json, q3_summary.csv, fig1_fig2_hist.png, ecdf.png, fig3_qq.png",
            "Result": "Summary:\n\n" + md_table(tab) + "\n\nFits and KS (D is the effect size; p is optimistic because "
                      f"parameters are fitted on the same data; power law fitted on the top "
                      f"{1 - POWER_LAW_XMIN_QUANTILE:.0%} tail with xmin = the {POWER_LAW_XMIN_QUANTILE:.0%} quantile):\n\n" + tab_fit,
            "Figure": "![hist](fig1_fig2_hist.png) ![ecdf](ecdf.png) ![qq](fig3_qq.png)  Caption: price and trade-size "
                      "histograms, ECDFs, and QQ plots before and after log. Why: a straight QQ line after log means "
                      "the log-values are close to normal. Source: this run folder.",
        }

    run_stage(out, STAGE, "Q3: summary statistics, histograms, ECDF, distribution fits, QQ plots, KS tests.", work)


if __name__ == "__main__":
    main()
