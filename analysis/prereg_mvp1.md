# Pre-registration: MVP1 (written before any Q1 result)

- Date: 2026-10-19. Decided by the owner from Job A (`runs/142041_pilotA_2025_06/`).
- Job A output pairs no price with an outcome. So these choices cannot follow a Q1 result.
- Parameters: `analysis/prereg_mvp1.json`.

## Choices and evidence

| Choice | Value | Evidence (Job A file) |
| --- | --- | --- |
| Close time T | `close_at` | `close_time_summary.json`: share of markets with a trade after `close_at` |
| Evaluation price | last `p_event` at or before T − 1 day, at most 24 h old | plan §0 |
| Minimum trades before T − 1 day | 10. Q1 is also reported without it | `activity_summary.json`: `kept_at_cutoff_close_rule` |
| Duplicate rows (same key) | kept | `duplicates.json`. No row id exists to tell repeat fills from copies |
| Up/Down markets | dropped by the default rule (`code/common.py` `UPDOWN_SQL`) | `updown_check.csv` |
| Bins, alpha | 10 equal-width bins, 0.05 | plan Q1 |

## Decision criteria (rules/measurement.md §1)

| Item | Q1 |
| --- | --- |
| Primary metric | chi-square goodness of fit over the 10 bins (observed Yes vs. n × mean price) |
| Line | p < 0.05 means the prices are not calibrated as a whole |
| Per-bin call | binomial test per bin, BH-corrected at 0.05. A bin is off when its corrected p < 0.05 |
| Effect size | observed rate − mean price per bin, with a 95% Wilson CI. Brier score next to it |
| Failure condition | no bin off after BH, and chi-square p ≥ 0.05: "no evidence of miscalibration at this n" |

- The pilot run (`scope = pilot`) is the first end-to-end cycle. It gets no verdict (`.claude/CLAUDE.md`, MVP ladder).
- The verdict applies to the full-data run with these same parameters.
