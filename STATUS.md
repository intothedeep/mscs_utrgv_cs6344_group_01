# Status

> Completed items live in `_archive/` (cold storage, do not read unless
> investigating history). This doc holds the active + planned log only.

One line per step, newest at the bottom. Why each choice was made: `DECISIONS.md`. Criteria fixed before results: `analysis/prereg_mvp1.md`.

## Constraints (hold for the final version)

| Constraint | Source |
| --- | --- |
| Only methods from our lectures. k-means is a side analysis, under 1/10 of the report | owner, 2026-10-18; plan Q2 |
| Every fact in a class post has a source. No source, no claim | owner, 2026-10-18; plan "Facts in the class post" |
| All data queries run on the cluster. The laptop only draws figures from saved outputs | root `CLAUDE.md`, 2026-10-18 |
| T, the minimum-trade cutoff and the Q1 criteria are fixed before any Q1 result | D-005, D-007 |
| Write "wallet" or "address", never "trader" or "person" | plan Q2 |
| Every test reports an effect size next to its p-value | plan "MVP1 is done when" |

## Log

2026-10-18 proposal: v3 posted with sourced facts only (tips/polymarket_proposal_tips.html)
2026-10-19 cluster: env `~/myEnvs/cs6330` ready, CPU-only jobs (D-001, D-002)
2026-10-19 data: `daily_aligned/` 1,248 files and `CTF/resolutions.parquet` on the cluster, sizes match the listing (D-003, analysis/hf_daily_aligned_listing.txt)
2026-10-19 code: pipeline v1 written, Job A and Job B scripts (code/, jobs/, CHANGELOG.md)
2026-10-19 pilot: Job A 142041 ran on gpul40q in about 2.5 min, inspect only (D-004, D-006, runs/142041_pilotA_2025_06/report_pilot_inspect.md)
2026-10-19 prereg: T = close_at, min 10 trades, keep duplicate rows (D-007, analysis/prereg_mvp1.md)
2026-10-19 next: commit the prereg, then Job B on the pilot set (first end-to-end cycle, no verdict)
2026-10-19 decision: gpul40q CPUs for all jobs; deliver report v1 (MVP1) and v2 (MVP1 + MVP2) (D-008, D-009)
2026-10-19 pilot: Job B 142056 ran in about 75 s; build_tables, q1, q2 ran; q3 failed on a scipy 1.18 KS call, fixed (runs/142056_mvp1b_pilot_2025_06/summary.md)
2026-10-19 pilot: 726 markets kept of 2,063; stale price (> 24 h) drops 851 (runs/142056_mvp1b_pilot_2025_06/tables_summary.json). First cycle, no verdict
2026-10-19 full: MVP1 full run submitted as 142057, 16 CPUs, 200 GB (runs/batch_20261019a.txt)
2026-10-19 plan: reviewer once at the end, then fix; tips page progress log updated each step (owner)
2026-10-19 plan: reports v1 and v2 in English; the Korean tips page is the single place to check progress (owner)
2026-10-19 full: MVP1 142057 ran all 4 stages in about 15 min; 688,131 markets in scope, 47,948 kept (runs/142057_mvp1_full_v1/summary.md)
2026-10-19 pilot: MVP2 pilot submitted as 142077 with code v2
2026-10-19 report: v1 (English) built from run 142057 by code/make_report.py (reports/report_v1.html)
2026-10-19 pilot: MVP2 142077 ran in about 5 min; q1b, q1c ran; q1a failed on a plot error bar (-1e-17), fixed in q1a and q1 (plot only). n_kept 726 = MVP1 pilot (runs/142077_mvp2_pilot_2025_06/summary.md). No verdict
2026-10-19 full: MVP2 full run submitted as 142078, 16 CPUs, 200 GB
2026-10-19 full: MVP2 142078 ran all 7 stages in about 14 min (runs/142078_mvp2_full_v2/summary.md)
2026-10-19 report: v2 (English) built with the v1 consistency table (reports/report_v2.html). Brier differs from v1 at the 6th digit: tie order in arg_max(p_event, ts); fix after review
2026-10-19 review: reviewer dispatched once (analysis/review_mvp1_mvp2.md)
2026-10-19 review: 0 blocker, 8 major, 16 minor; prereg verdicts hold; fixes dispatched as code v3 (D-011, analysis/review_mvp1_mvp2.md)
2026-10-19 rerun: code v3 full runs submitted, MVP1 142082 and MVP2 142083 (D-011)
2026-10-19 rerun: 142082 and 142083 ran all stages in about 27 min each; n_kept 47,948 and drop reasons unchanged; 77 of 77 MVP1 values equal across v1 and v2; verdicts unchanged (00.runs.md, runs/*_v*r3/verdicts.json)
2026-10-19 report: v1 and v2 rebuilt from the v3 runs (reports/report_v1.html, reports/report_v2.html)
