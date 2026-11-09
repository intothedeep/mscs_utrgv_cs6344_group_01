# Table design: main-text summary of every check (`tab:checks-summary`)

- Date: 2026-11-08. Author: data-analyst. Status: design only, not implemented.
- Decision served: D-042 (R1, R2 and the review checks move to appendices, one summary table stays in the main Results).
- Constraints carried: D-038 (rows sit next to the Q1 verdict and never replace it), D-040 and D-041 F11 (the Yes/No sentence), `rules/writing/book.md` principle 13 (no new interpretation).
- Sources read: `DECISIONS.md` D-036 to D-042; `papers/paper_mvp1/main.tex` lines 403 to 422, 690 to 916, 917 to 1011; `papers/paper_mvp1/numbers.tex`; `analysis/prereg_robustness.md`; `analysis/prereg_review_fixes.md`; JSON files in `runs/150310_r3_review_fixes_v6/`.

## 1. Purpose

- Question the table answers: does any setup choice behind Q1 change the Q1 result?
- One row per check. Each row shows one key number, the Q1 rule status, and the sentence the paper already uses.
- The full text, figures and all other numbers move to the appendix sections. Nothing is deleted (D-042).
- The table adds no verdict. `main.tex` line 771: "All checks are descriptive and add no verdict."

## 2. Column set

| # | Column | Width | Content | Why |
| --- | --- | --- | --- | --- |
| 1 | Check | 0.95 in | ID, short name, then `\Cref` to its appendix section on a second line | The reader finds the full section. No separate appendix column, to save width |
| 2 | Pre-reg. | 0.45 in | one code: R, T or D (§4) | The dispatch asks which rows carry a pre-registered result. The code shows it per row |
| 3 | Markets | 0.60 in | n of the analysed set (macro) | Every check is read against the 47,948 kept markets. A smaller set must show |
| 4 | Key number (95% CI) | 1.35 in | line 1: what the number is. Line 2: the value. Line 3: the CI, if any | The rows are not of one kind (§3). A label line keeps one item per line |
| 5 | Same Q1 rule result? | 0.65 in | yes / no per analysed set, or "n/a" | D-038: the sensitivity row is read against the original Q1 row. This is the saved `row_agreement` field |
| 6 | Reading | X (about 2.0 in) | the sentence from `main.tex`, verbatim, or a `\todo` | Principle 13: the table reuses the author's words only |

Why not a uniform numeric column set (n, chi-square, p, net gap, BH bins):

- R2 is a paired Brier difference. M4 is a median comparison. M5 is a logistic fit. They have no Q1 chi-square or net gap row in the text.
- M1 and the duplicate row have no p macro. Peer a and peer b have three subsets each.
- A uniform set leaves about a third of the cells "n/a" or "needs macro". The heterogeneous key column with a label line avoids that.

## 3. Rows

Reference row (row 0) is an addition, not one of the ten checks. See §6, open item 1.

### 3.1 Numbers per row

| Row | Pre-reg. | Markets | Key number: label / macros | Same Q1 rule result? |
| --- | --- | --- | --- | --- |
| 0 Q1 original (reference) | verdict | `\QOneN` | net gap / `\GapNetDiffMain` / CI: needs macro (`runs/150310_r3_review_fixes_v6/m1_results.json` `p_1d_net_gap_ci_low`, `p_1d_net_gap_ci_high`) | reference |
| R1 clean payout | T | `\RobROneSensN` | chi-square / `\RobROneSensChiSq` (original `\QOneChiSq`) / no CI | `\RobROneRuleSame` (prints "yes") |
| R2 last-day price | T | `\RobRTwoAllN` | mean sq. residual, p_T minus p_1d / `\RobRTwoAllMeanDiff` / [`\RobRTwoAllCiLow`, `\RobRTwoAllCiHigh`] | n/a (not a Q1 rerun) |
| M1 price rule | R | `\RThreeMOneVwapN` | net gap, VWAP / `\RThreeMOneVwapNetGap` / [`\RThreeMOneVwapNetGapCiLow`, `\RThreeMOneVwapNetGapCiHigh`] | needs macro: `m1_results.json` `rows.p_vwap.row_agreement` ("same") |
| M2 Yes/No label | R | Yes/No `\RThreeMTwoYesNoN`, other `\RThreeMTwoOtherN` | net gap, Yes/No markets / `\RThreeMTwoYesNoNetGap` / [`\RThreeMTwoYesNoNetGapCiLow`, `\RThreeMTwoYesNoNetGapCiHigh`] | Yes/No: needs macro `m2_results.json` `yes_no_row_agreement` ("same"). Other: needs macro `other_row_agreement` ("different") |
| M3 proxy clusters | R | `\QOneN` | net gap CI, first key (`\RThreeMThreeKOneNClusters` clusters) / [`\RThreeMThreeKOneNetGapCiLow`, `\RThreeMThreeKOneNetGapCiHigh`] | needs macro: `m3_bootstrap.json` `proxies.k1_slug_stem.row_agreement` ("same") |
| M4 kept vs dropped | D | `\QOneN` | median volume before T−1 day, kept vs dropped / `\RThreeMFourKeptMedianVolumeBeforeDay` vs `\RThreeMFourDroppedMedianVolumeBeforeDay` USDC | n/a (descriptive) |
| M5 practical size | R | `\QOneN` | largest implied gap vs practical line / `\RThreeMFiveMaxAbsDelta` vs `\RThreeMOneMeanHalfSpread` | n/a (not a Q1 rerun) |
| Duplicate rows | T | needs macro: `minor4_dedup.json` `kept_set.n_out` | net gap / `\RThreeMinorFourNetGap` / CI: needs macro `q1.net_gap_ci_low`, `q1.net_gap_ci_high` | needs macro: `minor4_dedup.json` `q1.row_agreement` ("same") |
| Peer a volume terciles | T | `\QOneN` | net gap, high minus low / `\RThreePeerADiff` / [`\RThreePeerADiffCiLow`, `\RThreePeerADiffCiHigh`], $p=$`\RThreePeerADiffP` | low, mid, high: needs macros `peer_a_results.json` `tercile_low_row_agreement` ("same"), `tercile_mid_row_agreement` ("same"), `tercile_high_row_agreement` ("different") |
| Peer b close periods | D | `\QOneN` | net gap, `\RThreePeerBPeriodThreeLabel` / `\RThreePeerBPeriodThreeNetGap` / [`\RThreePeerBPeriodThreeNetGapCiLow`, `\RThreePeerBPeriodThreeNetGapCiHigh`] | per period: needs macros `peer_b_results.json` `period_2022-2024_row_agreement` ("same"), `period_2025_row_agreement` ("same"), `period_2026_row_agreement` ("different") |

Notes on the numbers:

- The "same" and "different" values in quotes are read from the saved JSON. They are for the writer's check only. The cell must print the macro, never the typed word.
- A rule-agreement macro should print "yes" or "no", as `\RobROneRuleSame` does. Proposed names follow the existing pattern, for example `\RThreeMOneVwapRuleSame`. The macro generator owns the names.
- M3 point net gap: only the CI has macros. The table prints the CI only. If the writer wants the point value: needs macro `m3_bootstrap.json` `proxies.k1_slug_stem.net_gap`.
- M4 alternative key number: the stale-price net gap `\RThreeMFourStaleNetGap` [`\RThreeMFourStaleNetGapCiLow`, `\RThreeMFourStaleNetGapCiHigh`]. I picked the median volume because line 838 states the check's aim as the kept-vs-dropped comparison.
- Peer b key number: I picked the 2026 period because it is the only period the text reads (lines 905 to 907). The other two periods stay in the appendix.
- `\RThreeRun` is defined in `main.tex` line 76, not in `numbers.tex`. It is a run identifier, not a measured number.

### 3.2 Reading per row (reused sentences)

| Row | Reading cell (exact text for the `.tex`) | Source line in `main.tex` | Edit made |
| --- | --- | --- | --- |
| 0 Q1 original | `\VerdictQOne{}` | 405 | none |
| R1 | The Q1 rule result is the same without the unclear markets. | 995 (also 713) | none |
| R2 | So \pOne{} is not the price at the close. | 998 | none |
| M1 | So the pre-registered reading is that the price rule does not create the gap. | 782 | none |
| M2 | In the markets labelled Yes/No, Yes is priced above its observed rate. The other markets show no rejection. | 798, 801 | parentheticals with n, chi-square and p removed (n is in column 3) |
| M3 | Under the first key, the interval still lies below 0. The proxies are not true event keys. | 822, 827 (also 977) | 822: subject "it" made explicit, interval bounds removed (they are in column 4) |
| M4 | `\todo{owner: reading of M4}` | none | no reading sentence exists. Lines 839 to 843 hold numbers only |
| M5 | Of \RThreeMFiveGridPrices{} grid prices, \RThreeMFivePracticalPrices{} pass the practical line. | 860 | none |
| Duplicates | `\todo{owner: reading of the duplicate-row check}` | none | no reading sentence exists. Lines 879 to 880 hold numbers only |
| Peer a | `\todo{owner: reading of the volume terciles}` | none | no reading sentence exists. Line 892 holds numbers. Caption 898 only names the test |
| Peer b | In \RThreePeerBPeriodThreeLabel{} the chi-square test does not reject. Its \CiLevel{} CI excludes 0. | 905, 907 | 905: BH p and n parenthetical removed. 907: bounds removed (in column 4) |

Fallbacks for the three `\todo` cells, if the owner wants no `\todo` in the main text:

- Use the number sentence verbatim: M4 lines 839 to 840, duplicates line 880, peer a line 892.
- That repeats column 4. It adds no reading, so it stays inside principle 13.

Why not peer b caption line 913 ("overlapping intervals mean no sign that the gap changes with the period"): it is a reading rule, not a statement. The text never says the intervals overlap. Using it would add a claim.

## 4. Pre-registered result vs descriptive

| Code | Meaning | Rows | Pre-registration line |
| --- | --- | --- | --- |
| R | pre-registered reading rule with named outcomes | M1 | `prereg_review_fixes.md` §1.5, lines 119 to 126 (outcome A in `m1_results.json` `outcome`) |
| R | same | M2 | §2.3, lines 159 to 166 (Yes-bias, `m2_results.json` `yes_bias` true). Wording goes to the owner (D-040) |
| R | same | M3 | §3.4, lines 226 to 229 (`m3_bootstrap.json` `robust_to_proxy` true) |
| R | same | M5 | §5.2, lines 277 to 282 (practical-size line) |
| T | pre-registered test or row comparison, no reading rule | R1 | `prereg_robustness.md` line 60 (row agreement) |
| T | same | R2 | `prereg_robustness.md` lines 89, 94 (paired t-test, one p-value) |
| T | same | Duplicates | `prereg_review_fixes.md` line 309 (Q1 row, row agreement) |
| T | same | Peer a | line 322 (Welch t, high minus low) |
| D | descriptive only | M4 | line 258 ("M4 is descriptive") |
| D | descriptive only | Peer b | lines 331 to 334. Per-period Q1 analysis with BH over periods, but no between-period test, and line 334 says "descriptive" |

- No row carries a verdict. All codes sit under `main.tex` lines 694 and 771.
- Peer a: the Welch p is `\RThreePeerADiffP`. The text gives it with its CI (line 892) and no reading. The table does the same.
- Peer b: the per-period BH p-values are pre-registered tests inside each period. The code D says there is no test of the period effect itself.

## 5. Caption, label, note

- Caption: "Each sensitivity check next to the original Q1 row, with its key number and the reading from its appendix section. Why: each new row sits next to the original Q1 row and does not replace it. Source: runs \RunId, \RobustRun{} and \RThreeRun."
- Label: `tab:checks-summary`, after `\caption`, caption below the table (`rules/writing/latex.md` §10, §14).
- Note line under the caption (not counted in the two sentences, `rules/figures.md` §3):
  "Abbreviations: pre-registration status (Pre-reg.) · confidence interval (CI) · Benjamini-Hochberg (BH) · volume-weighted average price (VWAP) · R: pre-registered reading rule · T: pre-registered test without a reading rule · D: descriptive only · n/a: not a rerun of the Q1 analysis."
- The "Why" sentence is `main.tex` line 772 ("Each new row sits next to the original Q1 row and does not replace it."), also D-038. It adds no reading.
- Not used: "each row changes one choice behind the Q1 result". The text never says it, and it is false for M4 and M5.

## 6. Open items for the main session

1. Row 0 (Q1 original) is not in the dispatch's ten rows. D-038 and `rules/visualization.md` §1 put new rows next to the original. I recommend it. If the dispatch holds to ten rows, delete row 0 and keep `\QOneChiSq` and `\GapNetDiffMain` in the caption's first sentence.
2. D-041 F11 pins the D-040 Yes/No sentence to the review-checks section. After the move that section is an appendix. The M2 reading cell then carries the sentence into the main body too. Whether that satisfies F11 is the owner's call.
3. Three reading cells (M4, duplicates, peer a) have no sentence in the text. They need the owner's words or the number-sentence fallback (§3.2).
4. Three rows print "no" in column 5 for one subset: M2 other markets, peer a high tercile, peer b 2026. The text states the M2 and peer b cases (lines 801, 905). It does not state the peer a high tercile case. The cell is a saved field, not a reading, but the owner may want the appendix text to name it.
5. Appendix labels (`app:r1`, `app:r2`, `app:m1` to `app:m5`, `app:dup`, `app:peer-a`, `app:peer-b`) do not exist yet. The writer creates them when moving the sections.

## 7. LaTeX skeleton (for the writer)

Column types go once in the preamble. `tabularx` loads `array`, so no new package.

```latex
% preamble, after \usepackage{tabularx}
\newcolumntype{L}[1]{>{\raggedright\arraybackslash}p{#1}}
\newcolumntype{Y}{>{\raggedright\arraybackslash}X}
```

```latex
\begin{table}[H]
\centering
\small
\setlength{\tabcolsep}{4pt}
\begin{tabularx}{\textwidth}{L{0.95in}L{0.45in}L{0.60in}L{1.35in}L{0.65in}Y}
\toprule
Check & Pre-reg. & Markets & Key number (\CiLevel{} CI) & Same Q1 rule result? & Reading \\
\midrule
Q1 original (reference) & verdict & \QOneN &
  net gap\newline \GapNetDiffMain\newline [NEEDS MACRO p\_1d\_net\_gap\_ci] &
  reference & \VerdictQOne{} \\
\midrule
R1 clean payout\newline \Cref{app:r1} & T & \RobROneSensN &
  $\chi^2$\newline \RobROneSensChiSq{} (orig.\ \QOneChiSq) &
  \RobROneRuleSame &
  The Q1 rule result is the same without the unclear markets. \\
\midrule
R2 last-day price\newline \Cref{app:r2} & T & \RobRTwoAllN &
  mean sq.\ residual, \pT{} $-$ \pOne\newline \RobRTwoAllMeanDiff\newline [\RobRTwoAllCiLow, \RobRTwoAllCiHigh] &
  n/a &
  So \pOne{} is not the price at the close. \\
\midrule
M1 price rule\newline \Cref{app:m1} & R & \RThreeMOneVwapN &
  net gap, VWAP\newline \RThreeMOneVwapNetGap\newline [\RThreeMOneVwapNetGapCiLow, \RThreeMOneVwapNetGapCiHigh] &
  [NEEDS MACRO rows.p\_vwap.row\_agreement] &
  So the pre-registered reading is that the price rule does not create the gap. \\
\midrule
M2 Yes/No label\newline \Cref{app:m2} & R & Yes/No: \RThreeMTwoYesNoN\newline other: \RThreeMTwoOtherN &
  net gap, Yes/No\newline \RThreeMTwoYesNoNetGap\newline [\RThreeMTwoYesNoNetGapCiLow, \RThreeMTwoYesNoNetGapCiHigh] &
  Yes/No: [NEEDS MACRO]\newline other: [NEEDS MACRO] &
  In the markets labelled Yes/No, Yes is priced above its observed rate. The other markets show no rejection. \\
\midrule
M3 proxy clusters\newline \Cref{app:m3} & R & \QOneN &
  net gap CI, first key\newline (\RThreeMThreeKOneNClusters{} clusters)\newline [\RThreeMThreeKOneNetGapCiLow, \RThreeMThreeKOneNetGapCiHigh] &
  [NEEDS MACRO proxies.k1\_slug\_stem.row\_agreement] &
  Under the first key, the interval still lies below 0. The proxies are not true event keys. \\
\midrule
M4 kept vs dropped\newline \Cref{app:m4} & D & \QOneN &
  median volume before $T-\DaysShort$ day (USDC)\newline \RThreeMFourKeptMedianVolumeBeforeDay{} vs \RThreeMFourDroppedMedianVolumeBeforeDay &
  n/a &
  \todo{owner: reading of M4} \\
\midrule
M5 practical size\newline \Cref{app:m5} & R & \QOneN &
  largest implied gap vs practical line\newline \RThreeMFiveMaxAbsDelta{} vs \RThreeMOneMeanHalfSpread &
  n/a &
  Of \RThreeMFiveGridPrices{} grid prices, \RThreeMFivePracticalPrices{} pass the practical line. \\
\midrule
Duplicate rows\newline \Cref{app:dup} & T & [NEEDS MACRO kept\_set.n\_out] &
  net gap\newline \RThreeMinorFourNetGap\newline [NEEDS MACRO q1.net\_gap\_ci] &
  [NEEDS MACRO q1.row\_agreement] &
  \todo{owner: reading of the duplicate-row check} \\
\midrule
Peer a: volume terciles\newline \Cref{app:peer-a} & T & \QOneN &
  net gap, high $-$ low\newline \RThreePeerADiff{}, $p=\RThreePeerADiffP$\newline [\RThreePeerADiffCiLow, \RThreePeerADiffCiHigh] &
  low, mid, high:\newline [NEEDS MACROS] &
  \todo{owner: reading of the volume terciles} \\
\midrule
Peer b: close periods\newline \Cref{app:peer-b} & D & \QOneN &
  net gap, \RThreePeerBPeriodThreeLabel\newline \RThreePeerBPeriodThreeNetGap\newline [\RThreePeerBPeriodThreeNetGapCiLow, \RThreePeerBPeriodThreeNetGapCiHigh] &
  per period:\newline [NEEDS MACROS] &
  In \RThreePeerBPeriodThreeLabel{} the chi-square test does not reject. Its \CiLevel{} CI excludes 0. \\
\bottomrule
\end{tabularx}
\caption{Each sensitivity check next to the original Q1 row, with its key number and the reading from its appendix section. Why: each new row sits next to the original Q1 row and does not replace it. Source: runs \RunId, \RobustRun{} and \RThreeRun.}
\label{tab:checks-summary}
{\small Abbreviations: pre-registration status (Pre-reg.) $\cdot$ confidence interval (CI) $\cdot$ Benjamini-Hochberg (BH) $\cdot$ volume-weighted average price (VWAP) $\cdot$ R: pre-registered reading rule $\cdot$ T: pre-registered test without a reading rule $\cdot$ D: descriptive only $\cdot$ n/a: not a rerun of the Q1 analysis.\par}
\end{table}
```

- The abbreviation line is a separate paragraph after `\label`, not a `\newline` inside `\caption`. A `\newline` in a caption is fragile under the `caption` package (list of tables, short caption).

- Every `[NEEDS MACRO ...]` is a placeholder for the macro generator. It must not reach the PDF. The writer replaces it once `numbers.tex` holds the macro.
- The abbreviation line uses " · " as separator, not semicolons (`rules/writing/style.md` §3).
- The `\todo` cells print red in the PDF until the owner fills them.

## 8. Width estimate

| Item | Value |
| --- | --- |
| Text width | 8.5 in − 2 × 0.9 in (`geometry` margin, line 19) = 6.70 in |
| Gutters | 6 columns × 2 × 4 pt = 48 pt = 0.67 in |
| Fixed columns | 0.95 + 0.45 + 0.60 + 1.35 + 0.65 = 4.00 in |
| Reading column (X) | 6.70 − 0.67 − 4.00 = 2.03 in, about 30 characters per line at `\small` |
| Widest fixed cell | a CI line, e.g. "[−1.50%, −0.91%]", about 75 pt. Column 4 is 1.35 in = 97 pt. Fits |
| Widest "Check" cell | "Appendix B.10" from `\Cref` (noabbrev), about 60 pt. Column 1 is 68 pt. Fits |
| Row height | 3 lines in most rows (column 4 label, value, CI). M2 and M3 reading: 4 lines |
| Table height | about 35 lines × 12 pt + 11 midrules × 5 pt + head and caption about 70 pt ≈ 545 pt ≈ 7.5 in, about 0.8 of a page |

- How it fits the width: `tabularx` at `\textwidth`, `\small`, `\tabcolsep` 4 pt (the `tab:bins` setting, lines 428 to 429), ragged-right `p` columns, long names spelled out only in the abbreviation line.
- Overfull check: after the build, grep the `.log` for `Overfull \hbox` at the table's line range. Ragged-right `p` columns cannot overflow except on one unbreakable token wider than the column.
- Risk: the height (about 0.8 page) is the real cost, not the width. `[H]` may push it to the next page and leave a gap.

## 9. Options if it is too wide or too tall

| Option | What | Gain | Cost |
| --- | --- | --- | --- |
| A (recommended) | the six-column table above, `\small` | one row per check, one look gives number, rule and reading. Fits 6.7 in by the estimate in §8 | about 0.8 page. Reading wraps to 3 to 4 lines in a 2.0 in column |
| B | five columns plus a full-width reading line under each check: `\multicolumn{5}{L{6.0in}}{\textit{Reading:} ...}` in the same row block, `\midrule` only between checks | reading gets about 100 characters per line, 1 to 2 lines. Number columns can widen, so CI fits on the value line. Height drops to about 0.6 page | the reading line could look like a separate row. `rules/writing/latex.md` §8 wants a rule between every row, so the reviewer must accept the two lines as one row. More LaTeX for the writer |
| C (fallback for width only) | option A with `\footnotesize` | about 10% more characters per line, no layout change | font under the caption size. Harder to read in print |

- Recommendation: A. Width fits by the estimate, and it keeps one logical row per line block, as latex.md §8 asks.
- Switch to B if the built table runs past one page or shows Overfull. C only as a last step.
