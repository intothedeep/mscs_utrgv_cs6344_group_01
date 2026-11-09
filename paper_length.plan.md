# Paper length restructure (D-042, D-043)

> Split from `PLAN.md` (rules/docs.md §1). The PLAN.md stub is the truth if
> the two disagree; update both in the same edit.

Milestone: M5 in the `PLAN.md` mission block.
Design: `analysis/design_paper_length_d042.md` (invariants I1 to I16, steps S0 to S11). Table: `analysis/table_design_checks_summary.md` option A.

- Rows run top to bottom, one dispatch at a time. PL-06 to PL-09 may run in any order.
- Review happens once, at PL-15. No row reviews another row.
- Agents never commit. The main session commits where a row says "Commit".
- Each commit includes the rebuilt `papers/paper_mvp1/main.pdf`.
- Line numbers are locators in the pre-split `main.tex` (`$BASE/main.tex`). They die at PL-02.
- Find each block by its text and label after PL-02.
- "→ M5" is this milestone. "Check M5" is the practical-size check in the paper.

What D-043 and the dispatch change in the design:

- S0 is closed by D-043. Its picks are final.
- F1, F3, F4, F5 apply. F2, F6, F7 do not apply.
- The role tests, the Sports paragraph and the pipeline check stay in the body.
- `sec:app-q2-roles` and `sec:app-sports` are never created.
- Appendix D has two subsections. k-means is D.2, with label `sec:app-kmeans`.
- Design S11 "owner picks" is closed. Levers O2, O3, O4 are not applied at any page count (D-043).
- The Conclusion gets no new pointer. D-043 does not add one.
- Amended I6: `numbers.tex` may gain macros, additions only. `figures/` stays untouched.
- This amendment overrides design §3.2 "no new macro" and I6 "numbers.tex untouched".
- Labels follow the design, not the table design: `tab:checks` and `sec:app-*`.
- `tab:checks-summary` and every `app:` label are never created (`rules/writing/latex.md` §10).
- `tab:checks` has 11 rows: row 0 (original Q1) plus the 10 checks.
- Owner, 2026-11-08: each appendix (A to G) starts on a new page. Applied once in `main.tex` after `\appendix`. PL-13 and PL-15 check it.
- Design S9 runs before design S8. The Limitations pointer needs `tab:checks` to exist.

Shared checks, run from `papers/paper_mvp1/` in bash:

```bash
TEX='main.tex sections/*.tex'
BODY='main.tex sections/[0-9]*.tex'    # appendix files are sections/app-*.tex
BASE=x_base_d042                       # gitignored, written by PL-01
BUILD() { latexmk -C && latexmk -pdf main.tex; }
CLEAN() { grep -c '^!' main.log; grep -c Overfull main.log; grep -c undefined main.log; pdftotext main.pdf - | grep -c '??'; }
TODO()  { cat $TEX | grep -c 'todo{owner'; }
S='s/ ?\(?\\Cref\{[^}]*\}\)?//g'
MOVED() { comm -23 <(sed -E "$S" $BASE/main.tex | LC_ALL=C sort -u) <(cat $TEX | sed -E "$S" | LC_ALL=C sort -u); }
SRC()   { comm -23 <(grep '% src:' $BASE/main.tex | LC_ALL=C sort) <(cat $TEX | grep '% src:' | LC_ALL=C sort); }
FLOATH() { cat sections/app-*.tex | grep -E 'begin\{(figure|table)\}' | grep -vc '\[H\]'; }
NUMDEL() { diff $BASE/numbers.tex numbers.tex | grep -c '^<'; }
REFPAGE() { for p in $(seq 1 40); do pdftotext -f $p -l $p main.pdf - | grep -qx References && { echo $p; break; }; done; }
```

STD, the AC of every LaTeX row:

- `BUILD` exits 0. `CLEAN` prints four zeros (I7, I8). Judge the final latexmk pass only.
- `TODO` prints 5 (I2, I3). `SRC` prints nothing (I16). `NUMDEL` prints 0 (amended I6).
- `git diff --quiet -- figures/` exits 0 (amended I6).
- `MOVED` prints only pointer lines named in design §1.5 or in the row (I4).
- `FLOATH` prints 0 once `sections/app-*.tex` exist (I9).

Rows:

- [ ] → M5 PL-01 Save the pending work and the baseline. Executor: main session. Depends on: none. Commit: yes, first.
  - Commit the "0 to 10%" labels in `main.tex`, `tips/polymarket_paper_flow_tips.html`, its `index.html` and README rows, D-042, D-043, `PLAN.md`, this file, and the two design files.
  - Then run `BUILD`. Copy `main.tex`, `main.aux`, `main.log`, `numbers.tex` to `$BASE`. Run `pdftotext main.pdf $BASE/main.txt`.
  - AC: `git status --short` is empty, with `$BASE` ignored.
  - AC: `grep -c '0 to 10' $BASE/main.tex` returns at least 1. `grep -c 'D-043' ../../DECISIONS.md` returns at least 1.
  - AC: `grep 'Output written' $BASE/main.log` shows the page count. All later page checks compare with it.
- [ ] → M5 PL-02 Split `main.tex` (design S1). Executor: sonnet-writer. Depends on: PL-01. Commit: yes, alone.
  - One `sections/NN-slug.tex` per `\section`. Each Results `\subsection` gets its own file. Preamble, title, abstract and bibliography stay in `main.tex`.
  - Each slug repeats its label, for example `sec:intro` gives `01-intro.tex` and `sec:limits` gives `limits`.
  - Add one `sections/` line to "Each folder holds" in `papers/README.md`. No other edit. No other agent touches `main.tex` meanwhile.
  - AC: STD, with `MOVED` printing nothing.
  - AC: `diff <(grep newlabel $BASE/main.aux | LC_ALL=C sort) <(grep newlabel main.aux | LC_ALL=C sort)` is empty.
  - AC: `pdftotext main.pdf - | diff - $BASE/main.txt` is empty. The `Output written` page count equals `$BASE/main.log`.
  - AC: `grep -cE '\\(sub)?section\{' main.tex` returns 0. `grep -l 'label{sec:res-q[123]}' sections/*.tex | wc -l` returns 3.
  - AC: `grep -c sections/ ../README.md` returns at least 1.
- [ ] → M5 PL-03 Add the 16 table macros to `code/make_paper_numbers.py`. Executor: developer. Depends on: PL-02. Commit: yes.
  - Source: `runs/150310_r3_review_fixes_v6`, in the `--r3` path only. Each macro has a comment with file and key.
  - Rule macros print "yes" for "same" and "no" for "different", like `\RobROneRuleSame`.
  - `m1_results.json`: `RThreeQOneNetGapCiLow`, `RThreeQOneNetGapCiHigh` (`rows.p_1d.net_gap_ci_low`, `_high`), `RThreeMOneVwapRuleSame` (`rows.p_vwap.row_agreement`).
  - `m2_results.json`: `RThreeMTwoYesNoRuleSame`, `RThreeMTwoOtherRuleSame` (`yes_no_row_agreement`, `other_row_agreement`).
  - `m3_bootstrap.json`: `RThreeMThreeKOneRuleSame` (`proxies.k1_slug_stem.row_agreement`).
  - `minor4_dedup.json`: `RThreeMinorFourKeptN` (`kept_set.n_out`), `RThreeMinorFourNetGapCiLow`, `RThreeMinorFourNetGapCiHigh`, `RThreeMinorFourRuleSame` (`q1.*`).
  - `peer_a_results.json`: `RThreePeerALowRuleSame`, `RThreePeerAMidRuleSame`, `RThreePeerAHighRuleSame` (`tercile_*_row_agreement`).
  - `peer_b_results.json`: `RThreePeerBPeriodOneRuleSame`, `RThreePeerBPeriodTwoRuleSame`, `RThreePeerBPeriodThreeRuleSame` (`period_*_row_agreement`).
  - Run from `cs6344_group_01/` only the `paper_mvp1` command in `papers/README.md`, as `OMP_NUM_THREADS=1 timeout 300 uv run python ...`. Saved outputs only.
  - Read `rules/development/python.md` before the run. A timeout or any other need goes back to the main session.
  - AC: `NUMDEL` prints 0. If not, stop and hand back.
  - AC: `grep -cE 'RThree[A-Za-z]*RuleSame\}\{(yes|no)\}' numbers.tex` returns 11.
  - AC: `grep -E 'RThree[A-Za-z]*RuleSame\}\{no\}' numbers.tex` prints 3 lines, for `MTwoOther`, `PeerAHigh`, `PeerBPeriodThree`.
  - AC: `grep -cE 'newcommand\{.RThree(QOneNetGapCi(Low|High)|MinorFourKeptN|MinorFourNetGapCi(Low|High))\}' numbers.tex` returns 5.
  - AC: `git diff --quiet -- ../../future_work/papers/paper_mvp2/numbers.tex` exits 0.
  - AC: STD, and `pdftotext main.pdf - | diff - $BASE/main.txt` is empty. New macros are unused, so the text must not change.
- [ ] → M5 PL-04 Move the review checks to Appendix G (S2). Executor: sonnet-writer. Depends on: PL-02. Commit: yes.
  - Add `\appendix` in `main.tex` after the bibliography group. Add `sections/app-g-review.tex`. Appendix files are `\input` in A to G order.
  - Keep `sec:res-review`. Add `sec:app-m1` to `sec:app-m5`, `sec:app-dup`, `sec:app-peer`, and subsubsections `sec:app-peer-a`, `sec:app-peer-b`.
  - Create body `\subsection{Checks: summary}\label{sec:res-checks}` with framing lines 768 to 774 and one pointer to `sec:res-review`.
  - G opens with one back-pointer to `sec:res-checks`.
  - AC: STD.
  - AC: `grep -c 'label{sec:app-' sections/app-g-review.tex` returns 9. `cat $BODY | grep -c 'label{sec:res-checks}'` returns 1.
  - AC: `pdftotext main.pdf - | grep -c 'Appendix G'` returns at least 1.
- [ ] → M5 PL-05 Move R1, R2 to Appendix F (S3). Executor: sonnet-writer. Depends on: PL-04. Commit: yes.
  - Add `sections/app-f-robust.tex`. Keep `sec:res-robust`. Add `sec:app-r1`, `sec:app-r2`.
  - Move framing lines 692 to 697 to body `sec:res-checks`. F opens with one back-pointer to `sec:res-checks`.
  - AC: STD.
  - AC: `cat $BODY | grep -c 'sensitivity row below'` returns 1.
  - AC: `grep -cE 'label\{(fig:r1|tab:r1|fig:r2)\}' sections/app-f-robust.tex` returns 3.
- [ ] → M5 PL-06 Q1 moves (S4, F4). Executor: sonnet-writer. Depends on: PL-04. Commit: yes.
  - Move `fig:ecdf` and equal-frequency lines 495 to 499 to `sections/app-c-q1.tex`, label `sec:app-q1`. Lines 492 to 494 stay.
  - Line 491 keeps `\QOneKsD` and points to `sec:app-q1`. F4 leaves one pointer sentence.
  - AC: STD.
  - AC: `grep -c 'label{fig:ecdf}' sections/app-c-q1.tex` returns 1. `cat $BODY | grep -c QOneKsD` returns at least 1.
  - AC: `cat $BODY | grep -c 'label{fig:calib}'` returns 1. `cat $BODY | grep -c 'label{tab:bins}'` returns 1.
- [ ] → M5 PL-07 Q2 moves (S5, F1). Executor: sonnet-writer. Depends on: PL-04. Commit: yes.
  - Move `fig:wd-maker`, `fig:wd-taker`, `fig:lorenz` to D.1 `sec:app-q2-dist` in `sections/app-d-q2.tex`, label `sec:app-q2`.
  - Move k-means lines 366 to 371 and 610 to 620 to D.2 `sec:app-kmeans`. Line 365 stays, with a pointer.
  - Pointers at 513, 514. Each moved method keeps its outside-lecture label sentence (I15).
  - Role-test lines 360 to 362 and 605 to 608 and pipeline-check lines 588 to 593 stay in the body.
  - AC: STD.
  - AC: `cat $BODY | grep -c 'label{fig:ccdf}'` returns 1. `cat $BODY | grep -c 'label{tab:conc}'` returns 1.
  - AC: `grep -cE 'label\{fig:(wd-maker|wd-taker|lorenz)\}' sections/app-d-q2.tex` returns 3.
  - AC: `cat $TEX | grep -c 'sec:app-q2-roles'` returns 0.
- [ ] → M5 PL-08 Q3 moves (S6). Executor: sonnet-writer. Depends on: PL-04. Commit: yes.
  - Move `fig:hist` and `fig:qq-wallet` to `sections/app-e-q3.tex`, label `sec:app-q3`.
  - Pointers at 625 and 647. Line 644 gets `(\Cref{fig:hist-price})`, with its words unchanged.
  - AC: STD.
  - AC: `cat $BODY | grep -c 'label{fig:qq-size}'` returns 1. `cat $BODY | grep -c 'label{tab:fits}'` returns 1.
  - AC: `grep -cE 'label\{fig:(hist|qq-wallet)\}' sections/app-e-q3.tex` returns 2.
  - AC: `cat $BODY | grep -c 'Prices pile up near both ends'` returns 1.
- [ ] → M5 PL-09 Data and Methods moves (S7, F3). Executor: sonnet-writer. Depends on: PL-04. Commit: yes.
  - Move `fig:drops` to `sections/app-a-data.tex`, label `sec:app-data`. Its two describing lines move too.
  - Move `tab:prereg` to B.1 `sec:app-prereg` and Reproducibility lines 390, 392 to 400 to B.2 `sec:app-repro`, in `sections/app-b-methods.tex`, label `sec:app-methods`.
  - Lines 389, 391 stay, plus one pointer. Pointers at 207, 270.
  - AC: STD.
  - AC: `grep -c 'label{fig:drops}' sections/app-a-data.tex` returns 1. `grep -c 'label{tab:prereg}' sections/app-b-methods.tex` returns 1.
  - AC: `cat $TEX | grep -c 'sec:app-sports'` returns 0.
  - AC: after PL-06 to PL-09, `grep -n 'input{sections/app-' main.tex` lists a, b, c, d, e, f, g in that order.
- [ ] → M5 PL-10 Insert `tab:checks` in body 5.4 (S9). Executor: sonnet-writer. Depends on: PL-03, PL-04, PL-05. Commit: yes.
  - Use the table design §7 skeleton, option A, with the §2 column widths and §5 caption.
  - Labels change: `tab:checks`, and each `\Cref{app:x}` becomes `\Cref{sec:app-x}`.
  - Replace every `[NEEDS MACRO]` with the PL-03 macros.
  - Reading cells with no `\todo`: M4 uses lines 839 to 840, duplicates line 880, peer a line 892, verbatim (D-043).
  - Peer a high tercile "no" appears only through `\RThreePeerAHighRuleSame`. Write no sentence about it.
  - Add one body pointer to `tab:checks` in 5.4. Add `\Cref{tab:checks}` to the F and G back-pointers.
  - If the table runs past one page, stop and hand back. Options B and C are not picked.
  - AC: STD, with `TODO` still 5.
  - AC: `cat $BODY | grep -c 'label{tab:checks}'` returns 1. `cat $TEX | grep -c 'checks-summary'` returns 0. `cat $TEX | grep -c 'Cref{app:'` returns 0.
  - AC: `cat $TEX | grep -c 'NEEDS MACRO'` returns 0. `grep -c 'too large' main.log` returns 0.
  - AC: the table block has 10 `\Cref{sec:app-` and 11 data rows. `cat $TEX | grep -c RThreePeerAHighRuleSame` returns 1.
  - AC: in the `tabularx` block, a digit appears only in a check or question ID, a column width, a `\tabcolsep` length, `\chi^2`, or the reused words "below 0" and "excludes 0" (I5).
- [ ] → M5 PL-11 Limitations pointers and F5 (S8). Executor: sonnet-writer. Depends on: PL-04, PL-05, PL-10. Commit: yes.
  - Retarget line 970 to `sec:app-m4` and line 976 to `sec:app-m3`.
  - Move paragraph 992 to 999 to the F intro. The body keeps one pointer sentence to `tab:checks`.
  - The Sports paragraph (lines 956 to 964) stays.
  - AC: STD.
  - AC: `cat $BODY | grep -c 'Cref{sec:app-m4}'` and the same for `sec:app-m3` each return at least 1.
  - AC: `grep -c 'Cref{tab:checks}' sections/*limit*.tex` returns 1.
  - AC: `grep -c 'Sports is the largest topic' sections/*limit*.tex` returns 1.
- [ ] → M5 PL-12 Add `fig:flow` at the end of the Introduction (S10). Executor: sonnet-writer. Depends on: PL-10. Commit: yes.
  - One-row TikZ pipeline, design §4.2. No figure script is needed. Style from `figkit.sty`.
  - Float `[H]`, caption below with "Why:", then `\label{fig:flow}`. Add the pointer sentence "`\Cref{fig:flow}` shows the study flow."
  - Counts use `\NMarketsInScope`, `\NMarketsKept`, `\MinTrades`, `\DaysShort`, `\pOne` only.
  - AC: STD.
  - AC: `grep -c 'newlabel{fig:flow}{{1}' main.aux` returns 1.
  - AC: `grep -c 'Cref{fig:flow}' sections/*intro*.tex` returns 1.
  - AC: in the `tikzpicture` block, a digit appears only in a check or question ID, a TikZ length, or the name `Polymarket-v1` (I5).
- [ ] → M5 PL-13 Final build and page count (S11). Executor: main session. Depends on: PL-01 to PL-12. Commit: only if files changed.
  - Run `BUILD`. N is the `REFPAGE` output, the page where References starts.
  - Body pages B = N − 1 if `pdftotext -f N -l N main.pdf - | head -1` is "References". Otherwise B = N.
  - Record B in `STATUS.md`.
  - Build `../course_report_mvp1` once with `latexmk -C && latexmk -pdf main.tex`. Then `git restore` its `main.pdf`.
  - AC: STD on the final tree.
  - AC: the course report log shows `(2 pages`. `git status --short ../course_report_mvp1/` is empty (I14).
  - AC: `STATUS.md` holds B. The main session reports B to the owner as information.
  - AC: no text cut and no layout change is made at any B (D-043).
- [ ] → M5 PL-14 Update the tips pages about the paper. Executor: sonnet-writer. Depends on: PL-13. Commit: yes.
  - Read every number from the final `main.aux` and `REFPAGE`. Update both `lang="ko"` and `lang="en"` text.
  - `tips/polymarket_paper_flow_tips.html`: page bar (`#sec-pages`), section start pages, F and T counts, the `figs:` arrays, `pg:` lines, new appendix sections.
  - `tips/polymarket_paper_summaries_tips.html`: the section map and its 28 `L###` `main.tex` line locators. Use section names.
  - `tips/polymarket_paper_decisions_tips.html`: the Figure 2 section map, "5.4 Robustness", and "Robustness section" wording.
  - Scope widened by D-044: every other tips page is updated to the current paper and project state, with old content removed: `polymarket_paper_review_tips.html`, `class_questions`, `feedback_answers`, `mvp1_preprocessing`, `research_flow`, `data_erd`, `polymarket_plan_detailed.md`, `index.html` notes, `README.md`.
  - Remove stale counts, superseded plans, old figure numbers, and open items already done. Do not add history notes.
  - Exception: `polymarket_proposal_tips.html` keeps the proposal as posted, plus one line linking to the current state (D-044).
  - AC: every "Figure N" or "Table N" that names a paper float matches the final `main.aux`. `grep -l "17쪽\|17-page\|22쪽\|22 pages" tips/*` prints nothing.
  - AC: `grep -c '22 pages' tips/polymarket_paper_flow_tips.html` returns 0. `grep -c '22쪽' tips/polymarket_paper_flow_tips.html` returns 0.
  - Keep the `figs:` arrays at one entry per line, one entry per float.
  - AC: in that file, `grep -cE '\["Figure [0-9]+"'` returns 21 and `grep -cE '\["Table [0-9]+"'` returns 6.
  - AC: `grep -cE 'L[0-9]{3}\b' tips/polymarket_paper_summaries_tips.html` returns 0.
  - AC: `grep -c '5.4 Robustness' tips/polymarket_paper_decisions_tips.html` returns 0.
  - AC: the three pages render at 1040 px with no horizontal scroll and no overlap (`rules/answering.md` §3).
- [ ] → M5 PL-15 Gate review, cycle 1/2, recovery 0/2. Executor: reviewer. Depends on: PL-14. Commit: the review file, after the verdict.
  - Output: `analysis/review_gate_paper_length.md`.
  - AC: the file has one verdict line, PASS or ISSUE, and one line per invariant I1 to I16.
  - AC: STD passes on the reviewer's own build. The file states B, computed as in PL-13.
  - AC core flow (I12): `cat $BODY | grep -oE 'label\{(fig|tab):[^}]*' | LC_ALL=C sort` prints exactly `fig:calib`, `fig:ccdf`, `fig:flow`, `fig:qq-size`, `fig:timeline`, `tab:bins`, `tab:checks`, `tab:conc`, `tab:fits`.
  - AC core flow: each body key macro in design §4.1 still appears in `$BODY`. The reviewer reads Question to Conclusion without the appendix.
  - AC I1: `cat $BODY | grep -c 'The pre-registered rule gives this verdict'` returns 1.
  - AC I14: the course report row of PL-13 still holds.
  - AC tips: the page bar in `tips/polymarket_paper_flow_tips.html` matches `main.aux`.
  - PASS closes M5. ISSUE goes to the `recover` skill, within the milestone counters.
