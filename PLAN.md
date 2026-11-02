# Plan

> Completed items live in `_archive/` (cold storage, do not read unless
> investigating history). Split detail, if any, is linked from stubs below;
> a stub's state is the truth if it and the detail disagree.

## Mission block
- Mission: Test whether a Polymarket price can be read as a probability, using resolved Yes/No markets with a fresh price one day before the close and at least 10 trades, and only methods from our lectures. (owner, 2026-11-01; D-019; first set 2026-10-19)
- Vision: A reader can look at a Polymarket price and know how far to trust it: which price ranges, topics and horizons are off, by how much, and who sets the prices. (owner, 2026-10-19)
- Constraints: `STATUS.md` "Constraints" table (lecture methods only; k-means under 1/10 of the report; sourced facts only; cluster for all data queries; criteria fixed before results; "wallet", never "person"; effect size next to every p-value).
- Target scope: MVP1 only (Q1, Q2, Q3). MVP2 (Q1a, Q1b, Q1c) is not a target (owner, 2026-11-01; D-016).
- Goals (question-type): [RQ.md](./RQ.md): 6 answered, 0 open.
- S1 → RQ1–RQ6: MVP ladder. MVP1 answers RQ1–RQ3, MVP2 adds RQ4–RQ6 (picked by the owner, plan 2026-10-18; report v1 and v2, D-009); listed alternative: one full analysis without MVP stages.
- M1 → S1: MVP1; exit: the four "MVP1 is done when" boxes in `../tips/group_01/polymarket_plan_detailed.md`; first done 2026-10-19 (run `142082_mvp1_full_v1r3`, `reports/report_v1.html`); exit reopened 2026-11-01 by G1, box 3 (`analysis/review_mvp1_rq.md`), box 3 closed again 2026-11-01 (D-018); cycle 2/2, plus one review the owner allowed (D-022); recovery 0/2.
- M2 → S1: MVP2, not a target (D-016); exit: Q1a, Q1b, Q1c each with a pre-registered verdict; done 2026-10-19 (run `future_work/runs/142083_mvp2_full_v2r3`, `future_work/reports/report_v2.html`); cycle 1/2; recovery 0/2.
- M3 → S1: robustness cycle (D-013); exit: R1 and R2 stage reports from run `142123_robust_full_v4` and the Q1 sensitivity row; done 2026-10-19 (`runs/142123_robust_full_v4/report_r1_split_payout.md`, `report_r2_price_path.md`, `r1_results.json` `q1_sensitivity`); cycle 1/2; recovery 0/2.
- M4 → S1: paper v1 (D-014, D-023); exit: reviewer gate PASS (`analysis/review_papers.md`), `papers/paper_mvp1` builds clean, every measured number is a `numbers.tex` macro; gate PASS with 3 major and 17 minor findings, review fixes closed 2026-11-01, residual rows open below; cycle 1/2; recovery 0/2.

## Detail

- Method plan: `../tips/group_01/polymarket_plan_detailed.md`.
- Criteria: `analysis/prereg_mvp1.md`, `future_work/analysis/prereg_mvp2.md`.
- Decisions: `DECISIONS.md`. Progress: `STATUS.md`. Runs: `00.runs.md`.
- Progress page for the owner (Korean): `../tips/group_01/polymarket_research_flow_tips_ko.html`.

## Open tasks

- [ ] → M1 Split `code/make_report.py` (about 800 lines) in its own commit. Kept as is for now (owner, 2026-10-19). AC: same report HTML byte for byte from runs 142082 and 142083.
- [ ] → M1 Owner reviews report v1 (D-016). AC: owner's notes recorded in `STATUS.md`.
- [x] → M4 Apply review fixes F1–F19 to `paper_mvp1`, add title, subtitle, authors (owner, 2026-10-19), dataset citations. AC: `papers/paper_mvp1` rebuilds with 0 errors, 0 overfull boxes. Each of F1–F19 is marked fixed or skipped with a reason in `analysis/review_papers.md`. `grep '\todo{number:' papers/` returns no match. Closed 2026-11-01. Build evidence: `analysis/review_mvp1_rq.md` check 9. The `future_work/papers/paper_mvp2` clause is removed (D-016, D-017). AC PARTIALLY MET: F5 sentences of 16 and 17 words remain, see the F5 row below. F6 needs no row: `fig5_ecdf_yes_no.png` has its legend above the axes (`code/q1_calibration.py` `draw_ecdfs`).

### MVP1 gate 2026-11-01: closing order (`analysis/review_mvp1_rq.md`)

Scope: MVP1 only (D-016). No MVP2 task (D-017). Dispatches that may touch code cite `~/.claude/CLAUDE.md` "No local execution".

- [x] → M1 Owner picks how G1 closes: picked (a1) (owner, 2026-11-01; D-018). Options:
  - (a1) Draw the box plot locally from saved files, under "Allowed locally". `runs/142123_robust_full_v4/r2_markets.csv` has `category_group` and `p_1d`. `q3_results.json` `summary` has quantiles for price, trade size and wallet volume. So a `p_1d` box plot needs no job. A trade-size box plot from these files can use quantiles only. Trade rows sit in `trade_sizes_sample.parquet`, which is not local. Caveat: the PNG would not be a Q3 stage output of run 142082. The owner judges if that meets box 3.
  - (a2) Add the box plot to `code/q3_describe.py` and rerun Q3 by cluster job. The job needs the owner's OK. Slowest: code version, job, fetch.
  - (b) Drop "box plot" from the plan's Q3 row, with a dated note. Fastest: one owner edit, no figure. Choice (a1) is the fastest route that keeps the row.
  - AC: owner decides, and the pick is logged in `DECISIONS.md`.
- [x] → M1 Close G1 by the owner's pick. Closed 2026-11-01 by (a1): `reports/figures/box_p1d_by_category_group.png`, printed in `reports/report_v1.html`, drawn by `code/q3_box_p1d.py`. Blocked by the row above. AC for (a1) or (a2): a box plot PNG exists and `reports/report_v1.html` prints it with a caption. AC for (b): the plan's Q3 row no longer says "box plot". AC for all: box 3 is ticked again, and `grep -n 'box plot'` on the plan matches the outcome. A run outside "Allowed locally" goes back to the main session.
- [x] → M1 Owner picks how RQ2 closes (G4): title stays, 80/20 is a descriptive reference (owner, 2026-11-01; D-024). Options a and b were not picked:
  - (a) Reword RQ2 as descriptive, status "described (no verdict)". Evidence moves to the file holding the answer sentence.
  - (b) Owner sets a descriptive line, labeled post hoc in the prereg file and `DECISIONS.md`. `data-analyst` may draft it.
  - AC: owner decides, and the `RQ.md` row changes only after that.
- [x] → M1 Owner picks the wording of the Mission scope (G3): picked (a) (owner, 2026-11-01; D-019). The Mission line says "using every resolved market", but the deliverables test the kept set (`runs/142082_mvp1_full_v1r3/tables_summary.json` `n_kept`). Options:
  - (a) Reword the line to resolved Yes/No markets that have a price one day before close.
  - (b) Keep the line, and add a row that compares dropped and kept groups. Input: `runs/142123_robust_full_v4/markets.csv`, three columns, no raw pass.
  - AC: owner decides. The owner alone edits the Mission line.
- [x] → M1 Owner picks what happens to "topics and horizons" in the Vision (design page U1): line kept, MVP2 out of scope until the owner goes for it (owner, 2026-11-01; D-020). Q1a and Q1b answered these, and neither is a target now (D-016). Draft options, since the design page lists none:
  - (a) Keep the line, and state the gap in the report and paper.
  - (b) Reword the line to the MVP1 scope.
  - (c) Keep the line, and return to Q1a and Q1b if time allows (D-017).
  - AC: owner decides. The owner alone edits the Vision line.
- [x] → M1 Closed 2026-11-01: k-means share below 0.100, 0.0974 by the widest measure (G2, G14 in `analysis/review_mvp1_rq_r3.md`), other ACs checked. `future_work/reports/` shows only the staged D-017 rename. Fix `reports/report_v1.html` through `code/make_report.py` (G2, G8, G9, G10). Regenerate v1 only, from the saved run, under "Allowed locally". Read `rules/development/python.md` before the run. G8 cause: the path prints from the run argument (`self.run`), with no prefix in the code. Keep the Q1c note in v2, so make that edit v1-only.
  - AC G2: k-means share is below 0.100, by the method in the G2 row. The value is written on this row at close. The cut item stays in the saved run.
  - AC G8: `grep -o project_group_01 reports/report_v1.html | wc -l` returns 0. Every "Source:" path resolves from the project folder.
  - AC G9: table captions in print order run 1 to N with no gap. Today they run 13, 15, 16, 17, 18, 14, 19.
  - AC G10: `grep -c 'used in Q1c' reports/report_v1.html` returns 0.
  - AC scope: `git status --short future_work/reports/` is empty.
- [x] → M1 Fill the null `criteria_sha256_12` for Q1 (G7). Closed 2026-11-02 by a ledger line, not by a re-issue (owner, D-031). `verdicts.json` keeps its null (D-026). `code/verdicts.py` hashes `analysis/prereg_mvp1.md`, and that path may be missing on the cluster. Bump `CODE_VERSION`, add a `CHANGELOG.md` row, then re-issue verdicts for run 142082 only. The developer hands the run back, and the main session decides where it goes ("No local execution").
  - AC: the `142082_mvp1_full_v1r3` row of `00.runs.md` names both prereg commits and their hashes.
  - AC: `git diff --quiet -- runs/142082_mvp1_full_v1r3/verdicts.json` exits 0.
- [x] → M1 Update `00.runs.md` (G11, G12). Closed 2026-11-01. Pilots 142056 and 142077 have no recorded CPU count, and the ledger says so. AC G12: the ledger names partition, CPU count and env for each run, and cites D-015. AC G11: row `142140_q1eqfreq_v5` says the 142083 table matches by construction. That sentence cites the `build_tables.py` sha from `code.sha256`. Main session writes it.
- [ ] → M1 Compare the `markets.parquet` hash of run 142082 with `runs/142140_q1eqfreq_v5/input.sha256` (G11 optional, design page W1). Main session runs it on the cluster. AC: row `142140_q1eqfreq_v5` records equal or not equal. Not equal: stop and report to the owner.
- [ ] → M4 Owner writes or removes the 4 `\todo{owner: ...}` in `papers/paper_mvp1/main.tex`: related work, interpretation, wider implications, closing. AC: `grep -c 'todo{owner' papers/paper_mvp1/main.tex` returns 0.
- [ ] → M4 Finish F5 in `papers/paper_mvp1/main.tex`, after the owner's text is in. AC: a word count by `rules/writing/style.md` §2 lists 0 sentences over 15 words. AC build: exit 0, 0 errors, 0 overfull boxes.
- [ ] → M4 Owner picks the 3-person split (`docs/team_split_design.html` Steps 2 and 7). Options: A stable, B scalable, C cutting-edge. Answers to U2 to U10 feed the pick. AC: owner decides, and the pick is logged in `DECISIONS.md`.

The G5 prereg row and the G5, G13 paper row moved to the next section, merged with the D-026 work.

### Lecture scope 2026-11-01: closing order

Scope: D-024 to D-028. Sources: `analysis/lecture_method_audit.md`, `analysis/review_mvp1_rq_r3.md`. Deadline: 2026-11-15 (D-021). Dispatches that may touch code cite `~/.claude/CLAUDE.md` "No local execution". The G11, G12 row above stays open as is.

Outside-method check, used by the rows below. Run from the project folder.

```bash
NAMES='Wilson|Gini|Cohen|Cramér|Cramer|ARI|Rand|eta squared|d_z|Lorenz|Brier'
KEEP='D-02[5-8]|known as|outside the lectures|Team Brier|calls it the Brier|drops the Gini|Lorenz picture|picked from the lecture-method audit'
# The report is one physical line with base64 images. This prints one text block per line.
TEXT() { perl -pe 's/base64,[^"]+//g; s/<[^>]+>/\n/g' reports/report_v1.html; }
```

A kept mention sits in the departure note (cites a D-id), a rename sentence ("known as") or the Lorenz figure text ("outside the lectures").

- [x] → M1 Code and report: r2 import fix, `code/lecture_numbers.py`, `reports/report_v1.html`, `papers/paper_mvp1/numbers.tex` macros (D-024, D-026, D-028). Closed 2026-11-01. `same_bins` true.
  - AC import: `grep -n q1a_category code/r2_price_path.py` is empty. This one holds already (2026-11-01). `grep -nE '(from|import) q1a_category' code/*.py` is empty.
  - AC saved numbers: `reports/lecture_numbers.json` has `source_run` `142082_mvp1_full_v1r3` and 10 rows in `z_interval_95.bins`. The `same_bins` value is read from the file and written on this row at close.
  - AC names: `TEXT | grep -wE "$NAMES" | grep -vE "$KEEP"` is empty.
  - AC D-028: `grep -c 'drops Lorenz' code/make_report.py` returns 0. `TEXT | grep -w Lorenz | grep -c 'outside the lectures'` returns at least 1.
  - AC Fig. 4: `grep -c fig4_calibration_z code/make_report.py` returns at least 1. `TEXT | grep -c 'z interval'` returns at least 1.
  - AC verdict: `TEXT | grep -c 'Prices are not calibrated as a whole at this n'` returns at least 1. The verdict sentence in `runs/142082_mvp1_full_v1r3/verdicts.json` equals the committed file.
  - AC macros unused: `main.tex` uses none of the removed macros (row below). `numbers.tex` still defines them, because its generator also serves `future_work/papers/paper_mvp2` and stays additive (D-017).
  - AC macros new: `grep -c lecture_numbers.json papers/paper_mvp1/numbers.tex` returns at least 1.
  - AC R1 interval: `main.tex` prints no R1 agreement interval (row below). No z value is saved for it.
  - AC scope: `git diff --quiet -- future_work/reports/` exits 0.
- [x] → M4 Edit `papers/paper_mvp1/main.tex`: the same picks, plus G5 and G13. Do not touch the 4 `\todo{owner` parts. Closed 2026-11-01.
  - AC G5: the Up/Down sentence (`We drop Up/Down markets`) gives the settlement reason with `\citep{qin2026polymarketv1}`.
  - AC G13: `grep -c S-PAPER-4 main.tex` returns 0. `main.log` has no "inputenc package ignored".
  - AC names: `grep -nwE "$NAMES" main.tex | grep -vE "$KEEP"` is empty.
  - AC macros: `grep -cE 'MakerGini|TakerGini|PaperGini|QOneW|QOneNoMinW|RobROneSensW|RobROneDeltaW|RoleCohenD|KmeansCategoryV|KmeansAri|RobRTwoAllDz|RobRTwoTradedDz' main.tex` returns 0.
  - AC figures: `grep -c fig4_calibration_z main.tex` returns at least 1. `grep -c 'label{fig:lorenz}' main.tex` returns 1.
  - AC R1 interval: `main.tex` line "Wilson CI" on the R1 agreement rate goes. Either the sentence drops, or `RobROneAgreementLow` cites a saved z value in `numbers.tex`. No such saved value exists today (`r1_results.json` `mapping.agreement_ci95` is the Wilson interval).
  - AC owner parts: `grep -c 'todo{owner' main.tex` returns 4.
  - AC verdict: `grep -c 'not calibrated as a whole' main.tex` returns 2.
  - AC build: exit 0, `grep -c '^!' main.log` returns 0, `grep -c Overfull main.log` returns 0.
- [x] → M1 Append one note to `analysis/prereg_mvp1.md`. Closed 2026-11-01. `data-analyst` writes it. It holds the Up/Down citation (G5), the 80/20 reference (D-024) and the departures (D-026, D-028).
  - AC additions only: `git diff --numstat analysis/prereg_mvp1.md` shows 0 in the deleted column (`rules/measurement.md` §1).
  - AC G5: the note cites dataset paper section 6 and limitation 5: `grep -ci 'limitation 5' analysis/prereg_mvp1.md` returns at least 1.
  - AC content: `grep -c` returns at least 1 for each of `D-024`, `D-026`, `D-028`.
  - AC robustness: the note names `prereg_robustness.md`, whose Wilson, Cohen's w and d_z rows also stay as committed.
  - Order: the G7 row hashes this file. Run G7 after this note lands, or use its commit-SHA option.
- [x] → M1 Match `README.md` to the picks, and add the future-work line (D-024, D-026, D-027, D-028).
  - AC names: `grep -nwE "$NAMES" README.md | grep -vE "$KEEP|Q1: is the crowd right"` is empty. The excepted line is the criteria table, which quotes the prereg.
  - AC table: `grep -c 'Q1: is the crowd right.*Cohen' README.md` returns 0. Cohen's w is not in the prereg criteria.
  - AC D-027: `grep -ci lognormal README.md` returns at least 1. That line says no such analysis runs now.
- [x] → M1 Fix `docs/team_split_design.html` (G16). Closed 2026-11-01. The page names no outside method today, so only the stale facts change.
  - AC Mission: `grep -c 'every resolved market' docs/team_split_design.html` returns 0.
  - AC N3: `grep -c D-019 docs/team_split_design.html` returns at least 1.
  - AC MVP2: `grep paper_mvp2 docs/team_split_design.html | grep -vc 'not a target'` returns 0.
- [x] → M1 Add the G17 note: the box plot input comes from `bash jobs/fetch_run.sh 142123_robust_full_v4`. Main session writes it. AC: `grep -c fetch_run CHANGELOG.md` returns at least 1, or `grep -c fetch_run code/q3_box_p1d.py` does. Closed 2026-11-01.
- [x] → M4 Project-end review: `reviewer`, `system-architect` and `data-analyst` together, dispatched after every row above in this section is `[x]`. Closed 2026-11-02: `analysis/review_project_end.md`, then final review PASS with 14 minor findings (`analysis/review_final_2026_11_02.md`).
  - AC: `analysis/review_project_end.md` exists, with a verdict line and a list of open items.
  - AC: the file has one section per role.
  - AC: it re-checks "MVP1 is done when" boxes 3 and 4 under the new names, since `analysis/review_mvp1_rq_r3.md` Check 3 cites w, d and V.
  - AC: the verdict and open items reach the owner.

### Final review 2026-11-02: open minor items (`analysis/review_final_2026_11_02.md`)

- [x] → M4 Owner decides whether the paper states the independence limit beside the p-value in results, not only in limitations (finding 2). AC: owner decides, and `main.tex` matches. Closed 2026-11-02: one sentence after the p-value in results (owner, D-034).
- [x] → M4 Replace "names" in the departure sentence: the z interval is a different formula (finding 6, A12). AC: `main.tex` and report v1 say the interval changed, not just its name. Closed 2026-11-02.
