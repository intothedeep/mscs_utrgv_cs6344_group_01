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
