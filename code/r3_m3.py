"""Robustness v3, M3: dependence between markets of one event (prereg_review_fixes.md section 3).

No event key exists in the data (owner D-039: proxies only, no Gamma API). Two proxy clusterings and the market itself:
K1 = first 3 tokens of market_slug, K2 = (category_refined, close_at hour UTC), K0 = market (iid bootstrap, method check).
Cluster bootstrap of the per-bin gap, the net gap and a chi-square built on bootstrap standard errors (X2_cl, outside the
lectures: our construction, ignores covariance between bins). Descriptive. The Q1 verdict stays as committed.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests

from common import md_table, run_stage, write_json, write_manifest
from r3_common import OUTSIDE_LECTURE, bin_of, load_kept, load_main_q1, rule_text, stage_args

STAGE = "r3_m3"


def proxy_keys(kept: pd.DataFrame, n_tokens: int) -> pd.DataFrame:
    slug = kept["market_slug"].str.lower()
    k1 = slug.str.split("-").str[:n_tokens].str.join("-")
    k1 = k1.where(slug.notna(), "__null__" + kept["market_id"])   # NULL slug: own cluster
    cat = kept["category_refined"].fillna("Unknown").astype(str)   # NULL category = "Unknown", as in common.group_categories
    hour = pd.to_datetime(kept["close_at"]).dt.floor("h").astype(str)
    return pd.DataFrame({"market_id": kept["market_id"], "k0": kept["market_id"], "k1": k1, "k2": cat + "|" + hour})


def cluster_sums(key: pd.Series, b: np.ndarray, y: np.ndarray, p: np.ndarray, n_bins: int) -> tuple[np.ndarray, ...]:
    """Per cluster (sorted by key) and per bin: count, sum y, sum p."""
    codes, uniques = pd.factorize(key, sort=True)
    shape = (len(uniques), n_bins)
    n_cb = np.zeros(shape)
    y_cb, p_cb = np.zeros(shape), np.zeros(shape)
    np.add.at(n_cb, (codes, b), 1.0)
    np.add.at(y_cb, (codes, b), y)
    np.add.at(p_cb, (codes, b), p)
    return n_cb, y_cb, p_cb, codes


def stats_of(totals: tuple[np.ndarray, np.ndarray, np.ndarray]) -> tuple[np.ndarray, float, float]:
    """Per-bin gap, net gap and chi-square (E = n x mean price) from bin totals."""
    n_b, y_b, p_b = totals
    with np.errstate(divide="ignore", invalid="ignore"):
        gap = (y_b - p_b) / n_b
        chi2 = np.nansum((y_b - p_b) ** 2 * (1 / p_b + 1 / (n_b - p_b)))
    return gap, float((y_b.sum() - p_b.sum()) / n_b.sum()), float(chi2)


def bootstrap(n_cb: np.ndarray, y_cb: np.ndarray, p_cb: np.ndarray, reps: int, seed: int) -> dict:
    """Cluster bootstrap: draw as many clusters as there are, with replacement; fresh generator per proxy."""
    rng = np.random.default_rng(seed)
    c = n_cb.shape[0]
    gaps, nets, chis = [], [], []
    for _ in range(reps):
        w = np.bincount(rng.integers(0, c, c), minlength=c).astype(float)
        g, net, chi2 = stats_of((w @ n_cb, w @ y_cb, w @ p_cb))
        gaps.append(g)
        nets.append(net)
        chis.append(chi2)
    return {"gap": np.array(gaps), "net": np.array(nets), "chi2": np.array(chis)}


def summarize(name: str, key: pd.Series, arrays: tuple, params: dict, main_res: dict, n: int, var_k0: np.ndarray | None) -> dict:
    n_cb, y_cb, p_cb, codes = arrays
    alpha = float(params["alpha"])
    boot = bootstrap(n_cb, y_cb, p_cb, int(params["m3_bootstrap_B"]), int(params["m3_seed"]))
    gap_obs, net_obs, _ = stats_of((n_cb.sum(0), y_cb.sum(0), p_cb.sum(0)))
    se = np.nanstd(boot["gap"], axis=0, ddof=1)
    var = se ** 2
    z = gap_obs / se
    pz = 2 * stats.norm.sf(np.abs(z))
    off = multipletests(pz, alpha=alpha, method="fdr_bh")[0]
    x2 = float(np.nansum(z ** 2))
    df_ = int(np.isfinite(z).sum())
    p = float(stats.chi2.sf(x2, df_))
    lo, hi = np.percentile(boot["net"], [2.5, 97.5])
    sizes = np.bincount(codes)
    res_for_rule = {"n_markets": n, "brier": 0.0, "chi2_gof": {"chi2": x2, "df": df_, "p": p, "effect_w": float(np.sqrt(x2 / n))},
                    "bins_reject_bh": int(off.sum()), "bins_reject_bonferroni": 0}
    text, main_text = rule_text(res_for_rule, alpha), rule_text(main_res, alpha)
    return {"name": name, "n_clusters": len(sizes), "median_cluster_size": float(np.median(sizes)), "max_cluster_size": int(sizes.max()),
            "share_markets_in_size1_clusters": float((sizes == 1).sum() / n), "net_gap": net_obs, "net_gap_ci_low": float(lo),
            "net_gap_ci_high": float(hi), "x2_cl": x2, "df": df_, "p": p, "w_cl": float(np.sqrt(x2 / n)),
            "bins_off_bh": int(off.sum()), "rule_text": text, "row_agreement": "same" if text == main_text else "different",
            "per_bin": [{"bin": b, "gap": float(gap_obs[b]), "ci_low": float(np.nanpercentile(boot["gap"][:, b], 2.5)),
                         "ci_high": float(np.nanpercentile(boot["gap"][:, b], 97.5)), "se": float(se[b]),
                         "deff": float(var[b] / var_k0[b]) if var_k0 is not None else 1.0, "z": float(z[b]), "p": float(pz[b]),
                         "off_bh": bool(off[b])} for b in range(len(se))], "_var": var, "label": OUTSIDE_LECTURE}


def draw(proxies: dict[str, dict], out) -> None:
    fig, ax = plt.subplots(figsize=(7, 3.6), layout="constrained")
    for i, (nm, r) in enumerate(proxies.items()):
        ax.errorbar(r["net_gap"], i, xerr=[[r["net_gap"] - r["net_gap_ci_low"]], [r["net_gap_ci_high"] - r["net_gap"]]],
                    fmt="o", color="#222222", capsize=3, label="Net gap with bootstrap 95% interval" if i == 0 else None)
    ax.axvline(0, color="#888888", ls="--", label="No gap")
    ax.set(yticks=range(len(proxies)), yticklabels=[f"{n} ({r['n_clusters']} clusters)" for n, r in proxies.items()],
           xlabel="Net gap mean(y - p_1d) (USDC per share)")
    ax.invert_yaxis()
    ax.grid(alpha=0.3)
    fig.legend(loc="outside upper center", ncol=2)
    fig.savefig(out / "fig_r3_m3_cluster_bootstrap.png", dpi=150)
    plt.close(fig)


def main() -> None:
    _, out, src, params = stage_args()
    n_bins, alpha = int(params["n_bins"]), float(params["alpha"])

    def work() -> dict[str, str]:
        kept = load_kept(out)
        main_res = load_main_q1(src)
        n = len(kept)
        keys = proxy_keys(kept, int(params["m3_k1_stem_tokens"]))
        keys[["market_id", "k1", "k2"]].to_csv(out / "m3_clusters.csv", index=False)
        b, y, p = bin_of(kept["p_1d"].to_numpy(), n_bins), kept["y"].to_numpy(float), kept["p_1d"].to_numpy(float)

        arrays = {k: cluster_sums(keys[k], b, y, p, n_bins) for k in ["k0", "k1", "k2"]}
        proxies: dict[str, dict] = {}
        k0 = summarize("k0_market", keys["k0"], arrays["k0"], params, main_res, n, None)
        # Method check: K0 bootstrap SE within +-tol of sd(y - p | bin) / sqrt(n_b), every bin.
        diff = pd.Series(y - p).groupby(b)
        analytic = (diff.std(ddof=1) / np.sqrt(diff.size())).to_numpy()
        ratio = np.sqrt(k0["_var"]) / analytic
        check = bool(np.all(np.abs(ratio - 1) <= float(params["m3_k0_se_tol"])))
        proxies["k0_market"] = k0
        for nm, k in [("k1_slug_stem", "k1"), ("k2_category_close_hour", "k2")]:
            proxies[nm] = summarize(nm, keys[k], arrays[k], params, main_res, n, k0["_var"])
        for r in proxies.values():
            r["method_check_passed"] = check
            r["method_check_flag"] = None if check else "method check failed"
        widths = {nm: proxies[nm]["net_gap_ci_high"] - proxies[nm]["net_gap_ci_low"] for nm in ["k1_slug_stem", "k2_category_close_hour"]}
        read = max(widths, key=widths.get)
        r = proxies[read]
        robust = bool(r["p"] < alpha and r["net_gap_ci_high"] < 0)
        for r_ in proxies.values():
            r_.pop("_var")
        payload = {"read_proxy": read, "robust_to_proxy": robust, "method_check_ratios": [float(x) for x in ratio],
                   "method_check_passed": check, "B": int(params["m3_bootstrap_B"]), "seed": int(params["m3_seed"]),
                   "approximation_note": "X2_cl ignores covariance between bins inside one cluster", "proxies": proxies}
        write_json(out / "m3_bootstrap.json", payload)
        flat_res = {"read_proxy": read, "robust_to_proxy": robust, "method_check_passed": check}
        for nm, rr in proxies.items():
            flat_res |= {f"{nm}_{k}": v for k, v in rr.items() if not isinstance(v, (list, dict))}
        write_json(out / "m3_results.json", flat_res)
        draw(proxies, out)
        write_manifest(out, params, flat_res, __file__, STAGE)
        tab = pd.DataFrame([{"proxy": nm, "clusters": r_["n_clusters"], "median size": r_["median_cluster_size"],
                             "max size": r_["max_cluster_size"], "share in size-1": r_["share_markets_in_size1_clusters"],
                             "X2_cl (df)": f"{r_['x2_cl']:.1f} ({r_['df']})", "p": r_["p"], "w_cl": r_["w_cl"],
                             "bins off BH": r_["bins_off_bh"],
                             "net gap [95% CI]": f"{r_['net_gap']:.4f} [{r_['net_gap_ci_low']:.4f}, {r_['net_gap_ci_high']:.4f}]",
                             "agreement": r_["row_agreement"]} for nm, r_ in proxies.items()])
        return {
            "Why": "M3: markets of one event move together, but the tests assume independent markets. No event key exists, so proxies stand in.",
            "Input data": f"{n} kept markets (market_slug, category_refined, close_at). Real data. Proxies: K1 first 3 slug tokens, "
                          f"K2 category x close hour (NULL category = Unknown). B {payload['B']}, seed {payload['seed']}.",
            "Output data": "m3_clusters.csv, m3_bootstrap.json, m3_results.json, fig_r3_m3_cluster_bootstrap.png",
            "Result": md_table(tab) + f"\n\nRead proxy (wider net gap interval): {read}. Robust to the proxy: {robust}. K0 method check "
                      f"(+-{params['m3_k0_se_tol']}): {'passed' if check else 'FAILED, K1 and K2 rows flagged'}. X2_cl is "
                      f"{OUTSIDE_LECTURE}: compare K1 or K2 with K0, not with 67.99. It ignores covariance between bins.",
            "Figure": "![m3](fig_r3_m3_cluster_bootstrap.png)  Caption: net gap with bootstrap 95% interval per clustering. "
                      "Why: a wider interval under K1 or K2 than under K0 shows dependence between markets. Source: this run folder.",
        }

    run_stage(out, STAGE, "M3: cluster bootstrap with proxy event keys.", work)


if __name__ == "__main__":
    main()
