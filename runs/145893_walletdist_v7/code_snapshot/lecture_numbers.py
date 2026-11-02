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

CODE_VERSION = "lecture-v3"   # own label, like make_report.py; bumped by hand
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


def gap_direction(bins: pd.DataFrame) -> dict:
    """Direction of the gaps (observed rate minus mean price): bins below price, and the n-weighted net gap over all markets."""
    n, d = bins["n"], bins["diff_obs_minus_price"]
    return {"n_bins": len(bins), "n_negative": int((d < 0).sum()),
            "net_gap": float((n * d).sum() / n.sum()),                 # = (Yes count - expected Yes count) / markets
            "n_yes_minus_expected": float((n * d).sum())}


def chi2_contributions(bins: pd.DataFrame, saved_chi2: float) -> dict:
    """Per-bin share of the chi-square (n * gap^2 / (p * (1 - p)) equals the Yes term plus the No term). Checked against the saved total."""
    p = bins["mean_price"]
    contrib = bins["n"] * bins["diff_obs_minus_price"] ** 2 / (p * (1 - p))
    top = contrib.idxmax()
    return {"bin": int(bins.loc[top, "bin"]), "contribution": float(contrib[top]), "share": float(contrib[top] / contrib.sum()),
            "total_recomputed": float(contrib.sum()), "total_saved": saved_chi2,
            "matches_saved": bool(np.isclose(contrib.sum(), saved_chi2, rtol=1e-6))}


def no_min_longshot_bh(bins_raw: pd.DataFrame) -> dict:
    """Bins 0 and 1 without the minimum-trade filter: gap and the saved BH call (p_bh below alpha)."""
    out = {}
    for b in (0, 1):
        r = bins_raw[bins_raw["bin"] == b].iloc[0]
        out[str(b)] = {"n": int(r["n"]), "diff_obs_minus_price": float(r["diff_obs_minus_price"]),
                       "p_bh": float(r["p_bh"]), "reject_bh": bool(r["reject_bh"])}
    return out


def cluster_category_gap(ccdf_run: Path | None) -> dict | None:
    """Effect size of the cluster x category chi-square (D-030): the cell with the largest |observed share - expected share|.

    Reads cluster_category_crosstab.csv and cluster_category_expected.csv of the code/ccdf_redraw.py run. Shares are cells over the sample total.
    Returns None when the run is absent (the report then prints a pending marker).
    """
    if ccdf_run is None or not (ccdf_run / "cluster_category_crosstab.csv").exists():
        return None
    obs = pd.read_csv(ccdf_run / "cluster_category_crosstab.csv", index_col=0)
    exp = pd.read_csv(ccdf_run / "cluster_category_expected.csv", index_col=0)
    assert obs.shape == exp.shape and (obs.index == exp.index).all() and (obs.columns == exp.columns).all(), "crosstab and expected differ in shape"
    total = obs.to_numpy().sum()
    gap = (obs - exp) / total
    flat = gap.stack()
    cluster, category = flat.abs().idxmax()
    return {"source_run": ccdf_run.name, "n_sample": int(total), "cluster": int(cluster), "category": str(category),
            "observed_share": float(obs.loc[cluster, category] / total), "expected_share": float(exp.loc[cluster, category] / total),
            "diff": float(gap.loc[cluster, category]), "abs": float(abs(gap.loc[cluster, category]))}


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
    ap.add_argument("--ccdf-run", help="run folder of code/ccdf_redraw.py (cluster x category crosstab); omitted = effect pending")
    ap.add_argument("--fig", default="reports/figures/fig4_calibration_z.png")
    ap.add_argument("--lorenz-fig", default="reports/figures/lorenz_top_shares.png")
    a = ap.parse_args()
    run, out, fig = Path(a.run), Path(a.out), Path(a.fig)
    nomin_raw = pd.read_csv(run / "q1_bins_no_min.csv")
    main_b = z_bins(pd.read_csv(run / "q1_bins.csv"))
    nomin_b = z_bins(nomin_raw)
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
        "gap_direction": {"rule": "gap = observed rate - mean price; net gap is n-weighted (Yes count minus expected, per market)",
                          "main": gap_direction(main_b), "no_min_filter": gap_direction(nomin_b),
                          "equal_frequency": gap_direction(eqf_b)},
        "chi2_largest_contributor": chi2_contributions(main_b, q1["main_with_min_filter"]["chi2_gof"]["chi2"]),
        "no_min_filter_longshot_bh": no_min_longshot_bh(nomin_raw),
        "cluster_category_gap": cluster_category_gap(Path(a.ccdf_run) if a.ccdf_run else None),
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
