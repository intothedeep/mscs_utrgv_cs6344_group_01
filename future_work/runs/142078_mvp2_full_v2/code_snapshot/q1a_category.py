"""MVP2 Q1a: does accuracy depend on the topic? Category x favorite-won, bin tests per category, Brier across categories.

Population = markets kept WITH the min_trades filter (the Q1 main set). Category = category_refined.
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
from statsmodels.stats.multitest import multipletests

from common import load_params, md_table, run_stage, write_json, write_manifest
from q1_calibration import bin_table

STAGE = "q1a_category"
MIN_BIN_N = 5          # bins with fewer markets are listed but not tested
OTHER, UNKNOWN = "Other", "Unknown"


def group_categories(df: pd.DataFrame, min_n: int) -> tuple[pd.DataFrame, pd.Series]:
    """Add category_group: categories with >= min_n kept markets stay, the rest merge into 'Other'."""
    cat = df["category_refined"].fillna(UNKNOWN).astype(str)
    counts = cat.value_counts()
    big = counts[counts >= min_n].index
    out = df.copy()
    out["category_group"] = cat.where(cat.isin(big), OTHER)
    return out, counts


def chi_square_independence(tab: pd.DataFrame) -> dict:
    """Chi-square of independence on category x {won, lost}, with Cramer's V = sqrt(chi2 / (N * min(r-1, c-1)))."""
    tab = tab.loc[tab.sum(axis=1) > 0]
    if tab.shape[0] < 2 or (tab.sum(axis=0) == 0).any():
        return {"chi2": None, "df": None, "p": None, "cramers_v": None, "n": int(tab.to_numpy().sum()),
                "note": "fewer than 2 categories or an empty outcome column: test not defined"}
    chi2, p, dof, expected = stats.chi2_contingency(tab.to_numpy())
    n = int(tab.to_numpy().sum())
    v = float(np.sqrt(chi2 / (n * (min(tab.shape) - 1))))
    return {"chi2": float(chi2), "df": int(dof), "p": float(p), "cramers_v": v, "n": n,
            "n_categories": int(tab.shape[0]), "min_expected_count": float(expected.min())}


def category_bins(df: pd.DataFrame, n_bins: int, alpha: float) -> pd.DataFrame:
    """Bin table per category (equal-width bins), with Bonferroni and BH over every tested category x bin."""
    parts = []
    for cat, g in df.groupby("category_group"):
        g = g.assign(bin=np.minimum((g["p_1d"] * n_bins).astype(int), n_bins - 1))
        b = bin_table(g, "bin", alpha)
        b.insert(0, "category", cat)
        parts.append(b)
    bins = pd.concat(parts, ignore_index=True)
    tested = bins["n"] >= MIN_BIN_N
    bins["tested"] = tested
    for name, method in [("bonferroni", "bonferroni"), ("bh", "fdr_bh")]:
        bins[f"p_{name}"] = np.nan
        if tested.any():
            bins.loc[tested, f"p_{name}"] = multipletests(bins.loc[tested, "binom_p"], alpha=alpha, method=method)[1]
        bins[f"reject_{name}"] = bins[f"p_{name}"] < alpha
    return bins


def brier_across_categories(df: pd.DataFrame, n_perm: int, seed: int) -> dict:
    """One-way ANOVA on per-market Brier, and a permutation test of eta squared (category labels shuffled)."""
    err = df["brier"].to_numpy()
    codes, names = pd.factorize(df["category_group"])
    k = len(names)
    ss_total = float(((err - err.mean()) ** 2).sum())
    if k < 2 or ss_total == 0:
        return {"note": "fewer than 2 categories or zero variance: test not defined"}
    n_g = np.bincount(codes, minlength=k)

    def eta_squared(c: np.ndarray) -> float:
        ss_between = (np.bincount(c, weights=err, minlength=k) ** 2 / n_g).sum() - err.sum() ** 2 / len(err)
        return float(ss_between / ss_total)

    f = stats.f_oneway(*[err[codes == i] for i in range(k)])
    obs = eta_squared(codes)
    rng = np.random.default_rng(seed)
    perm = np.array([eta_squared(rng.permutation(codes)) for _ in range(n_perm)])
    return {"anova_F": float(f.statistic), "anova_p": float(f.pvalue), "eta_squared": obs,
            "perm_p": float((1 + (perm >= obs).sum()) / (1 + n_perm)), "n_perm": n_perm, "seed": seed,
            "n_categories": int(k), "mean_brier_by_category": df.groupby("category_group")["brier"].mean().to_dict()}


def analyze(df: pd.DataFrame, params: dict) -> tuple[dict, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    n_bins, alpha = int(params["n_bins"]), float(params["alpha"])
    df, raw_counts = group_categories(df, int(params["min_category_n"]))
    df["favorite_won"] = ((df["p_1d"] >= 0.5) & (df["y"] == 1)) | ((df["p_1d"] < 0.5) & (df["y"] == 0))
    df["brier"] = (df["p_1d"] - df["y"]) ** 2
    df["bin"] = np.minimum((df["p_1d"] * n_bins).astype(int), n_bins - 1)
    tab = pd.crosstab(df["category_group"], df["favorite_won"].map({True: "won", False: "lost"}))
    tab = tab.reindex(columns=["won", "lost"], fill_value=0)
    tab["n"] = tab["won"] + tab["lost"]
    tab["favorite_win_rate"] = tab["won"] / tab["n"]
    tab["mean_brier"] = df.groupby("category_group")["brier"].mean()
    tab = tab.sort_values("n", ascending=False)
    bins = category_bins(df, n_bins, alpha)
    merged = raw_counts[~raw_counts.index.isin(df["category_group"].unique())]
    sports = {c: int(n) for c, n in raw_counts.items() if "sport" in c.lower()}
    res = {
        "n_markets": len(df), "min_category_n": int(params["min_category_n"]),
        "n_by_category_raw": raw_counts.to_dict(), "merged_into_other": merged.to_dict(),
        "sports_n": sports if sports else "no category name contains 'sport'",
        "chi_square_independence": chi_square_independence(tab[["won", "lost"]]),
        "bin_tests": {"n_tested": int(bins["tested"].sum()), "bins_total": len(bins),
                      "reject_bonferroni": int(bins["reject_bonferroni"].sum()),
                      "reject_bh": int(bins["reject_bh"].sum())},
        "brier_tests": brier_across_categories(df, int(params["n_perm"]), int(params["seed"])),
    }
    return res, tab, bins, df


def draw_calibration_by_category(bins: pd.DataFrame, tab: pd.DataFrame, out: Path) -> None:
    cats = list(tab.index)
    ncols = min(3, len(cats))
    nrows = int(np.ceil(len(cats) / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(3.3 * ncols + 0.6, 3.3 * nrows + 1.0), sharex=True, sharey=True,
                             layout="constrained", squeeze=False)
    for ax, cat in zip(axes.flat, cats):
        b = bins[(bins["category"] == cat) & bins["tested"]]
        err = np.clip(np.vstack([b["observed_rate"] - b["ci_low"], b["ci_high"] - b["observed_rate"]]), 0, None)  # float rounding can give -1e-17 at rate 0 or 1; plot only
        ax.plot([0, 1], [0, 1], color="#888888", ls="--")
        ax.errorbar(b["mean_price"], b["observed_rate"], yerr=err, fmt="o", ms=3.5, capsize=2, color="#222222")
        ax.set_title(f"{cat} (n={int(tab.loc[cat, 'n'])})", fontsize=9)
        ax.set(xlim=(0, 1), ylim=(0, 1))
        ax.grid(alpha=0.3)
    for ax in axes.flat[len(cats):]:
        ax.set_visible(False)
    fig.supxlabel("Mean price p_1d in bin (USDC per share)", fontsize=9)
    fig.supylabel("Observed Yes rate (share of markets)", fontsize=9)
    handles = [Line2D([], [], color="#888888", ls="--", label="Perfect calibration"),
               Line2D([], [], color="#222222", marker="o", ls="", ms=4, label="Bin with n >= 5, 95% Wilson CI")]
    fig.legend(handles=handles, loc="outside upper center", ncol=2)
    fig.savefig(out / "fig9_calibration_by_category.png", dpi=150)
    plt.close(fig)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--params", required=True)
    ap.add_argument("--out", default=".")
    args = ap.parse_args()
    out, params = Path(args.out), load_params(args.params)

    def work() -> dict[str, str]:
        m = pd.read_parquet(out / "markets.parquet")
        main_df = m[m["kept"]][["market_id", "category_refined", "p_1d", "y"]]
        if len(main_df) < 20:
            raise ValueError(f"only {len(main_df)} kept markets: too few for Q1a")
        res, tab, bins, per_market = analyze(main_df, params)
        tab.to_csv(out / "q1a_contingency.csv")
        bins.to_csv(out / "q1a_bins_by_category.csv", index=False)
        # Individual-level output (measurement.md §3): every market in the test, with its group and error.
        per_market[["market_id", "category_refined", "category_group", "p_1d", "y", "favorite_won", "brier", "bin"]] \
            .to_csv(out / "q1a_markets.csv", index=False)
        write_json(out / "q1a_results.json", res)
        draw_calibration_by_category(bins, tab, out)
        write_manifest(out, params, res, __file__, STAGE)
        saved = json.loads((out / "q1a_results.json").read_text())  # report numbers come from the saved JSON
        chi, bt, br = saved["chi_square_independence"], saved["bin_tests"], saved["brier_tests"]
        tab_md = md_table(tab.reset_index().rename(columns={"category_group": "category"}))
        merged = ", ".join(f"{c} ({n})" for c, n in saved["merged_into_other"].items()) or "none"
        return {
            "Why": "Q1a: does the favorite win equally often in every topic, and is the price equally calibrated?",
            "Input data": f"markets.parquet: {saved['n_markets']} kept markets (with min_trades filter), real data. "
                          f"Category = category_refined, categories under {saved['min_category_n']} markets merged into "
                          f"'{OTHER}'. Favorite = side with p_1d >= 0.5.",
            "Output data": "q1a_contingency.csv, q1a_bins_by_category.csv, q1a_markets.csv, q1a_results.json, "
                           "fig9_calibration_by_category.png",
            "Result": (f"Chi-square of independence: chi2={chi.get('chi2')}, df={chi.get('df')}, p={chi.get('p')}, "
                       f"Cramer's V={chi.get('cramers_v')} (min expected count {chi.get('min_expected_count')}).\n\n"
                       f"Bin tests (n >= {MIN_BIN_N}): {bt['n_tested']} of {bt['bins_total']} category x bin cells tested. "
                       f"Rejected: Bonferroni {bt['reject_bonferroni']}, BH {bt['reject_bh']}.\n\n"
                       f"Brier across categories: ANOVA F={br.get('anova_F')}, p={br.get('anova_p')}, "
                       f"eta squared={br.get('eta_squared')}, permutation p={br.get('perm_p')} "
                       f"({br.get('n_perm')} perms, seed {br.get('seed')}).\n\n"
                       f"Under-represented: merged into '{OTHER}': {merged}. Sports: {saved['sports_n']}. "
                       f"Sports mostly drops out of the Standard Binary sample (plan, paper limitation 7).\n\n"
                       f"n per category, favorite win rate and mean Brier:\n\n{tab_md}"),
            "Figure": "![calibration by category](fig9_calibration_by_category.png)  Caption: observed Yes rate against "
                      "mean price per bin, one panel per category, shared axes. "
                      "Why: a panel off the diagonal shows a topic where the price is miscalibrated. Source: this run folder.",
        }

    run_stage(out, STAGE, "Q1a: does accuracy depend on the topic?", work)


if __name__ == "__main__":
    main()
