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

## Detail

- Method plan: `tips/polymarket_plan_detailed.md`.
- Criteria: `analysis/prereg_mvp1.md`, `analysis/prereg_mvp2.md`.
- Decisions: `DECISIONS.md`. Progress: `STATUS.md`. Runs: `00.runs.md`.
- Progress page for the owner (Korean): `tips/polymarket_research_flow_tips_ko.html`.

## Open tasks

- [ ] Split `code/make_report.py` (about 800 lines) in its own commit. Kept as is for now (owner, 2026-10-19). AC: same report HTML byte for byte from runs 142082 and 142083.
- [ ] Owner reviews report v1 and v2. AC: owner's notes recorded in `STATUS.md`.
