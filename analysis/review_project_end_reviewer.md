Verdict: PASS for the project end, MVP1 scope (0 blocker, 2 major, 9 minor, 11 open items). The Q1 verdict reproduces from saved files. All four "MVP1 is done when" boxes hold under the new names. The paper builds clean. The two major findings are a Wilson interval still printed in report Table 11 (a hit on the Constraints line "lecture methods only" and on D-026) and three run snapshots that no longer match their own hash lists. Neither flips PASS: no exit box names either, the longshot row has its z result in Table 10, and the fixes are one argument in `make_report.py` plus a regenerate, and three `git checkout` lines.

# Project-end review: reviewer part

- Date: 2026-11-01. Scope: MVP1 only (D-016). Deadline 2026-11-15 (D-021).
- Inputs read: `PLAN.md`, `DECISIONS.md` D-016 to D-028, `RQ.md`, `STATUS.md`, `00.runs.md`, `CHANGELOG.md`, `../tips/group_01/polymarket_plan_detailed.md` ("MVP1 is done when" and the MVP1 method tables), `analysis/review_mvp1_rq_r3.md`, `analysis/prereg_mvp1.md`, `analysis/lecture_method_audit.md` (grep only).
- Deliverables checked: `reports/report_v1.html` (text extracted, 808 lines), `reports/lecture_numbers.json`, `reports/figures/*.png`, `papers/paper_mvp1/main.tex`, `numbers.tex`, `main.pdf`, `README.md`, `docs/team_split_design.html` (AC greps only), `code/lecture_numbers.py`, `code/make_report.py` (grep only), `code/q1_calibration.py` (grep only).
- Saved sources: `runs/142082_mvp1_full_v1r3/` (`verdicts.json`, `q1_results.json`, `q1_bins*.csv`, `q2_results.json`, `q2_concentration.csv`, `q3_results.json`, `tables_summary.json`, `manifest_*.json`), `runs/142123_robust_full_v4/r1_results.json`, `r2_results.json`, `runs/142140_q1eqfreq_v5/q1_bins_eqfreq.csv`.
- Nothing was edited except this file and the LaTeX build products in `papers/paper_mvp1/`. No commit, no `rm`.
- Local runs: saved outputs only (CSV, JSON, HTML, PNG, PDF), one core, each under 10 s. No parquet, no cluster (`~/.claude/CLAUDE.md` "No local execution").
- State: the whole MVP1 gate state is still uncommitted (`git status`). The verdict applies to the working tree at review time.
- Routing classes: implementation (developer, sonnet-writer), reasoning (data-analyst), hierarchy (product-manager, owner line). L1 to L4 do not apply (not system or app work).
- IDs continue from r3. G1 to G17 are not reused.

## Findings

Fact and judgment are marked in each row.

| ID | Severity | Location | What is wrong | Evidence | What would close it | Class, fix owner |
| --- | --- | --- | --- | --- | --- | --- |
| G18 | major | `reports/report_v1.html` Table 11 ("Longshot bins against the dataset paper"), column "95% CI of ours" | Fact: the column prints the Wilson interval, which D-026 removed. Values [-0.006164, -0.002784] and [-0.03494, -0.009963] equal `q1_results.json` `longshot.*.ci_low_diff`, `ci_high_diff`. Those come from `code/q1_calibration.py` line 70 to 73, `wilson()`. Table 10 prints the z interval for the same gaps ([-0.006263, -0.00289], [-0.03547, -0.0105]) from `lecture_numbers.json` `longshot`. Fact: `code/make_report.py` `paper_longshot_block` prints the header "95% CI of ours" only when the dict has no `z_low_diff`, so the v1 call passes the `q1_results.json` dict, not the lecture one. Fact: `PLAN.md` line 10 and the `STATUS.md` Constraints table say "lecture methods only", so this is a Constraints hit, not a formatting slip. Judgment: two unlabeled 95% intervals for one quantity in one report, and one of them is an outside method. The AC names grep could not see it because the word "Wilson" is not printed. The gap values, the verdict and Table 10 are unaffected. | `reports/report_v1.html` Tables 10 and 11. `code/make_report.py` lines 414 to 424. `code/q1_calibration.py` lines 23 to 73. `DECISIONS.md` D-026. `PLAN.md` line 10. | `make_report.py` passes the `lecture_numbers.json` `longshot.main_with_min_filter` dict to `paper_longshot_block` for v1, regenerate v1 from the saved run under "Allowed locally", and Table 11 then prints "95% z interval of ours". v2 output stays unchanged (D-017). | implementation, developer |
| G19 | major | `runs/142082_mvp1_full_v1r3/code_snapshot/make_report.py`, same file in `runs/142123_robust_full_v4/` and `runs/142140_q1eqfreq_v5/` | Fact: `git diff --stat runs/` shows the three snapshot files modified (1 line each, the 6330 to 6344 label edit r3 reported). Each run's `code.sha256` lists the HEAD hash, so the snapshots no longer match their own hash lists. Fact: r3 reported this as "known corruption" with the fix, and it is still open. Judgment: a run snapshot is a record of what ran (`rules/measurement.md`). An edited snapshot is a provenance defect even when no number depends on it. Raised from note to major because it was flagged and left. | `git diff --stat runs/`. r3 "Known open rows" last row. | `git checkout -- runs/142082_mvp1_full_v1r3/code_snapshot/make_report.py runs/142123_robust_full_v4/code_snapshot/make_report.py runs/142140_q1eqfreq_v5/code_snapshot/make_report.py`. Do not checkout `DECISIONS.md`. The D-015 cell gets a surgical hand edit ("not 6344" to "not 6330", 1 hit today). | implementation, main session |
| G20 | minor | `papers/paper_mvp1/main.tex`, new lines today | Fact: 14 new prose sentences and 1 table cell exceed 15 words (`rules/writing/style.md` §2, §6). Method: a macro or a math span counts as one token, as in r3. The macro-only header and data rows of `tab:conc` are excluded as macro lists. The over-long cell is the `tab:prereg` "Effect size" cell (27). Longest sentences: the departure sentence at line 277 (31 words), the goodness-of-fit sentence at line 292 (25), the three-fits sentence at line 507 (22), the score sentence at line 414 (21), the Up/Down sentence at line 164 (20). Judgment: the F5 row was open before today, and today's edit moved it further from its AC. | `git diff -U0 -- papers/paper_mvp1/main.tex`, scratch count script. | Split each listed sentence and the cell. Part of the open F5 row. | implementation, sonnet-writer |
| G21 | minor | `papers/paper_mvp1/main.pdf` pages 6 and 7 (Figures 3 and 4) | Fact: the new PNGs (`fig4_calibration_z.png` 900 px wide, `lorenz_top_shares.png` 1050 px wide) sit at 0.46 of the line width beside PNGs of another aspect ratio. Fact: the paired panels have unequal heights (bottom-aligned, uneven tops), and both pages end with about one third of blank space. Judgment (estimate, not measured): a 6 inch matplotlib figure with default 10 pt text, placed at 0.46 of a text width of about 6.7 inch, scales to about 5 pt, below the 7 pt floor of `rules/figures.md` §4. The legend and tick text in the render look that small. The figures themselves pass §7 (legend above the axes, no overlap, units on axes). | PDF pages 6 and 7 rendered at 70 dpi. `reports/figures/*.png` opened. | Either a wider figure (one per row) or a larger font in `code/lecture_numbers.py` `draw_calibration` and `draw_lorenz`, then regenerate under "Allowed locally". | implementation, developer (font) or sonnet-writer (layout) |
| G22 | minor | `README.md` line 78 | Fact: the 84.1% is sourced as "`papers/paper_mvp1/main.tex` line 66". The macro `\PaperTopShare` is on line 65, and its real source is the dataset paper Table 5, which `main.tex` cites. Judgment: a README fact should cite the primary source, not our own tex. | `README.md:78`, `main.tex:65`, `main.tex:150-151`. | Cite "Qin and Yang 2026, Table 5" and drop the tex line number. | reasoning, data-analyst or main session |
| G23 | minor | `README.md` line 458 (criteria table) and `papers/paper_mvp1/main.tex` line 261 (`tab:prereg`) | Fact: both tables carry a "pre-registered criteria" heading and say "z interval", while `analysis/prereg_mvp1.md` line 25 says "95% Wilson CI" and stays as committed. Each document carries a departure note (README line 461, paper line 277). Judgment: disclosed, but the criteria table misquotes the prereg. The README AC excepted this line because it "quotes the prereg". It no longer does, so the exception is moot. | `README.md:458,461`, `main.tex:261,277`, `prereg_mvp1.md:25`. | The criteria table quotes the prereg verbatim (Wilson, Brier, Cohen's w) and the departure note names the replacements. | reasoning, data-analyst |
| G24 | minor | `../tips/group_01/polymarket_plan_detailed.md` Q1 row "Brier score" and Q2 row "CCDF" | Fact: the struck Brier row still says lecture "L15 + outside", while report Table 7 caption and paper line 298 say Lecture 20, and the audit row 12 names D20 s26. Fact: the Q2 CCDF row still says "test 80/20 rather than assume it", with no D-024 note, while README line 94 says no p-value test ran. Judgment: the plan's method table was amended for D-026 and D-028 but not for these two cells. | Plan lines 90 and 112 (method tables). `README.md:94`. `lecture_method_audit.md:47`. | Two dated cell notes on the plan rows (L20 by D-026; descriptive reference by D-024). | hierarchy, product-manager |
| G25 | minor | `README.md` lines 458 and 460 (new table rows) | Fact: semicolons in the citation cell ("owner, 2026-10-18; D-025, D-026 ..."). `rules/writing/style.md` §3. Judgment: the mission-block and D-row semicolons in `PLAN.md` and `DECISIONS.md` follow the `rules/docs.md` §0.1 and §8 templates and are exempt. | `git diff -U0 README.md`. | Split the cell with a period or a line break. | implementation, sonnet-writer |
| G26 | minor | report Figure 10 caption, paper `fig:lorenz` caption | Fact: the report caption has 5 sentences and the paper caption 4, against the two-sentence rule (`rules/figures.md` §3). Judgment: the extra sentences are the D-028 label ("outside the lectures", "nothing was measured below 80%"), which must stay somewhere. | `report_v1.html` Figure 10, `main.tex:458`. | Move the label sentences to the body text and keep "what" and "Why:" in the caption. | implementation, sonnet-writer |
| G27 | minor | `00.runs.md` header | Fact: the header still says "Environment for all runs: Cradle `gpul40q` ... `~/myEnvs/cs6330`" and then adds the rename sentence. Run 142082's manifests say host `gpu011`, 16 CPUs. The G12 row was closed today on the per-run CPU counts, which are now there. Judgment: the first sentence reads as current when it is historical. | `00.runs.md:4`, `manifest_q1_calibration.json`. | Reword to "ran on ... (renamed to `~/myEnvs/cs6344`, D-015)". | documentation, main session |
| G28 | minor | `papers/paper_mvp1/main.tex` line 458 | Fact: the Lorenz caption prints the 80% reference as a literal "80\%" while `\TopTwentyReference` exists and the body uses it. The M4 exit says every measured number is a macro. Judgment: 0.80 is a design constant (`lecture_numbers.py` `REFERENCE_SHARE`), not a measured number, so this is cosmetic. | `main.tex:458`, `numbers.tex:487`. | Use `\TopTwentyReference` or leave as a documented constant. | implementation, sonnet-writer |

## Checks

| # | Check | Result | Notes |
| --- | --- | --- | --- |
| 1 | Lecture-scope row 1 (code and report), all ACs rerun | PASS | import: both greps empty. saved numbers: `source_run` 142082, 10 rows in `z_interval_95.bins`, `same_bins` true (read from the file, equals the row). names: `TEXT \| grep -wE NAMES \| grep -vE KEEP` empty. The 3 raw hits are the departure note (D-025, D-026, D-028), "calls it the Brier score", and the Lorenz figure text with "outside the lectures". D-028: 0 and 1. Fig. 4: 2 and 6. verdict: 1, `verdicts.json` unchanged (`git diff --quiet`). macros new: 55. scope: `git diff --quiet -- future_work/reports/` exits 0 (only the staged rename). |
| 2 | Lecture-scope row 2 (`main.tex`), all ACs rerun | PASS | G5: line 163 to 164 give the settlement reason with `\citep{qin2026polymarketv1}`. G13: `S-PAPER-4` 0, `inputenc` 0. names: empty. removed macros: 0. figures: 1 and 1. R1 interval: no "Wilson" and no `RobROneAgreementLow` in `main.tex`; the agreement sentence prints the rate alone. owner parts: 4. verdict: 2. build: see check 10. |
| 3 | Lecture-scope row 3 (prereg note) | PASS | `git diff --numstat`: 58 added, 0 deleted. `limitation 5`: 1. D-024 3, D-026 4, D-028 4. `prereg_robustness.md` named once and unchanged (`git diff --quiet`). The note's Table in §4 equals `lecture_numbers.json` (5 bins 0, 1, 6, 7, 8 both ways; no-min 4 bins 6, 7, 8, 9 both ways; equal-frequency 8 outside vs 7 BH off, extra bin (0.0, 0.00122] with 1 Yes in 4,795). |
| 4 | Lecture-scope row 4 (README) | PASS, with G22, G23, G25 | names: empty. All 7 raw hits are a team name, the rename sentence, the D-028 label, the step 14 record, or the departure note. table: 0. lognormal: 2 hits, line 98 says "No such analysis runs now". |
| 5 | Lecture-scope rows 5 and 6 (design page, G17 note) | PASS | design page: 0, 4, 0. G17: `fetch_run` in `CHANGELOG.md` (1) and in `code/q3_box_p1d.py` docstring (1). |
| 6 | AC amendments made today: did any hollow out its AC? | PASS, see table below | Judgment per amendment. None hides a gap that the AC was written to catch. G18 is a gap no AC covered, not a loosened one. |
| 7 | "MVP1 is done when" boxes 3 and 4 under the new names | Box 3 PASS, Box 4 PASS | Section below. |
| 8 | Numbers against saved sources | PASS, with G18 | Section below. |
| 9 | Report, paper and README say the same thing on Q1, Q2, Q3 | PASS | Section below. |
| 10 | Build `papers/paper_mvp1` | PASS | `latexmk -C` then `latexmk -pdf -interaction=nonstopmode main.tex`. `.latexmkrc` maps `-pdf` to XeLaTeX (`main.log` line 1: XeTeX, TeX Live 2026). Exit 0. `^!` 0. Overfull 0. Underfull 0. "Warning" 0 (the r3 `inputenc` warning is gone). `main.blg` warnings 0. No "undefined". `main.pdf` 13 pages (r3: 11), written 2026-11-01 23:28. Pages 6 and 7 (the two changed figures) inspected: G21. The 4 `\todo{owner` boxes print red on pages 2, 10, 11. |
| 11 | Figures `fig4_calibration_z.png`, `lorenz_top_shares.png` | PASS | Opened both. fig4: both series with z error bars, dashed diagonal, legend above the axes (3 entries), no overlap, axes labeled with units, main points sit below the diagonal in bins 1 to 8, the no-filter top bin sits visibly below. Lorenz: 4 saved points per role at x 0.80, 0.90, 0.95, 0.99, 80/20 diamond at (0.80, 0.20), grey "not measured" band below x 0.80, legend above with all 5 entries. Both drawn by `code/lecture_numbers.py` sha d553342cb0d7 (equals `lecture_numbers.json` `code_sha`, recomputed with `shasum`). Paper copies in `papers/paper_mvp1/figures/` are byte-equal (`cmp`). |
| 12 | Style on new lines | ISSUE (G20, G25, G26) | em dash: none on new lines of `README.md`, `prereg_mvp1.md`, `main.tex`, `make_report.py`, `lecture_numbers.py`, `PLAN.md`, `DECISIONS.md`, `CHANGELOG.md`, `00.runs.md`, `STATUS.md`, nor in the report text. Semicolons: G25, plus the exempt template lines. "person": `main.tex` 0 hits for person, people, trader. Report hits are the three disclaimers ("not a person", "One person may use many addresses", "not groups of people"). README hits are the disclaimer (line 392), the constraint row (492), and "3-person split" (271, 275, 283), which is not a wallet label. |
| H1 | Hierarchy trace | PASS | Mission block has Mission, Vision, Constraints, Target scope, Goals, S1, M1 to M4. M1 line: `cycle 2/2`, plus one review by D-022, `recovery 0/2`. M4: `cycle 1/2; recovery 0/2`. No `budget:`. Every open and closed row under "Open tasks", "MVP1 gate" and "Lecture scope" tags `→ M1` or `→ M4` (r3 G15 closed: lines 28 and 29 now tag M1). `RQ.md`: RQ1 to RQ3 `answered` with run-file evidence. |
| H2 | Decisions logged | PASS | D-023 to D-028 each have a Why line naming a mission-block line or RQ, a Rejected cell, decider `owner`, and evidence (owner's words with date, or a file path). D-028 names D-026 in Supersedes. The AC amendments (check 6) are not choices between options and need no row. |

### AC amendments made today (check 6)

| Row and AC | Amendment visible in the text | Hollowed? | Why |
| --- | --- | --- | --- |
| Row 1, AC import | "This one holds already (2026-11-01)" added, and a second grep over `code/*.py` | no | The second grep widens the check. Both empty. |
| Row 1, AC macros unused | From "numbers.tex drops the removed macros" to "`main.tex` uses none of them; `numbers.tex` still defines them" | no | The generator is additive and serves `future_work/papers/paper_mvp2` (D-017). The check that matters, no removed macro in the MVP1 paper, is still there (row 2 AC macros: 0 hits). |
| Row 1 and 2, AC R1 interval | "Either the sentence drops, or ... cites a saved z value" | no | No saved z value exists for the agreement rate (`r1_results.json` `mapping.agreement_ci95` is Wilson). Dropping the interval is the only option under "no retyped number". `main.tex` prints the rate alone. |
| Rows 1, 2, 4, AC names, `KEEP` list | Gained `Team Brier`, `calls it the Brier`, `drops the Gini`, `Lorenz picture`, `picked from the lecture-method audit` | no | Every KEEP-matched line in the report (3) and README (7) is a team name, a rename sentence, a departure note or the D-028 label. None is a live use of the method. The whitelist is text-specific, so it would not hide a new live use that lacks those phrases. |
| Row 4, AC names, exception "Q1: is the crowd right" | The criteria table line is excepted "because it quotes the prereg" | moot | That line no longer names Wilson, Brier or Cohen's w (0 hits), so the exception is unused. The line misquotes the prereg instead: G23. |
| Row 2, AC G13 | "`main.log` has no 'inputenc package ignored'" | no | 0 hits after today's build. |

### Boxes 3 and 4 under the new names (check 7)

Name mapping (D-026, D-028): Wilson CI to z interval (Bernoulli SD, L5, L6). Cohen's w to per-bin gaps (observed rate minus mean price). Cohen's d to the log10 mean difference. Eta squared to SSB / (SSB + SSW). Brier score to mean squared residual of the price (same number). Gini, Cramér's V, ARI, Cohen's d_z and the cluster chi-square removed. Lorenz kept as a labeled figure. Chi-square goodness of fit kept as the L12 form.

Box 3, "Every row in the MVP1 tables above has a result", MVP1 method tables of the plan:

| Row | Result under the new name | Where |
| --- | --- | --- |
| Q3 summary, histogram, box plot, violin, ECDF, fits, QQ, KS, scaling | unchanged from r3 Check 3. Box plot PNG mtime 2026-11-01 20:51, unchanged since r3 verified it | report Tables 5, 6, Figures 2 to 6 |
| Q1 binomial per bin, 10 bins, equal-frequency check | BH p and call per bin | report Table 8, 12, 13; paper Table 2 |
| Q1 95% CI per bin, now z interval | `[z_low, z_high]` per bin and "mean price outside it" | report Table 8; `lecture_numbers.json`; paper Table 2 |
| Q1 chi-square goodness of fit, L12 form | 67.99, df 10, p 1.08e-10 | report Table 7; paper §5.1 |
| Q1 Bonferroni and BH | 4 / 5 | report Table 7 |
| Q1 Brier, now mean squared residual; log loss; entropy | 0.1071, 0.3234, 0.4751 | report Table 7; paper §5.1 |
| Q1 classifier at 0.5 | confusion matrix, precision 0.7768, recall 0.7677, accuracy 0.8343 | report Table 9 |
| Q1 KS Yes vs No | D 0.6729 | report Table 7; paper |
| Q1 longshot bins | gaps with z interval (Table 10). Table 11 still prints the Wilson interval: G18 | report Tables 10, 11 |
| Q2 mean vs median, top shares, CCDF with 80/20 | 139.4 and 61.67; top 1/5/10/20%; 98.9% and 98.0% against 80% | report Table 14, Figure 9; paper Table 3 |
| Q2 Lorenz (figure only, D-028), Gini removed | `lorenz_top_shares.png`, labeled | report Figure 10; paper Figure 4 |
| Q2 t-test and KS makers vs takers, now log10 mean difference | t 117.1, diff 0.219; D 0.05706 | report Table 16; paper §5.2 |
| Q2 k-means, elbow | K 4, 4 clusters | report Table 17, Figure 11 |
| Q2 cluster chi-square | removed by D-026, row struck in the plan | none, by decision |
| Q2 ANOVA and permutation, now SSB / (SSB + SSW) | F 509.9, perm p 0.0010, ratio 0.00759 | report Table 18; paper §5.2 |
| Q2 Spearman | rho 0.6554 | report Table 16 |

Judgment: every live row has a result. The two cells the plan did not annotate (G24) do not remove a result. Box 3 PASS.

Box 4, "Every test reports an effect size next to its p-value". I read "next to" as the same row or the same table, with a caption pointer allowed when the per-bin table follows directly.

| Test with a p | Effect size beside it | Where |
| --- | --- | --- |
| Chi-square goodness of fit (main, no-min) | mean squared residual in the same row; per-bin gaps in the next table, named in the caption | report Table 7; paper Table 5 (`tab:r1`), §5.1 text |
| Binomial per bin (BH p) | observed minus price in the same row | report Tables 8, 12; paper Table 2 |
| KS fits (6 rows) | D in the same row | report Table 6; paper Table 4 |
| KS Yes vs No | D in the same row | report Table 7 |
| Welch t makers vs takers | log10 mean difference in the same row | report Table 16; paper §5.2 |
| KS makers vs takers | D in the same row | report Table 16 |
| Spearman | rho in the same row | report Table 16 |
| ANOVA and permutation (2) | SSB / (SSB + SSW) in the same row | report Table 18; paper §5.2 |
| R2 paired t (paper only) | mean difference and 95% CI in the same sentence | paper §5.4 |
| R1 sensitivity chi-square (paper only) | mean squared residual and bins off in the same row | paper Table 5 |
| Power law KS (paper and report Q2 text) | alpha and D in the same sentence or row | report Table 6, Q2 text; paper §5.2 |

Judgment: Box 4 PASS. No p stands alone.

### Numbers against saved sources (check 8)

- Report, all 19 tables and the Summary, compared cell by cell to `q1_results.json`, `q2_results.json`, `q3_results.json`, `tables_summary.json`, `verdicts.json`, `lecture_numbers.json`, `q1_bins*.csv`, `q1_bins_no_min.csv` (BH p), `runs/142140_q1eqfreq_v5/q1_bins_eqfreq.csv`, and the four manifests (code shas, host `gpu011`, job 142082, 16 CPUs). All equal to the shown digits. Drop shares recomputed (37.1, 9.1, 31.3, 11.7, 3.9, 7.0). The one exception is Table 11's interval column (G18): the digits are correct for the Wilson method, but that method was removed.
- Report Reproduce block: `make_report.py` sha ec268fd9c4d6 (equals `shasum` of the working-tree file) and `verdicts.py` sha fdcca90b6588 (the working-tree `code/verdicts.py` is v4, sha 4e2ca7ac7dd6; the run's `verdicts.json` records fdcca90b6588 for v3, so the report is right to print the run's value).
- `lecture_numbers.json`: z intervals recomputed from `q1_bins.csv` (`n`, `n_yes`) for bins 0, 7, 9: [0.011988, 0.015361], [0.694245, 0.731222], [0.973990, 0.981117], equal. `same_bins` true follows from `bins_outside` [0, 1, 6, 7, 8] equal to `reject_bh` in `q1_bins.csv`. `largest_gap` bin 7, -0.0329, is the maximum absolute `diff_obs_minus_price` in `q1_bins.csv`. `top20_share` equals `q2_concentration.csv`. `log10_mean_difference` 0.2190 equals 2.1042 minus 1.8852 from `role_tests.welch_t`. `ssb_ratio` equals the two `eta_squared`. `power_law_wallet_volume` equals `q3_results.json` `fits.wallet_volume_usdc.power_law`. `code_sha` d553342cb0d7 equals `shasum` of `code/lecture_numbers.py`.
- Paper `numbers.tex` (428 macros): every macro used by `main.tex` and checked: `NMarketsKept`, `NMarketsInScope`, all drop counts and shares, `QOneChiSq` 68.0, `QOneP` 1.1e-10, `QOneBrier` 0.107, `QOneLogLoss` 0.323, `QOneEntropy` 0.475, `QOneYesRate` 36.6%, `QOneAccuracy` 83.4%, precision 77.7%, recall 76.8%, `QOneKsD` 0.673, `QOneBinsBh` 5, Bonferroni 4, `QOneNoMin*` (74,474, 0.134, 214.2, 1.7e-40), `QOneEqFreqBinsBh` 7, bin macros for 0 to 10, 10 to 20, 70 to 80, 90 to 100 (price, observed, z interval, gap, BH p), `ZInterval*` (5; 0, 1, 6, 7, 8; yes), `LargestGapAbs` 3.29%, `LargestGapBin` 7, maker and taker wallets, means, medians, top 1/5/10/20 shares, `TopTwentyReference` 80.0%, `RoleWelchT` 117.1, `RoleLogTen*` (0.219, 2.104, 1.885), `RoleKsD` 0.057, Spearman 0.655, k-means K 4, sample 200,000, cluster sizes and medians, `KmeansPriceSsbRatio` 0.008, `KmeansNPerm` 1,000, `PriceOneDayMean` 0.376, median 0.320, trade size 129.8 and 6.9, power-law alpha, xmin, D for both variables, normal and exponential D, `PilotNMarkets` 2,063, `PilotShareMarketsAfterClose` 51.3%, R1 (47,940, 7, 0, 1, 40, 47, 47,901, 64.3, 5.6e-10, 0.107, 4, agreement 99.92%), R2 (0.015, 18.98%, 10.97%, 4.65%, 8.02%, 5.9%, 0.107, 0.075, -0.032, [-0.033, -0.031], 45,112, -0.034, [-0.035, -0.033]), Sports shares (49.7%, 40.0%, survival 5.6%, drops 183,999, 66,807, 119). All equal their saved sources (`r2_results.json` `overall`, `brier_traded_only`; `r1_results.json`; r3 Check 10 for the Sports and pilot values, unchanged files).
- Literal digits in the paper body are structural only: bin edges, `1.96` in the z formula, `80/20`, `1/(N+1)`, CC-BY-4.0, TikZ coordinates, and the literal `80\%` of G28.
- `README.md`: the Q1, Q2, Q3 and robustness tables (lines 55 to 122) equal the saved files: 47,948, 67.99, 1.08e-10, -0.0329 bin 7, 5 of 10 bins 0, 1, 6, 7, 8, 5, 4, 0.1071, 581,435, 1,535,977, 86.1%, 75.9%, 98.9%, 98.0%, alpha 1.788, xmin 3,450, n_tail 211,742, D 0.0239, p 1.15e-105, 0.32, 0.376, 0.015 and 0.66, 6.93, 129.8, 91.1, 7,745, 1.875, 214.2, 47,901, 4 bins, 7 of 10. The k-means share line now reads 0.0974 and 0.0824 with the r3 source, and 0.0782 has 0 hits (G14 closed on the README side). Line 78: G22.
- `analysis/prereg_mvp1.md` note: §4 table equals `lecture_numbers.json` and `q1_bins_eqfreq.csv` (8 outside, 7 BH off, extra bin with 1 Yes in 4,795). The two dataset-paper quotes were verified by r3 Check 6.

### Report, paper and README agree (check 9)

| Item | Report | Paper | README | Same? |
| --- | --- | --- | --- | --- |
| Q1 verdict sentence | "Prices are not calibrated as a whole at this n." (Table 1, How to read) | `\VerdictQOne` printed once in §5.1, "not calibrated as a whole" twice | line 49, verbatim | yes |
| "The effect is small" | Q1 How to read: "The effect is small. The largest per-bin gap is -0.0329, in bin 7" | §5.1 and §6: "The effect is small: the largest per-bin gap is 3.29% ... bin 7, counting from 0" | lines 43, 66: "The largest per-bin gap is 3.29 percent points, so the effect is small" | yes (fraction vs percent, same value) |
| 80/20 | "Yes, far beyond the 80/20 reference. 98.9% / 98.0% against 80%. The 80/20 rule and the power law come from Lecture 6. No pre-registered verdict" | §5.2 and §6, same sentences, 80.0% | lines 43, 50, 76, 94 (no p-value test ran) | yes |
| Power law limits | Table 6 caption and How to read: tail only, D not comparable, lognormal not compared, KS p optimistic; Q2 text: close to a power law, KS rejects an exact one | §5.2 (close to, KS rejects), §5.3 (not ranked, lognormal not compared, KS p optimistic) | lines 95 to 98, 114, plus the D-027 future-work line | yes. Only the README carries the D-027 line, which is what D-027 asked |
| Departure from the prereg | Summary note (D-025, D-026, D-028) | §4.1 last two sentences | lines 461, 488 | yes |
| Wallet, never person | three disclaimers | "A wallet is one address" ×2 | lines 68, 392, 492 | yes |

## M1 and M4 exit lines

M1, "exit: the four 'MVP1 is done when' boxes":

| Box | Result | Evidence |
| --- | --- | --- |
| 1 market and wallet tables from the full data | PASS | r3 Check 3, files unchanged (`tables_summary.json` 688,131 in scope, 47,948 kept, 2,117,412 wallet-role rows) |
| 2 Figures 1 to 8 exist | PASS | run folder PNGs unchanged since 2026-10-19; plan Fig. 4 and Fig. 7 now also have the D-026 and D-028 versions in `reports/figures/` |
| 3 every MVP1 table row has a result | PASS | section above |
| 4 effect size next to every p | PASS | section above |

M1 can close on its exit line. Open M1 rows that do not block it:

| Row | State | Blocks exit? | Reason |
| --- | --- | --- | --- |
| Split `code/make_report.py` | open, owner deferred 2026-10-19 | no | code hygiene, no box names it |
| Owner reviews report v1 | open | no | the owner's own step, after this review |
| G7 `criteria_sha256_12` null | open | no | record gap, verdict reproduces (r3 Check 2). Needs a verdict-only cluster run, main session |
| Optional hash compare 142082 vs 142140 | open | no | provenance, cluster side, main session |
| G19 snapshot files (this review) | open | no | provenance, not a box. Fix is three `git checkout` lines |
| G18 Table 11 Wilson (this review) | open | no | one column of one report table. The box-3 row (longshot) has its z result in Table 10 |

M4, "exit: reviewer gate PASS (`analysis/review_papers.md`), `papers/paper_mvp1` builds clean, every measured number is a `numbers.tex` macro":

| Clause | Result | Evidence |
| --- | --- | --- |
| reviewer gate PASS | PASS | `STATUS.md` 2026-10-19, `analysis/review_papers.md` exists |
| `paper_mvp1` builds clean | PASS | check 10: exit 0, 0 errors, 0 overfull, 0 underfull, 0 warnings |
| every measured number is a macro | PASS | check 8, literal digits are structural (G28 is a constant) |

M4 can close on its exit line as written. Open M4 rows that the exit line does not name:

| Row | State | Blocks exit? | Reason |
| --- | --- | --- | --- |
| 4 `\todo{owner: ...}` (related work, interpretation, implications, closing) | open, 4 hits, print red on pages 2, 10, 11 | no, by the line as written | The owner said "not yet". That is a decision, not a gap. Fact: the PDF carries 4 red TODO boxes until the owner writes or removes them, so it is not a submission-ready document today. |
| F5 sentence length | open, 14 new long sentences and 1 cell today (G20) | no | after the owner's text |
| 3-person split pick | open, owner "not yet" | no | a decision, not a gap |

Judgment: both exit lines can close. The owner decides whether a paper with 4 red TODO boxes counts as "done" for the 2026-11-15 deadline. No recommendation here.

## Open items (11)

1. G18 report Table 11 Wilson interval (developer).
2. G19 three run snapshot files and the D-015 cell (main session).
3. G20 and F5 sentence length in `main.tex` (sonnet-writer, after the owner's text).
4. G21 figure text size and panel heights in the paper (developer or sonnet-writer).
5. G22, G23, G25 README lines 78, 458, 460 (data-analyst, sonnet-writer).
6. G24 two plan cells, L20 and the 80/20 "test" wording (product-manager).
7. G26, G28 captions (sonnet-writer).
8. G27 `00.runs.md` header sentence (main session).
9. G7 `criteria_sha256_12` null, and the optional 142082 vs 142140 hash compare (main session, cluster).
10. 4 `\todo{owner` parts and the 3-person split (owner, "not yet").
11. Owner review of report v1, and the deferred `make_report.py` split (owner).

## Could not check

- `future_work/`: out of scope (D-016, D-017). Not built, not opened.
- "Only methods from our lectures" against the decks themselves: checked against the plan's lecture column and the audit's grep rows only.
- Brier recomputation per market and the box plot PNG: not redone. r3 Check 3 covers the PNG (file unchanged, mtime 20:51), and the previous review recomputed chi-square, w, BH and Bonferroni from `q1_bins.csv`.
- `docs/team_split_design.html` beyond the three AC greps.
- Report rendering at 1040 px: the main session did it, per the task.
