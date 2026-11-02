# Final review before commit: MVP1 (2026-11-02)

- Reviewer: `reviewer` agent. Scope: MVP1 only (D-016).
- Trigger: the owner asked for a final check after the project-end fixes (D-029 to D-033).
- Inputs: saved outputs only. No parquet, no cluster, no code run. One LaTeX build in `papers/paper_mvp1/`.
- Diff base: the repository HEAD `fae4d7c` (2026-11-02 00:02). "Added lines" below means added since that commit.
- Marks: **Fact** is something I read or measured. **Judgment** is my reading of it.

## Verdict

**PASS. 0 blocker, 0 major, 14 minor. Nothing blocks a commit and push.**

One pre-commit action (not a blocker): do not stage `papers/paper_mvp1/main.xdv` and `main.synctex.gz` (minor 1). The known items (owner `\todo`, F5, split, hash compare, 999,999 note, D-015 cell and snapshot restore) stay with the main session as planned.

| Check | Result |
| --- | --- |
| 1 A1 to A15, G18 to G22 (20 items) | 13 fixed, 1 superseded (A13), 5 partly or open as minor (A9, A12, A14, A15, G20), 1 open by design (A10) |
| 2 Numbers against saved sources | PASS. Every macro `main.tex` uses (174), every report table I compared, the README tables and the feedback page equal the saved files |
| 3 Report, paper, README agree | PASS on content. One placement gap (minor 2) |
| 4 Feedback page | PASS. Counts 12 / 18 / 6+3+6+3 hold. Quotes exact. Sections exist. Figure 1 label is tight, no collision (minor 3) |
| 5 Figures | PASS. Pairs readable, text 7.7 pt at print size, captions match |
| 6 Build | PASS. Exit 0, XeTeX, 17 pages, 0 errors, 0 overfull, 0 underfull, 0 undefined, 4 `\todo{owner`, 16 of 16 figure files present |
| 7 Reproducibility and commit hygiene | PASS. All new files trackable. No secrets, no home paths. Two build products untracked and not ignored (minor 1) |
| 8 Style on new lines | PASS with 3 minor cell-level semicolon hits (minor 4) |

## 1. Project-end findings: state today

Sources: `analysis/review_project_end.md`. Line numbers are `papers/paper_mvp1/main.tex` unless named.

| ID | State | Where | Note |
| --- | --- | --- | --- |
| A1 CCDF chord | fixed | `main.tex` 499-500, 564-565. Report Figure 11. README 116 | Fact: `fig6_ccdf_top_sampled.png` from run 145892, ranks sampled from the top. Caption says the tail bends |
| A2 longshot over-reach | fixed | `main.tex` 421-432, 739-740, 816. README 77. Report 672 | Fact: "holds only with the filter" in all three. No-filter bins 0 and 1 printed with BH p |
| A3 "small" as sole reading | fixed | `main.tex` 98-102, 376-383, 734-738. README 72-75. Report 670 | Fact: 9 of 10 bins, net gap -0.99 points, 475 fewer Yes, "no size line set before the results". Numbers come from `lecture_numbers.json` `gap_direction` (a saved script, option A) |
| A4 limits not stated the same | fixed | `main.tex` 783-790. README 79. Report 90-91, 670-671 | Fact: independence covers p-values and z intervals in all three. Large-n line now "a tiny gap can give a tiny p-value" (788). Residual: placement in the paper, see minor 2 |
| A5 power law | fixed | `main.tex` 559-567. README 118-135. Report 85, 251 | Fact: "we do not say wallet volume follows a power law", KS rejects, fitted p too large, lognormal not compared, "wallet-role rows", alpha labeled as density exponent (README 122) |
| A6 80/20 scope | fixed | `main.tex` 103, 466-474, 744-751. README 46. Report 85 | Fact: "by USDC volume", "in the kept markets", "trades after T - 1 day", "trade-count shares were not measured" in all three |
| A7 compare sizes | fixed | Report Table 11 note (465) | Fact: "So we do not compare their sizes. We read only the direction, the sign." Matches `main.tex` 431-432 |
| A8 = G18 Wilson in report | fixed | Report Table 11 header "95% z interval of ours", values [-0.006263, -0.00289], [-0.03547, -0.0105] | Fact: equal to `lecture_numbers.json` `longshot.main_with_min_filter` `z_low_diff`, `z_high_diff` |
| A9 robustness wording | partly | `main.tex` 677-678, 419, 569-570 | Fact: "equal rows" is gone, chi-square 68.0 to 64.3 printed, gap sits next to each BH p. Judgment: no sentence says single-bin calls are fragile (5 to 4 bins off). Minor 5 |
| A10 meaning of "Yes" | open by design | none | Fact: needs a cluster query. Not collected. Not new |
| A11 z 8 vs BH 7 | fixed | `main.tex` 458-462. README 161. Report Table 13 and 666 | Fact: Table 13 now carries BH p and call from run 142140, and the note names the 1-Yes bin |
| A12 "names" understates | open | `main.tex` 286. Report 75 | Fact: both still say "names" differ. README 532 is correct. Minor 6 |
| A13 Lorenz picture | superseded | D-031, `wallet_lorenz_*.png` | Fact: full curve from run 145893, `lorenz_y_at_80` 0.0114 and 0.0199 |
| A14 k-means residue | partly | `main.tex` 338-344, 574-584, 750. Report Tables 17, 18 | Fact: the stability-check sentence and the dangling "does not make the clusters real" are gone. "Elbow method" became "a fixed rule on the elbow curve". Residual: report Table 17 column "Wallets" and caption "200,000 sampled wallets" are wallet-role rows (paper 575 is right). Report Table 18 prints p 0.0010 with no floor note. SSB ratio 0.008 has no reading. Minor 7 |
| A15 1/10 limit | acknowledged | README 276, PLAN 55 | Fact: README says "below the 0.100 limit, not remeasured after D-026". Not new |
| G18 | fixed | see A8 | |
| G19 snapshots | fixed | `git diff --stat -- runs/` is empty | Fact: the three snapshot files match HEAD. The D-015 cell still reads "not 6344" (1 hit), known, main session |
| G20 / F5 | known | `main.tex` | Fact: added lines over 15 tokens: lines 328 (16), 350 (17), 562 (16), and the `tab:prereg` effect-size cell (25 tokens, but two sentences of 12 and 8 words with `&` and `\\` counted). Known F5 row. README 372 claims the new lines keep to 15 words. Three lines contradict it. Minor 8 |
| G21 figure text size | fixed | D-033, `reports/figures/*.png` | Fact and arithmetic in §5 |
| G22 README source of 84.1% | fixed | README 91 | Fact: "Qin and Yang 2026, Table 5", no tex line number |
| G23 criteria table quotes z | open | README 529, `main.tex` 270 | Known from the project-end review, disclosed by the departure notes (README 532, paper 286-289). Minor 14, not new |
| G25 semicolons README 558 | open | README 558 | Minor 4 |
| G26 caption length | fixed in paper, open in report | `main.tex` 548. Report Figures 16, 17 | Report captions carry a third "outside the lectures" sentence. Minor 9 |
| G27 `00.runs.md` header | open | `00.runs.md` 4 | Still "Environment for all runs: ... `~/myEnvs/cs6330`". Minor 10 |
| G28 literal 80% | fixed | `main.tex` 548 | |

## 2. Numbers against saved sources

Method: I listed every `numbers.tex` macro that `main.tex` uses (perl over both files, 174 macros) and read each value against the run files. For the report I used the text extracted from the HTML. For the README, its own tables. For the feedback page, each number it prints.

| Document | Checked | Source | Result |
| --- | --- | --- | --- |
| `main.tex` via `numbers.tex` | 174 macros in use | `q1_results.json`, `q2_results.json`, `q3_results.json`, `tables_summary.json`, `verdicts.json`, `lecture_numbers.json`, `r1_results.json`, `r2_results.json`, `manifest_*.json`, `runs/145892_ccdf_v6/cluster_category_*.csv`, `runs/142140_q1eqfreq_v5/q1_bins_eqfreq.csv` | all equal to the printed digits. Examples: `QOneP` 1.1e-10 = 1.0834e-10. `GapNetYesShort` 475.2 = -475.237. `ChiTopShare` 31.3% = 0.31307. `ClusterCategoryGapObs` 6.7% = 13,482 / 200,000. `ClusterCategoryGapExp` 8.2% = 16,453.8 / 200,000. `ZIntervalEqFreqOutsideN` 8 = count of `price_outside` true. `QOneEqFreqBinsBh` 7 = `reject_bh` sum in the v5 CSV. `RobRTwoShareCrossing` 8.02% = 0.08019. `PilotShareVolumeAfterClose` 34.0% = 0.33970 |
| `reports/report_v1.html` | Tables 1 to 19, Figures 1 to 18 | same files | equal. Table 11 now prints z values (A8). Table 13 BH p and call from run 142140. Table 18 cell gap -0.0149 (0.0674 against 0.0823). Reproduce block: `make_report.py` sha 76826c4e9b1a and `lecture_numbers.json` `code_sha` a99f3b51abfd equal `shasum -a 256` of the working-tree files |
| `README.md` | Q1, Q2, Q3, power-law, robustness tables, Step 15 text | same files | equal. 1.08e-10, -0.0329 bin 7, 9 of 10, -0.99 points, 475, 31.3%, 86.1 / 75.9, 98.9 / 98.0, 1.788, 3,450, 211,742, 0.0239, 1.15e-105, 6,653.0 df 21, -1.49%, 7 and 8 bins, 47,901, 214.2 |
| `../tips/group_01/polymarket_feedback_answers_tips.html` | every number | `lecture_numbers.json`, `q2_results.json`, `tables_summary.json`, `r1_results.json`, `r2_results.json`, `report_r2_price_path.md`, `close_time_summary.json` (run 142041), `future_work/runs/142083_mvp2_full_v2r3/verdicts.json`, `report_q1b_deadline.md`, `report_q1a_category.md`, `q1c_binned.csv` | equal. Gap bars -0.46 to +0.03 equal `diff_obs_minus_price` x 100. Q1b 11,005, 0.0959 / 0.0702 (0.09588 / 0.07018), 0.0257 [0.0232, 0.0282], d 0.19. Q1a 3,203.8 df 7, V 0.258, Sports 72.18%, Crypto 94.75%. Q1c rho 0.226 [0.217, 0.235], deciles 0.0419 to 0.1641. R2 Sports median 0.020 and 20.67%, Crypto 0.004. Wallets 581,435 / 1,535,977, 14,103 / 101.2, 5,339 / 86.6 |

Figure files: the 14 PNGs that exist in both `reports/figures/` and `papers/paper_mvp1/figures/` are byte-equal (`cmp`). Twelve of them are new since HEAD in each folder. `fig4_calibration_z.png` and `lorenz_top_shares.png` were already tracked.

## 3. Do report, paper and README agree?

| Item | Report | Paper | README | Same? |
| --- | --- | --- | --- | --- |
| Q1 verdict sentence | Table 1, 668 | `\VerdictQOne` 373, 815 | 50 | yes, verbatim |
| Direction | 670: 9 of 10, Yes priced too high | 98-99, 376-378, 734 | 44, 72 | yes |
| Effect | -0.0329 bin 7, net -0.99 points, 475, "no size line" | 100-102, 379-383 | 61, 67, 73-74 | yes |
| Independence limit | Step 1 "How to read" (90-91) and Step 4 (670-671), beside the numbers | Limitations 783-790 only | 79, beside the Q1 table | content yes, placement differs (minor 2) |
| Longshot filter dependence | 672 | 421-430, 739-740 | 77 | yes |
| Q2 scope | 85: by USDC volume, kept markets, after T - 1 day, counts not measured | 466-474 | 46 | yes |
| CCDF bend | 85, Figure 11 | 500, 564-565 | 116 | yes |
| Power-law limits | 85, 251-252 | 559-567, 630-635 | 128-135 | yes. Only README has the D-027 future-work line, as D-027 asked |
| Cluster chi-square and effect size | Table 18 | 580-584 | 137 | yes: 6,653 df 21, cluster 2 Sports, 6.7% vs 8.2%, -1.49% |
| z 8 vs BH 7 | 666 | 458-462 | 161 | yes |

Specific question: the abstract (97) and Results (375) state p = 1.1e-10, and the independence caveat sits only in Limitations. Is that a reader-misleading gap?

- Fact: the abstract puts the effect size, the direction and "we set no size line" right after the p-value (98-102). Results does the same (376-383).
- Fact: the report and the README put the independence sentence beside the number. The paper puts it in Limitations, 400 lines later.
- Fact: the feedback page says exactly this (Step 5): "The caution sits in Limitations only."
- Judgment: not misleading enough to block. Limitations is the standard home for this caveat in IMRaD, and the effect size stands beside every p. But the three deliverables do not treat the caveat the same way, and A4 asked for one shared limit block. One clause after line 375, "The p-value assumes independent markets (\Cref{sec:limits})", closes the gap. Minor 2, reasoning, `sonnet-writer`, owner approves the wording.

## 4. Feedback page

- Fact: 12 posts in `01_mygroup.txt` (Amanda, Luis, Md, Ben, Yusuf, Victor, Siyi, Oscar, Hameem, Marcelo, Edgar, Robert). The page says 12.
- Fact: the "All 12 posts" table has 19 rows, 1 praise with no ask, so 18 asks. Status counts in the table: answered 6, partly 3, MVP2 6, not done 3. Sum 18. The header table and the SVG (bar widths 240 / 120 / 240 / 120 at 40 px per ask) agree.
- Fact: every discussion quote (27 distinct phrases) is a substring of `01_mygroup.txt`, including the curly apostrophe in "market’s". Checked by script.
- Fact: every paper quote in Step 5 is verbatim from `main.tex` 783-789, 794 and 710.
- Fact: the sections it cites exist: "Evaluation price and pre-registration" (211), "Filters and drop reasons" (179), "Market and wallet tables" (198), "Robustness" (654), "Limitations" (757), table "Calibration by price bin" (389).
- Fact: each "answered" row is backed by text: Amanda, Ben, Oscar, Marcelo by 213-228. Hameem by `tab:bins` (10 bins, gap and interval), 411-419. Robert by `tab:conc` 488-492 and 794.
- Judgment: the statuses are honest. "Partly" rows name the hole on the same row.
- Figure 1 SVG, "T = close_at": `<text x="610" y="40">` with the group's `text-anchor="middle"`, font 11 px, 12 characters at about 6.6 px each in a mono font, so the label spans about x 570 to 650, baseline y 40. The `close_at` tick is `<line x1="600" y1="40" ... y2="80">`. The tick top touches the label baseline at x 600, inside the label's span. Judgment: zero clearance but no glyph collision, since glyphs sit above the baseline and only the underscore in `close_at` (near x 633) reaches it. Tight. Minor 3: move the text to y 36.
- Note for the owner, not a finding: the page prints classmates' full names. The source txt is already tracked, so no new exposure. Memory says tips pages are Korean only (2026-10-27, 10-28). This page is bilingual with a toggle, default Korean. Owner call.

## 5. Figures

Font arithmetic. Text width = 8.5 in - 2 x 0.9 in = 6.7 in. A `0.49\linewidth` subfigure is 3.28 in.

| Figure | Pixels, dpi | Native width | Placed at | Scale | Font at print |
| --- | --- | --- | --- | --- | --- |
| `hist_price_p1d`, `hist_trade_size` | 1020 x 810, 300 | 3.4 in | 3.28 in | 0.965 | 8 pt x 0.965 = 7.7 pt |
| `wallet_dist_{maker,taker}_{count,volume}` | 1020 x 900, 300 | 3.4 in | 3.28 in | 0.965 | 7.7 pt |
| `wallet_lorenz_{maker,taker}` | 1020 x 1020, 300 | 3.4 in | 3.28 in | 0.965 | 7.7 pt |
| `qq_*_raw_log` | 2100 x 1170, 300 | 7.0 in | 6.7 in | 0.957 | 9 pt x 0.957 = 8.6 pt |
| `fig6_ccdf_top_sampled`, `fig4_calibration_z` | 900 px, 150 | 6.0 in | 6.7 in | 1.12 | above native |

- Fact: 8 pt and 9 pt come from `CHANGELOG.md` (D-033 row) and `manifest_q3_figs.json` `font: 9`.
- Fact: pages 10, 11, 12 rendered at 80 dpi. Pairs have equal heights and aligned tops. Legends sit above the axes, below the panel title. No overlap. Axes carry units.
- Fact: opened `hist_trade_size`, `wallet_dist_maker_volume`, `wallet_lorenz_maker`, `fig6_ccdf_top_sampled`, `qq_trade_size_raw_log`. The trade-size histogram title says 999,999 trades, and the subcaption (600) explains it (known).
- Fact: captions match content. Figure 6 and 7 "Why: the area is the share of wallets in (a) and the share of volume in (b)" matches the y labels. Figure 8 "Why: the height is the volume share of the lowest wallets" matches the axes. Figure 9 names both histograms. Figure 5 says the tail bends, and it does.
- Judgment: the CCDF bend is visible from about 10^6 USDC on. The tail from 10^3 to 10^6 is close to straight on the taker line, so "bends downward at the largest wallets" is the right wording.
- Report: the four `class="pair"` rows hold the same files. On an 860 px main column each image shows at about 424 px, so 8 pt at 300 dpi renders near 10 px CSS. Readable.

## 6. Build

Command from `papers/paper_mvp1/`: `latexmk -C`, then `latexmk -pdf -interaction=nonstopmode main.tex`. `.latexmkrc` routes `-pdf` to XeLaTeX.

| Item | Value |
| --- | --- |
| Exit | 0 |
| Engine | `This is XeTeX, Version 3.141592653-2.6-0.999998 (TeX Live 2026)` |
| Pages | 17 |
| `grep -c '^!' main.log` | 0 |
| Overfull | 0 |
| Underfull | 0 |
| undefined | 0 |
| Warnings | 0 after the standard package info lines |
| `grep -c 'todo{owner' main.tex` | 4. `pdftotext` finds 4 TODO boxes |
| `\figorbox` targets | 16 of 16 PNGs exist. No placeholder box in the PDF |
| Figure pages | 3, 4, 7, 8, 9, 10 (6, 7), 11, 12 (9, 10), 13, 14, 15 |

The build rewrote `main.pdf`, `main.aux`, `main.bbl`, `main.blg`, `main.fdb_latexmk`, `main.fls`, `main.log`, `main.out`, `main.synctex.gz`, `main.xdv`. Nothing else was edited.

## 7. Reproducibility before a commit

- Fact: `git status --short` lists 14 modified tracked files, 4 new scripts, 3 new job files, 3 new run folders, 12 new PNGs in each of two figure folders, and 2 build products.
- Fact: `git check-ignore` says none of the new PNGs, `reports/lecture_numbers.json`, or the new run files is ignored. `.gitignore` excludes `runs/**/*.parquet` and the per-market CSVs, and none of the three new runs holds those. Every file the report, paper and README cite is tracked or trackable.
- Fact: `wallet_dist_panels.png` is untracked in both figure folders and no deliverable prints it (0 hits in the report and in `main.tex`). It is the `make_report.py` fallback for the six singles. Trackable, and harmless either way.
- Fact: `papers/paper_mvp1/main.xdv` and `main.synctex.gz` are untracked and not ignored. `cs6344_group_01` is its own repository, so the parent `.gitignore` lines `*.xdv` and `*.synctex.gz` do not reach it. `git add -A` would commit them. Minor 1.
- Fact: new run manifests record host `sxm003`, 4 CPUs, job IDs 145892, 145893, 145897, source sha256 of their inputs, and wall time. No user name, no home path, no token. `grep` for `/Users/`, `/home/`, `hf_`, `ghp_`, `password`, `token=` over every file in `git status` returns nothing.
- Fact: team member names in `main.tex` and the README are by design (D-014). Classmate names appear only in the tips page, whose source txt is already tracked.
- Fact: `00.runs.md` rows 145892, 145893, 145897 name no partition, CPU count or env. The header sentence covers the old runs only. Row 145897 labels the code "q3-figs" while the manifest and CHANGELOG say "q3figs-v1". Minor 10.
- Fact: run folder provenance holds: `manifest_ccdf_redraw.json` `chi2_reproduced` true. `manifest_wallet_dist.json` `shares_match_q2_results` true. `manifest_q3_figs.json` counts 47,948, 999,999 of 1,000,000, 10,000 QQ rows per variable. `manifest_q3_figs.json` has no `wall_time_s`, unlike the other two. Cosmetic.
- Judgment: a reader can rebuild the report and the paper from the tracked files plus the two commands in README 315-316 and `papers/README.md`. The parquet inputs of the three figure runs stay on the cluster, and each manifest records their sha256.

## 8. Style on new lines

Checked with `git diff -U0` on every modified file and `grep` on every new file.

| Check | Result |
| --- | --- |
| Em dash `—` | 0 hits in added lines of `main.tex`, README, CHANGELOG, `00.runs.md`, PLAN, STATUS, the four new scripts, the three job files, the report prose, the feedback page prose |
| Semicolon | `main.tex`: 1, in the `S-PAPER-10` comment line (13). Report prose: 0 (the 24 hits are `&lt;` entities). README 558: the citation cell (G25, known). CHANGELOG: new cells on rows 15 and 17 join clauses with semicolons. `00.runs.md`: the new rows' Verdict cells ("none; chi2 reproduced"). STATUS: new lines use a semicolon between two clauses. DECISIONS and PLAN follow the `rules/docs.md` templates and are exempt. Minor 4 |
| "wallet" never "person" | No added line calls a wallet a person. The only "person" or "people" hits are disclaimers that deny it: report 791-792, 798; `ccdf_redraw.py` 6; `wallet_dist_figs.py` 5. PASS |

## Findings (14 minor)

| # | Severity | Finding | Fact or judgment | Owner |
| --- | --- | --- | --- | --- |
| 1 | minor | `papers/paper_mvp1/main.xdv` and `main.synctex.gz` are untracked and not ignored in this repository | Fact | main session: do not stage them, or add `papers/**/*.xdv`, `papers/**/*.synctex.gz` to `.gitignore` |
| 2 | minor | The paper states p at 97 and 375 with the independence caveat only at 784. Report and README put it beside the number | Fact, judgment on severity (§3) | `sonnet-writer`, owner approves the clause. Reasoning issue (A4 residual) |
| 3 | minor | Feedback page Figure 1: "T = close_at" baseline touches the tick top at y 40 | Fact from the SVG, judgment "no collision" | `sonnet-writer`: y 36 |
| 4 | minor | Semicolons in new cells: `main.tex` 13 (comment), CHANGELOG rows 15 and 17, `00.runs.md` rows 18-20, STATUS new lines, README 558 (G25) | Fact | main session for the living docs, `sonnet-writer` for `main.tex`. Implementation |
| 5 | minor | A9 residual: no sentence says single-bin calls move (5 to 4 bins off in R1) | Fact | `sonnet-writer`. Reasoning |
| 6 | minor | A12 open: `main.tex` 286 and report line 75 still say "names" differ. The z interval is a different formula | Fact | `sonnet-writer` (paper), `developer` (`make_report.py`). Reasoning |
| 7 | minor | A14 residual: report Table 17 "Wallets" column and "200,000 sampled wallets" are wallet-role rows. Table 18 p 0.0010 has no floor note. SSB ratio 0.008 has no reading in paper or report | Fact | `developer` (report), `sonnet-writer` (paper). Reasoning |
| 8 | minor | README 372 says the new lines of 2026-11-02 keep to 15 words. Three `main.tex` lines added since HEAD are longer: 328 (16), 350 (17), 562 (16). The `tab:prereg` effect-size cell is two sentences and is the known G20 item | Fact | `sonnet-writer`. Part of F5. Implementation |
| 9 | minor | Report Figures 16 and 17 captions have three sentences (the "outside the lectures" label). Paper Figure 8 is fixed | Fact | `developer` (`make_report.py`). Implementation (G26 pattern) |
| 10 | minor | `00.runs.md`: header still says "Environment for all runs ... `~/myEnvs/cs6330`" (G27). New rows 145892 to 145897 record no partition, CPUs (4) or env, which the G12 AC asks per run. Row 145897 code label "q3-figs" differs from the manifest "q3figs-v1" | Fact | main session. Documentation |
| 11 | minor | `main.tex` 380 prints `\GapNetYesShort` as 475.2 "fewer Yes outcomes". README says 475. A count should be an integer | Fact, judgment on form | `developer` (`make_paper_numbers.py` rounding). Implementation |
| 12 | minor | `PLAN.md`: the `[ ] → M4 Project-end review` row is unticked though `analysis/review_project_end.md` exists with a verdict and open items. The D-029 to D-033 work has no task rows. README 343 says the G17 note is "Open" while PLAN 122 closed it | Fact | `product-manager`. Hierarchy (H2 housekeeping, no missing line) |
| 13 | minor | `manifest_q3_figs.json` has no `wall_time_s`, unlike the two other new manifests | Fact | `developer`. Implementation, cosmetic |
| 14 | minor | G23 open: README 529 and `main.tex` 270 quote the criteria with "z interval" while the prereg says Wilson. Both carry a departure note | Fact, known from the project-end review | `data-analyst`. Reasoning |

Fix owners by class: implementation (1, 4, 8, 9, 11, 13) to `developer` or `sonnet-writer`. Reasoning (2, 5, 6, 7, 14) to `sonnet-writer`, `data-analyst`, owner approves wording. Hierarchy (12) to `product-manager`. Documentation (10) to the main session.

## Hierarchy check

- H1 trace: PASS. `PLAN.md` has the mission block. Every open task row tags a milestone. M1 line reads "cycle 2/2, plus one review the owner allowed (D-022); recovery 0/2". This final review is the owner's own request after the project-end review, not a gate cycle, so no counter moves. M4 "cycle 1/2; recovery 0/2". No `budget:` line.
- H2 decisions: PASS with minor 12. D-029 to D-033 cover the redraws, the returned chi-square, the full Lorenz and the layout. Each Why names a line (RQ2, RQ3, Constraints). Each cites the owner's words.

## MVP ladder

Not applicable. This is an analysis project with one phase (MVP1) and no mock/real split. M1 to M4 stand on their exit lines as the project-end review found.

## Not checked

- `future_work/` beyond the MVP2 numbers the feedback page cites.
- `CodeSetSha` 950ec496595b against `code.sha256` (not recomputed).
- Rendering the report HTML and the feedback page at 1040 px. The SVG judgment is from coordinates.
- Lecture decks themselves.
