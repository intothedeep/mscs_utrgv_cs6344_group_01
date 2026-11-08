# Gate review: MVP1 deliverables after review-fix round (D-038 to D-040)

- Reviewer: `reviewer` agent. Date: 2026-11-08. Cycle 1/2; recovery 0/2.
- Targets: `papers/paper_mvp1/main.tex`, `papers/course_report_mvp1/main.tex`, `reports/report_v1.html`, `tips/polymarket_paper_review_tips.html`.
- Run under review: `runs/150310_r3_review_fixes_v6/`. Prereg: `analysis/prereg_review_fixes.md` (aef0808). Code: 94f7ae6.
- Mode: report only. No file under review was edited. No analysis re-run.
- Deviation: JSON spot-checks ran as `python3 -I -c` over saved JSON only (seconds, one core), not as `OMP_NUM_THREADS=1 timeout 300 uv run python`. Same input class, lighter command. Stated here so the dispatcher sees it.

## Verdict

**PASS, with 2 major and 12 minor findings to fix before submission.**

- Why PASS: every blocking check holds. Both documents build clean on XeLaTeX (0 undefined, 0 Overfull, 22 and 2 pages). Every new number is a macro and matches the saved JSON. The Q1 verdict is unchanged. D-040 wording is in place. The 2026 nuance is stated correctly. No finding needs a re-run or changes a number.
- Why not clean: the paper contradicts itself on which methods are outside the lectures (F1), and the peer (a) caption reads the figure against the pre-registered test printed in the same paragraph (F2). Both are text fixes.
- Precedent: the M4 gate passed with 3 major and 17 minor findings (`PLAN.md` M4 line).

## Build

| Target | Engine | Pages | Undefined refs or cites | Overfull | Result |
| --- | --- | --- | --- | --- | --- |
| `papers/paper_mvp1/main.tex` | XeTeX (`.latexmkrc` `$pdf_mode = 5`) | 22 | 0 | 0 | PASS |
| `papers/course_report_mvp1/main.tex` | XeTeX | 2 | 0 | 0 (6 Underfull, not a criterion) | PASS |

- Command run: `latexmk -C && latexmk -xelatex main.tex` in each folder. `papers/README.md` documents `latexmk -pdf main.tex`. Both paths give XeTeX through `.latexmkrc`. Note only.

## Acceptance checks

| ID | Check | Result | Evidence |
| --- | --- | --- | --- |
| AC1 | Every number in `sec:res-review` and the course report is a `numbers.tex` macro from `--r3` | PASS | `sec:res-review` (main.tex 759-899) uses 54 `\RThree*` macros, the course report 6. No literal measured number in either (only design constants: `\NBins`, `\CiLevel`, `\DaysShort`, and the 80/20 reference) |
| AC1a | Spot-check of at least 8 macros against the run JSON | PASS (30 checked) | See table below |
| AC2 | Q1 verdict unchanged, new rows labelled sensitivity | PASS | `\VerdictQOne` = "Prices are not calibrated as a whole at this n." (numbers.tex:15, from `verdicts.json`). main.tex 763-765: "All checks are descriptive and add no verdict." `r3_gate.json` passed (n 47,948, chi2 67.99 rebuilt) |
| AC2a | Prereg aef0808 and code 94f7ae6 precede the run | PASS | aef0808 2026-11-07 22:31; 94f7ae6 2026-11-08 01:07:33; ledger run 01:07 to 01:29. `code.sha256` of the run matches `git show 94f7ae6:code/{r3_m1,r3_common,r3_build}.py` (5c3f8ad2…, 2b9dc9de…, 5f0eb8e5…). See F3 for a stale header |
| AC3 | D-040 wording: main result "outcome 1"; a Yes/No sentence in robustness | PASS (note F11) | main.tex 404 "So outcome 1 is priced too high." Yes/No sentence at 789: "In the Yes/No markets (n=30,112), Yes is priced above its observed rate." It sits in 5.5 "Checks requested in review", not in 5.4 "Robustness". Abstract and conclusion keep "outcome 1" (no Yes-bias rewording) |
| AC4 | 2026 period nuance | PASS | main.tex 889-890: chi-square does not reject (BH p = 0.105, n 26,688), net gap −0.65% with CI [−1.04, −0.25] excludes 0. JSON: `period_2026_p_bh` 0.10496, CI −0.01045 to −0.00253. `report_v1.html` Step 6 says the same |
| AC5 | Methods outside the lectures labelled | PASS with finding (F1) | Labelled at 312 (Lorenz), 794 (Wilson), 812 (cluster bootstrap chi-square), 850 (logistic calibration, skill score). But 312 says "All methods come from the CS 6344 course lectures, except the Lorenz curve", which the later labels contradict |
| AC6 | No em dash, no semicolon in new text, sentences ≤ 15 words where practical | PASS / minor (F6) | Em-dash grep (style.md §3): 0 hits in all four targets. Semicolons: 0 in 759-899 and in the report body (one in a `%` comment line). 7 sentences over 15 words in 759-899, 6 in the report body |
| AC7 | Captions "what. Why: …"; figures readable | PASS / minor (F4, F5) | All 7 new captions have "Why:" and a Source. Course report figures at 300 dpi, text about 7.5 pt, legible on the rendered page. Paper r3 figures print below 7 pt (F5). Fig 18 caption names a line that is not drawn (F4) |
| AC8 | `\todo` slots: 4 in paper, 2 in report | PASS | Paper: 185, 911, 925, 995. Report: 158, 159. Expected (book.md principle 13) |
| AC9 | Ledger `00.runs.md` has 150310 as ran | PASS | 00.runs.md:22, status **ran**, v6, prereg aef0808, "all stages ran, gate passed" |
| AC10 | HTML numbers match saved outputs; no stale "being redrawn" text | PASS / minor (F8, F13) | `report_v1.html` Step 6 numbers checked: M1 sides −2.62 / +0.34 pp, M3 each-market 74.59 [−1.28, −0.70], M4 13,372 / 142.7 USDC and rates 36.6 / 35.7%, dedup 1,926,484 rows, 47,809 kept, 281 changed, chi2 67.39, maker 86.12 → 85.95, taker 75.90 → 75.63, peer rows: all match the JSON. Tips page numbers (−1.20, −1.13, 1.57, 30,112, −1.32, 7 bins, 0.133, [−1.41, −0.58], 1,790.0 / 69.0, 292 / 17, 1.028, −0.089, 0.538, 63.4 / 83.4, 3.1%, −0.16 / −0.26 pp, 0.166, 0.105): match. No "being redrawn" text. One stale open item (F8). Note: `report_v1.html` M4 prints "median volume 13,372 / 142.7 USDC" (key `*_volume_usdc_median`, all trades) while the paper prints 1,790.0 / 69.0 (key `*_volume_before_T1d_median`). Both match the JSON, but the report line lacks the "all trades" qualifier, so the two deliverables show different "median volume" numbers |
| AC11 | `% src:` IDs resolve (source-citation skill) | PASS / minor (F14) | IDs used in 759-899: S-PAPER-8, S-PAPER-9. Both are rows of the file's source key (main.tex 4-14). The S-PAPER-9 definition does not name the new run or prereg (F14) |

### Macro spot-check (numbers.tex vs `runs/150310_r3_review_fixes_v6/`)

| Macro | numbers.tex | Saved value (file: key) | Match |
| --- | --- | --- | --- |
| `\RThreeMOneVwapNetGap` | −1.20% | m1_results.json rows.p_vwap.net_gap −0.012004 | yes |
| `\RThreeMOneVwapNetGapCiLow/High` | −1.50% / −0.91% | −0.014954 / −0.009054 | yes |
| `\RThreeMOneMidNetGap`, `\RThreeMOneMidN` | −1.13%, 37,446 | rows.p_mid.net_gap −0.011327, n 37446 | yes |
| `\RThreeMOneMeanHalfSpread`, `\RThreeMOneShareBoth` | 1.57%, 78.1% | mean_h 0.015702, coverage.share_S_both 0.78097 | yes |
| `\RThreeMOneGapWithinHalfSpread` | yes | side_line.gap_within_half_spread True | yes |
| `\RThreeMTwoYesNoN`, `\RThreeMTwoYesNoNetGap` | 30,112, −1.32% | m2_results.json yes_no_n 30112, yes_no_net_gap −0.013216 | yes |
| `\RThreeMTwoYesNoBinsBh`, `\RThreeMTwoOtherP` | 7, 0.133 | 7, other_p 0.13347 | yes |
| `\RThreeMThreeKOneNClusters`, CI | 16,161, [−1.41%, −0.58%] | m3_bootstrap.json proxies.k1_slug_stem 16161, −0.014093 / −0.005789 | yes |
| `\RThreeMThreeKOneChiSq`, `\RThreeMThreeKOneP` | 62.8, 1.1e-9 | x2_cl 62.833, p 1.05e-9 | yes |
| `\RThreeMFourKeptMedianVolumeBeforeDay` / Dropped | 1,790.0 / 69.0 | m4_results.json 1789.987 / 69.0006 | yes |
| `\RThreeMFourKeptMedianTrades` | 292 | kept_n_trades_median **292.5** | rounding, see F7 |
| `\RThreeMFourStaleNetGap` | −0.35% | stale_q1_net_gap −0.003538 | yes |
| `\RThreeMFiveA`, `\RThreeMFiveB` | −0.089, 1.028 | m5_calibration_fit.json a −0.08876, b 1.02767 | yes |
| `\RThreeMFiveSkill`, Brier, climatology | 0.538, 0.107, 0.232 | 0.53848, 0.10707, 0.23200 | yes |
| `\RThreeMFiveMaxAbsDelta`, practical / grid | 2.22%, 0 / 7 | max abs delta 0.022175, practically_sized 0 of 7 | yes |
| `\RThreeMinorFourDupShare`, Removed, ChiSq, NetGap | 3.1%, 139, 67.4, −0.99% | minor4_dedup.json 0.030567, 139, 67.391, −0.009870 | yes |
| `\RThreeMinorFourMakerTopOneDeltaPp` | −0.16 | q2.maker.top1_share.delta_pp −0.1643 | yes |
| `\RThreePeerACutLowMid` / MidHigh | 498.5 / 6,207.4 | peer_a_results.json 498.5085 / 6207.447 | yes |
| `\RThreePeerADiff`, CI, p | 0.71%, [0.01%, 1.40%], 0.046 | high_vs_low diff 0.007067, 0.000130 / 0.014004, p 0.04586 | yes |
| `\RThreePeerAHighBhP`, High CI high | 0.166, 0.03% | tercile_high_p_bh 0.16601, ci_high 0.000269 | yes |
| `\RThreePeerBPeriodThreeBhP`, NetGap, CI, N | 0.105, −0.65%, [−1.04%, −0.25%], 26,688 | peer_b_results.json 0.10496, −0.006491, −0.010448 / −0.002535, 26688 | yes |
| `\RThreePeerBPeriodOneN` / TwoN | 3,444 / 17,816 | 3444 / 17816 | yes |

## Hierarchy check

| ID | Check | Result | Evidence |
| --- | --- | --- | --- |
| H1 | Mission block, milestone trace, counters | PASS | `PLAN.md` 7-17: mission block present. M4 line "cycle 1/2; recovery 0/2" matches the dispatch. No `budget:` line |
| H2 | Decisions logged with Why | PASS | D-038 (owner's words 2026-11-07), D-039 (owner's answers), D-040 (owner picks "둘 다 쓰기", 2026-11-08) in `DECISIONS.md` 44-46, each with Why and the dropped alternatives |

MVP ladder (L1 to L4): not applicable. The targets are documents from saved runs, no mock or pipeline slice.

## Findings

### Major

**F1. The paper contradicts itself on which methods are outside the lectures.** Reasoning issue → `data-analyst` (text), and `product-manager` for the D-039 count.
- `papers/paper_mvp1/main.tex:312`: "All methods come from the CS 6344 course lectures, except the Lorenz curve, which is outside the lectures."
- Same file: 794 "The figure uses Wilson intervals, which are outside the lectures." 812 "The cluster bootstrap chi-square is outside the lectures." 850 "Logistic calibration and the skill score are outside the lectures."
- `analysis/prereg_review_fixes.md` §8 marks cluster chi-square, Brier, Brier skill score as "not found", Welch t, cluster resampling, logistic calibration use as "partly".
- D-039 says "keep the two methods outside the lectures with a label". The paper labels five (Lorenz, Wilson, cluster bootstrap chi-square, logistic calibration, Brier skill score). The tips page (Step 4) names two (bootstrap chi-square, Brier skill score).
- The mission line (`PLAN.md:8`) says "only methods from our lectures". A reader of 312 takes the whole paper as in-lecture, which the review section itself denies. One sentence at 312 needs to list every labelled method, or point to 5.5. D-039 should state the same count.

**F2. The peer (a) caption reads the figure against the pre-registered difference test printed in the same paragraph.** Reasoning issue → `data-analyst`.
- `main.tex:882` (`fig:r3-peer-a`): "Why: overlapping intervals mean no sign that the gap changes with volume."
- `main.tex:876` prints the pre-registered Welch test (prereg §7.1 "High vs low"): high minus low 0.71%, CI [0.01%, 1.40%], p = 0.046. Saved: `peer_a_results.json` high_vs_low diff 0.0071, ci 0.00013 to 0.0140, p 0.0459. The CI excludes 0, so "no sign" contradicts the paper's own number.
- `reports/report_v1.html` Figure 24 caption reads the same figure the other way: "Why: the net gap is smaller in the most traded markets."
- The paper may stay descriptive (D-038), but the caption's reading rule must not contradict the printed test. Either name the difference test in the caption, or make the Why neutral ("Why: it shows whether the gap moves with volume").
- Peer (b) is different and is a minor (F11b): no difference test was pre-registered (prereg §7.2), so the paper caption at 896 ("no sign that the gap changes with the period") is a defensible descriptive reading. There the report caption is the one that over-reads.

### Minor

**F3. Prereg file and run manifest still say DRAFT and "not approved".** Implementation issue → `product-manager` (living doc) or `developer` (manifest text).
- `analysis/prereg_review_fixes.md:1-4`: "Pre-registration DRAFT", "Not yet a committed prereg", "Decision: pending." It is committed (aef0808) and logged (D-039).
- `runs/150310_r3_review_fixes_v6/manifest_r3_build.json:33` and `prereg.json`: `decided_by: "system-architect draft, 2026-11-07. Not approved. DECISIONS.md row pending"`.
- The paper (393, 762) and `report_v1.html` cite this file as the fixed prereg. The commit order proves the timing (AC2a), but the file's own header denies it. Do not edit the run folder (measurement.md §2.3 immutability). An amendment note at the top of the `.md`, dated, is enough.

**F4. Figure 18 caption names a practical line that the figure does not draw.** Implementation issue → `developer` (`code/fig_r3_paper.py`) or `sonnet-writer` (caption).
- `main.tex:856`: "Implied gap between the fitted probability and the price, against the practical line." The rendered figure (page 19) shows only the "Calibrated" 0 line and the bootstrap bands. No ±1.57% line.
- `report_v1.html` Figure 23 caption says "how it compares with zero", which matches the figure.

**F5. Paper r3 figure text prints below 7 pt.** Implementation issue → `developer`.
- `code/fig_r3_paper.py` uses matplotlib default 10 pt at figsize 8 × 4.4, 7.5 × 4.4, 6 × 6 in, saved at 150 dpi. `main.tex` prints them at 0.8\linewidth (about 5.2 in) and 0.55\linewidth (about 3.6 in). Scale 0.65 to 0.69 → about 6.5 to 6.9 pt; the 6 × 6 figure at 0.55\linewidth → about 6 pt. `rules/figures.md` §4 asks for 7 pt or more. Pages 16 to 20 confirm small tick labels.
- The course report figures are fine: drawn at 300 dpi at their print width (`code/q3_figs_single.py` FONT_HALF; `fig4_calibration_gap_half` 1226 px = 4.088 in at 300 dpi).

**F6. Sentences over 15 words in new text.** Style issue → `sonnet-writer`. "Where practical", so minor.
- `main.tex`: 762 (16), 773 (21), 790 (18), 806 (16), 811 (16), 864 (16), 890 (17).
- `course_report_mvp1/main.tex`: 64 (21), 67 (18), 98 (17), 117 (22), 124 (18), 132 (18).

**F7. A median of 292.5 prints as 292.** Implementation issue → `developer` (`code/make_paper_numbers.py` format rule).
- `m4_results.json` `kept_n_trades_median` = 292.5. `\RThreeMFourKeptMedianTrades` = 292 (numbers.tex:1003). The paper (828) and the tips page say 292. The integer rule drops the half. Either print 292.5 or state the rounding in the macro comment.

**F8. Tips page lists the half-width redraw as open after saying it is done.** Implementation issue → `sonnet-writer`.
- `tips/polymarket_paper_review_tips.html:280` "Open: … the half-width redraw of the 2-page report figures". Lines 187 and 234 say the figures are redrawn for half width. Stale open item.

**F9. Course report status column uses synonyms.** Style issue (style.md §2 "용어 고정") → `sonnet-writer`.
- `course_report_mvp1/main.tex:140-152`: Answered, Done, In part, Partly, Outside. "Done" and "Answered" mean the same. "In part" and "Partly" mean the same. Pick one term each.

**F10. Course report captions have no Source folder.** Rule conflict, owner's call. Not blocking.
- `course_report_mvp1/main.tex:75, 115, 122`: captions end after "Why: …". `rules/figures.md` §3 asks for a source folder at the caption end. `rules/writing/paper.md` lets the venue format win, and the memory note "No paths in hw reports" points the other way for course submissions. The owner decides which rule this 2-page report follows.

**F11. D-040 sentence placement.** Note only, no action unless the owner wants it in 5.4.
- D-040 says "add one sentence in the robustness section". The sentence is in 5.5 "Checks requested in review" (789), which is the robustness v3 section. 5.4 "Robustness" (683-758) holds R1 and R2 only.

**F11b. The peer (b) report caption claims a trend with no test behind it.** Reasoning issue → `data-analyst`.
- `reports/report_v1.html` Figure 25: "Why: the net gap shrinks in the newest period." Prereg §7.2 registers per-period rows and BH over the three chi-square p-values, no trend test. D-038: descriptive, no verdict. The paper caption (896) is neutral. Make the report caption match the paper, or state what the trend claim rests on.

**F12. "Yes/No markets" names two different sets.** Style issue (style.md §2 "용어 고정") → `sonnet-writer`.
- `course_report_mvp1/main.tex:63`: "Of 688,131 Yes/No markets in scope we keep 47,948" (all binary markets). Line 105: "Yes/No markets (n=30,112)" (the subset whose outcome labels are literally Yes and No).
- `paper_mvp1/main.tex:96, 161, 987` use the first sense; 789, 793, 799 use the second. A grader of the 2-page report sees 688,131 and 30,112 under one name. Rename one set, for example "binary markets" for the first or "markets labelled Yes/No" for the second.

**F13. Proxy key count differs between the paper and the report.** Implementation issue → `sonnet-writer`.
- `paper_mvp1/main.tex:805`: "we use two proxy keys" (k1, k2). `reports/report_v1.html` Step 6 M3: "Three proxy keys group the markets" (it counts k0 each-market as a key). Same data, one sentence disagrees. Pick one count and say that k0 is the no-cluster row.

**F14. The paper's source key was not extended for the new section.** Implementation issue (source-citation skill) → `sonnet-writer`.
- `paper_mvp1/main.tex:4-14` is the Sources table of the file. Every `% src:` ID in 759-899 resolves (S-PAPER-8, S-PAPER-9), so no dangling ID.
- But `S-PAPER-9` is defined as "analysis/prereg_robustness.md, runs/142123_robust_full_v4 (reports r1, r2)". The new section's facts come from `analysis/prereg_review_fixes.md` and `runs/150310_r3_review_fixes_v6`. Neither is in the key. Add an ID (for example S-PAPER-12) and point the new section's `% src:` comments at it. IDs are never renumbered (skill rule).

## Not found (checked, clean)

- Em dashes: 0 in all four targets.
- Semicolons in new prose: 0.
- Undefined references or citations: 0 in both logs.
- Overfull boxes: 0 in both logs.
- "being redrawn" or placeholder text in the two HTML pages: 0.
- Abstract, discussion and conclusion keep "outcome 1". No Yes-bias rewording (the D-040 rejected option).
- Figure captions: every new figure has "Why:" and a Source. Every float is `[H]` with `\caption` then `\label`.
- `% src:` IDs in the new section resolve to the file's source key (see F14 for the stale definition).
- Run code hashes match commit 94f7ae6.

## Routing summary

| Finding | Class | Route |
| --- | --- | --- |
| F1 | reasoning | `data-analyst` (sentence 312), `product-manager` (D-039 count) |
| F2, F11b | reasoning | `data-analyst` |
| F3 | implementation (living doc) | `product-manager` |
| F4, F5, F7 | implementation (figure script, number format) | `developer` |
| F6, F8, F9, F12, F13, F14 | implementation (text, source key) | `sonnet-writer` |
| F10, F11 | owner's call | main session asks the owner |

---

# Cycle 2 (cycle 2/2; recovery 0/2)

- Date: 2026-11-08. Target: the uncommitted working tree after the F1 to F14 fixes (D-041).
- Mode: report only. JSON reads via `OMP_NUM_THREADS=1 timeout 300 uv run python`.




## Verdict (cycle 2): **PASS**

- 14 of 14 cycle-1 findings closed. Two small residues and one new minor remain (C2-1 to C2-3 below). None needs a re-run, changes a number, or touches the Q1 verdict.
- No regression: both builds clean, numbers match the JSON, 22 and 2 pages, `\todo` 4 + 2, em dash 0.

## Build (cycle 2)

| Target | Engine | Pages | Undefined | Overfull | Result |
| --- | --- | --- | --- | --- | --- |
| `papers/paper_mvp1/main.tex` | XeTeX | 22 | 0 | 0 | PASS |
| `papers/course_report_mvp1/main.tex` | XeTeX | 2 | 0 | 0 | PASS |

Command: `latexmk -C && latexmk -xelatex main.tex` in each folder, on the uncommitted working tree.

## Per-finding status

| Finding | Status | Evidence |
| --- | --- | --- |
| F1 methods outside the lectures | closed | `main.tex:313-314` lists five methods (Lorenz, Wilson, cluster bootstrap chi-square, logistic calibration, Brier skill score) and says all other methods come from the lectures. Labels at 356, 510, 799, 820, 859 unchanged. `DECISIONS.md:47` D-041 corrects the D-039 count to five. Tips Step 4 lists the same five. Residue: C2-2 |
| F2 peer (a) caption vs Welch test | closed | `main.tex` `fig:r3-peer-a` caption: "Why: the pre-registered difference test compares the high and low terciles, with high minus low 0.71% (CI [0.01%, 1.40%], p = 0.046)." Rendered page 20 confirms |
| F3 prereg DRAFT header | closed | `analysis/prereg_review_fixes.md:3` amendment note (2026-11-08): committed as the fixed prereg in aef0808, before 94f7ae6 and run 150310 (D-039); the DRAFT lines kept as pre-commit text. Run folder untouched |
| F4 practical line in Fig 18 | closed | `code/fig_r3_paper.py` draws ±`mean_h` from `m1_results.json` (dotted, in the legend). Rendered page 19 shows both dotted lines and the legend entry "Practical line: ± mean half spread". `report_v1.html` Figure 23 caption names the line (± 1.57 pp) |
| F5 figure text below 7 pt | closed | `fig_r3_paper.py`: `W_WIDE = 0.8 × 6.7 in`, `W_NARROW = 0.55 × 6.7 in`, `FONT_PT = 7.5`, `DPI = 300`. `main.log` textwidth 484.2 pt = 6.7 in, so print scale is 1:1. PNGs 1608 px = 5.36 in at 300 dpi, 1105 px = 3.685 in. `papers/paper_mvp1/figures/fig_r3_*.png` are byte-identical to `runs/local_r3figs_v12/` (cmp on m1, m5, peer_b). Pages 16 to 20: tick labels legible |
| F6 sentences over 15 words | closed, one residue | Paper 759-910: 1 left (C2-1). Course report body: 0 left (lines flagged by the per-line count hold two sentences each) |
| F7 median 292.5 | closed | `numbers.tex:1003` `\RThreeMFourKeptMedianTrades` = 292.5; JSON `kept_n_trades_median` 292.5. Paper page 18 "292.5 against 17". Tips page 292.5 (4 places) |
| F8 stale open item in tips | closed | Tips line 280 "Open:" now lists the `\todo` lines, a real event ID, the presentation slide. The half-width redraw item is gone |
| F9 status synonyms | closed | Course report status column: Answered ×4, Partly ×2, Outside ×1 |
| F10 captions without source folder | closed by decision | D-041: the 2-page report keeps captions without source folders (memory "No paths in hw reports") |
| F11 D-040 sentence placement | closed by decision | D-041: the sentence stays in the review-checks section |
| F11b report peer (b) caption | closed | `report_v1.html` Figure 25: "Why: it shows whether the gap moves across close periods." Neutral, matches the paper (`fig:r3-peer-b` caption unchanged) |
| F12 "Yes/No markets" two senses | closed | Subset is now "markets labelled Yes/No" in the paper (793, 798, 804), the course report (107), the report HTML (M2 heading, text, caption) and the M2 figure legend. "Yes/No markets" is kept only for the binary set (paper 97, 162, 998; report 63) |
| F13 proxy key count | closed | Paper 811-812: "two proxy keys" plus "The reference row k0 treats each market alone, with no cluster, and is not a key." `report_v1.html` M3: "Two proxy keys (slug stem, topic x close hour) … The each-market row has no clustering." Figure 21 caption: "the each-market row and two proxy keys" |
| F14 source key | closed | `main.tex:15` adds `S-PAPER-12 analysis/prereg_review_fixes.md (commit aef0808), runs/150310_r3_review_fixes_v6 via numbers.tex`. The new section's `% src:` lines use S-PAPER-12 (8) and S-PAPER-8 (2); S-PAPER-9 no longer appears there |

## Regression checks (cycle 2)

| Check | Result | Evidence |
| --- | --- | --- |
| RThree macros vs JSON | PASS | 15 macros re-read with `OMP_NUM_THREADS=1 timeout 300 uv run python` (script in the scratchpad, reads saved JSON only): VWAP net gap −1.20 / −0.012004, mean h 1.57 / 0.015702, Yes/No n 30,112, Yes/No net gap −1.32 / −0.013216, k1 CI low −1.41 / −0.014093, kept median trades 292.5 / 292.5, kept median volume 1,790.0 / 1789.987, b 1.028 / 1.02767, skill 0.538 / 0.53848, max delta 2.22 / 0.022175, dedup chi2 67.4 / 67.391, peer diff 0.71 / 0.007067, p 0.046 / 0.04586, 2026 BH p 0.105 / 0.10496, 2026 CI high −0.25 / −0.002535. 115 `\RThree*` macros, same count as cycle 1 |
| Q1 verdict, D-040 wording, 2026 nuance | PASS | `\VerdictQOne` unchanged. Page 20: "In 2026 the chi-square test does not reject (BH p = 0.105, n = 26,688). … Its 95% CI [−1.04%, −0.25%] excludes 0." Course report page 1: "Markets labelled Yes/No (n=30,112): Yes is priced above its observed rate" |
| Em dash | PASS | 0 in the four targets |
| `\todo` | PASS | 4 (paper) + 2 (course report) |
| Course report layout | PASS | 2 pages, rendered: three figures legible, feedback table complete, TODO slots red, references on page 2 |
| `report_v1.html` at 1040 px | PASS | Headless Chrome screenshot, 1040 × 32000. No horizontal scroll, no overlap. Step 6 uses the v12 figures (`runs/local_r3figs_v12/…` in every figure source line), the practical line is drawn in Figure 23, Figure 24 caption states the Welch test, Figure 25 caption is neutral, M4 says "Median volume over all trades" |
| Tips page at 1040 px | PASS | Headless Chrome screenshot, 1040 × 3000 (top). No horizontal scroll, no overlap. Table cells and open-item colouring render |
| Ledger | PASS | `00.runs.md:22` unchanged, 150310 **ran** |
| H1, H2 | PASS | D-041 row has Why ("owner's go, 2026-11-08") and the dropped option ("Leave the minors open"). PLAN M4 counters unchanged |

## Remaining findings (cycle 2)

**C2-1 (minor, residue of F6).** `papers/paper_mvp1/main.tex:812` "The reference row k0 treats each market alone, with no cluster, and is not a key." 16 words. → `sonnet-writer`, if wanted.

**C2-2 (minor, residue of F1).** `reports/report_v1.html` Step 6 banner: "Logistic calibration, Brier skill score and the cluster bootstrap chi-square are outside the lectures (D-039)." Figure 20 of the report uses "95% Wilson intervals" with no label. The paper (313) and D-041 now count five methods. The report banner names three. One sentence, `code/make_report.py`. → `sonnet-writer` or `developer`.

**C2-3 (minor, new).** `papers/paper_mvp1/main.tex:76` `\newcommand{\RThreeFigRun}{local\_r3figs\_v10}`. The seven r3 figures in `papers/paper_mvp1/figures/` are now byte-identical to `runs/local_r3figs_v12/`, and `runs/local_r3figs_v12/README.md` says "Used in papers/paper_mvp1/figures/". Every r3 caption therefore prints "Source: runs 150310_r3_review_fixes_v6 and local_r3figs_v10" (pages 16 to 20), which is the old folder. One macro value. → `sonnet-writer`.

Not re-flagged: `fig:r3-peer-b` caption keeps "overlapping intervals mean no sign that the gap changes with the period" (no difference test was pre-registered for periods, prereg §7.2; defensible as descriptive).

## Routing (cycle 2)

| Finding | Class | Route |
| --- | --- | --- |
| C2-1, C2-3 | implementation (text, macro value) | `sonnet-writer` |
| C2-2 | implementation (report generator text) | `sonnet-writer` or `developer` |

## Cycle 2 addendum (after advisor review)

| Check | Result | Evidence |
| --- | --- | --- |
| `numbers.tex` regenerated, not hand-edited (F7) | PASS | Ran the documented command (`papers/README.md`) with `OMP_NUM_THREADS=1 timeout 300 uv run python code/make_paper_numbers.py … --r3 runs/150310_r3_review_fixes_v6 --out <scratchpad>/numbers_check.tex`: 574 macros. `diff` against `papers/paper_mvp1/numbers.tex`: identical. The rule change is one helper `median_count()` in `code/make_paper_numbers.py` ("keep the half (292.5), never round it away"), applied to `RThreeMFour*MedianTrades` and `Cluster*Median*`. Only one macro value changed, so the other medians were whole numbers |
| Tips page at 1040 px, full height | PASS | Headless Chrome 1040 × 12000, cropped. Steps 3 and 4 render: five outside-lecture methods, the k0 note, 292.5, the trimmed "Open" line. No horizontal scroll, no overlap. The cycle 2 regression row "Tips page at 1040 px" above covered the top 3000 px only; this row completes it |

C2-3 framing: it is a regression introduced by the fix round, not a leftover. Before the fix the figures and the macro both said v10. After the fix the seven PNGs are v12 copies while `\RThreeFigRun` still prints v10, so every r3 caption points the reader at a folder whose files no longer match the printed figure. One macro value (`main.tex:76`) fixes all seven captions. Severity stays minor.
