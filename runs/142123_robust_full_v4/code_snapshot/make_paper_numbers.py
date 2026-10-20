"""Write a LaTeX numbers file (one \\newcommand per number) from a run's saved outputs.

Purpose: every number in a paper comes from a saved run file, never from hand typing
(rules/answering.md section 3, DECISIONS D-014).

Usage:
    OMP_NUM_THREADS=1 timeout 300 uv run python code/make_paper_numbers.py \
        --run runs/142083_mvp2_full_v2r3 --out papers/paper_mvp2/numbers.tex

Reads saved JSON/CSV only. Files of MVP2 (q1a_*, q1b_*, q1c_*) are optional.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Any

__all__ = ["main"]

ONES = ["Zero", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine",
        "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen",
        "Seventeen", "Eighteen", "Nineteen"]
TENS = {20: "Twenty", 30: "Thirty", 40: "Forty", 50: "Fifty", 60: "Sixty", 70: "Seventy",
        80: "Eighty", 90: "Ninety", 100: "Hundred"}
CATEGORY_NAME = {"Sports": "Sports", "Crypto": "Crypto", "Politics": "Politics",
                 "Finance": "Finance", "Other": "Other", "Culture": "Culture",
                 "Sci-Tech": "SciTech", "Price Action": "PriceAction"}
DROP_NAME = {"updown": "Updown", "non_binary": "NonBinary", "no_outcome": "NoOutcome",
             "no_price": "NoPrice", "stale_price": "StalePrice",
             "below_min_trades": "BelowMinTrades", "kept": "Kept"}
LONGSHOT_BINS = (0, 1)  # price bins 0-10% and 10-20%


def word(n: int) -> str:
    return ONES[n] if n < 20 else TENS[n]


class Macros:
    """Collects macros; each carries a source comment."""

    def __init__(self) -> None:
        self.lines: list[str] = []
        self.names: set[str] = set()

    def add(self, name: str, tex: str, src: str) -> None:
        if not re.fullmatch(r"[A-Za-z]+", name):
            raise ValueError(f"macro name must be letters only: {name}")
        if name in self.names:
            raise ValueError(f"duplicate macro: {name}")
        self.names.add(name)
        self.lines.append(f"% {src}\n\\newcommand{{\\{name}}}{{{tex}}}")


def count(n: int) -> str:
    return "\\ensuremath{" + f"{n:,}".replace(",", "{,}") + "}"


def num(x: float, d: int = 3) -> str:
    return "\\ensuremath{" + f"{x:.{d}f}" + "}"


def pct(x: float, d: int = 1) -> str:
    """x is a fraction; output is a percent in text mode."""
    return "\\ensuremath{" + f"{100 * x:.{d}f}" + "}\\%"


def pval(p: float) -> str:
    if p == 0:  # float underflow, below about 1e-308
        return "\\ensuremath{<10^{-300}}"
    if p >= 0.001:
        return "\\ensuremath{" + f"{p:.3f}" + "}"
    mant, exp = f"{p:.1e}".split("e")
    return "\\ensuremath{" + f"{mant}\\times10^{{{int(exp)}}}" + "}"


def text(s: str) -> str:
    return s.replace("\\", "\\textbackslash{}").replace("%", "\\%").replace("&", "\\&") \
            .replace("_", "\\_").replace("#", "\\#")


def load(run: Path, name: str, required: bool = True) -> Any:
    path = run / name
    if not path.exists():
        if required:
            raise FileNotFoundError(path)
        return None
    return json.loads(path.read_text())


def read_csv(run: Path, name: str) -> list[dict[str, str]]:
    with (run / name).open() as f:
        return list(csv.DictReader(f))


def bin_label(i: int) -> str:
    return word(10 * i) + word(10 * (i + 1))


def add_data(m: Macros, run: Path) -> None:
    t = load(run, "tables_summary.json")
    src = "tables_summary.json"
    scope = t["n_markets_in_scope"]
    m.add("NMarketsInScope", count(scope), f"{src}: n_markets_in_scope")
    m.add("NMarketsKept", count(t["n_kept"]), f"{src}: n_kept")
    m.add("PctMarketsKept", pct(t["n_kept"] / scope), f"{src}: n_kept / n_markets_in_scope")
    m.add("NMarketsKeptNoMin", count(t["n_kept_no_min_filter"]), f"{src}: n_kept_no_min_filter")
    for key, n in t["drop_reasons"].items():
        name = DROP_NAME[key]
        m.add(f"N{name}", count(n), f"{src}: drop_reasons.{key}")
        m.add(f"Pct{name}", pct(n / scope), f"{src}: drop_reasons.{key} / n_markets_in_scope")
    m.add("NTradesKeptMarkets", count(t["n_trades_in_kept_markets"]),
          f"{src}: n_trades_in_kept_markets")
    m.add("NWalletRoleRows", count(t["n_wallet_role_rows"]), f"{src}: n_wallet_role_rows")
    m.add("NTradeSizeSample", count(t["trade_size_sample_rows"]), f"{src}: trade_size_sample_rows")
    m.add("NKeptOpenSevenDays", count(t["n_kept_open_ge_7d"]), f"{src}: n_kept_open_ge_7d")
    m.add("NKeptWithPriceSevenDays", count(t["n_kept_with_p_7d"]), f"{src}: n_kept_with_p_7d")


def add_q1(m: Macros, run: Path) -> None:
    r = load(run, "q1_results.json")
    src = "q1_results.json"
    main = r["main_with_min_filter"]
    chi = main["chi2_gof"]
    m.add("QOneN", count(main["n_markets"]), f"{src}: main_with_min_filter.n_markets")
    m.add("QOneChiSq", num(chi["chi2"], 1), f"{src}: main_with_min_filter.chi2_gof.chi2")
    m.add("QOneDf", count(chi["df"]), f"{src}: main_with_min_filter.chi2_gof.df")
    m.add("QOneP", pval(chi["p"]), f"{src}: main_with_min_filter.chi2_gof.p")
    m.add("QOneW", num(chi["effect_w"], 3), f"{src}: main_with_min_filter.chi2_gof.effect_w")
    m.add("QOneBrier", num(main["brier"], 3), f"{src}: main_with_min_filter.brier")
    m.add("QOneLogLoss", num(main["log_loss"], 3), f"{src}: main_with_min_filter.log_loss")
    m.add("QOneEntropy", num(main["mean_entropy_bits"], 3),
          f"{src}: main_with_min_filter.mean_entropy_bits")
    m.add("QOneYesRate", pct(main["class_balance_yes"]),
          f"{src}: main_with_min_filter.class_balance_yes")
    m.add("QOneAccuracy", pct(main["confusion_at_0.5"]["accuracy"]),
          f"{src}: main_with_min_filter.confusion_at_0.5.accuracy")
    m.add("QOneKsD", num(main["ks_yes_vs_no"]["D"], 3),
          f"{src}: main_with_min_filter.ks_yes_vs_no.D")
    m.add("QOneBinsBh", count(main["bins_reject_bh"]), f"{src}: main_with_min_filter.bins_reject_bh")
    m.add("QOneBinsBonferroni", count(main["bins_reject_bonferroni"]),
          f"{src}: main_with_min_filter.bins_reject_bonferroni")
    nm = r["no_min_filter"]
    m.add("QOneNoMinN", count(nm["n_markets"]), f"{src}: no_min_filter.n_markets")
    m.add("QOneNoMinBrier", num(nm["brier"], 3), f"{src}: no_min_filter.brier")
    m.add("QOneNoMinChiSq", num(nm["chi2_gof"]["chi2"], 1), f"{src}: no_min_filter.chi2_gof.chi2")
    m.add("QOneNoMinP", pval(nm["chi2_gof"]["p"]), f"{src}: no_min_filter.chi2_gof.p")
    m.add("QOneNoMinW", num(nm["chi2_gof"]["effect_w"], 3), f"{src}: no_min_filter.chi2_gof.effect_w")
    m.add("MinTrades", count(r["min_trades"]), f"{src}: min_trades")

    for row in read_csv(run, "q1_bins.csv"):
        i = int(row["bin"])
        lab = bin_label(i)
        s = f"q1_bins.csv: bin={i}"
        m.add(f"Bin{lab}N", count(int(row["n"])), f"{s} n")
        m.add(f"Bin{lab}Price", pct(float(row["mean_price"])), f"{s} mean_price")
        m.add(f"Bin{lab}Obs", pct(float(row["observed_rate"])), f"{s} observed_rate")
        m.add(f"Bin{lab}Diff", pct(float(row["diff_obs_minus_price"]), 2),
              f"{s} diff_obs_minus_price")
        m.add(f"Bin{lab}CiLow", pct(float(row["ci_low"])), f"{s} ci_low")
        m.add(f"Bin{lab}CiHigh", pct(float(row["ci_high"])), f"{s} ci_high")
        m.add(f"Bin{lab}P", pval(float(row["binom_p"])), f"{s} binom_p")
        m.add(f"Bin{lab}BhP", pval(float(row["p_bh"])), f"{s} p_bh")


def add_q1a(m: Macros, run: Path) -> None:
    r = load(run, "q1a_results.json", required=False)
    if r is None:
        return
    src = "q1a_results.json"
    chi = r["chi_square_independence"]
    m.add("QOneAN", count(chi["n"]), f"{src}: chi_square_independence.n")
    m.add("QOneAChiSq", num(chi["chi2"], 1), f"{src}: chi_square_independence.chi2")
    m.add("QOneADf", count(chi["df"]), f"{src}: chi_square_independence.df")
    m.add("QOneAP", pval(chi["p"]), f"{src}: chi_square_independence.p")
    m.add("QOneAV", num(chi["cramers_v"], 3), f"{src}: chi_square_independence.cramers_v")
    m.add("QOneAMinExpected", num(chi["min_expected_count"], 1),
          f"{src}: chi_square_independence.min_expected_count")
    m.add("QOneANCategories", count(chi["n_categories"]), f"{src}: chi_square_independence.n_categories")
    bt = r["bin_tests"]
    m.add("QOneABinsTested", count(bt["n_tested"]), f"{src}: bin_tests.n_tested")
    m.add("QOneABinsBh", count(bt["reject_bh"]), f"{src}: bin_tests.reject_bh")
    m.add("QOneABinsBonferroni", count(bt["reject_bonferroni"]), f"{src}: bin_tests.reject_bonferroni")
    bs = r["brier_tests"]
    m.add("QOneAAnovaF", num(bs["anova_F"], 1), f"{src}: brier_tests.anova_F")
    m.add("QOneAAnovaP", pval(bs["anova_p"]), f"{src}: brier_tests.anova_p")
    m.add("QOneAEtaSq", num(bs["eta_squared"], 3), f"{src}: brier_tests.eta_squared")
    m.add("QOneAPermP", pval(bs["perm_p"]), f"{src}: brier_tests.perm_p")
    m.add("QOneANPerm", count(bs["n_perm"]), f"{src}: brier_tests.n_perm")

    cont = {c["category_group"]: c for c in read_csv(run, "q1a_contingency.csv")}
    for cat, c in cont.items():
        k = CATEGORY_NAME[cat]
        s = f"q1a_contingency.csv: category_group={cat}"
        m.add(f"Cat{k}N", count(int(c["n"])), f"{s} n")
        m.add(f"Cat{k}FavWin", pct(float(c["favorite_win_rate"])), f"{s} favorite_win_rate")
        m.add(f"Cat{k}Brier", num(float(c["mean_brier"]), 3), f"{s} mean_brier")
    for row in read_csv(run, "q1a_bins_by_category.csv"):
        i = int(row["bin"])
        if i not in LONGSHOT_BINS:
            continue
        k, lab = CATEGORY_NAME[row["category"]], bin_label(i)
        s = f"q1a_bins_by_category.csv: category={row['category']} bin={i}"
        m.add(f"Cat{k}Bin{lab}N", count(int(row["n"])), f"{s} n")
        m.add(f"Cat{k}Bin{lab}Price", pct(float(row["mean_price"])), f"{s} mean_price")
        m.add(f"Cat{k}Bin{lab}Obs", pct(float(row["observed_rate"])), f"{s} observed_rate")
        m.add(f"Cat{k}Bin{lab}Diff", pct(float(row["diff_obs_minus_price"]), 2),
              f"{s} diff_obs_minus_price")
        m.add(f"Cat{k}Bin{lab}BhP", pval(float(row["p_bh"])), f"{s} p_bh")


def add_q1b(m: Macros, run: Path) -> None:
    r = load(run, "q1b_results.json", required=False)
    if r is None:
        return
    src = "q1b_results.json"
    d = r["brier_diff_7d_minus_1d"]
    m.add("QOneBN", count(d["n"]), f"{src}: brier_diff_7d_minus_1d.n")
    m.add("QOneBMeanDiff", num(d["mean_diff"], 4), f"{src}: brier_diff_7d_minus_1d.mean_diff")
    m.add("QOneBCiLow", num(d["ci_low"], 4), f"{src}: brier_diff_7d_minus_1d.ci_low")
    m.add("QOneBCiHigh", num(d["ci_high"], 4), f"{src}: brier_diff_7d_minus_1d.ci_high")
    m.add("QOneBT", num(d["t"], 1), f"{src}: brier_diff_7d_minus_1d.t")
    m.add("QOneBDf", count(d["df"]), f"{src}: brier_diff_7d_minus_1d.df")
    m.add("QOneBP", pval(d["p"]), f"{src}: brier_diff_7d_minus_1d.p")
    m.add("QOneBD", num(d["cohens_d"], 2), f"{src}: brier_diff_7d_minus_1d.cohens_d")
    m.add("QOneBBrierSevenDays", num(r["brier"]["7d"], 3), f"{src}: brier.7d")
    m.add("QOneBBrierOneDay", num(r["brier"]["1d"], 3), f"{src}: brier.1d")
    a = r["abs_error_diff_7d_minus_1d"]
    m.add("QOneBAbsMeanDiff", num(a["mean_diff"], 4), f"{src}: abs_error_diff_7d_minus_1d.mean_diff")
    m.add("QOneBAbsD", num(a["cohens_d"], 2), f"{src}: abs_error_diff_7d_minus_1d.cohens_d")
    m.add("QOneBEntropyDiff", num(r["mean_entropy_bits"]["diff_7d_minus_1d"], 3),
          f"{src}: mean_entropy_bits.diff_7d_minus_1d")
    for tag, key in (("SevenDays", "7d"), ("OneDay", "1d")):
        m.add(f"QOneBKsD{tag}", num(r["ks_yes_vs_no"][key]["D"], 3), f"{src}: ks_yes_vs_no.{key}.D")
    sel = r["selection"]
    m.add("QOneBMaxStaleHours", count(int(sel["max_staleness_h"])), f"{src}: selection.max_staleness_h")


def add_q1c(m: Macros, run: Path) -> None:
    r = load(run, "q1c_results.json", required=False)
    if r is None:
        return
    src = "q1c_results.json"
    for tag, key in (("Volume", "spearman_log_volume_vs_error"), ("Trades", "spearman_log_trades_vs_error")):
        d = r[key]
        m.add(f"QOneC{tag}N", count(d["n"]), f"{src}: {key}.n")
        m.add(f"QOneC{tag}Rho", num(d["rho"], 3), f"{src}: {key}.rho")
        m.add(f"QOneC{tag}CiLow", num(d["ci_low"], 3), f"{src}: {key}.ci_low")
        m.add(f"QOneC{tag}CiHigh", num(d["ci_high"], 3), f"{src}: {key}.ci_high")
        m.add(f"QOneC{tag}P", pval(d["p"]), f"{src}: {key}.p")


def add_q2(m: Macros, run: Path) -> None:
    r = load(run, "q2_results.json")
    src = "q2_results.json"
    for role in ("maker", "taker"):
        c, R = r["concentration"][role], role.capitalize()
        m.add(f"{R}NWallets", count(c["n_wallets"]), f"{src}: concentration.{role}.n_wallets")
        m.add(f"{R}Gini", num(c["gini"], 3), f"{src}: concentration.{role}.gini")
        m.add(f"{R}TopOneShare", pct(c["top1_share"]), f"{src}: concentration.{role}.top1_share")
        m.add(f"{R}TopFiveShare", pct(c["top5_share"]), f"{src}: concentration.{role}.top5_share")
        m.add(f"{R}TopTenShare", pct(c["top10_share"]), f"{src}: concentration.{role}.top10_share")
        m.add(f"{R}MeanVolume", count(round(c["mean"])), f"{src}: concentration.{role}.mean")
        m.add(f"{R}MedianVolume", num(c["median"], 1), f"{src}: concentration.{role}.median")
    w = r["role_tests"]["welch_t"]
    m.add("RoleWelchT", num(w["t"], 1), f"{src}: role_tests.welch_t.t")
    m.add("RoleWelchP", pval(w["p"]), f"{src}: role_tests.welch_t.p")
    m.add("RoleCohenD", num(w["cohens_d"], 2), f"{src}: role_tests.welch_t.cohens_d")
    m.add("RoleKsD", num(r["role_tests"]["ks"]["D"], 3), f"{src}: role_tests.ks.D")
    sp = r["spearman_n_trades_vs_volume"]
    m.add("SpearmanTradesVolumeRho", num(sp["rho"], 3), f"{src}: spearman_n_trades_vs_volume.rho")
    km = r["kmeans"]
    m.add("KmeansK", count(km["k_chosen"]), f"{src}: kmeans.k_chosen")
    m.add("KmeansNSample", count(km["n_sample"]), f"{src}: kmeans.n_sample")
    m.add("KmeansAri", num(km["robust_scaling_check"]["adjusted_rand_index_vs_zscore"], 2),
          f"{src}: kmeans.robust_scaling_check.adjusted_rand_index_vs_zscore")
    cx = km["chi2_cluster_x_category"]
    m.add("KmeansCategoryV", num(cx["cramers_v"], 3), f"{src}: kmeans.chi2_cluster_x_category.cramers_v")
    for c in km["cluster_summary"]:
        i, s = word(c["cluster"]), f"{src}: kmeans.cluster_summary[cluster={c['cluster']}]"
        m.add(f"Cluster{i}N", count(c["n"]), f"{s}.n")
        m.add(f"Cluster{i}MedianVolume", num(c["median_volume"], 1), f"{s}.median_volume")
        m.add(f"Cluster{i}MedianTrades", num(c["median_n_trades"], 0), f"{s}.median_n_trades")
        m.add(f"Cluster{i}MedianMarkets", num(c["median_n_markets"], 0), f"{s}.median_n_markets")


def add_q3(m: Macros, run: Path) -> None:
    r = load(run, "q3_results.json")
    src = "q3_results.json"
    p1 = r["summary"]["p_1d"]
    m.add("PriceOneDayMean", num(p1["mean"], 3), f"{src}: summary.p_1d.mean")
    m.add("PriceOneDayMedian", num(p1["median"], 3), f"{src}: summary.p_1d.median")
    ts = r["summary"]["trade_size_usdc"]
    m.add("TradeSizeMean", num(ts["mean"], 1), f"{src}: summary.trade_size_usdc.mean")
    m.add("TradeSizeMedian", num(ts["median"], 2), f"{src}: summary.trade_size_usdc.median")
    for tag, key in (("TradeSize", "trade_size_usdc"), ("WalletVolume", "wallet_volume_usdc")):
        pl = r["fits"][key]["power_law"]
        m.add(f"{tag}PowerAlpha", num(pl["alpha"], 2), f"{src}: fits.{key}.power_law.alpha")
        m.add(f"{tag}PowerXmin", num(pl["xmin"], 1), f"{src}: fits.{key}.power_law.xmin")
        m.add(f"{tag}PowerKsD", num(pl["D"], 3), f"{src}: fits.{key}.power_law.D")
        m.add(f"{tag}NormalKsD", num(r["fits"][key]["normal"]["D"], 3), f"{src}: fits.{key}.normal.D")


def add_meta(m: Macros, run: Path) -> None:
    man = load(run, "manifest_q1_calibration.json")
    src = "manifest_q1_calibration.json"
    m.add("RunId", text(run.name), "run directory name")
    m.add("CodeVersion", text(man["code_version"]), f"{src}: code_version")
    m.add("CodeSha", text(man["code_sha"]), f"{src}: code_sha")
    m.add("SlurmJobId", text(man["env"]["slurm_job_id"]), f"{src}: env.slurm_job_id")
    v = load(run, "verdicts.json")
    for q, d in v["comparisons"].items():
        name = "QOne" + q[2:].upper()
        m.add(f"Verdict{name}", text(d["verdict"]), f"verdicts.json: comparisons.{q}.verdict")
    m.add("Alpha", num(v["alpha"], 2), "verdicts.json: alpha")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--run", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args()
    m = Macros()
    for fn in (add_meta, add_data, add_q1, add_q1a, add_q1b, add_q1c, add_q2, add_q3):
        fn(m, a.run)
    a.out.parent.mkdir(parents=True, exist_ok=True)
    header = f"% Generated by code/make_paper_numbers.py from {a.run}. Do not edit by hand.\n"
    a.out.write_text(header + "\n".join(m.lines) + "\n")
    print(f"{a.out}: {len(m.names)} macros")


if __name__ == "__main__":
    main()
