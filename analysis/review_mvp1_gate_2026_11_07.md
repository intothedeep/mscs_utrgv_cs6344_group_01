# MVP1 gate review (owner-requested, 2026-11-07)

- Scope: MVP1 only (Q1, Q2, Q3 / RQ1–RQ3). MVP2 (`future_work/`) out of scope (D-016, D-017).
- Counters: cycle 2/2 plus one owner-allowed review (D-022); recovery 0/2.
- Reviewer: reviewer agent. Findings only. No file was fixed.
- Status: DONE. Verdict PASS for M1 (0 blocker, 1 major, 11 minor). Order of checks below is the order verified.

## Checks

### A4. Verdicts follow the prereg, prereg before results: PASS

- Rule (`analysis/prereg_mvp1.md` lines 22-26): chi-square p < 0.05 means "not calibrated as a whole". Per-bin call: binomial test, BH at 0.05.
- `verdicts.json` `comparisons.Q1`: chi-square 67.99, df 10, p 1.08e-10, n 47,948. p < 0.05, so the verdict "Prices are not calibrated as a whole at this n." follows.
- `extra.bins_off_bh` 5 equals the count of `reject_bh` True in `q1_bins.csv` (bins 0, 1, 6, 7, 8). `bins_off_bonferroni` 4 equals `reject_bonferroni` True (0, 1, 6, 7).
- Effect size column per bin (observed − price, with CI) exists in `q1_bins.csv` (`diff_obs_minus_price`, `ci_low`, `ci_high`).
- Prereg hashes recomputed by `git show <c>:./analysis/prereg_mvp1.md | shasum -a 256`: 530fe0d → db17cf8833fe, f78de3e → ce65f66cdedf. Both equal the `00.runs.md` row 142082 (D-031).
- `verdicts.json` `prereg_json_sha256_12` 498ee2a5d4a8 equals `shasum` of `runs/142082_mvp1_full_v1r3/prereg.json`.
- `git diff --quiet 530fe0d -- analysis/prereg_mvp1.json`: exit 0, parameters unchanged since the prereg commit.
- `git diff --numstat 530fe0d HEAD -- analysis/prereg_mvp1.md`: 69 added, 0 deleted. Additions only (amendment of 2026-10-19 and note of 2026-11-01).
- Order: commit 530fe0d (2026-10-19 12:48) holds the prereg and only run 142041 (Job A, no price-outcome output). Pilot 142056 enters at a6fb2c7 (12:55), full runs at bba0185 (14:23).
- Limit (minor M-1, carried, known G7/D-031): `criteria_sha256_12` stays null in `verdicts.json`. Manifests hold no wall-clock start time, so "prereg before the run" rests on commit order and job IDs, not on a run timestamp.
- Note: the amendment (tie rule) came after the first full result. It is labeled so, and the verdict is the same in 142057 and 142082. Accepted as disclosed.

### A1. Exit criteria, the four "MVP1 is done when" boxes: PASS

Source: `../tips/group_01/polymarket_plan_detailed.md` lines 132-137.

| Box | Result | Evidence |
| --- | --- | --- |
| 1 Market and wallet tables from the full data | PASS | `runs/142082_mvp1_full_v1r3/tables_summary.json`: `n_markets_in_scope` 688,131, `n_kept` 47,948, `n_wallet_role_rows` 2,117,412. Drop reasons sum to 688,131 (checked by hand: 255,420 + 62,718 + 215,289 + 80,230 + 26,526 + 47,948). `prereg.json` `scope` full |
| 2 Figures 1-8 exist | PASS | run folder: `fig1_fig2_hist.png`, `fig3_qq.png`, `fig4_calibration.png`, `fig5_ecdf_yes_no.png`, `fig6_ccdf.png`, `fig7_lorenz.png`, `fig8_elbow.png`. Redrawn versions in `reports/figures/` (runs 145892, 145893, 145897) |
| 3 Every MVP1 table row has a result | PASS | Q3: `q3_results.json` `summary` (mean, median, mode, range, variance, quantiles), `fits.*` (normal, exponential, power law, KS D and p), QQ, violin, ECDF, box plot. Q1: `q1_bins.csv` (binomial p, Bonferroni, BH), `q1_results.json` (chi-square, scores, confusion, KS, longshot), `reports/lecture_numbers.json` `z_interval_95`. Q2: `q2_results.json` (shares, Welch t, KS, Spearman, k-means, ANOVA + permutation, robust-scaling check), `runs/145892_ccdf_v6/cluster_category_crosstab.csv` (D-030 cell gap) |
| 4 Effect size next to every p-value | PASS | Report Tables 6, 7, 8, 16, 18 and paper lines 374-383, 570-585 carry D, gap, rho, log10 difference or SSB ratio beside p |

- Box 3, G1 box plot: the base64 image under "Figure 8" in `reports/report_v1.html` has the same sha as `base64 reports/figures/box_p1d_by_category_group.png` (f4a94722ed3c). The PNG is printed, with a caption.
- New minor m-1: `q3_results.json` `summary.trade_size_usdc.mode_50bin_mid` is 7,984 USDC and `wallet_volume_usdc.mode_50bin_mid` is 938,759 USDC. Both lie above their own q99 (1,955 and 69,734). A 50-bin linear histogram puts nearly all mass in bin 1, so the "mode" is that bin's midpoint. The value is not printed in the report or paper, so no claim depends on it. It is a weak result for the plan row "mode".

### A2. AC of every `[x]` M1 row in `PLAN.md`: PASS with 2 AC drifts (minor)

Commands run from the project folder, as written in `PLAN.md` lines 76-122.

| PLAN line | AC | Today |
| --- | --- | --- |
| 41 G1 | box plot PNG printed with caption | holds (sha match above) |
| 57 G8 | `grep -o project_group_01` count 0 | 0 |
| 58 G9 | captions run 1 to N with no gap | Tables 1-19, Figures 1-18, no gap |
| 59 G10 | `grep -c 'used in Q1c'` 0 | 0 |
| 60, 97 scope | `git status --short future_work/reports/` empty, `git diff --quiet` 0 | empty, exit 0 |
| 63 G7 | `git diff --quiet -- runs/142082_mvp1_full_v1r3/verdicts.json` 0 | exit 0. Ledger row names both commits and hashes, recomputed equal (A4) |
| 64 G11/G12 | ledger names partition, CPUs, env, cites D-015 | holds. Rows 145892-145897 now name `kimq`, 4 CPUs, env (closes 2026-11-02 minor 10) |
| 88 import | both greps empty | empty |
| 89 saved numbers | `source_run` 142082, 10 bins, `same_bins` | 142082_mvp1_full_v1r3, 10, true |
| 90 names (report) | `TEXT \| grep -wE "$NAMES" \| grep -vE "$KEEP"` empty | empty |
| 91 D-028 | 0 / at least 1 | 0 / 2 |
| 92 Fig. 4 | at least 1 / at least 1 | 2 / 10 |
| 93 verdict | at least 1 | 1 |
| 95 macros new | at least 1 | 78 |
| 108-113 prereg note | 0 deleted, `limitation 5`, D-024, D-026, D-028, `prereg_robustness.md` | 0 deleted, 1, 3, 4, 4, 1 |
| 115 README names | empty | **NOT EMPTY** (minor m-2) |
| 116, 117 README | 0 / at least 1 | 0 / 3 |
| 119-121 G16 | 0 / at least 1 / 0 | 0 / 4 / 0 |
| 122 G17 | at least 1 | 1 and 1 |

M4 rows in the same section, checked for drift:

| PLAN line | AC | Today |
| --- | --- | --- |
| 99 G5 | Up/Down sentence cites the paper | holds (`main.tex` 172-173) |
| 100 G13 | `S-PAPER-4` 0 | 0 |
| 101 names (paper) | empty | **NOT EMPTY** (minor m-2) |
| 102 removed macros | 0 | 0 |
| 103 figures | at least 1 / 1 | 1 / 1 |
| 105 owner parts | 4 | 4 |
| 106 verdict | 2 | 2 |

- New minor m-2 (AC drift, hierarchy/docs): the names AC no longer returns empty.
  - `main.tex` 328, 479, 549 say "Lorenz" without a KEEP phrase. Line 330 next to 328 does say "outside the lectures".
  - `README.md` 104, 105, 293, 298, 299, 331 say "Lorenz". `README.md` 137 says "No Cramér's V".
  - Cause: the 2026-11-02 work (D-030 cell gap, D-031 full Lorenz) added these lines after the rows closed on 2026-11-01. Each use is labeled or is a negation, so no outside method is used unlabeled.
  - Why it matters: the closed row's AC now fails as written, so a re-check cannot tell drift from regression. Fix: `product-manager` widens the KEEP list (e.g. `Lorenz curve|No Cramér`) or adds a dated note on the row.
- Carried minors now closed: 2026-11-02 minor 1 (`.gitignore` 272-273 ignore `*.xdv`, `*.synctex.gz`), minor 10 (ledger rows), minor 12 (M4 project-end row ticked, PLAN 123), minor 13 (`manifest_q3_figs.json` has `wall_time_s` 4.7), r3 G14 (PLAN 55 now 0.0974), r3 G15 (PLAN 28-29 tag `→ M1`, line 29 says report v1).

### A3. Numbers trace to saved outputs: PASS (40 of 40 sampled match)

Report text extracted with the `TEXT` function of `PLAN.md` line 82. Paper values read from `papers/paper_mvp1/numbers.tex`, whose comment line above each macro names the source key.

| # | Q | Saved file:key | Saved value | Report | `numbers.tex` | Match |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | scope | `tables_summary.json`:`n_markets_in_scope` | 688,131 | 688,131 | `NMarketsInScope` 688,131 | yes |
| 2 | scope | `tables_summary.json`:`n_kept` | 47,948 | 47,948 | `NMarketsKept` 47,948 | yes |
| 3 | scope | `tables_summary.json`:`n_kept_no_min_filter` | 74,474 | 74,474 | `NMarketsKeptNoMin` 74,474 | yes |
| 4 | scope | `tables_summary.json`:`drop_reasons.no_price` / scope | 215,289 / 0.313 | 215,289, 31.3% | `PctNoPrice` 31.3% | yes |
| 5 | scope | `tables_summary.json`:`n_trades_in_kept_markets` | 63,023,987 | 63,023,987 | `NTradesKeptMarkets` | yes |
| 6 | Q1 | `verdicts.json`:`comparisons.Q1.statistic.value` | 67.9867 | 67.99 (df 10) | `QOneChiSq` 68.0 | yes |
| 7 | Q1 | `verdicts.json`:`comparisons.Q1.p` | 1.083e-10 | < 0.0001 | `QOneP` 1.1e-10 | yes |
| 8 | Q1 | `q1_results.json`:`main_with_min_filter.brier` | 0.10707 | 0.1071 | `QOneBrier` 0.107 | yes |
| 9 | Q1 | `q1_results.json`:`main_with_min_filter.log_loss` | 0.32336 | 0.3234 | `QOneLogLoss` 0.323 | yes |
| 10 | Q1 | `q1_results.json`:`main_with_min_filter.mean_entropy_bits` | 0.47510 | 0.4751 | `QOneEntropy` 0.475 | yes |
| 11 | Q1 | `q1_results.json`:`...bins_reject_bh`, `bins_reject_bonferroni` | 5, 4 | 5 / 4 | `QOneBinsBh` 5, `QOneBinsBonferroni` 4 | yes |
| 12 | Q1 | `q1_results.json`:`...confusion_at_0.5` tp, fp, fn, tn, accuracy | 13,467 / 3,870 / 4,074 / 26,537 / 0.83432 | same, 0.8343 | `QOneAccuracy` 83.4% | yes |
| 13 | Q1 | `q1_results.json`:`...precision`, `recall` | 0.77678, 0.76774 | 0.7768, 0.7677 | 77.7%, 76.8% | yes |
| 14 | Q1 | `q1_results.json`:`...ks_yes_vs_no.D` | 0.67293 | 0.6729 | `QOneKsD` 0.673 | yes |
| 15 | Q1 | `q1_results.json`:`no_min_filter.chi2_gof.chi2` | 214.200 | 214.2 | `QOneNoMinChiSq` 214.2 | yes |
| 16 | Q1 | `q1_bins.csv`:bin 7 `observed_rate`, `p_bh` | 0.71273, 0.001799 | 0.7127, 0.0018 | `BinSeventyEightyObs` 71.3%, `BhP` 0.002 | yes |
| 17 | Q1 | `lecture_numbers.json`:`z_interval_95.bins[0]` z_low, z_high | 0.011988, 0.015361 | [0.01199, 0.01536] | 1.2%, 1.5% | yes |
| 18 | Q1 | `lecture_numbers.json`:`z_interval_95.bins_outside`, `same_bins` | 0,1,6,7,8; true | bins 0, 1, 6, 7, 8 | `ZIntervalBinsOutsideList`, `ZIntervalSameAsBh` yes | yes |
| 19 | Q1 | `lecture_numbers.json`:`gap_direction.main` n_negative, net_gap, n_yes_minus_expected | 9, -0.00991, -475.24 | 9 of 10, -0.99 pp, 475 | `GapNegBinsMain` 9, `GapNetDiffMain` -0.99%, `GapNetYesShort` 475.2 | yes |
| 20 | Q1 | `lecture_numbers.json`:`chi2_largest_contributor` bin, share | 0, 0.31307 | bin 0, 31.3% | `ChiTopBin` 0, `ChiTopShare` 31.3% | yes |
| 21 | Q1 | `lecture_numbers.json`:`largest_gap` | bin 7, -0.032862 | -0.0329, bin 7 | `LargestGapAbs` 3.29% | yes |
| 22 | Q1 | `lecture_numbers.json`:`no_min_filter_longshot_bh.0.p_bh` | 0.60055 | 0.6006 | `NoMinBinZeroPBh` 0.601 | yes |
| 23 | Q1 | `runs/142140_q1eqfreq_v5/q1_bins_eqfreq.csv`:count `reject_bh` True | 7 | 7 | `QOneEqFreqBinsBh` 7 | yes |
| 24 | Q1 | `runs/142123_robust_full_v4/r1_results.json`:`sensitivity.n_excluded`, `q1_sensitivity.chi2_gof.chi2` | 47, 64.280 | n/a | `RobROneNExcluded` 47, `RobROneSensChiSq` 64.3 | yes |
| 25 | Q2 | `q2_results.json`:`concentration.maker.top20_share` | 0.98860 | 98.9% | `MakerTopTwentyShare` 98.9% | yes |
| 26 | Q2 | `q2_results.json`:`concentration.taker.top20_share` | 0.98008 | 98.0% | `TakerTopTwentyShare` 98.0% | yes |
| 27 | Q2 | `q2_results.json`:`concentration.maker.top1_share`, taker | 0.86115, 0.75899 | 86.1%, 75.9% | `MakerTopOneShare` 86.1%, `TakerTopOneShare` 75.9% | yes |
| 28 | Q2 | `q2_results.json`:`concentration.maker.n_wallets`, taker | 581,435; 1,535,977 | same | `MakerNWallets`, `TakerNWallets` | yes |
| 29 | Q2 | `q2_results.json`:`concentration.maker.median` | 101.188 | 101.2 | `MakerMedianVolume` 101.2 | yes |
| 30 | Q2 | `q2_results.json`:`role_tests.welch_t.t` | 117.095 | 117.1 | `RoleWelchT` 117.1 | yes |
| 31 | Q2 | `lecture_numbers.json`:`log10_mean_difference_maker_minus_taker.difference` | 0.21896 | 0.219 | `RoleLogTenDiff` 0.219 | yes |
| 32 | Q2 | `q2_results.json`:`role_tests.ks.D` | 0.057057 | 0.05706 | `RoleKsD` 0.057 | yes |
| 33 | Q2 | `q2_results.json`:`spearman_n_trades_vs_volume.rho` | 0.65535 | 0.6554 | `SpearmanTradesVolumeRho` 0.655 | yes |
| 34 | Q2 | `q2_results.json`:`kmeans.chi2_cluster_x_category` chi2, df | 6,652.96, 21 | 6,653 (df 21) | `KmeansCategoryChi` 6,653.0, `Df` 21 | yes |
| 35 | Q2 | `lecture_numbers.json`:`cluster_category_gap` obs, exp, diff | 0.06741, 0.08227, -0.01486 | 0.0674, 0.0823, -0.0149 | 6.7%, 8.2%, -1.49% | yes |
| 36 | Q2 | `lecture_numbers.json`:`ssb_ratio.mean_trade_price` | 0.0075900 | 0.00759 | `KmeansPriceSsbRatio` 0.008 | yes |
| 37 | Q3 | `q3_results.json`:`summary.p_1d.mean`, `median` | 0.37575, 0.32 | 0.3757, 0.32 | `PriceOneDayMean` 0.376, `Median` 0.320 | yes |
| 38 | Q3 | `q3_results.json`:`summary.trade_size_usdc.mean`, `median` | 129.816, 6.9304 | 129.8, 6.93 | `TradeSizeMean` 129.8, `TradeSizeMedian` 6.9 | yes |
| 39 | Q3 | `q3_results.json`:`fits.trade_size_usdc.power_law` alpha, xmin; `exponential.D` | 1.8755, 154.0; 0.53428 | D 0.5343 | `TradeSizePowerAlpha` 1.875, `Xmin` 154.0, `ExponentialKsD` 0.534 | yes |
| 40 | Q3 | `q3_results.json`:`fits.wallet_volume_usdc.power_law` alpha, D, n_tail | 1.7879, 0.023919, 211,742 | 1.788, 0.024 | `WalletVolumePowerAlpha` 1.788, `KsD` 0.024, `NTail` 211,742 | yes |

- Also checked: `numbers.tex` `CodeSetSha` 950ec496595b equals `shasum -a 256 runs/142082_mvp1_full_v1r3/code.sha256` (an item the 2026-11-02 review left unchecked). `CodeSha` 8efcddf9ef94 equals the snapshot `code_snapshot/q1_calibration.py`.
- Report footer `make_report.py` sha e47446f67433 equals `shasum` of `code/make_report.py` today.
- `SportsShareKept` 40.0%: `q3_results.json` violin n Sports 19,162 of 47,948 = 0.3996. Consistent.
- Carried minor (2026-11-02 minor 11): `GapNetYesShort` prints 475.2 as a count of outcomes. Still open.

### A6. Paper build: PASS

- PDF staleness first: `git diff --quiet -- main.tex numbers.tex references.bib figures` exits 0. `pdftotext` of the working-tree `main.pdf` equals `pdftotext` of `HEAD:main.pdf`. The 6-byte diff is metadata (CreationDate 01:31:32 against 00:59:01 on 2026-11-02). The PDF is not out of date. It is a re-build of the committed source, not a content change.
- Build: `latexmk -C`, then `latexmk -xelatex -interaction=nonstopmode main.tex` in `papers/paper_mvp1/`.

| Item | Value |
| --- | --- |
| Exit | 0 |
| Engine (`main.log` line 1) | XeTeX, TeX Live 2026 |
| Pages | 17 |
| `^!` errors | 0 |
| Overfull | 0 |
| Underfull | 0 |
| "undefined" | 0 |
| Warnings | 0 |
| "inputenc package ignored" | 0 |
| `\todo{` in `main.tex` | 4, all `\todo{owner` (lines 163, 742, 756, 823). Known open M4 row, `PLAN.md` 66 |
| `TODO` in PDF text | 4 |
| Rebuilt PDF text vs `HEAD:main.pdf` text | identical |

- Known open, not counted as new: F5 sentences over 15 words (`PLAN.md` 67).
- Figures: every PNG in `papers/paper_mvp1/figures/` is byte-equal to its source in `reports/figures/` or `runs/142082_mvp1_full_v1r3/` / `runs/142123_robust_full_v4/`.
- Side effect: the build rewrote `main.pdf` again (still ` M` in git). The committed text is unchanged. The main session decides whether to restore it with `git checkout`.

### A5. Constraints table in `STATUS.md` lines 10-17: PASS

| Constraint | Result | Evidence |
| --- | --- | --- |
| Effect size next to every p-value | PASS | Report Tables 6 (KS D), 7-8 (per-bin gap, z interval), 11-12, 16 (log10 difference, D, rho), 18 (cell gap, SSB ratio). Paper 374-383 (gap after chi-square p), 420-429 (gap before each BH p), 570-573, 579-585, 725-726 (mean difference with CI). The no-filter chi-square p (paper 457) has the mean squared residual beside it, and report Table 12 gives its per-bin gaps |
| "wallet"/"address", never "trader"/"person" | PASS | `grep -iwE 'traders?\|persons?\|people\|bettors?'`: report hits are only negations ("A wallet is an address, not a person", "not groups of people"). Paper hit 795 is "one owner may control many addresses". No "trader" anywhere |
| k-means under 1/10 of the report | PASS | Re-measured, because the report was regenerated on 2026-11-02 after the r3 measure. Style and script removed, tags to lines, blank lines dropped: 22,369 characters. k-means block (Table 17 rows and caption, Figure 18 caption, Table 18 rows and caption) 974 characters, plus the two "K-means is a side analysis" bullets 153. Share 1,127 / 22,369 = 0.050. Paper: lines 337-344 and 575-585 |
| Lecture methods only | PASS | `analysis/lecture_method_audit.md` lists 10 not-found methods. Report and paper print none of them by name except the Lorenz curve, labeled "outside the lectures" (D-028, D-031), and negations ("No Cramér's V", "drops the Gini"). Report and paper names grep: A2. `verdicts.json` still stores "Cohen's w" as `effect_size.name`; D-026 and the prereg note (line 77) keep that by design |
| Criteria fixed before results | PASS | A4 |
| Data queries on the cluster | PASS | All runs in `00.runs.md` ran on Cradle. This review ran no data query |

### H1, H2. Hierarchy: PASS with 1 minor

- H1 trace: `PLAN.md` lines 7-17 hold Mission, Vision, Constraints, Goals (RQ.md), S1, M1-M4. Every open row tags `→ M1` or `→ M4` (lines 28, 29, 65-68). M1 line: "cycle 2/2, plus one review the owner allowed (D-022); recovery 0/2". No `budget:` line.
- H2 decisions: no commit since 2026-11-02 in this folder, and D-034 is the last row. No new choice between options was found.
- New minor m-3 (hierarchy): D-022 allows one more review "for this review only" (the r3 gate of 2026-11-01). This 2026-11-07 review is a further owner request, and no D-row or M1-line note records it. The dispatch reuses the D-022 counter text. Why it matters: the K1 bound reads from the milestone line, so a later reader cannot see that a fifth M1 review ran or why. Fix: main session writes one D-row copying the owner's words of 2026-11-07 ("verify and validate mvp1 for group project"). Route: `product-manager` or main session.

### MVP ladder L1-L4

- Not applicable as a mock/real system. MVP1 here is one analysis phase on real data, with no mock API. The root `CLAUDE.md` puts MVP2 out of target (D-016). Same reading as the 2026-11-02 review.
- MVP1 independence from `future_work/`: `grep -nE '(from|import) q1a_category' code/*.py` is empty. `PLAN.md` 88-89 hold. Report and paper source lines name no `future_work/` path (`grep -c future_work` on the extracted report text and `main.tex`: see B1). The one remaining link is benign: run `142140_q1eqfreq_v5` copied `markets.parquet` from 142083 (`00.runs.md` row 17), and the open `PLAN.md` 65 row (hash compare) still has no result.

## Validate (built the right thing)

### B1. Do the deliverables answer RQ1-RQ3 and serve Mission and Vision? PASS with gaps

| Line | What it asks | What was tested | Gap |
| --- | --- | --- | --- |
| RQ1 | events priced at p happen with frequency p | chi-square GOF + per-bin binomial/BH on 47,948 markets, verdict in `verdicts.json` | none for the verdict. The direction reading has a gap (V-1) |
| RQ2 | do a few wallets do most of the trading | USDC volume shares per role in kept markets, CCDF, Lorenz, 80/20 as reference | "trading" is measured as volume only. Stated in report and paper ("Trade counts were not measured") |
| RQ3 | trade sizes, wallet activity, prices | summary, histograms, QQ, fits with KS D | none |
| Mission | price read as probability, resolved Yes/No markets, fresh price, ≥10 trades, lecture methods | exactly this kept set and these filters | "Yes/No": y = 1 when the winner equals the `outcome_seq = 1` label (`code/build_tables.py` 32-33). No saved output lists those label values (V-1) |
| Vision | which price ranges, topics, horizons are off, by how much, who sets prices | price ranges and size: yes. Topics, horizons: not in MVP1 (D-016, D-020). Who sets prices: not tested | the report never states the topics/horizons/price-setting gap. The paper states only the price-setting part (750, 796). Carried from the project-end review (`review_project_end.md` 393) |

### B2. Is the scope claim honest? PASS

- `tables_summary.json`: 47,948 kept of 688,131 in scope (7.0%). Report Table 3 and paper 181-189 give all five drop reasons with counts and shares, in rule order. The counts sum to scope.
- The Mission line (D-019) names the kept population, not "every resolved market". The paper conclusion says "On 47,948 resolved Yes/No markets".
- Q2 population (wallets of kept markets, trades after T - 1 day included, wallet-role rows) is stated in report Step 5 and paper 319-322, 473-475, 561, 576.
- Q3 trade size uses a 1,000,000-row hash-order sample of 63,023,987 trades. It is stated (report Table 2, paper 354).
- Sports share (49.7% in scope, 40.0% kept) is stated as a limit (paper 770-777).

### B3. Are the conclusions supported? ISSUE on one sentence (major), else PASS

- **V-1 (major, carried A10 with a raised severity).**
  - Where: `papers/paper_mvp1/main.tex` 379 "So Yes is priced too high."
  - Also: report Q1 "How to read" ("so Yes is priced too high"), `README.md` 44 and 72.
  - What is wrong: "Yes" here is the `outcome_seq = 1` leg. Sports is 40.0% of kept markets (`SportsShareKept`). In Sports and similar markets the first leg may be a team or player, not "Yes". No saved file shows how many first labels are "Yes" (`review_project_end_analyst.md` A10).
  - So the sentence may describe a first-listed-leg bias, not a Yes bias.
  - Also: it rests on the sign of 9 of 10 gaps, and only 5 bins are off after BH. The net gap -0.99 pp has no interval. No pre-registered line covers direction.
  - Why it matters: it is the one interpretive claim of RQ1, and README 44 puts it in the headline. The pre-registered verdict does not depend on it, because the chi-square over mirrored bins does not depend on which leg is labeled 1.
  - Fix options: (a) cluster query of `label1` value counts in the 47,948 kept markets ("needs a cluster run"), or (b) reword to "the outcome_seq = 1 leg" and mark the direction as descriptive.
  - Route: reasoning issue. `data-analyst` drafts. The owner approves the wording (`book.md` principle 13; the interpretation slot is the owner's `\todo` at 742).
- Independence caveat (D-034): PASS. Paper 376 and 785-791, report Summary "How to read" and Q1 "How to read". The abstract carries no caveat, by the owner's pick (D-034). Open limit, not a finding: no saved event-level count exists (paper 788). How much dependence would move p is unknown. chi-square 67.99 on df 10 needs a design effect above about 3.7 to fall under the 0.05 critical value 18.31 (my arithmetic, `scipy` not run). Sizing it "needs a cluster run".
- Multiple testing: PASS. Bonferroni and BH over the 10 bins (Q1). Q2 and Q3 tests carry no verdict and are labeled descriptive. The R1 drop from 5 to 4 bins off is in `tab:r1` with no sentence. Carried 2026-11-02 minor 5 (A9).
- 80/20 and power law (D-024, D-025): PASS. Both are written as descriptive references. "We do not say wallet volume follows a power law" (paper 567). The KS rejection direction is argued correctly (paper 563-564: fitted parameters make p too large).
- Longshot: PASS. The claim is limited to the minimum-trade filter, and the flip without it is printed (paper 427-431, conclusion 817).
- New minor m-4: report text uses "optimistic" for opposite directions. Q1 "How to read" and Method notes: dependence makes p too small. Q3 "How to read" 627 and Method notes 1945: KS p with fitted parameters is too large (paper 563 says so plainly). Why it matters: a reader can take both as "too small" and read the Q3 KS rejection as weaker than it is. Route: `developer` (`make_report.py` text). Reasoning, wording.
- New minor m-5: paper 733 "The answer to Q1 is no." and 815 "the answer is not exactly". These are two strengths for one verdict, and the verdict rule says "not calibrated as a whole at this n". Route: `sonnet-writer`, owner approves. Reasoning, wording.

## Findings

Severity: 0 blocker, 1 major, 11 minor. Known open rows not counted: 4 `\todo{owner`, F5 (`PLAN.md` 66-67).

| ID | Sev | Part | File:line | What | New or carried |
| --- | --- | --- | --- | --- | --- |
| V-1 | major | validate | `main.tex` 379; report Q1 "How to read"; `README.md` 44, 72 | "Yes is priced too high" asserts a Yes bias. "Yes" is the `outcome_seq = 1` leg, with unverified label values | carried A10 (minor), raised to major |
| m-1 | minor | verify | `runs/142082_mvp1_full_v1r3/q3_results.json` `summary.*.mode_50bin_mid` | trade-size and wallet-volume "mode" is the first linear bin's midpoint, above q99. Not printed | new |
| m-2 | minor | verify | `PLAN.md` 101, 115; `main.tex` 328, 479, 549; `README.md` 104-105, 137, 293, 298-299, 331 | names AC of two closed rows now fails as written, after the 2026-11-02 Lorenz and D-030 lines | new |
| m-3 | minor | hierarchy | `PLAN.md` 14; `DECISIONS.md` D-022 | this fifth M1 review has no D-row. D-022 covered one review only | new |
| m-4 | minor | validate | report Q3 "How to read", Method notes | "optimistic" used for p too small and p too large | new |
| m-5 | minor | validate | `main.tex` 733 vs 815 | "no" and "not exactly" for the same verdict | new |
| m-6 | minor | validate | `reports/report_v1.html`, `main.tex` | no sentence states that topics and horizons of the Vision are not answered in MVP1 | carried (`review_project_end.md` 393) |
| m-7 | minor | validate | `main.tex` `tab:r1`, 415-418 | R1 moves bins off from 5 to 4. No sentence says single-bin calls are fragile | carried 2026-11-02 minor 5 (A9) |
| m-8 | minor | verify | report Table 17 caption | "200,000 sampled wallets" are wallet-role rows. Table 18 p 0.0010 has no floor note | carried 2026-11-02 minor 7 (A14) |
| m-9 | minor | verify | report Figures 16, 17 captions | three sentences | carried 2026-11-02 minor 9 |
| m-10 | minor | verify | `main.tex` 381, `numbers.tex` 511 | count printed as 475.2 | carried 2026-11-02 minor 11 |
| m-11 | minor | validate | `main.tex` 270, `README.md` | criteria cell says "z interval", the prereg says Wilson. A departure note exists | carried 2026-11-02 minor 14 (G23) |

Closed since 2026-11-02: minors 1, 2 (D-034), 6, 10, 12, 13; r3 G14, G15.
Not re-checked: minor 3 (feedback page), minor 4 (semicolons).

## Needs a cluster run (not run here)

1. Value counts of `label1` (`outcome_seq = 1` label) in the 47,948 kept markets (V-1).
2. Event-level grouping of kept markets, to size the dependence behind the Q1 p-value.
3. `PLAN.md` 65: hash of `markets.parquet` of 142082 against `runs/142140_q1eqfreq_v5/input.sha256`.

## Verdict

**PASS for M1.** All four exit boxes hold on saved files. The Q1 verdict follows the prereg, which was committed before any price-outcome result. 40 of 40 sampled numbers match. The paper builds clean, and the working-tree PDF has the committed text.

The major finding V-1 is one interpretive sentence, not an exit box. It should be resolved before submission (deadline 2026-11-15, D-021).

Routing:
- Reasoning (V-1, m-4, m-5, m-6, m-7, m-11): `data-analyst` and `sonnet-writer`. The owner approves wording.
- Implementation (m-1, m-8, m-9, m-10): `developer`.
- Hierarchy (m-2, m-3): `product-manager` or main session.
- No ladder issue.
