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

## Amendment (2026-10-19, after review, AFTER the first full Q1 result)

- The original rule "last `p_event` at or before T − 1 day" left the order of trades inside one block undefined. Many trades share one block timestamp.
- New rule: the mean `p_event` of the trades at the last timestamp at or before T − 1 day (D-011, review F1). Motivation: determinism, not the result.
- This change came after Q1 results were seen (run 142057). The verdict did not change:

| Run | Rule | chi-square p | Cohen's w | Verdict |
| --- | --- | --- | --- | --- |
| `runs/142057_mvp1_full_v1` | last trade, unordered ties | `q1_results.json` | `q1_results.json` | not calibrated as a whole |
| `runs/142082_mvp1_full_v1r3` | mean at last timestamp | `verdicts.json` | `verdicts.json` | not calibrated as a whole |

## Note (2026-11-01, written AFTER the results)

- We wrote this note after seeing the Q1, Q2 and Q3 results.
- It changes no rule, line or verdict in this file.
- All lines above stay as committed (`rules/measurement.md` §1).

### 1. Why Up/Down markets are dropped (G5)

- The rule on line 15 stays. This note only adds the reason.
- Source: the dataset paper, `polymarket_v1_paper.pdf` (Qin and Yang, 2026).
- Exact wording comes from `analysis/review_mvp1_rq.md` row G5.

| Paper location | Wording |
| --- | --- |
| Section 6, first paragraph | Standard Binary excludes "Up-Down (high-frequency price-interval) markets, which have fundamentally different settlement mechanics" |
| Limitation 5 | "Standard Binary, Up-Down, and Neg-Risk markets are structurally distinct and should not be pooled" |

### 2. RQ2 reference (D-024, D-025)

- The 80/20 rule (80/20 법칙) is a descriptive reference, not a verdict line (D-024).
- Power law (멱법칙) is also a descriptive reference. It needs no new run (D-025).
- This note adds no Q2 verdict line. D-024 rejected a line set after results.
- The class post named 80/20 before results (`proposal_md/polymarket_proposal_v3.md` line 12).
- The post went up on 2026-10-18 (`STATUS.md` line 21).
- The earlier draft also names 80/20 (`archive/polymarket_proposal_v2.md` line 12).

### 3. Departures in the report and paper (D-026, D-028)

- The rule on lines 20 to 26 still decides the verdict.
- The table lists what D-026 and D-028 decide for the report and paper.

| Method | Report and paper | Detail |
| --- | --- | --- |
| Effect size column, line 25 | Per-bin gap (구간별 차이) and z interval (z 구간) | Replaces the Wilson interval (윌슨 구간) |
| Brier score (브라이어 점수) | Shown as mean squared residual (평균 제곱 잔차) of the price | Same number |
| Cohen's w (코언의 w) | Not reported | `verdicts.json` still stores it: `comparisons.Q1.effect_size` |
| Gini coefficient (지니 계수) | Dropped | D-026, D-028 |
| Lorenz curve (로렌츠 곡선) | Stays as a labeled figure | Labeled as outside the lectures (D-028) |

### 4. Does the z interval (z 구간) change the bins read as off?

- Main 10 bins: no. The verdict run reads the same 5 bins both ways.
- Equal-frequency check: yes, in one bin.

| Bin set | Mean price outside the z interval (z 구간) | Off after Benjamini-Hochberg (BH, 거짓 발견율 보정) | Same bins |
| --- | --- | --- | --- |
| Main, 10 equal-width bins | 5: bins 0, 1, 6, 7, 8 | 5: bins 0, 1, 6, 7, 8 | yes (`same_bins`: true) |
| No minimum trades, 10 equal-width bins | 4: bins 6, 7, 8, 9 | 4: bins 6, 7, 8, 9 | yes |
| Equal-frequency, 10 bins | 8 | 7 | no. Extra bin: (0.0, 0.00122] |

- Interval columns: `reports/lecture_numbers.json` `z_interval_95`.
- Equal-frequency rows there carry no off call (`runs/142140_q1eqfreq_v5/q1_bins_eqfreq.csv` has them).
- The extra bin has 1 Yes in 4,795 markets. Its z interval (z 구간) starts below 0.
- Bin-off calls come from the binomial test (이항 검정) with Benjamini-Hochberg (BH, 거짓 발견율 보정).
- The z interval (z 구간) makes no call.

Robustness: `analysis/prereg_robustness.md` also stays as committed. Its Wilson, Cohen's w and d_z rows remain as written. Reports and the paper do not print them (D-026).
