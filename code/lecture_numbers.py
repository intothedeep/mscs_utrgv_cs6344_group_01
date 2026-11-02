"""Lecture-method numbers for MVP1 (D-025, D-026), read from SAVED files of one run (CSV and JSON only).

Replaces the outside methods: Wilson interval -> z interval with Bernoulli SD (L5 s24, L6 s25),
Cohen's w -> per-bin gaps (L12 s3, L10 s7), Cohen's d -> log10 mean difference, eta squared -> SSB / (SSB + SSW) (L11 s11).
Usage (from the project folder):
  OMP_NUM_THREADS=1 timeout 300 uv run python code/lecture_numbers.py --run runs/142082_mvp1_full_v1r3
"""
import argparse
import hashlib
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

CODE_VERSION = "lecture-v1"   # own label, like make_report.py; bumped by hand
Z95 = 1.959963984540054       # two-sided 95% normal quantile
REFERENCE_SHARE = 0.8         # the 80/20 reference of L6 (D-024)


def z_bins(bins: pd.DataFrame) -> pd.DataFrame:
    """Per bin: observed rate +- Z95 * Bernoulli SD / sqrt(n), and whether the mean price lies outside it."""
    rate = bins["n_yes"] / bins["n"]
    sd = np.sqrt(rate * (1 - rate))
    half = Z95 * sd / np.sqrt(bins["n"])
    keep = ["bin", "n", "n_yes", "mean_price", "observed_rate", "diff_obs_minus_price"]
    out = bins[keep + [c for c in ["reject_bh"] if c in bins]].copy()
    out["bernoulli_sd"], out["z_low"], out["z_high"] = sd, rate - half, rate + half
    out["price_outside"] = (out["mean_price"] < out["z_low"]) | (out["mean_price"] > out["z_high"])
    return out


def z_longshot(q1: dict) -> dict:
    """The longshot bins (price below 0.2) with the z interval of the observed rate, shown as a gap to the mean price."""
    out = {}
    for key in ("main_with_min_filter", "no_min_filter"):
        out[key] = {}
        for b, v in q1[key]["longshot"].items():
            half = Z95 * np.sqrt(v["observed_rate"] * (1 - v["observed_rate"]) / v["n"])
            out[key][b] = {"n": v["n"], "mean_price": v["mean_price"], "observed_rate": v["observed_rate"],
                           "obs_minus_expected": v["obs_minus_expected"],
                           "z_low_diff": v["obs_minus_expected"] - half, "z_high_diff": v["obs_minus_expected"] + half}
    return out


def draw_calibration(main: pd.DataFrame, nomin: pd.DataFrame, png: Path) -> None:
    fig, ax = plt.subplots(figsize=(6, 6), layout="constrained")
    ax.plot([0, 1], [0, 1], color="#888888", ls="--", label="Perfect calibration")
    for name, b, color, dx in [("With min_trades filter (main)", main, "#222222", 0.0),
                               ("Without filter", nomin, "#aa5500", 0.006)]:
        err = np.vstack([b["observed_rate"] - b["z_low"], b["z_high"] - b["observed_rate"]])
        ax.errorbar(b["mean_price"] + dx, b["observed_rate"], yerr=np.clip(err, 0, None), fmt="o", ms=4,
                    capsize=3, color=color, label=name)
    ax.set(xlabel="Mean price p_1d in bin (USDC per share)", ylabel="Observed Yes rate", xlim=(0, 1), ylim=(0, 1))
    ax.grid(alpha=0.3)
    fig.legend(loc="outside upper center", ncol=3)
    fig.savefig(png, dpi=150)
    plt.close(fig)


def draw_lorenz(csv: Path, png: Path) -> None:
    """Coarse Lorenz picture (D-028) from the four saved top shares per role. No Gini column is read. Below x = 0.80 nothing was measured."""
    shares = pd.read_csv(csv, index_col=0).loc[:, ["top1_share", "top5_share", "top10_share", "top20_share"]]  # the gini column is dropped here
    fig, ax = plt.subplots(figsize=(7, 6.4), layout="constrained")
    ax.plot([0, 1], [0, 1], color="#888888", ls="--", label="Equality, y = x")
    for role, color in [("maker", "#222222"), ("taker", "#aa5500")]:
        t = shares.loc[role]
        x = [0, 0.80, 0.90, 0.95, 0.99, 1]
        y = [0, 1 - t["top20_share"], 1 - t["top10_share"], 1 - t["top5_share"], 1 - t["top1_share"], 1]
        ax.plot(x, y, color=color, marker="o", ms=5, label=f"{role} (4 saved points)")
    ax.plot([0.80], [0.20], marker="D", ms=8, ls="none", color="#0432ff", label="80/20 reference")
    ax.axvspan(0, 0.80, color="#dddddd", alpha=0.5, label="Not measured (x < 0.80)")
    ax.set(xlabel="Cumulative share of wallets, smallest volume first", ylabel="Cumulative share of volume (USDC)", xlim=(0, 1), ylim=(0, 1))
    ax.grid(alpha=0.3)
    fig.legend(loc="outside upper center", ncol=3)
    fig.savefig(png, dpi=150)
    plt.close(fig)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--out", default="reports/lecture_numbers.json")
    ap.add_argument("--fig", default="reports/figures/fig4_calibration_z.png")
    ap.add_argument("--lorenz-fig", default="reports/figures/lorenz_top_shares.png")
    a = ap.parse_args()
    run, out, fig = Path(a.run), Path(a.out), Path(a.fig)
    main_b = z_bins(pd.read_csv(run / "q1_bins.csv"))
    nomin_b = z_bins(pd.read_csv(run / "q1_bins_no_min.csv"))
    eqf_b = z_bins(pd.read_csv(run / "q1_bins_eqfreq.csv"))
    q1 = json.loads((run / "q1_results.json").read_text())
    q2 = json.loads((run / "q2_results.json").read_text())
    q3 = json.loads((run / "q3_results.json").read_text())

    outside = main_b.loc[main_b["price_outside"], "bin"].astype(int).tolist()
    bh_off = main_b.loc[main_b["reject_bh"], "bin"].astype(int).tolist()
    gap = main_b.loc[main_b["diff_obs_minus_price"].abs().idxmax()]
    w, an = q2["role_tests"]["welch_t"], q2["kmeans"]["anova_mean_trade_price"]
    an_old = q2["kmeans"]["anova_log_median_trade_size"]
    pl = q3["fits"]["wallet_volume_usdc"]["power_law"]
    res = {
        "code_version": CODE_VERSION,
        "code_sha": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()[:12],
        "source_run": run.name,
        "z_interval_95": {
            "rule": "rate +- 1.96 * sqrt(rate * (1 - rate)) / sqrt(n), rate = n_yes / n (L5 s24, Bernoulli SD L6 s25)",
            "z": Z95,
            "bins": main_b.assign(bin=main_b["bin"].astype(int)).to_dict(orient="records"),
            "bins_no_min_filter": nomin_b.assign(bin=nomin_b["bin"].astype(int)).to_dict(orient="records"),
            "bins_equal_frequency": eqf_b.to_dict(orient="records"),
            "longshot": z_longshot(q1),
            "n_outside": len(outside), "bins_outside": outside,
            "n_bh_off": len(bh_off), "bins_bh_off": bh_off,
            "same_bins": outside == bh_off,
        },
        "largest_gap": {"bin": int(gap["bin"]), "diff_obs_minus_price": float(gap["diff_obs_minus_price"]),
                        "abs": float(abs(gap["diff_obs_minus_price"]))},
        "log10_mean_difference_maker_minus_taker": {
            "mean_log10_maker": w["mean_log10_maker"], "mean_log10_taker": w["mean_log10_taker"],
            "difference": w["mean_log10_maker"] - w["mean_log10_taker"], "welch_t": w["t"]},
        "top20_share": {"reference": REFERENCE_SHARE,
                        **{role: q2["concentration"][role]["top20_share"] for role in ("maker", "taker")}},
        "ssb_ratio": {"definition": "SSB / (SSB + SSW) (L11 s11), the saved eta_squared", "mean_trade_price": an["eta_squared"],
                      "log_median_trade_size": an_old["eta_squared"]},
        "power_law_wallet_volume": {"alpha": pl["alpha"], "xmin": pl["xmin"], "xmin_quantile": pl["xmin_quantile"],
                                    "n_tail": pl["n_tail"], "ks_D": pl["D"], "ks_p": pl["p"]},
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(res, indent=2) + "\n")
    draw_calibration(main_b, nomin_b, fig)
    draw_lorenz(run / "q2_concentration.csv", Path(a.lorenz_fig))
    print(f"outside z interval: {outside}; BH off: {bh_off}; wrote {out} and {fig}")


if __name__ == "__main__":
    main()
