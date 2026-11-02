# Project-end review: MVP1 (2026-11-01)

Verdict: PASS for M1 and M4 exit lines (reviewer). Reading of results needs fixes: analyst 0 blocker, 8 major, 7 minor. Reviewer 0 blocker, 2 major, 9 minor. Architect: design holds, 1 owner conflict on G7.

Open items: each section below. Main session verified G18, A1 and A2 against saved files.

## Reviewer

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


## System architect

Verdict: the design holds, and every number traces to a saved run. Clean-clone rebuild fails today. Four plan lines lag D-024 to D-028, and one open task contradicts D-026.

# Project-end review: system-architect part

- Date: 2026-11-01. Scope: MVP1 (D-016). Deadline: 2026-11-15 (D-021).
- Remit: does what was built match the design and the plan's contract?
- Nothing ran. I read files only, and edited only this file.
- Marks: **[F]** fact from a named file. **[J]** my judgment. **[?]** needs an answer.
- Git state comes from reading the submodule index file, `.git/modules/.../cs6344_group_01/index`.
- That index stores full paths: the byte before each path is its length. So absence is meaningful.
- The main session confirms it with `git status`. The index shows staged paths, not commits.
- `analysis/review_mvp1_rq_r3.md` line 11 reports the same uncommitted state.
- Options serve M1 and M4 under S1 and RQ1 to RQ3. No option changes a number.
- "Plan line N" means `../tips/group_01/polymarket_plan_detailed.md`. `PLAN.md` is named in full.

Terms: index (스테이징 목록), snapshot (스냅샷: the code copy in a run folder), manifest (실행 기록 파일), provenance (출처 추적), gitignored (git 제외).

## 1. Reproducibility

**Answer: not today. It works after one commit and one environment file, without the cluster, for a rebuild from committed inputs.**

```
runs/142082 (tracked) ─► lecture_numbers.py* ─► lecture_numbers.json*, z PNG*, Lorenz PNG*
runs/142123 r2_markets.csv (gitignored, fetch) ─► q3_box_p1d.py* ─► box PNG*
all of the above ─► make_report.py ─► report_v1.html

runs/142082, 142041, 142140 (tracked)  ┐
runs/142123 results (tracked)          ├► make_paper_numbers.py ─► numbers.tex
runs/142123 markets.csv (gitignored)   ┘
numbers.tex + figures/ (copied by hand, 3*) ─► latexmk ─► main.pdf

* = on disk, not in the index
```

### Missing inputs

| Item | State | Effect on a clean clone |
| --- | --- | --- |
| `code/lecture_numbers.py` | [F] not in index | Cannot regenerate the JSON or 2 figures |
| `code/q3_box_p1d.py` | [F] not in index | Cannot regenerate the box plot |
| `reports/lecture_numbers.json` | [F] not in index | `make_report.py` v1 exits, line 831 |
| `reports/figures/*.png` | [F] not in index | The report prints a skip note for each |
| `papers/paper_mvp1/figures/fig4_calibration_z.png` | [F] not in index | The paper shows a dashed box |
| `papers/paper_mvp1/figures/lorenz_top_shares.png` | [F] not in index | The paper shows a dashed box |
| `papers/paper_mvp1/figures/fig6_ccdf.png` | [F] not in index | The paper shows a dashed box |
| `runs/142123_robust_full_v4/r2_markets.csv` | [F] gitignored by design | Needs fetch to redraw the box plot |
| `runs/142123_robust_full_v4/markets.csv` | [F] gitignored by design | Needs fetch to regenerate `numbers.tex` |
| `pyproject.toml`, `uv.lock`, `.python-version` | [F] at the course repo root, not in the group repo | [J] A clone of the group repo alone gets no dependencies from `uv run` |
| `../tips/group_01/polymarket_plan_detailed.md` | [F] in the parent repo, modified and uncommitted | M1 exit cites a file outside the group repo |

### Traps

- [F] `\figorbox` draws a dashed box and the build still exits 0 (`figkit.sty` line 51).
- [F] So the plan's build AC (0 errors, 0 overfull) passes with a figure missing.
- [F] `Page.figure` skips a missing PNG and the report still writes (`make_report.py` lines 191, 192).
- [F] `add_categories` is skipped when `markets.csv` is absent (`make_paper_numbers.py` line 620).
- [F] Then the 4 `main.tex` lines that use those macros fail at build. That failure is loud.
- [F] `fetch_run.sh` line 12 uses `~/cs6344_polymarket/runs` on the remote host.
- [J] The `~` is the owner's home only. A teammate's account would not resolve it.
- [?] Do teammates have Cradle access? The script needs an answer, or a stated owner-only fetch.
- [F] No rebuild order exists. `papers/README.md` covers `numbers.tex` and the build only.
- [F] `papers/README.md` line 13 says figures come from the run folder. Two come from `reports/figures/`.
- [F] No script copies figures into `papers/paper_mvp1/figures/`.

### Is `reports/lecture_numbers.json` tied to the run?

- [F] By a name only: `source_run` = `142082_mvp1_full_v1r3`.
- [F] It stores its own `code_sha` `d553342cb0d7`, which equals the `CHANGELOG.md` value.
- [F] It stores no input-file hash and no pointer to the run's `code.sha256`.
- [F] `make_report.py` line 830 and `make_paper_numbers.py` line 443 compare the name only.
- [J] Once committed, the git commit pins both sides, because `runs/` stays as committed (D-026).
- [J] So the gap is low risk after the commit, and real before it.

### Paper v1 spans four runs

| Input | Run | Tie that is checked |
| --- | --- | --- |
| Main numbers | 142082 | Run name macro |
| Box plot, category macros | 142123 | [F] Row counts match `tables_summary.json` |
| Equal-frequency BH count | 142140 | [F] `binom_p` compared, stops on a difference |
| Close-time macros | 142041 | [F] None |

- [F] The 142083 and 142082 table match is "by construction". Byte equality is not measured (`00.runs.md`).
- [F] The open G11 row closes that gap.

### Options for the rebuild path (owner picks)

| | What | Gain | Cost |
| --- | --- | --- | --- |
| A stable | Commit derived files, add `pyproject.toml` and `uv.lock`, write one "Rebuild v1" section, tag the submitted commit | A teammate builds with no cluster. The commit is the pointer | [J] About one hour. No input-file hashes |
| B scalable | A, plus `jobs/rebuild_v1.sh` and `reports/manifest_v1.json` with run, input hashes, script hashes, output hashes. Stop on a missing figure | One command, and drift is caught | New code and a new contract, 2 weeks before the deadline |
| C cutting-edge | Content-addressed pipeline (Make or DVC) with a shared store for individual-level files | Full rebuild for anyone | Needs storage and access rules. Individual-level data leaves the cluster |

- [J] All three keep the `.gitignore` individual-level rows unchanged. C alone strains the reason for them.

## 2. Separation of MVP1 and `future_work/`

**Answer: the boundary is clean and one-way. MVP2 should still run. It has not run since the move, and its record would break.**

```
future_work/code/q1a,q1b,q1c ──PYTHONPATH──► code/common.py, code/q1_calibration.py
code/*.py ──────────────────────────────────► nothing in future_work/
```

### What crosses the boundary

| Importer | Imported | Source |
| --- | --- | --- |
| `q1a_category.py`, `q1b_deadline.py`, `q1c_volume.py` | `common`: 5 helpers | [F] import lines |
| `q1a_category.py` | `q1_calibration.bin_table` | [F] exists, line 28 |
| `q1b_deadline.py` | `q1_calibration.LOG_CLIP` | [F] exists, line 20 |
| Any file in `code/` | nothing from `future_work/` | [F] grep is empty, the r2 import is fixed |

### Code in `code/` that serves MVP2

| File | Part | Keep? |
| --- | --- | --- |
| `build_tables.py` | `add_long_horizon_columns`, `p_7d` | [J] Keep. Removal changes the table a rerun builds |
| `verdicts.py` | `q1a`, `q1b`, `q1c`, `CRITERIA` rows | [J] Keep. Skipped when result files are absent |
| `make_summary.py` | `MVP2_STAGES` | [J] Keep. Listed only when a report exists |
| `make_report.py` | `sec_q1a`, `sec_q1b`, `sec_q1c`, `sec_compare`, `--version v2` | [J] Keep. D-017 and D-020 require a way back |
| `make_paper_numbers.py` | `add_q1a`, `add_q1b`, `add_q1c`, unused macros | [J] Keep. Additive by design |
| `common.py` | `horizon_long_days`, `min_category_n`, `n_perm`, `seed` | [F] Not MVP2 only. `q3_describe.py` line 128 and `r2_price_path.py` line 98 read `min_category_n` |

### Can MVP2 run if the owner goes for it (D-020)?

- [F] `future_work/jobs/mvp2.slurm` sets `PYTHONPATH`, snapshots both code folders, and calls the moved files.
- [J] So it should run. It is unproven: no run has used the moved layout.
- [?] Is `future_work/` on the cluster? A pilot job proves this at low cost.
- [F] `verdicts.py` `CRITERIA` points to `analysis/prereg_mvp2.md`. D-017 moved the file to `future_work/analysis/`.
- [F] `sha12` returns null without error (line 19). So Q1a to Q1c would repeat the G7 defect.
- [F] The job writes to `runs/`, and `fetch_run.sh` fetches into `runs/`. The ledger keeps MVP2 runs in `future_work/runs/`, so a hand move follows.
- [F] `future_work/code/q1a_category.py` line 27 keeps its own `group_categories`, and `common.py` has a second copy.
- [J] That copy is the price of "leave MVP2 unchanged" (D-017). Drift risk is low while MVP2 sleeps.
- [F] D-026 applies to MVP1. `future_work/README.02.md` still names Cramér's V, Cohen's d and eta squared.
- [J] Going back to MVP2 therefore means a second lecture-method audit, because the Constraint holds there too.
- [J] Unused macros in `numbers.tex` are harmless. `main.tex` does not use them (AC in `PLAN.md`).

## 3. Code version

**Answer: the run-to-code link holds by snapshot and hash. The labels no longer identify code. The derived layer has only a partial link.**

### Layer 1: cluster runs. The link holds.

- [F] 142082, 142123 and 142140 each track `code_snapshot/` and `code.sha256`.
- [F] `verdicts.json` `verdicts_py_sha256_12` `fdcca90b6588` equals the 142082 `code.sha256` row.
- [J] `code/` moving past the snapshots harms nothing. The snapshot answers "which code made this number".

### Layer 2: derived files. The link is partial.

| Script | Label | Sha recorded where | Gap |
| --- | --- | --- | --- |
| `lecture_numbers.py` | `lecture-v1` | [F] In its JSON and `CHANGELOG.md`, equal | Script not in the index |
| `make_report.py` | `v3` | [F] In the report and `CHANGELOG.md`, equal: `ec268fd9c4d6` | Label misleads, see below |
| `make_paper_numbers.py` | none | [F] `CHANGELOG.md` only | `numbers.tex` does not stamp it |
| `q3_box_p1d.py` | none | [F] Nowhere | No sha on file for the box plot |

### Labels that no longer identify code

- [F] `make_report.py` says `v3` at sha `c37079965d60` in all three snapshots and `ec268fd9c4d6` now.
- [F] `common.py` gained `group_categories` under a "no version bump" row, and it still says `v5`.
- [F] The v5 snapshot in 142140 has sha `61557c0422c3`. It lacks the moved function.
- [J] Any new cluster run would stamp `v5` on different code. This repeats the F6 retro-note pattern.
- [J] The move is safe in effect. The `CHANGELOG.md` row states "moved unchanged", with no hash comparison.
- [F] `rules/measurement.md` §2.2 asks for invariance evidence with each change.
- [F] `jobs/mvp1_b.slurm` now names `kimq` and 8 CPUs. Run 142082 used `gpul40q` and 16 CPUs (`00.runs.md`).
- [F] `common.py` line 84 ties thread count to the v1 and v2 non-determinism.
- [J] A full rerun may not match bytes. No plan row needs one, so do not rerun.

### Options (owner picks)

| | What | Gain | Cost |
| --- | --- | --- | --- |
| A stable | Add two `CHANGELOG.md` lines: the `q3_box_p1d.py` sha, and "labels of derived scripts do not identify code, use the sha". Bump `common.py` before any cluster run | Honest record, no code change | Labels stay loose |
| B scalable | A, plus `make_paper_numbers.py` and `q3_box_p1d.py` stamp their own sha, with a run-style manifest beside the outputs | Every derived file names its code | Small code change, then regenerate |
| C cutting-edge | Stamp a git commit id into every output | One id for everything | Needs a clean tree before each build, which this shared checkout lacks |

## 4. Decision hierarchy against D-025 to D-028

**Answer: no owner line is broken in substance. One open task contradicts D-026. Four lower lines lag the decisions.**

| Line | Says | Decision | Finding |
| --- | --- | --- | --- |
| `PLAN.md` G7 row | [F] "re-issue verdicts for run 142082" | [F] D-026: "`runs/` stay as committed" | **Real conflict.** Task against an owner decision. Goes to the owner. See options below |
| Plan line 118 | [F] Main Q2 answer comes from "the shares and the Lorenz curve" | [F] D-028: a picture of the top shares. README line 488: "a labeled figure, not an analysis" | Wording conflict. Lorenz cannot be a main source and also only a picture |
| Plan line 124 | [F] "test 80/20 rather than assume it" | [F] D-024: descriptive reference, not a verdict line | Wording conflict |
| Plan line 32 | [F] "All lecture concepts" | [F] D-026 removes the independence test | [J] Holds at lecture level, since L12 stays through goodness of fit. The line 40 note is enough until the owner edits |
| Plan lines 32, 38 | [F] "three forced uses" | [F] D-026 removes one | [F] Row 128 shows two remain: ANOVA with permutation, Spearman. One owner edit |
| Plan line 169 | [F] "three forced Q2 tests stay" in MVP2 | [F] v2 is unchanged | [J] Still true of report v2. No action |
| Mission, `STATUS.md` Constraints | [F] "only methods from our lectures", no exception | [F] D-028 keeps Lorenz, labeled outside | [J] The owner's later word governs. The text lacks the exception, which only README line 488 states |
| Constraint: effect size next to every p-value | [F] D-026 removes w, d, V, d_z | [F] Box 4 names "difference, D, ρ" | [J] Consistent in form. The chi-square p now has per-bin gaps. `reviewer` and `data-analyst` check each row |
| Vision: "topics and horizons" | [F] Kept by D-020 | [F] MVP1 does not answer them | [J] No conflict, since a Vision has no date. But the paper states no gap |
| `RQ.md`: 6 answered | [F] RQ4 to RQ6 cite `future_work/runs/` | [F] D-016: not a target | [J] True, evidence exists. Only the owner edits RQ rows. No action |
| `.claude/rules/visualization.md` §7 | [F] Asks for three panels: f(x), x f(x), Lorenz | [F] D-026: "D-025 wins" here. D-028 restores Lorenz only | [F] The audit put this to the owner (line 248). Resolved. The exception sits only in a D-row |

Notes on the rows above:

- [F] The only place for the Vision gap sentence is `main.tex` line 684, an owner todo on future work.
- [J] If the owner deletes that todo with no text, the paper never names the gap.
- [F] `fig7_lorenz.png` prints Gini in its legend. So the 4-point redraw has a reason, and it is not a defect.
- [J] §7 protects against reading an area as a share. CCDF plus Lorenz has no such area, so no harm remains.
- [F] Panels 1 and 2 of §7 are absent from the `main.tex` figure list.
- [J] Drawing them needs wallet rows, so a job.
- [J] A later reviewer will flag §7 again unless the exception is written where rules live.
- [F] `rules/docs.md` §6: repo exceptions belong in the owner's section of root `CLAUDE.md`. Agents never write there.

### Options for G7 (owner picks)

Facts first:

- [F] The Q1 hash is null (`verdicts.json` line 29).
- [F] `verdicts.py` hashes the working file. The prereg note has changed that file.
- [F] So a plain re-issue cannot meet the AC, which needs the hash from `f78de3e`.
- [F] `prereg.json` is in the run folder, so the numeric criteria are pinned already.

| | What | Keeps D-026? | Cost |
| --- | --- | --- | --- |
| A stable | Leave `verdicts.json`. Record prereg commit and hash in the `00.runs.md` row. Rewrite the G7 AC | Yes | One edit. The file itself keeps a null |
| B scalable | Write `analysis/verdict_criteria_pin.json`: run, file, commit, hash. Rewrite the AC | Yes | One small file. A second place to look |
| C cutting-edge | Change `verdicts.py` to take a pinned hash, bump the version, re-issue into the run | No. The owner lifts D-026 for this file | Code change. The verdict file changes after citation |

- [F] `verdicts.py` reads saved JSON only, so C may fit "Allowed locally". The main session decides.

## 5. Before 2026-11-15, ranked

### Must change

| Rank | Item | Who | Why this rank |
| --- | --- | --- | --- |
| 1 | Commit today's state: `code/`, `reports/`, `papers/paper_mvp1/figures/`, `analysis/`, living docs. Also commit the parent repo's plan file | Main session | [J] A lost checkout loses everything. It unblocks a clone, at low cost |
| 2 | Write or remove 4 owner todos, then finish F5. State the Vision gap in the closing text if wanted | Owner, then `sonnet-writer` | [F] Open rows. The paper cannot ship with them |
| 3 | Pick the 3-person split | Owner | [F] Open row. Teammates wait on it |
| 4 | Pick the rebuild option (§1), and answer Cradle access | Owner, then `developer` | [J] Without it, teammates depend on the owner's laptop |
| 5 | Pick the G7 option (§4) | Owner | [F] The open row contradicts D-026 |
| 6 | Add a missing-figure check to the final build AC: every `\figorbox` target exists | `product-manager` | [F] Today's build AC cannot catch it |
| 7 | Run the G11 parquet hash compare | Main session, cluster | [F] Open row. It proves the 142140 tie. Not equal stops work |
| 8 | Owner edits plan lines 32, 38, 118, 124, and the `STATUS.md` Constraint row | Owner | [J] No number depends on them. The next reader will trip on them |
| 9 | Record the derived-layer sha gap and the v5 label (§3) | Main session | [J] Record only. Bump `common.py` before any cluster run |
| 10 | Clean stale text, listed below | Main session or `sonnet-writer` | [J] Cosmetic |

Stale text for rank 10:

- [F] README line 272 shows the G17 note as open. `PLAN.md` closed it.
- [F] `papers/README.md` line 3 says "Two LaTeX papers", against D-023.
- [F] `make_paper_numbers.py` lines 7 and 8 show old MVP2 paths.
- [F] Plan line 153 cites `papers/paper_mvp2/numbers.tex`, which moved.
- [J] Add one note to `future_work/README.02.md`: the `CRITERIA` path, and the second audit.

### Should not change

| Item | Why |
| --- | --- |
| `runs/` and the prereg files | [F] D-026. They are the evidence |
| `q1_calibration.py`, `r1_split_payout.py`, `q2_concentration.py` outside methods | [J] They match the snapshots. `lecture_numbers.py` is the right layer for lecture names |
| `common.py` defaults | [F] MVP1 reads `min_category_n` |
| Extra macros in `numbers.tex` | [F] By design, and the paper does not use them |
| MVP2 paths in `make_report.py` and `make_paper_numbers.py` | [F] D-017, D-020 |
| `verdicts.py` `CRITERIA` code | [J] Note it only. Fixing it now touches a cited stage for no target |
| `.gitignore` individual-level rows | [F] Deliberate |
| `future_work/` contents | [F] D-017 |
| Any new cluster analysis, power-law test or lognormal run | [F] D-025, D-027 |
| Full rerun of 142082 | [J] Different partition and CPU count. It risks numbers for no gain |

### Do not do before the deadline

- The `make_report.py` split row.
- [F] Its AC asks for byte-equal HTML, but the page prints the script's own sha (lines 789, 802).
- [F] So that AC cannot pass as written. `product-manager` rewrites it if the row stays open.
- [J] The `code.md` 400-line review line is passed by a wide margin. That is debt, not risk.

## Unverified

- [?] Current sha of `code/*.py` against `CHANGELOG.md`. Checking needs a hash run, and I ran nothing.
- [?] k-means share since D-026. The `PLAN.md` value 0.0974 came before the lecture edits. `reviewer` re-measures.


## Data analyst

# Project-end review: data-analyst part (MVP1)

- Date: 2026-11-01.
- Scope: analysis method and number reading in `reports/report_v1.html`, `papers/paper_mvp1/main.tex`, `papers/paper_mvp1/numbers.tex`, `README.md`.
- Nothing was run. All inputs are saved outputs and code snapshots.
- Report locations use Table and Figure numbers. The HTML body is one minified line.

## 1. Result

**The Q1 verdict sentence stands. 0 blockers, 8 major, 7 minor. The numbers are correct. The readings go further than the numbers.**

| Rank | ID | Severity | Finding in one line |
| --- | --- | --- | --- |
| 1 | A3 | major | "The effect is small" rests on a maximum and hides a one-way bias of 0.99 points |
| 2 | A2 | major | "Cheap bets pay off less" holds for cheap Yes legs, main set only |
| 3 | A4 | major | README omits independence. The paper's "read the intervals first" does not escape it |
| 4 | A1 | major | The "long straight" CCDF tail is one drawn chord, a plotting artifact |
| 5 | A5 | major | "Close to a power law" conflicts with README, with the paper's own KS line and with Figure 9 |
| 6 | A6 | major | "Most of the trading" means volume. Scope and post-close trades are not stated |
| 7 | A7 | major | Paper says do not compare sizes. Report says compare the size |
| 8 | A8 | major | Report Table 11 still prints Wilson intervals, against D-026 |

Rank order: what changes a reader's conclusion on the verdict comes first. Q2 readings come next, then consistency. IDs follow the question order, not the rank.

Why this review: step 4 of the workflow cycle gives the analyst the numbers, tables and method at project end.

Data used:

- `runs/142082_mvp1_full_v1r3/`: bin CSVs, `q2_*`, `q3_results.json`, code snapshot, `fig6_ccdf.png`, `fig7_lorenz.png`.
- `runs/142123_robust_full_v4/report_r1_split_payout.md`, `runs/142140_q1eqfreq_v5/q1_bins_eqfreq.csv`, `reports/lecture_numbers.json`.
- `analysis/prereg_mvp1.md`, `analysis/lecture_method_audit.md`, `analysis/review_mvp1_rq_r3.md` G14, `DECISIONS.md` D-024 to D-028.

All data is real run output, with no generated data. D-024 to D-028 are the owner's picks. This memo does not reopen them.

What passed:

- `numbers.tex` bin, z, top-share and power-law macros match the saved files I compared.
- Maker and taker wallet counts sum to the 2,117,412 rows. So the `volume_usdc > 0` filter dropped nothing.
- Maker and taker total volume are equal, about 8.2 billion USDC. So no trade is double counted inside a role.
- The chi-square reproduces from `q1_bins.csv` (§7). The 5 z bins and 5 BH (Benjamini-Hochberg, 거짓 발견율 보정) bins match.
- "Wallet = address" appears in all three deliverables.

## 2. Q1: is "the effect is small" supported?

Signs of observed rate minus mean price (`-` below price, `+` above, `*` BH off):

```
bin set               0    1    2    3    4    5    6    7    8    9
main (47,948)         -*   -*   -    -    -    -    -*   -*   -*   +
no min filter (74,474)+    -    -    -    -    -    -*   -*   -*   -*
equal frequency       -    -*   -*   -*   -*   -*   -    -*   -*   +
```

Reading:

- 9 of 10 gaps are negative in all three bin sets.
- So the prices run above the outcomes, one way, and not as scatter.
- The exception moves. It is the top bin in the main set and bin 0 without the filter.
- The off bins also move: 0, 1, 6, 7, 8 become 6, 7, 8, 9.

### A3. Largest gap as the only size reading (major)

- Location: `main.tex` 92, 356, 608. `README.md` 43, 66. Report Table 1, Step 4 "How to read".
- Fact: no prereg line defines "small" (`prereg_mvp1.md` 18 to 26).
- Fact: the paper states the one-way direction (93, 384, 607).
- Fact: README and report do not state it. Report Table 8 shows signs, with no sentence.
- Fact: mean price 0.3757 against Yes rate 0.3658 is a net gap of 0.99 points. Both numbers are printed, and no text joins them.
- Fact: bin 7 has the largest gap in points. Bin 0 has the largest chi-square share, 21.3 of 68.0 (§7).
- Fact: the gap is bounded by price. In bin 0 it cannot pass 1.8 points downward, and 38% of markets sit there.
- Fact: per dollar of price, payout shortfall is 25% (bin 0), 15.5% (bin 1), 4.4% (bin 7) (§7).
- Judgment: the largest gap is a true number, but the wrong sole reading.
- Judgment: a maximum cannot show direction or count. "Small" in points is not small in relative terms for cheap bins.
- Judgment: "small" is a post-result word with no line. It should say so.
- Fix owner: owner picks the wording. `sonnet-writer` edits the paper and README. `developer` edits `make_report.py`.

| Option | Change | Gain | Cost |
| --- | --- | --- | --- |
| A | Add one sentence: prices sit above outcomes in 9 of 10 bins, net 0.99 points | Direction and size in one line, from the mean only | Adds a derived number. A saved script must produce it |
| B | A plus a shortfall column (gap / mean price) in Table 8 and `tab:bins` | Shows cheap bins fairly | Wider table. Low-price ratios are noisy |
| C | Keep "small", add "in percent points, with no size line set before the results" | Fewest edits | Direction still missing from README and report |

### A2. Longshot claim over-reaches (major)

- Location: `main.tex` 395, 396, 609, 680. Abstract has no longshot line.
- Fact, filter: without the minimum-trade filter, bin 0 is +0.05 points and bin 1 is -0.93 points. Neither is off (`q1_bins_no_min.csv`).
- Fact, disclosure: report Tables 10 and 12 show this. The paper (421) says only that chi-square also rejects. README shows no bin detail.
- Fact, range: bins 6, 7, 8 are also below price. Their YES price is high, so these are the favorites.
- Fact, complement: bin 7 YES at 0.746 happens 0.713 of the time. So No, near 0.254, happens 0.287 of the time.
- Judgment: "Cheap bets pay off less" fails for that cheap No leg, if No trades near 1 minus YES.
- Judgment: the data shows Yes overpriced across the range. That is not a longshot-only pattern.
- Judgment: "matches the horse-racing direction" is true for the two cheapest Yes bins only.
- Not verified: Snowberg and Wolfers also report favorites winning more than priced. That comes from memory. `researcher` should confirm it before any sentence uses it.
- Fix owner: owner, since the interpretation `\todo` at `main.tex` 610 is open. `sonnet-writer` applies it.

| Option | Change | Gain | Cost |
| --- | --- | --- | --- |
| A | "Cheap Yes legs pay off less in the main set. The gap disappears without the filter" | True to the saved numbers | Weaker headline |
| B | A plus "favorite Yes bins also sit below price, so this is not longshot-only" | Reads the full pattern | Needs owner words (`book.md` principle 13) |

### A9. Robustness wording (minor)

- Removing 47 of 47,948 markets drops one off bin, 5 to 4 (`report_r1_split_payout.md`). So bin calls are fragile. I did not read which bin.
- `main.tex` 562 explains "equal rows", and the two rows are not equal. No text reads the difference.
- Bin 8 is near the line: BH p 0.036, not off under Bonferroni.
- `main.tex` 132 promises an effect size next to every p-value. Lines 420 and 571 give p with no gap beside it.
- Judgment: the verdict is robust. Single bin calls are not. Say that.
- Fix owner: `sonnet-writer`.

### A10. Meaning of "Yes" cannot be checked here (minor, open)

- Fact: y = 1 when the winner equals the `outcome_seq = 1` label (`build_tables.py` 32, 33).
- Fact: Sports is 40.0% of kept markets (`numbers.tex`).
- Fact: no saved output lists label values, so I cannot say how many first labels are not "Yes".
- Judgment: A3 reads a bias of the first listed leg. "Yes" in the text assumes more than I can confirm.
- This data was not collected. I stop here. If the owner wants it, it is a cluster query. The main session decides.

## 3. Q2: where the z interval fails

| Bin set | Smallest n_yes, n_no | z interval state |
| --- | --- | --- |
| Main 10 bins | 249, 149 | Fine |
| No min filter | 550, 376 | Fine |
| Equal frequency, lowest | n_yes 1 | Fails. `z_low` is below 0 |
| Equal frequency, second | n_yes 6 | Weak |
| Equal frequency, top | n_no 24 | Weak |

### A11. Failure disclosed only in the prereg note (minor)

- Location: report Table 13. `main.tex` 422. `README.md` 122.
- Fact: lowest equal-frequency bin has 1 Yes in 4,795. `z_low` is -0.0002. Report Table 13 prints `[0, 0.0006173]`.
- Fact: its Wilson interval contains the price and binomial BH p is 0.129. Only z marks it off.
- Fact: report Table 13 gives 8 "yes" and no BH column. Paper and README give 7. Only `prereg_mvp1.md` §4 explains the gap.
- Fact: the Table 8 caption says ends are cut at 0 and 1. The Table 13 caption does not.
- Judgment: the main result is untouched. A reader comparing report and README sees 8 against 7.
- Fact: "same bins as BH" has thin margins. Bin 3 is inside by 0.0004 and bin 8 outside by 0.0027.
- Judgment: the agreement is an observation here, not a property. z is uncorrected and differs in its centre from the test.
- Dependency: the 7 comes from run 142140 and Table 13 from run 142082. `README.md` 265 keeps the hash comparison open.
- Fix owner: `developer` for Table 13. `sonnet-writer` for one sentence at `main.tex` 422.

| Option | Change | Cost |
| --- | --- | --- |
| A | Add BH p and call columns to Table 13, plus one note on the 1-Yes bin | Small edit, needs the v5 CSV as input |
| B | Note only, in the caption and at `main.tex` 422 | Reader still counts 8 in the table |

### A12. "Names" understates the change (minor)

- `main.tex` 277 and report Step 1 say "names" differ. A z interval is a different formula, with different ends.
- `README.md` 247 and 250 state it correctly.
- Fix owner: `sonnet-writer`.

### A8. Wilson left in the report (major)

- Location: report Table 11.
- Fact: bin 0 prints `[-0.006164, -0.002784]`. That equals `ci_low` and `ci_high` minus mean price in `q1_bins.csv`.
- Fact: Table 10, same bin, prints the z values `[-0.006263, -0.00289]`.
- Judgment: the size is tiny. But D-026 replaced Wilson and the method is not in lecture.
- Fix owner: `developer`. Table 11 in `make_report.py` (around 420) should read the z longshot rows in `lecture_numbers.json`.

## 4. Q3: the Lorenz picture, and a larger CCDF problem

### A1. CCDF tail is one straight chord (major)

- Location: `fig6_ccdf.png` in the report (Figure 9) and paper (`fig:lorenz`). Captions at `main.tex` 458 and report Figure 9.
- Fact: `q2_concentration.py` 140, 141 sorts volume ascending. It then picks 3,000 log-spaced positions from the low end.
- Fact: so points are dense at small wallets and sparse at large ones.
- Fact: the last gap skips the top 0.44% of makers and 0.47% of takers.
- Fact: Figure 9 shows the kink at those heights. The curve ends at 2/n, as the code predicts.
- Fact: the top 1% of wallets gets about 3 plotted points. Those wallets hold 86.1% and 75.9% of volume.

```
 log CCDF
 0.0044 + kink: last real plotted point before the top
        |\
        | \   one chord, no data drawn between the ends
        |  \
  2/n   +---\ second-largest wallet
        +------------------ log volume
```

- Judgment: the caption says "a long straight CCDF tail means a few wallets trade very large volumes". The straight part is made by the plot.
- Judgment: the chord connects two true points. So the figure is not false about those points, only about the shape between them.
- Judgment: the straight look also lends visual support to the power-law sentence (A5).
- Fix owner: `developer` for the drawing. Main session decides how it runs.

| Option | Change | Gain | Cost |
| --- | --- | --- | --- |
| A | Redraw with log-spaced ranks from the top | True tail shape | Needs `wallets.parquet`. Audit §3 sends that read to the main session. Else a cluster job |
| B | Keep the figure, change the caption: above the kink it is one chord, not measured shape | No new read | The best-known visual part stays uninformative |
| C | Mark the chord dashed from saved values | Honest look | Needs the same read for the kink location |

### A13. Lorenz picture (minor)

- Location: `main.tex` 313, 314, 458. Report Figure 10. `README.md` 80.
- Fact: points are x = 0, 0.80, 0.90, 0.95, 0.99, 1 (`lecture_numbers.py` 72).
- Judgment: a real Lorenz curve is convex, so each chord lies above it. Every segment understates concentration.
- Judgment: so the straight lines are not misleading on the claim. The error runs against it. The caption does not say so.
- Judgment: the 0.80 to 1 part, where the message lives, rests on measured points. The grey band is clear.
- Fact: "nothing was measured below 80%" is loose. `fig7_lorenz.png` drew the full curve from all wallets, and the numbers were not saved.
- Judgment: the caption is enough for honesty. It needs direction and one word changed.
- Fix owner: `sonnet-writer`, `developer` for the HTML caption.

| Option | Change | Cost |
| --- | --- | --- |
| A | Caption: "values below 80% were not saved. Straight lines lie above the true curve, so they understate concentration" | Small edit |
| B | A plus dashed lines for segments | Redraw from CSV. Allowed locally |
| C | Draw the full curve from `wallets.parquet`, no Gini | Best picture. Needs the parquet decision |

## 5. Q4: the 80/20 and power-law statements

Population, from code and manifest:

| Item | Value | Source |
| --- | --- | --- |
| Row | one wallet x role | `build_tables.py` 92 to 114 |
| Markets | kept markets only: 47,948 of 688,131 | `build_tables.py` 95, 98 |
| Trades | every trade in those markets, no time cut | `build_tables.py` 94 to 98 |
| Maker wallets | 581,435 | `q2_concentration.csv` |
| Taker wallets | 1,535,977 | `q2_concentration.csv` |
| Same address in both roles | two rows. Unique addresses not saved | `q2_concentration.py` 41 |
| Duplicate rows | kept | `manifest_q2_concentration.json` |

### A6. 80/20 sentence (major)

- Location: `main.tex` 94, 95, 426, 613, 681. `README.md` 26, 43, 50. Report Table 1.
- Supported: 98.9% and 98.0% against 80%, by role, inside kept markets. Direction is clear and D-024 sets it as descriptive.
- Over-reach 1: "do most of the trading" measures USDC volume only. Trade-count shares were not saved.
- Over-reach 2: "a few" is 116,287 makers and 307,196 takers at the top 20%. The top 1% is 5,815 and 15,360.
- Over-reach 3: the abstract (94) and answer (426, 613) omit "in the kept markets". Line 466 has it.
- Fact: kept markets hold about 13% of the dataset paper's $61 billion (§7). A wallet's rank uses only this part.
- Fact: post-close trades count, since no time cut applies. In the pilot they were 34.0% of volume.
- Fact: report says "after T - 1 day". Paper and README say nothing. The paper warns about these trades for price (206 to 211).
- Judgment: RQ2's title stays (D-024). The answer sentence should say "by volume" and "in the kept markets".
- Judgment: wallet against person is handled. The effect's direction is not measured, and the text claims none. That is right.
- Judgment: calling 86.1% against 84.1% a "pipeline check" says more than two different populations can. "Reference" already appears in the text. It is enough.
- Fix owner: `sonnet-writer`, `developer` for the report text.

| Option | Change | Cost |
| --- | --- | --- |
| A | "Yes by volume, in the kept markets", plus one limit line on post-close trades | Text only |
| B | A plus top 1% wallet counts in `tab:conc` | Derived from counts. Needs a saved script |
| C | Measure shares with post-close trades removed | Cluster job. Beyond MVP1 scope. Owner call |

### A5. Power-law sentence (major)

- Location: `main.tex` 469, 470, 503, 504. Report Table 1, Step 5. `README.md` 86, 88, 96.
- Fact: paper and report say "close to a power law". README says "we do not say wallet volume follows a power law".
- Fact: the paper relies on the KS p at 470. It says "we do not rely on them" at 504.
- Judgment: fitted parameters inflate p. So a rejection survives, and the two lines can be reconciled. The text does not do it.
- Fact: "close" has no line. D 0.024 is the only support.
- Fact: Figure 9's slope runs near 0.6 before the kink and near 1.3 after. The fit implies 0.788. This is read by eye (§7).
- Judgment: the tail bends. "Close" says more than D, with xmin fixed and lognormal not compared.
- Fact: the fit pools maker and taker rows (`q3_results.json` `notes`). Only report Step 3 says so. It is cited under Q2 as if wallet-level.
- Fact: README 88 labels 211,742 as "wallets". They are wallet x role rows.
- Fact: README 86 calls alpha "tail slope". `q3_describe.py` 41 is the density exponent. The CCDF slope is alpha minus 1.
- Fix owner: `sonnet-writer`, `developer` for the report text.

| Option | Change | Cost |
| --- | --- | --- |
| A | Use the README wording everywhere: alpha reported, KS rejects, we do not say it follows | Fewest words. Loses "close" |
| B | "D 0.024 on the top 10% of pooled rows, and we set no line for close" | Keeps the number. Adds a limit |

## 6. Q5 and Q6

### A4. Limits are not stated the same way (major)

| Limit | Report | Paper | README |
| --- | --- | --- | --- |
| Per-bin multiple tests | BH and Bonferroni, Table 7 | 291, 385, 386 | 53, 62, 63 |
| Independent markets | Step 1, Step 6. No direction | 650, 651. "p-values are optimistic" | **Absent** |
| Large n | Step 1: small effect, tiny p | 652: underflow only | 95: KS only. 66: "read the gaps first" |
| Scope to kept markets | Step 2 | 646 to 649 | 45 |

- Fact: only README lacks the independence limit, and it is the file a newcomer reads first.
- Fact: paper 652 gives underflow as the large-n issue. The real issue is that tiny gaps reach significance. Only the report says so.
- Judgment: paper 653 says "therefore read the effect sizes and the intervals first". z intervals use the same independence assumption, so they are also too narrow.
- Judgment: report Step 4 calls a gap "real but small". "Real" claims more than the optimistic p allows.
- Fact: no event-level count is saved, so the dependence size is unknown.
- Hand check: variance would need to grow about 3.7 times to lose the chi-square line (§7). This is not an estimate of the real factor.
- Fact: binomial(n, mean p) overstates variance when prices differ inside a bin. That works against the optimism. No text says so. `lecture_method_audit.md` row 1 notes the approximation.
- Fact: Welch and KS role tests compare groups that share addresses and trades. The stated limit covers markets only.
- Judgment: t 117.1 with p under 10^-300 beside a D of 0.057 is the large-n case, and the text does not read it.
- Fix owner: `sonnet-writer`, one shared limit block. The owner approves the wording.

| Option | Change | Cost |
| --- | --- | --- |
| A | One limit block, same sentences in all three | Three small edits |
| B | A plus a test by event group | New query. No event key was reviewed here. Owner call |

### A7. Compare sizes or not (major)

- Fact: `main.tex` 397, 398: "we do not compare their sizes".
- Fact: report under Table 11: "Compare the sign and the size, not the digits".
- Fact: bin 1 is -0.0230 ours against -0.0019 in the dataset paper. That is 12 times, on different units.
- Judgment: the paper is right. Per-market and per-trade gaps do not share a scale. Only the sign can be read.
- Fix owner: `developer` for `make_report.py`.

### A14. k-means after the removals (minor)

- Location: `main.tex` 324, 481, 482, 656, 657. Report Tables 17, 18.
- Fact: 324 announces a stability check. 656 says no agreement score is reported. No result appears.
- Fact: 657, "This does not make the clusters real", lost its referent when the ARI sentence left.
- Fact: SSB ratio 0.008 is printed with no reading. It means clusters barely differ on mean trade price.
- Fact: report Table 18 prints p 0.0010 with no floor note. The paper states the floor.
- Fact: report Table 17 says "wallets". They are wallet x role rows. The paper is correct at 478.
- Fact: paper 323, 477 say "elbow method". The K comes from a fixed chord rule, which only the report states.
- Fact: inertia falls smoothly, by 84,974, then 44,308, then 29,590. No sharp bend.
- Fact: median volume differs across clusters by construction, because volume is a feature.
- Judgment: the analysis is still honest. Paper 618 says it carries no claim, and no removed number leaks into a claim.
- Judgment: the dangling check is the one flaw. It implies stability evidence without showing it.
- Fix owner: `sonnet-writer`.

| Option | Change | Gain | Cost |
| --- | --- | --- | --- |
| A | Drop 324 and 656, 657 | Simplest. Removes the implied check | Stability goes unmentioned |
| B | Report the `cluster_z` x `cluster_robust` table from `q2_kmeans_sample.csv` | In lecture, CSV only | New output adds to the k-means share. The main session runs it |

### A15. The 1/10 limit (minor)

- Fact: `README.md` 235 cites 0.0974 and 0.0824. Those came from `review_mvp1_rq_r3.md` G14, before the D-026 removals.
- Estimate: the same text-character method now gives about 0.06. I counted the extracted text by eye. It is not for citation.
- Fact: by exhibit count it is 3 of 29 (Tables 17, 18, Figure 11), or 0.103.
- Fact: the paper's k-means text is about 3% of its source characters, also by eye.
- Judgment: within 1/10 by the only stated measure, characters. The owner's limit names no measure.
- Fix owner: main session measures and saves the number. README then cites that.

## 7. Hand checks

Done by hand from the named saved files. Not for citation. A saved script must produce any number before a deliverable uses it (`rules/answering.md` §3).

Source: `q1_bins.csv`.

| Bin | n | Chi-square share | Shortfall = gap / mean price |
| --- | --- | --- | --- |
| 0 | 18,209 | 21.3 | -25.1% |
| 1 | 2,703 | 11.3 | -15.5% |
| 2 | 2,543 | 1.4 | -4.0% |
| 3 | 2,769 | 3.6 | -4.9% |
| 4 | 3,859 | 2.4 | -2.7% |
| 5 | 4,240 | 0.6 | -1.1% |
| 6 | 2,553 | 8.7 | -4.3% |
| 7 | 2,301 | 13.1 | -4.4% |
| 8 | 2,133 | 5.8 | -2.2% |
| 9 | 6,638 | 0.0 | +0.0% |
| All | 47,948 | 68.0, saved 67.99 | |

Others:

- Net: 17,541 Yes against 18,016 expected, 475 short, 0.99 points.
- The net shortfall alone is about 6.6 SD. Its square is about 44 of the 68.0.
- Variance factor to lose the line: 68.0 / 18.31 = 3.7. The 18.31 is the df 10 value in `lecture_method_audit.md` §2.
- Volume share: maker mean x n is about 8.2 billion USDC, against $61 billion at `main.tex` 62.
- Plot gaps: 3,000 log-spaced positions give steps of 0.44% (maker) and 0.47% (taker) at the top.
- CCDF slopes are read from `fig6_ccdf.png` by eye, so they are rough.

## 8. Not checked

- Other figures against their code, except Lorenz, CCDF and calibration code.
- Which bin R1 drops.
- Every macro in `numbers.tex` against its source. I compared the ones this memo uses.
- Label values of `outcome_seq = 1` (A10).
- Whether No prices equal 1 minus YES in the kept markets (A2).

Terms (용어):

| English | 한국어 | Short meaning |
| --- | --- | --- |
| CCDF (complementary cumulative distribution function) | 여누적 분포 | Share of wallets above a volume |
| BH (Benjamini-Hochberg) | 거짓 발견율 보정 | Correction for many tests at once |
| z interval | z 구간 | Rate plus or minus 1.96 standard errors |
| Wilson interval | 윌슨 구간 | Another rate interval, outside the lectures |
| chord | 현 | Straight line between two curve points |
| SSB (between-group sum of squares) | 집단 간 제곱합 | Spread of group means |
| ARI (adjusted Rand index) | 군집 일치 지수 | Agreement of two clusterings, removed by D-026 |
| KS (Kolmogorov-Smirnov) | 분포 거리 검정 | Largest gap between two CDFs |
