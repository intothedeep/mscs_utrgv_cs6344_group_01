# Pre-registration: robustness cycle R1 and R2 (written before any v4 result)

- Date: 2026-10-19. Decision: `DECISIONS.md` D-013. Extends `analysis/prereg_mvp1.md` and `analysis/prereg_mvp2.md`. All their choices stay.
- Parameters: `analysis/prereg_robustness.json`. New keys: `robust_agree_min` 0.95, `robust_delta_thresholds` [0.10, 0.25, 0.50], `robust_quantiles`, `robust_yes_payout_index` 0.
- Population: markets kept WITH the min_trades filter (the Q1 main set, 47,948 markets in the MVP1/MVP2 full runs).
- R1 and R2 are descriptive. They get no verdict and add no primary test.
- The MVP1 and MVP2 verdicts stay as they are. The R1 sensitivity row sits next to the Q1 row and never replaces it.
- Wording: a "wallet" is one address, never a person. This cycle has no wallet analysis.

## R1: split payouts

Why: a market whose payout is not 0/1 has no single winner. Our label y then rests on `winning_outcome_label` alone.

### Choices

| Choice | Value |
| --- | --- |
| Source | `CTF/resolutions.parquet` (`condition_id`, `outcome_slot_count`, `payout_numerators` as strings) |
| Join | `lower(markets.market_id) = lower(resolutions.condition_id)` |
| Numerators | each string cast to DOUBLE. A failed cast makes the market class "other" |
| Duplicate rows | rows per `condition_id` are counted. The market class uses the DISTINCT numerator lists. If the distinct lists differ, class = "other" |
| Yes side | our `outcome_seq = 1` leg. Primary mapping: it is payout index 0 (first slot) |

### Classes (first match wins)

| Class | Rule |
| --- | --- |
| missing | no row in resolutions |
| clean | 2 slots, exactly one numerator is 1 and the other is 0 |
| split | 2 or more slots, all numerators equal and non-zero |
| other | everything else: unequal non-0/1 values, all zero, 3 or more slots, failed cast, conflicting duplicates |

- Interpretation rule: if "missing" is nearly all kept markets, the join key format differs. That is a key problem, not a data gap. The report says so and no class share is read.

### Index mapping check

- Winner index of a clean market = the slot with numerator 1.
- Agreement = share of clean markets where (winner index = Yes index) equals (our y = 1).
- Not recorded before the run: whether `outcome_seq` starts at 0 or 1, and whether `outcome_seq = 1` is always the first slot. The agreement rate tests this.

| Agreement (index 0) | Mapping used | Mismatch exclusion |
| --- | --- | --- |
| >= 0.95 | index 0 (validated) | applied |
| <= 0.05 | index 1 (flipped, validated) | applied |
| between | none | skipped, flagged "mapping not validated" |

- The agreement under index 1 is 1 minus the agreement under index 0. Both are reported.
- Mismatch = a clean market where the mapped resolutions winner differs from our y.

### Outputs and the sensitivity row

| Item | Value |
| --- | --- |
| Class table | n per class, share of kept markets, duplicates (rows per id, ids with more than 1 row, identical vs conflicting) |
| Our y on split markets | counts of y = 1 and y = 0 |
| Agreement | rate with Wilson 95% CI, n clean, n mismatch |
| Sensitivity set | kept markets minus split, other and mismatch. Missing markets stay in (no evidence against them) |
| Sensitivity statistic | the Q1 analysis of `q1_calibration.py`: same bins (10, equal width), same chi-square test, same alpha 0.05 |
| Reported next to Q1 | chi-square, df, p, Cohen's w, n, Brier, bins off after BH, and the Q1 rule result for both rows |
| Agreement of the rows | "same" if the Q1 rule result text is identical, else "different". The change in w is reported either way |

## R2: price path in the last day

Why: p_1d is a price 24 hours before T. R2 shows how far the price moves from p_1d to the last trade before T.

### Choices

| Choice | Value |
| --- | --- |
| T | `close_at` (as in MVP1) |
| p_1d | as in the markets table (mean `p_event` at the last timestamp at or before T − 1 day) |
| p_T | mean `p_event` of the trades at the last timestamp strictly before T. Same tie rule as p_1d. No staleness limit |
| Window | trades with T − 1 day < ts < T (open at both ends) |
| No trade in the window | p_T = p_1d, delta = 0, counted in "no trade" |
| delta | p_T − p_1d |
| Crossing | (p_1d >= 0.5) differs from (p_T >= 0.5). It compares the two end points, not the path |
| Brier | (p − y)² per market, at p_1d and at p_T |
| Category | `category_refined`, missing = "Unknown", fewer than 30 kept markets = "Merged" (as in Q1a) |

### Outputs

| Item | Value |
| --- | --- |
| Quantiles of abs(delta) | 0.5, 0.75, 0.9, 0.95, 0.99, and the maximum |
| Shares of abs(delta) | >= 0.10, >= 0.25, >= 0.50 |
| Shares | crossing 0.5, no trade in the window |
| Trade count in the window | median, 0.9 quantile, maximum |
| Brier | mean at p_1d and at p_T, mean paired difference (p_T minus p_1d) |
| Paired difference | 95% t interval, paired t-test p, Cohen's d_z. All markets, and only markets with a trade in the window |
| By category | the same shares and Brier per category group. Mean difference with 95% t interval, no p-value |
| Figure | ECDF of abs(delta), overall |

- Bootstrap is not used. At n near 48,000 the t interval is enough.
- The overall paired t-test has one p-value. Its effect size (mean difference with CI and d_z) is printed next to it.
- The sign of the difference is read as is. A negative mean difference means p_T is closer to the outcome than p_1d.
- Many markets have no trade in the last day. That is a result, not a defect, and it is reported.

## Note after the run (2026-10-19, review F19)

- The class rules are applied in table order. The first match wins.
- So a vector with 3 or more equal non-zero slots is "split", not "other". This is how `code/r1_split_payout.py` already works.
- The rule did not change. Run 142123 has 0 "other" markets, so no number moves.
