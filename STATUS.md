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

2026-10-18 proposal: v3 posted with sourced facts only (../tips/group_01/polymarket_proposal_tips.html)
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
2026-10-19 prereg: MVP1 amendment records the tie rule change after the first full result; verdict unchanged (analysis/prereg_mvp1.md)
2026-10-19 hygiene: individual-level CSVs untracked (stay on cluster; jobs/fetch_run.sh); proposal states 9.1% no usable winner label (owner)
2026-10-19 plan: mission and vision set by the owner; PLAN.md and RQ.md created (D-012)
2026-10-19 class: answers to 4 classmate questions (../tips/group_01/polymarket_class_questions_tips.html); open next steps: split payouts in CTF/resolutions.parquet, price path in the last 24 h
2026-10-19 robustness: prereg and code v4 committed (3182a89), job 142123 submitted (D-013, analysis/prereg_robustness.md)
2026-10-19 papers: numbers.tex from runs 142082, 142083; LaTeX drafts in progress (D-014, papers/)
2026-10-19 robustness: 142123 ran in about 42 min; n_kept 47,948 and q1_results.json equal to 142082; 7 split payouts, label agreement 0.9992; Q1 sensitivity rule result same (runs/142123_robust_full_v4/report_r1_split_payout.md, report_r2_price_path.md)
2026-10-19 papers: reviewer gate PASS (0 blocker, 3 major, 17 minor); fixes applied; owner title, subtitle, authors; dataset paper and dataset cited (analysis/review_papers.md, papers/)
2026-10-19 tips: robustness results added to the progress page and the class questions page (../tips/group_01/)
2026-10-19 papers: review F7 (one number format rule) and F9 (code v5, run 142140 saves BH p; q1 outputs equal 142083) fixed; papers rebuilt (analysis/review_papers.md)
2026-11-01 scope: D-016, target goal is MVP1 only (root CLAUDE.md)
2026-11-01 scope: D-017, MVP2 files moved to future_work/
2026-11-01 review: M1 gate ISSUE, exit reopened by G1, cycle 2/2, task rows added (analysis/review_mvp1_rq.md, PLAN.md)
2026-11-01 scope: D-018, D-019, D-020; Mission line reworded by owner pick (PLAN.md)
2026-11-01 report: G1 closed by box plot (D-018); G2, G8, G9, G10 fixed; report v1 regenerated, numbers unchanged (reports/report_v1.html, CHANGELOG.md)
2026-11-01 scope: D-021, deadline 2026-11-15 (DECISIONS.md)
2026-11-01 review: D-022, third M1 gate review dispatched (analysis/review_mvp1_rq_r3.md)
2026-11-01 scope: D-023, M4 exit names paper_mvp1 only (PLAN.md)
2026-11-01 rq: D-024, RQ2 title stays, 80/20 is a descriptive reference (DECISIONS.md)
2026-11-01 scope: D-025, power law descriptive, all analysis within lecture contents; method audit dispatched (analysis/lecture_method_audit.md)
2026-11-01 review: third M1 gate PASS, 0 blocker, 0 major, 4 minor (analysis/review_mvp1_rq_r3.md)
2026-11-01 audit: 52 methods, 35 in lecture, 7 partly, 10 not found; owner picks open (analysis/lecture_method_audit.md)
2026-11-01 code: code/r2_price_path.py imports q1a_category, moved by D-017; rerun fails, saved run unaffected (analysis/lecture_method_audit.md §5)
2026-11-01 scope: D-026, D-027, audit picks and future-work line (DECISIONS.md)
2026-11-01 plan: 7 rows for D-024 to D-028 added, method plan rows struck (PLAN.md "Lecture scope 2026-11-01", ../tips/group_01/polymarket_plan_detailed.md)
2026-11-01 close: lecture-scope rows closed against AC, project-end review dispatched (PLAN.md, analysis/review_project_end.md)
2026-11-02 scope: D-029, D-030; CCDF job prepared, cluster chi-square returns, plan wording updated (DECISIONS.md, ../tips/group_01/polymarket_plan_detailed.md)
2026-11-02 scope: D-031, G7 closed by ledger line; wallet distribution figures job prepared (00.runs.md, DECISIONS.md)
2026-11-02 runs: 145892 ccdf, 145893 wallet figures, 145897 split Q3 figures; report v1 regenerated (reports/report_v1.html, 00.runs.md)
2026-11-02 scope: D-032, D-033, figure layout; pairs redrawn for half width (DECISIONS.md)
2026-11-02 review: final review PASS, 0 blocker, 0 major, 14 minor; tips index and bilingual pages added (analysis/review_final_2026_11_02.md, ../tips/group_01/index.html)
2026-11-02 paper: D-034, independence caveat after the Q1 p-value; departure wording fixed; paper builds, 17 pages (papers/paper_mvp1/main.tex)
2026-11-07 review: D-035, M1 gate PASS, 0 blocker, 1 major (V-1 "Yes is priced too high" wording), 11 minor; 40 of 40 numbers match; paper builds, 17 pages (analysis/review_mvp1_gate_2026_11_07.md)
2026-11-07 tips: tips moved from ../tips/group_01/ to tips/; one EN/KO toggle page per topic; ERD, paper decisions and proposal pages made bilingual; rendered at 1040px in both languages (tips/README.md, tips/index.html)
2026-11-07 decision: D-036, V-1 settled by a cluster label count, wording rule pre-registered first
2026-11-07 run: 150296 on gpu011, decision B; outcome 1 is "Yes" in 63.9% of kept markets (Sports 14.0%); reword V-1 to "outcome 1" (runs/150296_v1label/label1_counts.json)
2026-11-07 wording: D-037 done; paper, report v1 and README say "outcome 1"; Yes-only sentence by macros (30,630 markets, 9 of 9 bins, 0.4 to 5.6 points); paper builds, 17 pages; tips updated with D-035 to D-037 and their reasons; open: fig5_ecdf_yes_no.png text may still say Yes/No
2026-11-07 review: two-reviewer review page (conference, course professor); fixes started: prereg draft, fig 4 gap panel, related work (D-038, analysis/review_paper_mvp1_two_reviewers.html)
2026-11-08 run: robustness v3 job 150310 submitted on kimq sxm003, 16 CPU, 200G (prereg aef0808, code 94f7ae6, runs/batch_20261108a.txt)
2026-11-08 run: 150310 done in 22 min, all 9 stages ran, gate passed; fetched to runs/150310_r3_review_fixes_v6
2026-11-08 decision: M2 Yes sentence added next to outcome-1 wording (D-040)
2026-11-08 deliverables: paper section 'Checks requested in review' (22 pages), report_v1.html Robustness v3 step, 2-page course report papers/course_report_mvp1 (2 pages, clean build), tips/polymarket_paper_review_tips.html updated (D-040)
- 2026-11-08 gate review analysis/review_gate_mvp1_r3.md: PASS cycle 2/2, F1 to F14 closed (D-041), C2-1 to C2-3 fixed by main session; paper 22 pages, course report 2 pages, 0 warnings
- 2026-11-09 paper restructure (D-042 to D-045): body B = 7 pages in two columns (References start on page 7), appendices A to G on pages 9 to 21 in one column, 21 pages total; course report still 2 pages (PL-13)
