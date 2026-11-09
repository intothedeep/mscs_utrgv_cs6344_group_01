# Gate review PL-15: paper length restructure (D-042 to D-046)

Reviewer, 2026-11-09. Milestone M5. Cycle 1/2, recovery 0/2.
Build: copy of `papers/paper_mvp1` (without `x_base_d042`) in the session scratchpad `pl15_build/`, `latexmk -pdf main.tex` (XeTeX via `.latexmkrc`).
Course report: copy of `papers/course_report_mvp1` beside that copy, same command.
Baseline: `papers/paper_mvp1/x_base_d042` (22 pages).
Judged against the owner's later facts (D-045 two columns, numbered References section, appendix pages, Figure 3 split, Table 4 before Discussion, D-044 and D-046 tips scope), not the older plan text.

## Verdict

**PASS** (M5 exit criteria closed). Blockers: none. Majors: 2 (H2 decision-log Why column → `product-manager`; `paper.md` §3.3 run names, file paths and caption source lines → `sonnet-writer`). Minors: 8.

- Body pages **B = 7**. N = 8 (`REFPAGE`). `pdftotext -f 8 -l 8 | head -1` prints `9`, not `References`, because References is now numbered Section 9 (owner, 2026-11-09). The literal PL-13 rule would give B = 8. By inspection of page 8 (the heading "9 References" is its first line, page 7 ends with the Conclusion) B = 7. `STATUS.md` line 89 records B = 7.
- Pages: 21. Body p1 to p7, References p8, Appendix A p9, B p10, C p11, D p12, E p14, F p15, G p17. All match `main.aux`.
- Course report: 2 pages, `git status --short papers/course_report_mvp1/` empty.

## Shared checks (own build)

| Check | Result | Expected | Status |
| --- | --- | --- | --- |
| BUILD | exit 0, `Output written on main.pdf (21 pages)` | exit 0 | PASS |
| CLEAN | `^!` 0, Overfull 0, undefined 0, `??` 0 | four zeros | PASS |
| TODO | 5 | 5 | PASS |
| SRC | prints nothing | nothing | PASS |
| NUMDEL | 0 removed (32 lines added: 16 new macros) | 0 | PASS |
| figures/ git diff | quiet, exit 0; `*_half.png` unchanged; `*_col.png` tracked | exit 0 | PASS |
| FLOATH | 0 | 0 | PASS |
| MOVED | 12 lines, listed below | pointer lines only | PASS as superseded (each line attributed) |
| REFPAGE | 8 | | see B above |
| newlabel diff vs baseline | not applicable after PL-04 to PL-12 (new labels) | | n/a |

MOVED lines and their reason (none is a lost sentence):

| Baseline line (Cref stripped) | Now | Reason |
| --- | --- | --- |
| `\documentclass[11pt]{article}` | `[10pt,twocolumn]` | D-045 |
| `\usepackage[margin=0.9in]{geometry}` | `margin=0.7in` | D-045 |
| 3 `\figorbox{...}{\linewidth}` lines (calib, ccdf, qq) | new `_col` files at `\linewidth` | PL-12a redraw |
| `\caption{Observed outcome-1 rate ... (top) ... (bottom)...}` | two captions, 3(a) and 3(b) | owner's Figure 3 split |
| `\caption{CCDF ...}`, `\caption{QQ plot ...}` | same words, new source folder `runs/local_column_figs_v13` | PL-12a redraw |
| `\subsection{Checks requested in review}`, `\subsection{Robustness}` | `\section` in appendix files | appendix structure (PL-04, PL-05) |
| `... (after the amendment below) ...` (tab:prereg row) | `(after the amendment in \Cref{sec:methods-prereg})` | nearness wording, design §1.5 last bullet |
| `The two robustness checks in \Cref{sec:res-robust} speak to two limits.` | `... in this appendix speak ...` | F5 move into Appendix F intro, design §1.5 last bullet |

## Invariants I1 to I16

| ID | Check | Result | Status |
| --- | --- | --- | --- |
| I1 | verdict sentence once in body | `grep -c 'The pre-registered rule gives this verdict'` over BODY = 1 (`sections/06-res-q1.tex`); `\VerdictQOne` = "Prices are not calibrated as a whole at this n." unchanged (NUMDEL 0) | PASS |
| I2 | 5 owner `\todo` kept | TODO = 5 | PASS |
| I3 | no new `\todo` | TODO = 5 | PASS |
| I4 | no text deleted | MOVED table above; Q1 numeric tokens of the baseline all present in the new text (only `22`, `5.5`, `9.` differ: old page count, old subsection number, pdftotext line break) | PASS |
| I5 | numbers only via macros | body digit scan: literal digits only in pre-existing lines (`353 million`, `of 9 bins`, `24 real datasets`, `80/20`, bin labels, TikZ lengths, column widths); `tab:checks` block digits: check IDs, widths, `4pt`, `8pt`, "below 0.", "excludes 0."; `fig:flow` TikZ: only `Polymarket-v1`, Q1 to Q3, R1, R2, M1 to M5. New-only numeric tokens in the PDF (0.65%, 0.69%, 0.70%, 0.71%, 1.28%, 1.57%, 17,836, 47,809) all resolve to `numbers.tex` macros (`RThree*`) | PASS |
| I6 (amended) | `numbers.tex` additions only, `figures/` untouched | NUMDEL 0, 32 added lines; `git diff --quiet -- figures/` exit 0 | PASS |
| I7 | 0 undefined | 0, no `??` | PASS |
| I8 | 0 Overfull | 0 | PASS |
| I9 | appendix floats `[H]` | FLOATH 0 | PASS |
| I10 | caption below, label after caption | awk scan of all section files: no `\label{fig/tab:` before its `\caption` | PASS |
| I11 | real headings | no `\textbf{N.` fake headings | PASS |
| I12 | core flow in body | body labels: `fig:calib, fig:calib-gap, fig:calib-rate, fig:ccdf, fig:flow, fig:qq-size, fig:timeline, tab:bins, tab:checks, tab:conc, tab:fits` (11, the plan's 9 plus the two Figure 3 sub-labels from the owner's split: superseded). Key macros in BODY: HookPct 5, PaperTrades 2, NMarketsInScope 6, NMarketsKept 7, DaysShort 15, MaxStaleHours 3, MinTrades 3, NBins 4, Alpha 4, eq:chisq 1, VerdictQOne 2, QOneChiSq 3, GapNetDiffMain 5, QOneKsD 1, pOne 19. Read p1 to p7 as images: Q1 (5.1, Table 1, Figure 3), Q2 (5.2, Table 2, Figure 4), Q3 (5.3, Table 3, Figure 5), checks (5.4, Table 4), Discussion, Limitations, Conclusion follow without the appendix | PASS |
| I13 | pointers updated | every body `\Cref{sec:app-*}` resolves and prints "Appendix X.Y" (e.g. "Appendix G.3", "Appendix D.1", "Appendix B.1"); `\Cref{sec:res-robust,sec:res-review}` prints "Appendices F and G"; F and G each open with one `\Cref{sec:res-checks}` and one `\Cref{tab:checks}`; `\Cref{fig:flow}` in the Introduction; Limitations has `\Cref{sec:app-m4}`, `\Cref{sec:app-m3}`, `\Cref{tab:checks}` | PASS |
| I14 | course report unchanged, 2 pages | own build `(2 pages)`; git status empty; `*_half.png` unchanged | PASS |
| I15 | outside-lecture labels | 5 methods listed in `04-methods.tex` line 53; label sentences kept at Lorenz (04-methods, 07-res-q2), Wilson (app-g line 34), cluster bootstrap (app-g 57), logistic calibration and skill score (app-g 98) | PASS |
| I16 | `% src:` travel | SRC prints nothing | PASS |

## MVP ladder L1 to L4

Not applicable: this milestone is a paper restructure, not system or app work. No schema, mock or pipeline is involved.

## Hierarchy H1, H2

| ID | Check | Result | Status |
| --- | --- | --- | --- |
| H1 | trace | `PLAN.md` mission block has Mission, Vision, S1 → RQ1–RQ6, `M5 → S1 ... cycle 1/2; recovery 0/2`; no `budget:`; every PL row tags `→ M5`; design doc quotes the block (§0) | PASS |
| H2 | decisions logged, Why per `rules/docs.md` §8 | D-042 to D-046 exist with Rejected, Decided by, Evidence. Their **Why column names no mission-block line or RQ ID**: D-042 "Conference review (length, Q1 focus), D-038"; D-043 "D-042, owner's ..."; D-044, D-045, D-046 likewise cite D-rows, owner quotes and rule files only. D-035 to D-041 name M1, RQ1, Mission, Constraints | ISSUE (hierarchy, major, → `product-manager`) |

## AC per PL row

| Row | AC checked | Result |
| --- | --- | --- |
| PL-01 | `$BASE` exists and is gitignored; `grep -c '0 to 10' $BASE/main.tex` = 2; `grep -c D-043 DECISIONS.md` = 3; base log 22 pages | pass |
| PL-02 | one file per section in `sections/` (19 files); `grep -l 'label{sec:res-q[123]}'` = 3; `papers/README.md` has `sections/`; `grep -cE '\\(sub)?section\{' main.tex` = 1 (`\renewcommand{\bibsection}{\section{References}...}`) | pass; the section count AC is superseded by the owner's numbered References section (2026-11-09) |
| PL-03 | RuleSame yes/no = 11; the three `no` are `MTwoOther`, `PeerAHigh`, `PeerBPeriodThree`; 5 CI/KeptN newcommands; `future_work/papers/paper_mvp2/numbers.tex` unchanged; NUMDEL 0 | pass |
| PL-04 | `label{sec:app-` in app-g = 9; `label{sec:res-checks}` in body = 1; "Appendix G" in pdftotext = 11; G back-pointers present | pass |
| PL-05 | "sensitivity row below" in body = 1; fig:r1, tab:r1, fig:r2 in app-f = 3; F back-pointers present | pass |
| PL-06 | fig:ecdf in app-c = 1; QOneKsD in body = 1; fig:calib in body = 1; tab:bins = 1 | pass |
| PL-07 | fig:ccdf = 1, tab:conc = 1 in body; wd-maker, wd-taker, lorenz in app-d = 3; `sec:app-q2-roles` = 0 | pass |
| PL-08 | fig:qq-size = 1, tab:fits = 1 in body; hist, qq-wallet in app-e = 2; "Prices pile up near both ends" = 1 | pass |
| PL-09 | fig:drops in app-a = 1; tab:prereg in app-b = 1; `sec:app-sports` = 0; `\input{sections/app-*}` in a to g order (lines 183 to 189) | pass |
| PL-10 | `tab:checks` in body = 1 (in `sections/08-res-q3.tex`, accepted by the owner); `checks-summary` 0; `Cref{app:` 0; `NEEDS MACRO` 0; `too large` 0; table block has 10 `\Cref{sec:app-` and 11 data rows (`\midrule` 11); `RThreePeerAHighRuleSame` = 1; digits in the block only IDs, widths, `4pt`, `8pt`, "below 0", "excludes 0"; table fits one page (p6) | pass |
| PL-11 | `Cref{sec:app-m4}` = 2, `Cref{sec:app-m3}` = 2 in body; `Cref{tab:checks}` in limits = 1; "Sports is the largest topic" = 1 | pass |
| PL-12 | `newlabel{fig:flow}{{1}` = 1; `Cref{fig:flow}` in intro = 1; TikZ digits only in IDs and `Polymarket-v1` | pass |
| PL-12a | `*_half.png` byte-identical (git status clean); `*_col.png` tracked; body figures print at column width with legible text (p4, p5 images) | pass |
| PL-12b | `\documentclass[10pt,twocolumn]`, `margin=0.7in`, `\columnsep` 0.25in; `fig:flow`, `fig:timeline` `figure*[t]`; `tab:bins`, `tab:conc`, `tab:fits`, `tab:checks` `table*[t]`; column figures `[H]`; `\onecolumn` after `\appendix`; p9 is one column; `\raggedbottom` and `\@colht` reset present (`paper.md` §3.2) | pass |
| PL-13 | STD passes; B = 7 in `STATUS.md`; course report 2 pages and clean git status; no text cut | pass; B rule literal reading superseded (see Verdict) |
| PL-14 | stale greps (`17쪽`, `17-page`, `22쪽`, `22 pages`) print nothing; `["Figure N"` = 21, `["Table N"` = 6; `L[0-9]{3}` in summaries = 0; `5.4 Robustness` in decisions = 0; page bar p1 to p17 matches `main.aux`; every Figure N / Table N naming a paper float in tips, `polymarket_plan_detailed.md`, `README.md`, `papers/README.md` matches `main.aux` (checked: Figures 1 to 21, Tables 1 to 6, Appendix A to G.7.2); proposal page keeps its text plus one link line; `tips/README.md` and `index.html` current; static HTML: tags balanced in all 11 pages, no fixed width over 1040 px (svg `min-width:520px` only), SVG elements inside viewBox, no text overlap after recomputing with inherited `text-anchor` and font size; mermaid 22 static blocks (ERD 6, plus 2 the ERD page builds in JS; decisions 16) read for syntax only, not rendered | pass |
| PL-15 | this file; B stated; one line per invariant | pass |

Numbers spot-checked against `numbers.tex` or the paper PDF (more than 10): 47,948; 688,131; 7.0%; chi-square 68.0; net gap −0.99%; 9 of 10 bins; top 20% 98.9% / 98.0%; price mean 0.376 / median 0.320; 62,718 (9.1%); R1 47,940 (99.98%), 7 split; M1 −1.20% / −1.13%; M2 −1.32%, 30,112 / 17,836; M4 1,790.0 vs 69.0, 292.5 vs 17; M5 63.4% / 83.4%; peer a 0.71%; R2 18.98%; wallets 581,435 / 1,535,977; drop counts 255,420 / 215,289 / 80,230 / 26,526; 11 cited works (bbl has 11). Feedback page status counts: table rows give 8 answered, 5 partly, 5 out of scope, 1 praise, as the page claims. Decision counts: `DECISIONS.md` has 46 rows; decisions page says 46, and its Figure 1 says 38 after excluding the 8 it names.

## Findings

### Blocker

None.

### Major

| # | Where | Finding | Class and route |
| --- | --- | --- | --- |
| M1 | `DECISIONS.md` rows D-042 to D-046, Why column | Why names no mission-block line or RQ ID (`rules/docs.md` §8). Earlier rows D-035 to D-041 name M1, RQ1, Mission. Not an M5 exit criterion, so it does not block M5; it is the H2 check above | hierarchy → `product-manager` |
| M2 | `papers/paper_mvp1/sections/*.tex`: 27 captions carry `Source: run ...` or a `runs/...` path (visible p2 Figure 1, p3 Figure 2, p4 Table 1 and Figure 3, p5 Figures 4, 5 and Tables 2, 3, p6 Table 4); body 4.5 prints `142082_mvp1_full_v1r3 (job 142082)`; body 5.4 line 13 prints `analysis/prereg_review_fixes.md` | `rules/writing/paper.md` §3.3 (2026-11-09, changed on disk during this review) forbids run names and file paths in text and source lines in captions. The baseline (D-041 PASS) had the same pattern; the restructure added four new instances (`fig:flow` caption, the three redrawn captions with `runs/local_column_figs_v13`). Whether the new rule applies retroactively is the owner's call | implementation → `sonnet-writer` |

### Minor

| # | Where | Finding | Class |
| --- | --- | --- | --- |
| m1 | PDF p4, left column | About 1.35 in of blank space between the end of the text and Figure 3(a) at the column bottom (measured on the 100 dpi image: text ends y≈540, figure starts y≈675 of 1100). `paper.md` §3.2 "Leave no large blank area in a column". Cause: `\flushbottom` stretch around the `[H]` float | implementation → `sonnet-writer` |
| m2 | PDF p4 | Figure 3(b) with caption "Figure 3: Continued" sits at the top of the right column, above Figure 3(a) at the bottom of the left column. Column reading order is still (a) then (b). Noted, not a defect | layout, owner's call |
| m3 | PDF p6 | Left column ends about 0.6 in above the right column bottom. Small, from `\flushbottom` with no stretch available | implementation |
| m4 | PDF p7, p8, p9 | p7 right column ends after the Conclusion with about 3.8 in free (last body page, no float after the Conclusion). p8 (References) and p9 (Appendix A) are each about half blank. These follow the owner's "new page" rules, not a defect | none |
| m5 | `paper_length.plan.md` PL-13 | The B rule `head -1 == "References"` no longer matches the numbered heading `9 References`. The plan text is stale after the owner's 2026-11-09 request | reasoning → `product-manager` (plan text) |
| m6 | `tips/polymarket_paper_decisions_tips.html` lines 120, 132, 154, 172, 190, 214, 230, 408 to 410 | Unicode circled numbers `①` to `⑦` (`rules/writing/style.md` §3 allows only 1, 2, 3 / (1) / a, b, c) | implementation → `sonnet-writer` |
| m7 | `tips/polymarket_paper_decisions_tips.html` | Section 5.4 named both "5.4 Checks summary" (2 places) and "5.4 Checks: summary" (1 place); the paper heading is "Checks: summary". `tips/polymarket_paper_summaries_tips.html` section map chips use parent names ("5.4 Results", "4.5 Methods") rather than the subsection names the PL-14 row asked for. `tips/polymarket_research_flow_tips.html` SVG line 145 writes "Fig. 5" (`latex.md` §10: "Figure N") | implementation → `sonnet-writer` |
| m8 | `tips/polymarket_paper_flow_tips.html` lines 149 to 206 | 8 `href="#sec-*"` anchors in the Figure 1 SVG have no static `id`; the ids are built at runtime (`sec.id="sec-"+s.id`, ids `intro`, `data`, `methods`, `q1`, `q2`, `q3`, `checks`, `discussion` exist in the JS array). Resolve with JS on; dead without JS | info |

Lang span counts: ko and en differ by one in 8 pages. The difference is `<html lang="ko">`, CSS selectors `html[data-lang=...]`, or paired `<title>` elements inside SVGs. Every content span is paired. Not an issue.

## Routing summary

- M1 (H2): `product-manager` adds the served line (M5 → S1 → RQ1, Mission) to the Why of D-042 to D-046, surgically.
- M2, m1, m3, m6, m7: `sonnet-writer`, after the owner says whether `paper.md` §3.3 (2026-11-09) applies to this paper now.
- m5: `product-manager`, plan text.
- PASS closes M5 under its exit criteria. The majors stay open as listed items.
