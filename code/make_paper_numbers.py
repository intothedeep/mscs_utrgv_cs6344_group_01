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
import hashlib
import json
import re
from pathlib import Path
from typing import Any

import pandas as pd

__all__ = ["main"]

# Number format, one rule per quantity type (F7). Every macro goes through exactly one helper.
#
# | Quantity                                             | Helper   | Format                               |
# | ---------------------------------------------------- | -------- | ------------------------------------ |
# | Counts (markets, trades, wallets, n, df, permutations) | count  | integer, thousands separator {,}     |
# | Shares and percent                                   | pct      | 1 decimal + \%                       |
# | Exception (a): gaps in percentage points (*Diff)     | pct2     | 2 decimals + \%                      |
# | Exception (b): shares near 0 or 100 percent where 1  | pct2     | 2 decimals + \%                      |
# |   decimal hides estimate vs CI (R1 classes, agreement, |        |                                      |
# |   R2 crossing and delta shares)                      |          |                                      |
# | Brier, w, V, d, d_z, rho, Gini, ARI, eta squared,    | est      | 3 decimals                           |
# |   KS D, entropy, log loss, power-law exponent        |          |                                      |
# | Test statistics (chi-square, t, F)                   | stat     | 1 decimal                            |
# | USDC amounts, expected counts, x_min                 | amount   | 1 decimal, thousands separator       |
# | Confidence interval ends                             | as estimate | same helper and decimals as the estimate |
# | p-value                                              | pval     | below 0.001: 2 significant digits    |
# |                                                      |          |   in scientific form; else 3 decimals |
# | Significance level alpha                             | level    | shortest exact form (0.05)           |
#
# A p-value of exactly 0 in the saved file is float underflow and prints as <10^{-300}.

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


def median_count(x: float) -> str:
    """A median of whole counts is an integer or a half; keep the half (292.5), never round it away."""
    return count(int(x)) if x == int(x) else "\\ensuremath{" + _grouped(x, 1) + "}"


def _grouped(x: float, d: int) -> str:
    """Fixed decimals with a thousands separator that also works in math mode."""
    text_ = f"{x:,.{d}f}"
    if float(text_.replace(",", "")) == 0:
        text_ = text_.lstrip("-")  # no negative zero such as -0.0
    return text_.replace(",", "{,}")


def est(x: float) -> str:
    return "\\ensuremath{" + _grouped(x, 3) + "}"


def stat(x: float) -> str:
    return "\\ensuremath{" + _grouped(x, 1) + "}"


def amount(x: float) -> str:
    return "\\ensuremath{" + _grouped(x, 1) + "}"


def level(x: float) -> str:
    return "\\ensuremath{" + f"{x:g}" + "}"


def pct(x: float) -> str:
    """x is a fraction; output is a percent in text mode, one decimal."""
    return "\\ensuremath{" + _grouped(100 * x, 1) + "}\\%"


def pct2(x: float) -> str:
    """Percent with two decimals: gaps in points, and shares near 0 or 100 percent."""
    return "\\ensuremath{" + _grouped(100 * x, 2) + "}\\%"


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
    m.add("QOneChiSq", stat(chi["chi2"]), f"{src}: main_with_min_filter.chi2_gof.chi2")
    m.add("QOneDf", count(chi["df"]), f"{src}: main_with_min_filter.chi2_gof.df")
    m.add("QOneP", pval(chi["p"]), f"{src}: main_with_min_filter.chi2_gof.p")
    m.add("QOneW", est(chi["effect_w"]), f"{src}: main_with_min_filter.chi2_gof.effect_w")
    m.add("QOneBrier", est(main["brier"]), f"{src}: main_with_min_filter.brier")
    m.add("QOneLogLoss", est(main["log_loss"]), f"{src}: main_with_min_filter.log_loss")
    m.add("QOneEntropy", est(main["mean_entropy_bits"]),
          f"{src}: main_with_min_filter.mean_entropy_bits")
    m.add("QOneYesRate", pct(main["class_balance_yes"]),
          f"{src}: main_with_min_filter.class_balance_yes")
    m.add("QOneAccuracy", pct(main["confusion_at_0.5"]["accuracy"]),
          f"{src}: main_with_min_filter.confusion_at_0.5.accuracy")
    m.add("QOnePrecision", pct(main["confusion_at_0.5"]["precision"]),
          f"{src}: main_with_min_filter.confusion_at_0.5.precision")
    m.add("QOneRecall", pct(main["confusion_at_0.5"]["recall"]),
          f"{src}: main_with_min_filter.confusion_at_0.5.recall")
    m.add("QOneKsD", est(main["ks_yes_vs_no"]["D"]),
          f"{src}: main_with_min_filter.ks_yes_vs_no.D")
    m.add("QOneBinsBh", count(main["bins_reject_bh"]), f"{src}: main_with_min_filter.bins_reject_bh")
    m.add("QOneBinsBonferroni", count(main["bins_reject_bonferroni"]),
          f"{src}: main_with_min_filter.bins_reject_bonferroni")
    nm = r["no_min_filter"]
    m.add("QOneNoMinN", count(nm["n_markets"]), f"{src}: no_min_filter.n_markets")
    m.add("QOneNoMinBrier", est(nm["brier"]), f"{src}: no_min_filter.brier")
    m.add("QOneNoMinChiSq", stat(nm["chi2_gof"]["chi2"]), f"{src}: no_min_filter.chi2_gof.chi2")
    m.add("QOneNoMinP", pval(nm["chi2_gof"]["p"]), f"{src}: no_min_filter.chi2_gof.p")
    m.add("QOneNoMinW", est(nm["chi2_gof"]["effect_w"]), f"{src}: no_min_filter.chi2_gof.effect_w")
    m.add("MinTrades", count(r["min_trades"]), f"{src}: min_trades")

    for row in read_csv(run, "q1_bins.csv"):
        i = int(row["bin"])
        lab = bin_label(i)
        s = f"q1_bins.csv: bin={i}"
        m.add(f"Bin{lab}N", count(int(row["n"])), f"{s} n")
        m.add(f"Bin{lab}Price", pct(float(row["mean_price"])), f"{s} mean_price")
        m.add(f"Bin{lab}Obs", pct(float(row["observed_rate"])), f"{s} observed_rate")
        m.add(f"Bin{lab}Diff", pct2(float(row["diff_obs_minus_price"])),
              f"{s} diff_obs_minus_price")
        m.add(f"Bin{lab}CiLow", pct(float(row["ci_low"])), f"{s} ci_low")
        m.add(f"Bin{lab}CiHigh", pct(float(row["ci_high"])), f"{s} ci_high")
        m.add(f"Bin{lab}P", pval(float(row["binom_p"])), f"{s} binom_p")
        m.add(f"Bin{lab}BhP", pval(float(row["p_bh"])), f"{s} p_bh")


def bh_reject_count(p_values: list[float], alpha: float) -> int:
    """Benjamini-Hochberg: number of rejections at level alpha (step-up on sorted p)."""
    ps = sorted(p_values)
    m = len(ps)
    k = max((i for i, p in enumerate(ps, start=1) if p <= alpha * i / m), default=0)
    return k


def add_q1_eqfreq(m: Macros, run: Path, alpha: float, q1eqfreq: Path | None) -> None:
    rows = read_csv(run, "q1_bins_eqfreq.csv")
    m.add("QOneEqFreqBins", count(len(rows)), "q1_bins_eqfreq.csv: row count")
    if q1eqfreq is not None:
        saved = read_csv(q1eqfreq, "q1_bins_eqfreq.csv")
        same = len(saved) == len(rows) and all(
            abs(float(a["binom_p"]) - float(b["binom_p"])) <= 1e-12 * max(1.0, abs(float(a["binom_p"])))
            for a, b in zip(rows, saved))
        if not same:
            raise ValueError(f"{q1eqfreq.name}/q1_bins_eqfreq.csv binom_p differs from {run.name}")
        k = sum(r["reject_bh"] == "True" for r in saved)
        m.add("QOneEqFreqBinsBh", count(k), f"{q1eqfreq.name}/q1_bins_eqfreq.csv: reject_bh (saved run output, code v5)")
        return
    # Fallback when no --q1eqfreq run is given: the 142082/142083 file has no p_bh column.
    k = bh_reject_count([float(r["binom_p"]) for r in rows], alpha)
    m.add("QOneEqFreqBinsBh", count(k), "q1_bins_eqfreq.csv: COMPUTED by this script (BH on the saved binom_p at "
          "verdicts.json alpha), not a saved run output; the file has no p_bh column")


def add_pilot(m: Macros, pilot: Path) -> None:
    r = load(pilot, "close_time_summary.json")
    src = "close_time_summary.json (pilot run)"
    m.add("PilotNMarkets", count(r["n_markets"]), f"{src}: n_markets")
    m.add("PilotShareMarketsAfterClose", pct(r["share_markets_trade_after_close"]),
          f"{src}: share_markets_trade_after_close")
    m.add("PilotShareVolumeAfterClose", pct(r["share_volume_after_close"]),
          f"{src}: share_volume_after_close")


def add_label1(m: Macros, path: Path) -> None:
    """D-036 rule B: share of kept markets whose outcome-1 label is Yes."""
    r = json.loads(path.read_text())
    m.add("OutcomeOneYesShare", pct(r["overall"]["share_yes_like"]),
          "label1_counts.json (run 150296_v1label): overall.share_yes_like")
    src = "label1_counts.json (run 150296_v1label)"
    m.add("OutcomeOneYesN", count(r["overall"]["n_yes_like"]), f"{src}: overall.n_yes_like")
    gaps = [r["by_bin_yes_only"][str(b)]["diff_obs_minus_price"] for b in range(9)]   # bins 0 to 8, descriptive
    m.add("OutcomeOneYesBinsNegative", count(sum(g < 0 for g in gaps)),
          f"{src}: by_bin_yes_only bins 0 to 8 with diff_obs_minus_price < 0")
    m.add("OutcomeOneYesGapMin", "\\ensuremath{" + _grouped(100 * min(abs(g) for g in gaps), 1) + "}",
          f"{src}: by_bin_yes_only bins 0 to 8, smallest |diff_obs_minus_price|, percentage points")
    m.add("OutcomeOneYesGapMax", "\\ensuremath{" + _grouped(100 * max(abs(g) for g in gaps), 1) + "}",
          f"{src}: by_bin_yes_only bins 0 to 8, largest |diff_obs_minus_price|, percentage points")


DROP_REASONS = ("updown", "no_outcome", "no_price", "stale_price", "below_min_trades")


def add_categories(m: Macros, run: Path, markets_csv: Path) -> None:
    """In-scope, kept and dropped-by-reason markets per category (individual-level markets.csv, 3 columns only)."""
    df = pd.read_csv(markets_csv, usecols=["category_refined", "drop_reason", "kept"])
    n_scope, n_kept = len(df), int(df["kept"].sum())
    ts = load(run, "tables_summary.json")
    if (n_scope, n_kept) != (ts["n_markets_in_scope"], ts["n_kept"]):
        raise ValueError(f"{markets_csv} has {n_scope} in scope / {n_kept} kept, "
                         f"{run.name} has {ts['n_markets_in_scope']} / {ts['n_kept']}")
    src = f"{markets_csv.parent.name}/markets.csv"
    for cat, g in df.groupby("category_refined"):
        if cat not in CATEGORY_NAME:
            continue
        k, n, kept = CATEGORY_NAME[cat], len(g), int(g["kept"].sum())
        s = f"{src}: category_refined={cat}"
        m.add(f"Cat{k}NInScope", count(n), f"{s}, row count")
        m.add(f"Cat{k}ShareInScope", pct(n / n_scope), f"{s}, row count / all rows")
        m.add(f"Cat{k}NKept", count(kept), f"{s}, kept=True")
        m.add(f"Cat{k}ShareKept", pct(kept / n_kept), f"{s}, kept=True / all kept")
        m.add(f"Cat{k}Survival", pct(kept / n), f"{s}, kept=True / row count")
        if cat == "Sports":  # names the reviewer asked for (F1)
            m.add("SportsNInScope", count(n), f"{s}, row count")
            m.add("SportsShareInScope", pct(n / n_scope), f"{s}, row count / all rows")
            m.add("SportsShareKept", pct(kept / n_kept), f"{s}, kept=True / all kept")
        by = g["drop_reason"].value_counts()
        for r in DROP_REASONS:
            m.add(f"Cat{k}Drop{DROP_NAME[r]}N", count(int(by.get(r, 0))), f"{s}, drop_reason={r}")


def add_q1a(m: Macros, run: Path) -> None:
    r = load(run, "q1a_results.json", required=False)
    if r is None:
        return
    src = "q1a_results.json"
    chi = r["chi_square_independence"]
    m.add("QOneAN", count(chi["n"]), f"{src}: chi_square_independence.n")
    m.add("QOneAChiSq", stat(chi["chi2"]), f"{src}: chi_square_independence.chi2")
    m.add("QOneADf", count(chi["df"]), f"{src}: chi_square_independence.df")
    m.add("QOneAP", pval(chi["p"]), f"{src}: chi_square_independence.p")
    m.add("QOneAV", est(chi["cramers_v"]), f"{src}: chi_square_independence.cramers_v")
    m.add("QOneAMinExpected", amount(chi["min_expected_count"]),
          f"{src}: chi_square_independence.min_expected_count")
    m.add("QOneANCategories", count(chi["n_categories"]), f"{src}: chi_square_independence.n_categories")
    bt = r["bin_tests"]
    m.add("QOneABinsTested", count(bt["n_tested"]), f"{src}: bin_tests.n_tested")
    m.add("QOneABinsBh", count(bt["reject_bh"]), f"{src}: bin_tests.reject_bh")
    m.add("QOneABinsBonferroni", count(bt["reject_bonferroni"]), f"{src}: bin_tests.reject_bonferroni")
    bs = r["brier_tests"]
    m.add("QOneAAnovaF", stat(bs["anova_F"]), f"{src}: brier_tests.anova_F")
    m.add("QOneAAnovaP", pval(bs["anova_p"]), f"{src}: brier_tests.anova_p")
    m.add("QOneAEtaSq", est(bs["eta_squared"]), f"{src}: brier_tests.eta_squared")
    m.add("QOneAPermP", pval(bs["perm_p"]), f"{src}: brier_tests.perm_p")
    m.add("QOneANPerm", count(bs["n_perm"]), f"{src}: brier_tests.n_perm")

    q1 = load(run, "q1_results.json")["main_with_min_filter"]["confusion_at_0.5"]
    m.add("CatAllFavWin", pct(q1["accuracy"]),
          "q1_results.json: main_with_min_filter.confusion_at_0.5.accuracy (share of kept markets whose p>0.5 side won)")
    cont = {c["category_group"]: c for c in read_csv(run, "q1a_contingency.csv")}
    for cat, c in cont.items():
        k = CATEGORY_NAME[cat]
        s = f"q1a_contingency.csv: category_group={cat}"
        m.add(f"Cat{k}N", count(int(c["n"])), f"{s} n")
        m.add(f"Cat{k}FavWin", pct(float(c["favorite_win_rate"])), f"{s} favorite_win_rate")
        m.add(f"Cat{k}Brier", est(float(c["mean_brier"])), f"{s} mean_brier")
    for row in read_csv(run, "q1a_bins_by_category.csv"):
        i = int(row["bin"])
        if i not in LONGSHOT_BINS:
            continue
        k, lab = CATEGORY_NAME[row["category"]], bin_label(i)
        s = f"q1a_bins_by_category.csv: category={row['category']} bin={i}"
        m.add(f"Cat{k}Bin{lab}N", count(int(row["n"])), f"{s} n")
        m.add(f"Cat{k}Bin{lab}Price", pct(float(row["mean_price"])), f"{s} mean_price")
        m.add(f"Cat{k}Bin{lab}Obs", pct(float(row["observed_rate"])), f"{s} observed_rate")
        m.add(f"Cat{k}Bin{lab}Diff", pct2(float(row["diff_obs_minus_price"])),
              f"{s} diff_obs_minus_price")
        m.add(f"Cat{k}Bin{lab}BhP", pval(float(row["p_bh"])), f"{s} p_bh")


def add_q1b(m: Macros, run: Path) -> None:
    r = load(run, "q1b_results.json", required=False)
    if r is None:
        return
    src = "q1b_results.json"
    d = r["brier_diff_7d_minus_1d"]
    m.add("QOneBN", count(d["n"]), f"{src}: brier_diff_7d_minus_1d.n")
    m.add("QOneBMeanDiff", est(d["mean_diff"]), f"{src}: brier_diff_7d_minus_1d.mean_diff")
    m.add("QOneBCiLow", est(d["ci_low"]), f"{src}: brier_diff_7d_minus_1d.ci_low")
    m.add("QOneBCiHigh", est(d["ci_high"]), f"{src}: brier_diff_7d_minus_1d.ci_high")
    m.add("QOneBT", stat(d["t"]), f"{src}: brier_diff_7d_minus_1d.t")
    m.add("QOneBDf", count(d["df"]), f"{src}: brier_diff_7d_minus_1d.df")
    m.add("QOneBP", pval(d["p"]), f"{src}: brier_diff_7d_minus_1d.p")
    m.add("QOneBD", est(d["cohens_d"]), f"{src}: brier_diff_7d_minus_1d.cohens_d")
    m.add("QOneBBrierSevenDays", est(r["brier"]["7d"]), f"{src}: brier.7d")
    m.add("QOneBBrierOneDay", est(r["brier"]["1d"]), f"{src}: brier.1d")
    a = r["abs_error_diff_7d_minus_1d"]
    m.add("QOneBAbsMeanDiff", est(a["mean_diff"]), f"{src}: abs_error_diff_7d_minus_1d.mean_diff")
    m.add("QOneBAbsD", est(a["cohens_d"]), f"{src}: abs_error_diff_7d_minus_1d.cohens_d")
    m.add("QOneBEntropyDiff", est(r["mean_entropy_bits"]["diff_7d_minus_1d"]),
          f"{src}: mean_entropy_bits.diff_7d_minus_1d")
    for tag, key in (("SevenDays", "7d"), ("OneDay", "1d")):
        m.add(f"QOneBKsD{tag}", est(r["ks_yes_vs_no"][key]["D"]), f"{src}: ks_yes_vs_no.{key}.D")
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
        m.add(f"QOneC{tag}Rho", est(d["rho"]), f"{src}: {key}.rho")
        m.add(f"QOneC{tag}CiLow", est(d["ci_low"]), f"{src}: {key}.ci_low")
        m.add(f"QOneC{tag}CiHigh", est(d["ci_high"]), f"{src}: {key}.ci_high")
        m.add(f"QOneC{tag}P", pval(d["p"]), f"{src}: {key}.p")


def add_q2(m: Macros, run: Path) -> None:
    r = load(run, "q2_results.json")
    src = "q2_results.json"
    for role in ("maker", "taker"):
        c, R = r["concentration"][role], role.capitalize()
        m.add(f"{R}NWallets", count(c["n_wallets"]), f"{src}: concentration.{role}.n_wallets")
        m.add(f"{R}Gini", est(c["gini"]), f"{src}: concentration.{role}.gini")
        m.add(f"{R}TopOneShare", pct(c["top1_share"]), f"{src}: concentration.{role}.top1_share")
        m.add(f"{R}TopFiveShare", pct(c["top5_share"]), f"{src}: concentration.{role}.top5_share")
        m.add(f"{R}TopTenShare", pct(c["top10_share"]), f"{src}: concentration.{role}.top10_share")
        m.add(f"{R}MeanVolume", count(round(c["mean"])), f"{src}: concentration.{role}.mean")
        m.add(f"{R}MedianVolume", amount(c["median"]), f"{src}: concentration.{role}.median")
    w = r["role_tests"]["welch_t"]
    m.add("RoleWelchT", stat(w["t"]), f"{src}: role_tests.welch_t.t")
    m.add("RoleWelchP", pval(w["p"]), f"{src}: role_tests.welch_t.p")
    m.add("RoleCohenD", est(w["cohens_d"]), f"{src}: role_tests.welch_t.cohens_d")
    m.add("RoleKsD", est(r["role_tests"]["ks"]["D"]), f"{src}: role_tests.ks.D")
    sp = r["spearman_n_trades_vs_volume"]
    m.add("SpearmanTradesVolumeRho", est(sp["rho"]), f"{src}: spearman_n_trades_vs_volume.rho")
    km = r["kmeans"]
    an = km["anova_mean_trade_price"]
    m.add("KmeansPriceEtaSq", est(an["eta_squared"]), f"{src}: kmeans.anova_mean_trade_price.eta_squared")
    m.add("KmeansPricePermP", pval(an["perm_p"]), f"{src}: kmeans.anova_mean_trade_price.perm_p")
    m.add("KmeansK", count(km["k_chosen"]), f"{src}: kmeans.k_chosen")
    m.add("KmeansNSample", count(km["n_sample"]), f"{src}: kmeans.n_sample")
    m.add("KmeansAri", est(km["robust_scaling_check"]["adjusted_rand_index_vs_zscore"]),
          f"{src}: kmeans.robust_scaling_check.adjusted_rand_index_vs_zscore")
    m.add("KmeansNPerm", count(an["n_perm"]), f"{src}: kmeans.anova_mean_trade_price.n_perm")
    cx = km["chi2_cluster_x_category"]
    m.add("KmeansCategoryV", est(cx["cramers_v"]), f"{src}: kmeans.chi2_cluster_x_category.cramers_v")
    m.add("KmeansCategoryChi", stat(cx["chi2"]), f"{src}: kmeans.chi2_cluster_x_category.chi2")
    m.add("KmeansCategoryDf", count(cx["df"]), f"{src}: kmeans.chi2_cluster_x_category.df")
    m.add("KmeansCategoryP", pval(cx["p"]), f"{src}: kmeans.chi2_cluster_x_category.p")
    for c in km["cluster_summary"]:
        i, s = word(c["cluster"]), f"{src}: kmeans.cluster_summary[cluster={c['cluster']}]"
        m.add(f"Cluster{i}N", count(c["n"]), f"{s}.n")
        m.add(f"Cluster{i}MedianVolume", amount(c["median_volume"]), f"{s}.median_volume")
        m.add(f"Cluster{i}MedianTrades", median_count(c["median_n_trades"]), f"{s}.median_n_trades")
        m.add(f"Cluster{i}MedianMarkets", median_count(c["median_n_markets"]), f"{s}.median_n_markets")


def add_q3(m: Macros, run: Path) -> None:
    r = load(run, "q3_results.json")
    src = "q3_results.json"
    p1 = r["summary"]["p_1d"]
    m.add("PriceOneDayMean", est(p1["mean"]), f"{src}: summary.p_1d.mean")
    m.add("PriceOneDayMedian", est(p1["median"]), f"{src}: summary.p_1d.median")
    ts = r["summary"]["trade_size_usdc"]
    m.add("TradeSizeMean", amount(ts["mean"]), f"{src}: summary.trade_size_usdc.mean")
    m.add("TradeSizeMedian", amount(ts["median"]), f"{src}: summary.trade_size_usdc.median")
    for tag, key in (("TradeSize", "trade_size_usdc"), ("WalletVolume", "wallet_volume_usdc")):
        pl = r["fits"][key]["power_law"]
        m.add(f"{tag}PowerAlpha", est(pl["alpha"]), f"{src}: fits.{key}.power_law.alpha")
        m.add(f"{tag}PowerXmin", amount(pl["xmin"]), f"{src}: fits.{key}.power_law.xmin")
        m.add(f"{tag}PowerKsD", est(pl["D"]), f"{src}: fits.{key}.power_law.D")
        m.add(f"{tag}ExponentialKsD", est(r["fits"][key]["exponential"]["D"]),
              f"{src}: fits.{key}.exponential.D")
        m.add(f"{tag}NormalKsD", est(r["fits"][key]["normal"]["D"]), f"{src}: fits.{key}.normal.D")
        m.add(f"{tag}PowerKsP", pval(pl["p"]), f"{src}: fits.{key}.power_law.p")
        m.add(f"{tag}PowerNTail", count(pl["n_tail"]), f"{src}: fits.{key}.power_law.n_tail")


def add_lecture(m: Macros, run: Path, path: Path) -> None:
    """Lecture-method numbers (D-026) from reports/lecture_numbers.json. Skipped when it is absent or from another run."""
    if not path.exists():
        return
    r = json.loads(path.read_text())
    if r["source_run"] != run.name:
        return
    src = "lecture_numbers.json"
    z = r["z_interval_95"]
    m.add("ZIntervalBinsOutsideN", count(z["n_outside"]), f"{src}: z_interval_95.n_outside")
    m.add("ZIntervalBinsOutsideList", text(", ".join(map(str, z["bins_outside"]))), f"{src}: z_interval_95.bins_outside")
    m.add("ZIntervalBinsBhOffList", text(", ".join(map(str, z["bins_bh_off"]))), f"{src}: z_interval_95.bins_bh_off")
    m.add("ZIntervalSameAsBh", "yes" if z["same_bins"] else "no", f"{src}: z_interval_95.same_bins")
    m.add("ZIntervalEqFreqOutsideN", count(sum(1 for b in z["bins_equal_frequency"] if b["price_outside"])),
          f"{src}: z_interval_95.bins_equal_frequency[price_outside]")
    for b in z["bins"]:
        lab, s = bin_label(b["bin"]), f"{src}: z_interval_95.bins[bin={b['bin']}]"
        m.add(f"Bin{lab}ZSd", est(b["bernoulli_sd"]), f"{s}.bernoulli_sd")
        m.add(f"Bin{lab}ZLow", pct(b["z_low"]), f"{s}.z_low")
        m.add(f"Bin{lab}ZHigh", pct(b["z_high"]), f"{s}.z_high")
        m.add(f"Bin{lab}ZOutside", "yes" if b["price_outside"] else "no", f"{s}.price_outside")
    gap = r["largest_gap"]
    m.add("LargestGapBin", count(gap["bin"]), f"{src}: largest_gap.bin")
    m.add("LargestGapDiff", pct2(gap["diff_obs_minus_price"]), f"{src}: largest_gap.diff_obs_minus_price")
    m.add("LargestGapAbs", pct2(gap["abs"]), f"{src}: largest_gap.abs")
    d = r["log10_mean_difference_maker_minus_taker"]
    m.add("RoleLogTenDiff", est(d["difference"]), f"{src}: log10_mean_difference_maker_minus_taker.difference")
    m.add("RoleLogTenMaker", est(d["mean_log10_maker"]), f"{src}: log10_mean_difference_maker_minus_taker.mean_log10_maker")
    m.add("RoleLogTenTaker", est(d["mean_log10_taker"]), f"{src}: log10_mean_difference_maker_minus_taker.mean_log10_taker")
    t20 = r["top20_share"]
    m.add("MakerTopTwentyShare", pct(t20["maker"]), f"{src}: top20_share.maker")
    m.add("TakerTopTwentyShare", pct(t20["taker"]), f"{src}: top20_share.taker")
    m.add("TopTwentyReference", pct(t20["reference"]), f"{src}: top20_share.reference")
    for key, name in (("main", "Main"), ("no_min_filter", "NoMin"), ("equal_frequency", "EqFreq")):
        g = r["gap_direction"][key]
        m.add(f"GapNegBins{name}", count(g["n_negative"]), f"{src}: gap_direction.{key}.n_negative")
        m.add(f"GapNetDiff{name}", pct2(g["net_gap"]), f"{src}: gap_direction.{key}.net_gap (n-weighted)")
    m.add("GapBinsTotal", count(r["gap_direction"]["main"]["n_bins"]), f"{src}: gap_direction.main.n_bins")
    m.add("GapNetYesShort", amount(abs(r["gap_direction"]["main"]["n_yes_minus_expected"])),
          f"{src}: gap_direction.main.n_yes_minus_expected (absolute value)")
    c = r["chi2_largest_contributor"]
    m.add("ChiTopBin", count(c["bin"]), f"{src}: chi2_largest_contributor.bin")
    m.add("ChiTopContribution", stat(c["contribution"]), f"{src}: chi2_largest_contributor.contribution")
    m.add("ChiTopShare", pct(c["share"]), f"{src}: chi2_largest_contributor.share")
    for b, name in (("0", "Zero"), ("1", "One")):
        v = r["no_min_filter_longshot_bh"][b]
        s = f"{src}: no_min_filter_longshot_bh.{b}"
        m.add(f"NoMinBin{name}Diff", pct2(v["diff_obs_minus_price"]), f"{s}.diff_obs_minus_price")
        m.add(f"NoMinBin{name}PBh", pval(v["p_bh"]), f"{s}.p_bh")
        m.add(f"NoMinBin{name}BhOff", "yes" if v["reject_bh"] else "no", f"{s}.reject_bh")
    cg = r.get("cluster_category_gap")
    if cg:   # D-030: effect size of the cluster x category chi-square; absent until the ccdf_redraw run is fetched
        s = f"{src}: cluster_category_gap"
        m.add("ClusterCategoryGapCluster", count(cg["cluster"]), f"{s}.cluster")
        m.add("ClusterCategoryGapCategory", text(cg["category"]), f"{s}.category")
        m.add("ClusterCategoryGapObs", pct(cg["observed_share"]), f"{s}.observed_share")
        m.add("ClusterCategoryGapExp", pct(cg["expected_share"]), f"{s}.expected_share")
        m.add("ClusterCategoryGapDiff", pct2(cg["diff"]), f"{s}.diff")
    m.add("KmeansPriceSsbRatio", est(r["ssb_ratio"]["mean_trade_price"]), f"{src}: ssb_ratio.mean_trade_price")
    m.add("KmeansTradeSizeSsbRatio", est(r["ssb_ratio"]["log_median_trade_size"]), f"{src}: ssb_ratio.log_median_trade_size")


def add_code_set(m: Macros, run: Path, sha_name: str, file_name: str) -> None:
    """The run's code.sha256 lists every script of the code set. Its own hash names the set."""
    f = run / "code.sha256"
    m.add(sha_name, text(hashlib.sha256(f.read_bytes()).hexdigest()[:12]),
          f"{f.name}: sha256 of the file that lists the hash of every script (first 12 hex)")
    m.add(file_name, text(f"runs/{run.name}/code.sha256"), "path of the per-script hash list")


def add_meta(m: Macros, run: Path) -> None:
    man = load(run, "manifest_q1_calibration.json")
    src = "manifest_q1_calibration.json"
    m.add("RunId", text(run.name), "run directory name")
    m.add("CodeVersion", text(man["code_version"]), f"{src}: code_version")
    m.add("CodeSha", text(man["code_sha"]),
          f"{src}: code_sha (hash of the script q1_calibration.py alone, first 12 hex, not of the code set)")
    add_code_set(m, run, "CodeSetSha", "CodeShaFile")
    m.add("SlurmJobId", text(man["env"]["slurm_job_id"]), f"{src}: env.slurm_job_id")
    v = load(run, "verdicts.json")
    for q, d in v["comparisons"].items():
        name = "QOne" + q[2:].upper()
        m.add(f"Verdict{name}", text(d["verdict"]), f"verdicts.json: comparisons.{q}.verdict")
    m.add("Alpha", level(v["alpha"]), "verdicts.json: alpha")


ROB_CLASS = {"clean": "Clean", "split": "Split", "other": "Other", "missing": "Missing"}
ROB_QUANTILE = {"q0.5": "Median", "q0.75": "SevenFive", "q0.9": "Ninety", "q0.95": "NinetyFive",
                "q0.99": "NinetyNine", "max": "Max"}
ROB_THRESHOLD = {"0.10": "Ten", "0.25": "TwentyFive", "0.50": "Fifty"}


def add_robust_r1(m: Macros, r: dict[str, Any]) -> None:
    src = "r1_results.json"
    m.add("RobROneNKept", count(r["n_kept"]), f"{src}: n_kept")
    for c, name in ROB_CLASS.items():
        m.add(f"RobROne{name}N", count(r["class_counts"][c]), f"{src}: class_counts.{c}")
        m.add(f"RobROne{name}Share", pct2(r["class_shares"][c]), f"{src}: class_shares.{c}")
    d = r["duplicates"]
    m.add("RobROneDupIds", count(d["kept_ids_with_duplicate_rows"]), f"{src}: duplicates.kept_ids_with_duplicate_rows")
    m.add("RobROneDupConflicting", count(d["kept_duplicates_conflicting"]),
          f"{src}: duplicates.kept_duplicates_conflicting")
    m.add("RobROneSplitYesOne", count(r["our_y_on_split_markets"]["y1"]), f"{src}: our_y_on_split_markets.y1")
    m.add("RobROneSplitYesZero", count(r["our_y_on_split_markets"]["y0"]), f"{src}: our_y_on_split_markets.y0")
    mp = r["mapping"]
    m.add("RobROneNClean", count(mp["n_clean"]), f"{src}: mapping.n_clean")
    m.add("RobROneAgreement", pct2(mp["agreement_index_primary"]), f"{src}: mapping.agreement_index_primary")
    m.add("RobROneAgreementLow", pct2(mp["agreement_ci95"][0]), f"{src}: mapping.agreement_ci95[0]")
    m.add("RobROneAgreementHigh", pct2(mp["agreement_ci95"][1]), f"{src}: mapping.agreement_ci95[1]")
    m.add("RobROneNMismatch", count(mp["n_mismatch"]), f"{src}: mapping.n_mismatch")
    m.add("RobROneMappingValidated", "yes" if mp["validated"] else "no", f"{src}: mapping.validated")
    s = r["sensitivity"]
    m.add("RobROneNExcluded", count(s["n_excluded"]), f"{src}: sensitivity.n_excluded")
    m.add("RobROneSensN", count(s["n_markets"]), f"{src}: sensitivity.n_markets")
    q = s["q1_sensitivity"]
    m.add("RobROneSensChiSq", stat(q["chi2_gof"]["chi2"]), f"{src}: sensitivity.q1_sensitivity.chi2_gof.chi2")
    m.add("RobROneSensDf", count(q["chi2_gof"]["df"]), f"{src}: sensitivity.q1_sensitivity.chi2_gof.df")
    m.add("RobROneSensP", pval(q["chi2_gof"]["p"]), f"{src}: sensitivity.q1_sensitivity.chi2_gof.p")
    m.add("RobROneSensW", est(q["chi2_gof"]["effect_w"]), f"{src}: sensitivity.q1_sensitivity.chi2_gof.effect_w")
    m.add("RobROneSensBrier", est(q["brier"]), f"{src}: sensitivity.q1_sensitivity.brier")
    m.add("RobROneSensBinsBh", count(q["bins_reject_bh"]), f"{src}: sensitivity.q1_sensitivity.bins_reject_bh")
    m.add("RobROneDeltaW", est(s["delta_effect_w"]), f"{src}: sensitivity.delta_effect_w")
    m.add("RobROneRuleSame", "yes" if s["rule_results_same"] else "no", f"{src}: sensitivity.rule_results_same")
    m.add("RobROneRuleOriginal", text(s["rule_result_original"]), f"{src}: sensitivity.rule_result_original")
    m.add("RobROneRuleSens", text(s["rule_result_sensitivity"]), f"{src}: sensitivity.rule_result_sensitivity")


def add_robust_r2(m: Macros, r: dict[str, Any]) -> None:
    src = "r2_results.json"
    o = r["overall"]
    m.add("RobRTwoN", count(o["n"]), f"{src}: overall.n")
    m.add("RobRTwoMedianAbsDelta", est(o["median_abs_delta"]), f"{src}: overall.median_abs_delta")
    m.add("RobRTwoShareNoTrade", pct(o["share_no_trade"]), f"{src}: overall.share_no_trade")
    m.add("RobRTwoShareCrossing", pct2(o["share_crossing"]), f"{src}: overall.share_crossing")
    for t, name in ROB_THRESHOLD.items():
        m.add(f"RobRTwoShareDeltaAtLeast{name}", pct2(o[f"share_abs_delta_ge_{t}"]),
              f"{src}: overall.share_abs_delta_ge_{t}")
    for k, name in ROB_QUANTILE.items():
        m.add(f"RobRTwoAbsDelta{name}", est(o["quantiles_abs_delta"][k]), f"{src}: overall.quantiles_abs_delta.{k}")
    for k, name in (("median", "Median"), ("q0.9", "Ninety"), ("max", "Max")):
        m.add(f"RobRTwoWindowTrades{name}", count(int(o["n_window_trades"][k])), f"{src}: overall.n_window_trades.{k}")
    for tag, key in (("All", "brier"), ("Traded", "brier_traded_only")):
        b = o[key]
        s = f"{src}: overall.{key}"
        m.add(f"RobRTwo{tag}N", count(b["n"]), f"{s}.n")
        m.add(f"RobRTwo{tag}BrierOneDay", est(b["brier_1d"]), f"{s}.brier_1d")
        m.add(f"RobRTwo{tag}BrierAtClose", est(b["brier_T"]), f"{s}.brier_T")
        m.add(f"RobRTwo{tag}MeanDiff", est(b["mean_diff"]), f"{s}.mean_diff")
        m.add(f"RobRTwo{tag}CiLow", est(b["ci_low"]), f"{s}.ci_low")
        m.add(f"RobRTwo{tag}CiHigh", est(b["ci_high"]), f"{s}.ci_high")
        m.add(f"RobRTwo{tag}T", stat(b["t"]), f"{s}.t")
        m.add(f"RobRTwo{tag}P", pval(b["p"]), f"{s}.p")
        m.add(f"RobRTwo{tag}Dz", est(b["cohens_dz"]), f"{s}.cohens_dz")
    for cat, c in r["by_category"].items():
        k, s = CATEGORY_NAME.get(cat, text(cat)), f"{src}: by_category.{cat}"
        if k not in CATEGORY_NAME.values():
            continue  # Unknown or Merged groups have no fixed macro name
        m.add(f"RobRTwoCat{k}N", count(c["n"]), f"{s}.n")
        m.add(f"RobRTwoCat{k}MedianAbsDelta", est(c["median_abs_delta"]), f"{s}.median_abs_delta")
        m.add(f"RobRTwoCat{k}MeanDiff", est(c["brier"]["mean_diff"]), f"{s}.brier.mean_diff")


def add_robust_meta(m: Macros, robust: Path) -> None:
    m.add("RobustRun", text(robust.name), "robustness run directory name")
    versions = set()
    for tag, stage in (("ROne", "r1_split_payout"), ("RTwo", "r2_price_path")):
        man = load(robust, f"manifest_{stage}.json", required=False)
        if man is None:
            continue
        versions.add(man["code_version"])
        m.add(f"RobustCodeSha{tag}", text(man["code_sha"]),
              f"manifest_{stage}.json: code_sha (hash of the script {stage}.py alone)")
    if len(versions) > 1:
        raise ValueError(f"r1 and r2 manifests disagree on code_version: {versions}")
    if versions:
        m.add("RobustCodeVersion", text(versions.pop()), "manifest_r1_split_payout.json, manifest_r2_price_path.json: code_version")
    add_code_set(m, robust, "RobustCodeSha", "RobustCodeShaFile")


def add_robust(m: Macros, robust: Path) -> None:
    """Robustness macros (prefix Rob). Each stage is skipped when its result file is absent."""
    add_robust_meta(m, robust)
    r1 = load(robust, "r1_results.json", required=False)
    if r1 is not None:
        add_robust_r1(m, r1)
    r2 = load(robust, "r2_results.json", required=False)
    if r2 is not None:
        add_robust_r2(m, r2)


# Robustness v3 (--r3): prefix RThree. Net gaps and gap CIs use pct2 (gaps in points); the
# minor-4 shift in points is already in points, so it uses 2 decimals without a percent sign.
R3_FIELDS = {
    "n": ("N", count, "n"), "chi": ("ChiSq", stat, "chi2"), "p": ("P", pval, "p"),
    "pbh": ("BhP", pval, "p_bh"), "bins": ("BinsBh", count, "bins_off_bh"),
    "gap": ("NetGap", pct2, "net_gap"), "cilow": ("NetGapCiLow", pct2, "net_gap_ci_low"),
    "cihigh": ("NetGapCiHigh", pct2, "net_gap_ci_high"),
}
R3_GAP_CI = ("gap", "cilow", "cihigh")


def _r3_row(m: Macros, name: str, row: dict[str, Any], src: str, path: str, key_prefix: str,
            fields: tuple[str, ...]) -> None:
    """Macros RThree<name><Field> from row[key_prefix + key]; comment names file and key path."""
    for f in fields:
        suffix, fmt, key = R3_FIELDS[f]
        m.add(f"RThree{name}{suffix}", fmt(row[key_prefix + key]), f"{src}: {path}{key_prefix}{key}")


def add_r3_m1(m: Macros, run: Path) -> None:
    src, r = "m1_results.json", load(run, "m1_results.json")
    for key, name in (("p_vwap", "MOneVwap"), ("p_mid", "MOneMid")):
        _r3_row(m, name, r["rows"][key], src, f"rows.{key}.", "", ("n", "chi", "bins") + R3_GAP_CI)
    m.add("RThreeMOneMeanHalfSpread", pct2(r["mean_h"]), f"{src}: mean_h")
    m.add("RThreeMOneShareBoth", pct(r["coverage"]["share_S_both"]), f"{src}: coverage.share_S_both")
    m.add("RThreeMOneGapWithinHalfSpread", "yes" if r["side_line"]["gap_within_half_spread"] else "no",
          f"{src}: side_line.gap_within_half_spread")


def add_r3_m2(m: Macros, run: Path) -> None:
    src, r = "m2_results.json", load(run, "m2_results.json")
    _r3_row(m, "MTwoYesNo", r, src, "", "yes_no_", ("n", "chi", "p", "bins") + R3_GAP_CI)
    _r3_row(m, "MTwoOther", r, src, "", "other_", ("n", "chi", "p") + R3_GAP_CI)


def add_r3_m3(m: Macros, run: Path) -> None:
    src, r = "m3_bootstrap.json", load(run, "m3_bootstrap.json")
    for key, name in (("k1_slug_stem", "MThreeKOne"), ("k2_category_close_hour", "MThreeKTwo")):
        p = r["proxies"][key]
        s = f"proxies.{key}."
        m.add(f"RThree{name}NClusters", count(p["n_clusters"]), f"{src}: {s}n_clusters")
        m.add(f"RThree{name}NetGapCiLow", pct2(p["net_gap_ci_low"]), f"{src}: {s}net_gap_ci_low")
        m.add(f"RThree{name}NetGapCiHigh", pct2(p["net_gap_ci_high"]), f"{src}: {s}net_gap_ci_high")
        m.add(f"RThree{name}ChiSq", stat(p["x2_cl"]), f"{src}: {s}x2_cl")
        m.add(f"RThree{name}P", pval(p["p"]), f"{src}: {s}p")
    m.add("RThreeMThreeReadProxy", text(r["read_proxy"]), f"{src}: read_proxy")


def add_r3_m4(m: Macros, run: Path) -> None:
    src, r = "m4_results.json", load(run, "m4_results.json")
    for pre, name in (("kept_", "Kept"), ("eligible_dropped_pooled_", "Dropped")):
        m.add(f"RThreeMFour{name}MedianVolumeBeforeDay", amount(r[pre + "volume_before_T1d_median"]),
              f"{src}: {pre}volume_before_T1d_median")
        m.add(f"RThreeMFour{name}MedianDuration", amount(r[pre + "duration_days_median"]),
              f"{src}: {pre}duration_days_median")
        m.add(f"RThreeMFour{name}MedianTrades", median_count(r[pre + "n_trades_median"]),
              f"{src}: {pre}n_trades_median")
    _r3_row(m, "MFourStale", r, src, "", "stale_q1_", ("gap", "cilow", "cihigh"))


def add_r3_m5(m: Macros, run: Path) -> None:
    src, r = "m5_calibration_fit.json", load(run, "m5_calibration_fit.json")
    for key, name in (("a", "A"), ("b", "B")):
        m.add(f"RThreeMFive{name}", est(r[key]), f"{src}: {key}")
        m.add(f"RThreeMFive{name}WaldLow", est(r[key + "_wald_ci"][0]), f"{src}: {key}_wald_ci[0]")
        m.add(f"RThreeMFive{name}WaldHigh", est(r[key + "_wald_ci"][1]), f"{src}: {key}_wald_ci[1]")
    m.add("RThreeMFiveBrier", est(r["brier"]), f"{src}: brier")
    m.add("RThreeMFiveClimatologyBrier", est(r["climatology"]), f"{src}: climatology")
    m.add("RThreeMFiveSkill", est(r["brier_skill_score"]), f"{src}: brier_skill_score")
    m.add("RThreeMFiveMajorityAccuracy", pct(r["majority_accuracy"]), f"{src}: majority_accuracy")
    m.add("RThreeMFiveAccuracyHalf", pct(r["accuracy_at_0.5"]), f"{src}: accuracy_at_0.5")
    grid = r["delta_table"]
    m.add("RThreeMFiveMaxAbsDelta", pct2(max(abs(g["delta"]) for g in grid)),
          f"{src}: delta_table[].delta, largest absolute value")
    m.add("RThreeMFivePracticalPrices", count(sum(g["practically_sized"] for g in grid)),
          f"{src}: delta_table[].practically_sized, count of True")
    m.add("RThreeMFiveGridPrices", count(len(grid)), f"{src}: delta_table, length")


def add_r3_minor4(m: Macros, run: Path) -> None:
    src, r = "minor4_dedup.json", load(run, "minor4_dedup.json")
    m.add("RThreeMinorFourDupShare", pct(r["duplicates"]["share_dup_all_columns"]),
          f"{src}: duplicates.share_dup_all_columns")
    m.add("RThreeMinorFourRemoved", count(r["kept_set"]["n_removed"]), f"{src}: kept_set.n_removed")
    m.add("RThreeMinorFourChiSq", stat(r["q1"]["chi2"]), f"{src}: q1.chi2")
    m.add("RThreeMinorFourNetGap", pct2(r["q1"]["net_gap"]), f"{src}: q1.net_gap")
    for role in ("maker", "taker"):
        for top, tag in (("top1_share", "TopOne"), ("top20_share", "TopTwenty")):
            m.add(f"RThreeMinorFour{role.capitalize()}{tag}DeltaPp",
                  "\\ensuremath{" + _grouped(r["q2"][role][top]["delta_pp"], 2) + "}",
                  f"{src}: q2.{role}.{top}.delta_pp (percentage points)")


def add_r3_peer(m: Macros, run: Path) -> None:
    src, a = "peer_a_results.json", load(run, "peer_a_results.json")
    m.add("RThreePeerACutLowMid", amount(a["cut_low_mid"]), f"{src}: cut_low_mid")
    m.add("RThreePeerACutMidHigh", amount(a["cut_mid_high"]), f"{src}: cut_mid_high")
    for t, name in (("low", "Low"), ("mid", "Mid"), ("high", "High")):
        _r3_row(m, f"PeerA{name}", a, src, "", f"tercile_{t}_", ("n", "chi", "pbh") + R3_GAP_CI)
    d = a["high_vs_low"]
    m.add("RThreePeerADiff", pct2(d["diff"]), f"{src}: high_vs_low.diff")
    m.add("RThreePeerADiffCiLow", pct2(d["ci_low"]), f"{src}: high_vs_low.ci_low")
    m.add("RThreePeerADiffCiHigh", pct2(d["ci_high"]), f"{src}: high_vs_low.ci_high")
    m.add("RThreePeerADiffP", pval(d["p"]), f"{src}: high_vs_low.p")
    src, b = "peer_b_results.json", load(run, "peer_b_results.json")
    periods = list(dict.fromkeys(b["year_to_period"].values()))  # file order: early to late
    for i, label in enumerate(periods, start=1):
        name = f"PeerBPeriod{word(i)}"
        m.add(f"RThree{name}Label", text(label), f"{src}: year_to_period values, period {i} in file order")
        _r3_row(m, name, b, src, "", f"period_{label}_", ("n", "chi", "pbh") + R3_GAP_CI)


def add_r3(m: Macros, run: Path) -> None:
    for fn in (add_r3_m1, add_r3_m2, add_r3_m3, add_r3_m4, add_r3_m5, add_r3_minor4, add_r3_peer):
        fn(m, run)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--run", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--q1eqfreq", type=Path, help="run dir (code v5) whose q1_bins_eqfreq.csv has p_bh and reject_bh")
    ap.add_argument("--pilot", type=Path, help="pilot run dir with close_time_summary.json")
    ap.add_argument("--robust", type=Path, help="robustness run dir with r1_results.json, r2_results.json")
    ap.add_argument("--r3", type=Path, help="robustness v3 run dir (m1..m5, minor4, peer_a, peer_b JSON); adds RThree macros")
    ap.add_argument("--lecture", type=Path, default=Path(__file__).resolve().parent.parent / "reports" / "lecture_numbers.json",
                    help="lecture_numbers.json (code/lecture_numbers.py); used only when it is from --run")
    ap.add_argument("--label1", type=Path,
                    default=Path(__file__).resolve().parent.parent / "runs" / "150296_v1label" / "label1_counts.json",
                    help="label1_counts.json of the label check run (D-036)")
    a = ap.parse_args()
    m = Macros()
    for fn in (add_meta, add_data, add_q1, add_q1a, add_q1b, add_q1c, add_q2, add_q3):
        fn(m, a.run)
    add_lecture(m, a.run, a.lecture)
    add_label1(m, a.label1)
    add_q1_eqfreq(m, a.run, load(a.run, "verdicts.json")["alpha"], a.q1eqfreq)
    if a.pilot is not None:
        add_pilot(m, a.pilot)
    if a.robust is not None:
        add_robust(m, a.robust)
        if (a.robust / "markets.csv").exists():  # same build as the main runs, checked by row counts
            add_categories(m, a.run, a.robust / "markets.csv")
    if a.r3 is not None:
        add_r3(m, a.r3)
    a.out.parent.mkdir(parents=True, exist_ok=True)
    header = f"% Generated by code/make_paper_numbers.py from {a.run}. Do not edit by hand.\n"
    a.out.write_text(header + "\n".join(m.lines) + "\n")
    print(f"{a.out}: {len(m.names)} macros")


if __name__ == "__main__":
    main()
