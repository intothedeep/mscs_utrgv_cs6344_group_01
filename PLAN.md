# Plan

> Completed items live in `_archive/` (cold storage, do not read unless
> investigating history). Split detail, if any, is linked from stubs below;
> a stub's state is the truth if it and the detail disagree.

## Mission block
- Mission: Test whether a Polymarket price can be read as a probability, using every resolved market and only methods from our lectures. (owner, 2026-10-19)
- Vision: A reader can look at a Polymarket price and know how far to trust it: which price ranges, topics and horizons are off, by how much, and who sets the prices. (owner, 2026-10-19)
- Constraints: `STATUS.md` "Constraints" table (lecture methods only; k-means under 1/10 of the report; sourced facts only; cluster for all data queries; criteria fixed before results; "wallet", never "person"; effect size next to every p-value).
- Goals (question-type): [RQ.md](./RQ.md): 6 answered, 0 open.
- S1 → RQ1–RQ6: MVP ladder. MVP1 answers RQ1–RQ3, MVP2 adds RQ4–RQ6 (picked by the owner, plan 2026-10-18; report v1 and v2, D-009); listed alternative: one full analysis without MVP stages.
- M1 → S1: MVP1; exit: the four "MVP1 is done when" boxes in `tips/polymarket_plan_detailed.md`; done 2026-10-19 (run `142082_mvp1_full_v1r3`, `reports/report_v1.html`); cycle 1/2; recovery 0/2.
- M2 → S1: MVP2; exit: Q1a, Q1b, Q1c each with a pre-registered verdict; done 2026-10-19 (run `142083_mvp2_full_v2r3`, `reports/report_v2.html`); cycle 1/2; recovery 0/2.
- M3 → S1: robustness cycle (D-013); exit: R1 and R2 stage reports from run `142123_robust_full_v4` and the Q1 sensitivity row; done 2026-10-19 (`runs/142123_robust_full_v4/report_r1_split_payout.md`, `report_r2_price_path.md`, `r1_results.json` `q1_sensitivity`); cycle 1/2; recovery 0/2.
- M4 → S1: papers v1 and v2 (D-014); exit: reviewer gate PASS (`analysis/review_papers.md`), both papers build clean, every measured number is a `numbers.tex` macro; gate PASS with 3 major and 17 minor findings, fixes in progress; cycle 1/2; recovery 0/2.

## Detail

- Method plan: `tips/polymarket_plan_detailed.md`.
- Criteria: `analysis/prereg_mvp1.md`, `analysis/prereg_mvp2.md`.
- Decisions: `DECISIONS.md`. Progress: `STATUS.md`. Runs: `00.runs.md`.
- Progress page for the owner (Korean): `tips/polymarket_research_flow_tips_ko.html`.

## Open tasks

- [ ] Split `code/make_report.py` (about 800 lines) in its own commit. Kept as is for now (owner, 2026-10-19). AC: same report HTML byte for byte from runs 142082 and 142083.
- [ ] Owner reviews report v1 and v2. AC: owner's notes recorded in `STATUS.md`.
- [ ] → M4 Apply review fixes F1–F19 to both papers, add title, subtitle, authors (owner, 2026-10-19), dataset citations. AC: `papers/paper_mvp1` and `papers/paper_mvp2` rebuild with 0 errors, 0 overfull boxes; each of F1–F19 marked fixed or skipped with a reason in `analysis/review_papers.md`; `grep '\todo{number:' papers/` returns no match (1 match in `paper_mvp1/main.tex` on 2026-10-19).
