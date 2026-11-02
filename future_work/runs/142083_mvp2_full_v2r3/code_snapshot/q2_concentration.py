"""Job B stage 4 (Q2): who is the crowd? Concentration of volume, Gini, role tests, k-means side analysis.

A wallet is one address, never a person. k-means is a side analysis (under 1/10 of the report).
"""
import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score

from common import load_params, md_table, run_stage, write_json, write_manifest

STAGE = "q2_concentration"
SEED = 42
KMEANS_SAMPLE = 200_000
K_RANGE = range(2, 9)
N_PERM = 1000
PAPER_GINI = {"maker": 0.970, "taker": 0.943}  # dataset paper, full data: reference only, not a target
ROLE_COLOR = {"maker": "#222222", "taker": "#aa5500"}


def gini(x: np.ndarray) -> float:
    xs = np.sort(x)
    n = len(xs)
    return float(2 * np.sum(np.arange(1, n + 1) * xs) / (n * xs.sum()) - (n + 1) / n)


def top_share(x: np.ndarray, frac: float) -> float:
    xs = np.sort(x)[::-1]
    return float(xs[: max(1, int(np.ceil(frac * len(xs))))].sum() / xs.sum())


def concentration(wallets: pd.DataFrame) -> dict:
    res = {}
    for role, g in wallets.groupby("role"):
        v = g["volume_usdc"].to_numpy(float)
        res[role] = {"n_wallets": len(v), "mean": float(v.mean()), "median": float(np.median(v)),
                     "mean_over_median": float(v.mean() / np.median(v)),
                     "top1_share": top_share(v, 0.01), "top5_share": top_share(v, 0.05),
                     "top10_share": top_share(v, 0.10), "top20_share": top_share(v, 0.20),  # 80/20 is tested, not assumed
                     "gini": gini(v)}
    return res


def role_tests(wallets: pd.DataFrame) -> dict:
    a = np.log10(wallets.loc[wallets["role"] == "maker", "volume_usdc"].to_numpy(float))
    b = np.log10(wallets.loc[wallets["role"] == "taker", "volume_usdc"].to_numpy(float))
    t = stats.ttest_ind(a, b, equal_var=False)
    pooled = np.sqrt((a.var(ddof=1) + b.var(ddof=1)) / 2)
    ks = stats.ks_2samp(a, b)
    return {"welch_t": {"t": float(t.statistic), "p": float(t.pvalue), "cohens_d": float((a.mean() - b.mean()) / pooled),
                        "mean_log10_maker": float(a.mean()), "mean_log10_taker": float(b.mean())},
            "ks": {"D": float(ks.statistic), "p": float(ks.pvalue)}}


def pick_k(inertia: dict[int, float]) -> int:
    """Fixed elbow rule: K whose point is farthest from the line joining the first and last (K, inertia) points."""
    ks = np.array(sorted(inertia))
    x = (ks - ks[0]) / (ks[-1] - ks[0])
    y = np.array([inertia[k] for k in ks])
    y = (y - y[-1]) / (y[0] - y[-1])
    return int(ks[np.argmax(np.abs(x + y - 1) / np.sqrt(2))])  # line from (0,1) to (1,0)


def scale_features(feats: np.ndarray, names: list[str]) -> tuple[np.ndarray, np.ndarray, pd.DataFrame]:
    """z-score (mean, sd) and robust scaling (median, IQR) of the k-means features, plus the table of the constants.

    An IQR of 0 (most wallets share one value) would divide by zero. That feature is then scaled by its sd and
    the table says so (`robust_scale_used`).
    """
    mean, sd = feats.mean(0), feats.std(0)
    med = np.median(feats, axis=0)
    iqr = np.quantile(feats, 0.75, axis=0) - np.quantile(feats, 0.25, axis=0)
    used = np.where(iqr > 0, iqr, sd)
    table = pd.DataFrame({"feature": names, "mean": mean, "sd": sd, "median": med, "iqr": iqr,
                          "robust_scale_used": used, "iqr_was_zero": iqr == 0})
    return (feats - mean) / sd, (feats - med) / used, table


def anova_with_permutation(y: np.ndarray, labels: np.ndarray, k: int) -> dict:
    """One-way ANOVA F, eta squared and a permutation p (labels shuffled, fixed seed) of y across clusters."""
    groups = [y[labels == c] for c in range(k)]
    f_obs = float(stats.f_oneway(*groups).statistic)
    eta2 = float(sum(len(g) * (g.mean() - y.mean()) ** 2 for g in groups) / ((y - y.mean()) ** 2).sum())
    rng = np.random.default_rng(SEED)
    n_ge = 0
    for _ in range(N_PERM):
        perm = rng.permutation(labels)
        means = np.bincount(perm, y) / np.bincount(perm)
        ssb = (np.bincount(perm) * (means - y.mean()) ** 2).sum()
        ssw = ((y - means[perm]) ** 2).sum()
        n_ge += (ssb / (k - 1)) / (ssw / (len(y) - k)) >= f_obs
    return {"F": f_obs, "eta_squared": eta2, "perm_p": float((1 + n_ge) / (1 + N_PERM)), "n_perm": N_PERM}


def cluster_analysis(wallets: pd.DataFrame) -> tuple[dict, dict[int, float], pd.DataFrame, pd.DataFrame]:
    # Sort by the full key before sampling: row order must not decide which wallets are drawn (review F4).
    wallets = wallets.sort_values(["wallet", "role"]).reset_index(drop=True)
    sample = wallets.sample(min(KMEANS_SAMPLE, len(wallets)), random_state=SEED).sort_values(["wallet", "role"]).reset_index(drop=True)
    # mean_trade_price is NOT a feature: the ANOVA below tests it across clusters (plan Q2 row, D-011).
    names = ["log1p_volume_usdc", "log1p_n_trades", "log1p_n_markets"]
    feats = np.column_stack([np.log1p(sample["volume_usdc"]), np.log1p(sample["n_trades"]), np.log1p(sample["n_markets"])])
    z, robust, scale_table = scale_features(feats, names)
    inertia = {k: float(KMeans(k, n_init=5, random_state=SEED).fit(z).inertia_) for k in K_RANGE}
    k = pick_k(inertia)
    labels = KMeans(k, n_init=5, random_state=SEED).fit_predict(z)
    labels_robust = KMeans(k, n_init=5, random_state=SEED).fit_predict(robust)
    sample["cluster"] = labels
    summary = sample.groupby("cluster").agg(n=("wallet", "size"), median_volume=("volume_usdc", "median"),
                                            median_n_trades=("n_trades", "median"),
                                            median_n_markets=("n_markets", "median"),
                                            mean_trade_price=("mean_trade_price", "mean")).reset_index()
    # Chi-square of cluster x dominant category (forced use of L12). category_refined, so few categories.
    ct = pd.crosstab(sample["cluster"], sample["dominant_category"].fillna("Unknown"))
    chi2, p, dof, expected = stats.chi2_contingency(ct)
    cramers_v = float(np.sqrt(chi2 / (ct.to_numpy().sum() * (min(ct.shape) - 1))))
    price = sample["mean_trade_price"].to_numpy(float)
    size = np.log1p(sample["median_trade_size"].to_numpy(float))
    res = {"n_sample": len(sample), "sample_seed": SEED, "k_chosen": k, "k_rule": "farthest point from the first-last line of the elbow curve",
           "features": names, "inertia": inertia, "cluster_summary": summary.to_dict("records"),
           "chi2_cluster_x_category": {"chi2": float(chi2), "df": int(dof), "p": float(p), "cramers_v": cramers_v,
                                       "n_categories": int(ct.shape[1]), "min_expected_count": float(expected.min())},
           "anova_mean_trade_price": anova_with_permutation(price, labels, k),
           "anova_log_median_trade_size": anova_with_permutation(size, labels, k),  # secondary line
           "robust_scaling_check": {"adjusted_rand_index_vs_zscore": float(adjusted_rand_score(labels, labels_robust)),
                                    "k": k, "seed": SEED, "features_with_zero_iqr": [n for n, z0 in zip(names, scale_table["iqr_was_zero"]) if z0]}}
    members = sample[["wallet", "role"]].assign(cluster_z=labels, cluster_robust=labels_robust)
    return res, inertia, scale_table, members


def draw_ccdf(wallets: pd.DataFrame, out: Path) -> None:
    fig, ax = plt.subplots(figsize=(6, 4), layout="constrained")
    for role, g in wallets.groupby("role"):
        xs = np.sort(g["volume_usdc"].to_numpy(float))
        idx = np.unique(np.logspace(0, np.log10(len(xs)), 3000).astype(int)) - 1
        ax.loglog(xs[idx], 1 - idx / len(xs), label=role, color=ROLE_COLOR[role])
    ax.set(xlabel="Wallet volume (USDC)", ylabel="CCDF (share of wallets above)")
    ax.grid(alpha=0.3)
    fig.legend(loc="outside upper center", ncol=2)
    fig.savefig(out / "fig6_ccdf.png", dpi=150)
    plt.close(fig)


def draw_lorenz(wallets: pd.DataFrame, out: Path) -> None:
    fig, ax = plt.subplots(figsize=(5.5, 5.5), layout="constrained")
    ax.plot([0, 1], [0, 1], color="#888888", ls="--", label="Equality")
    for role, g in wallets.groupby("role"):
        xs = np.sort(g["volume_usdc"].to_numpy(float))
        cum = np.concatenate([[0], np.cumsum(xs) / xs.sum()])
        idx = np.linspace(0, len(xs), 2000).astype(int)
        ax.plot(idx / len(xs), cum[idx], label=f"{role} (Gini {gini(xs):.3f})", color=ROLE_COLOR[role])
    ax.set(xlabel="Share of wallets (lowest volume first)", ylabel="Share of volume (USDC)")
    ax.grid(alpha=0.3)
    fig.legend(loc="outside upper center", ncol=3)
    fig.savefig(out / "fig7_lorenz.png", dpi=150)
    plt.close(fig)


def draw_elbow(inertia: dict[int, float], k: int, out: Path) -> None:
    fig, ax = plt.subplots(figsize=(5, 4), layout="constrained")
    ax.plot(list(inertia), list(inertia.values()), "o-", color="#222222")
    ax.axvline(k, color="#aa0000", ls="--")  # chosen K, explained in the caption
    ax.set(xlabel="K (number of clusters)", ylabel="Inertia (within-cluster squared distance)")
    ax.grid(alpha=0.3)
    fig.savefig(out / "fig8_elbow.png", dpi=150)
    plt.close(fig)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--params", required=True)
    ap.add_argument("--out", default=".")
    args = ap.parse_args()
    out, params = Path(args.out), load_params(args.params)

    def work() -> dict[str, str]:
        wallets = pd.read_parquet(out / "wallets.parquet")
        wallets = wallets[wallets["volume_usdc"] > 0]
        conc = concentration(wallets)
        tests = role_tests(wallets)
        rho = stats.spearmanr(wallets["n_trades"], wallets["volume_usdc"])
        clusters, inertia, scale_table, members = cluster_analysis(wallets)
        results = {"concentration": conc, "paper_gini_full_data_reference": PAPER_GINI, "role_tests": tests,
                   "spearman_n_trades_vs_volume": {"rho": float(rho.statistic), "p": float(rho.pvalue), "n": len(wallets)},
                   "kmeans": clusters}
        write_json(out / "q2_results.json", results)
        pd.DataFrame(conc).T.to_csv(out / "q2_concentration.csv")
        pd.DataFrame(clusters["cluster_summary"]).to_csv(out / "q2_clusters.csv", index=False)
        scale_table.to_csv(out / "q2_kmeans_scaling.csv", index=False)
        members.to_csv(out / "q2_kmeans_sample.csv", index=False)  # individual-level output (measurement.md §3)
        draw_ccdf(wallets, out)
        draw_lorenz(wallets, out)
        draw_elbow(inertia, clusters["k_chosen"], out)
        write_manifest(out, params, {"n_wallet_role_rows": len(wallets), "k": clusters["k_chosen"]}, __file__, STAGE)
        tab = md_table(pd.DataFrame(conc).T.reset_index().rename(columns={"index": "role"})[
            ["role", "n_wallets", "mean", "median", "top1_share", "top5_share", "top10_share", "gini"]])
        c = clusters
        return {
            "Why": "Q2: how concentrated is volume across wallets (addresses), and do wallet groups differ?",
            "Input data": f"wallets.parquet: {len(wallets)} wallet x role rows from kept markets. k-means on a fixed-seed sample of "
                          f"{c['n_sample']} rows (a wallet in both roles has two rows).",
            "Output data": "q2_results.json, q2_concentration.csv, q2_clusters.csv, q2_kmeans_scaling.csv, q2_kmeans_sample.csv, fig6_ccdf.png, fig7_lorenz.png, fig8_elbow.png",
            "Result": tab + f"\n\nPaper Gini (full data, reference only): maker {PAPER_GINI['maker']}, taker {PAPER_GINI['taker']}. "
                      f"Welch t on log10 volume: d={tests['welch_t']['cohens_d']:.3f}, p={tests['welch_t']['p']:.3g}. "
                      f"KS D={tests['ks']['D']:.3f}. Spearman rho(n_trades, volume)={rho.statistic:.3f}. "
                      f"K={c['k_chosen']}. Chi-square cluster x category: Cramer's V={c['chi2_cluster_x_category']['cramers_v']:.3f}, "
                      f"p={c['chi2_cluster_x_category']['p']:.3g} (min expected count {c['chi2_cluster_x_category']['min_expected_count']:.3g}). "
                      f"ANOVA on mean trade price across clusters: eta^2={c['anova_mean_trade_price']['eta_squared']:.3f}, "
                      f"permutation p={c['anova_mean_trade_price']['perm_p']:.3g}. "
                      f"Secondary, log median trade size: eta^2={c['anova_log_median_trade_size']['eta_squared']:.3f}. "
                      f"Stability: adjusted Rand index of robust-scaled vs z-score clusters = "
                      f"{c['robust_scaling_check']['adjusted_rand_index_vs_zscore']:.3f}.",
            "Figure": "![ccdf](fig6_ccdf.png) ![lorenz](fig7_lorenz.png) ![elbow](fig8_elbow.png)  Caption: wallet volume CCDF "
                      "(log-log), Lorenz curves, and the k-means elbow (dashed line = chosen K). Why: a curve far below the "
                      "equality line means few wallets hold most volume. Source: this run folder.",
        }

    run_stage(out, STAGE, "Q2: volume concentration, Gini, role tests, k-means side analysis.", work)


if __name__ == "__main__":
    main()
