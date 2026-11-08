# Pre-registration: label of the side coded 1 (review V-1)

- Date: 2026-11-07. Written before the run. Decision: D-036.
- Finding: `analysis/review_mvp1_gate_2026_11_07.md` V-1.
- Sentence under check: "So Yes is priced too high".
- Where: `papers/paper_mvp1/main.tex` 379, report v1 Q1 "How to read" (`code/make_report.py`), `README.md` 44 and 72.
- Base run: `runs/142082_mvp1_full_v1r3/` (47,948 kept markets, `q1_results.json` `main_with_min_filter.n_markets`).
- This is a count over the whole kept set, not a sample. It has no sampling noise. So the line below is a wording tolerance, not a noise-derived line (`rules/measurement.md` §1).
- No new hypothesis test. Counts and shares only (`STATUS.md` Constraints, lecture methods).

## 1. Question

In the 47,948 kept markets, how often is the outcome label of the side coded 1 the word "Yes"?

## 2. Measure

### 2.1 Where the label comes from (code)

| Item | Code | What it does |
| --- | --- | --- |
| `label1` | `code/common.py` 156, `build_market_set` | `max(outcome_label) FILTER (WHERE CAST(outcome_seq AS BIGINT) = 1)`, grouped by `condition_id`, table `mkts` |
| `y` | `code/build_tables.py` 32-33 | 1 when `winning_outcome_label = label1`, raw string equality. NULL when either is NULL |
| `p_1d` | `code/build_tables.py` 38-56 | mean `p_event` at the last timestamp at or before T − 1 day. `p_event` is on the side-coded-1 scale |
| kept set | `markets.parquet` column `kept` | `drop_reason IS NULL`. Q1 main uses `m[m["kept"]]` (`code/q1_calibration.py` 130) |

- `label1` is not saved in `markets.parquet`. Table `mk_stats` selects `category_refined` and `y`, not `label1`.
- So the job must rebuild `label1` from the raw parquet with the same expression as `common.py` 156.
- Join key: `condition_id` = `market_id`.
- Kept list: `market_id` where `kept` is true in `runs/142082_mvp1_full_v1r3/markets.parquet`.
- Check: the joined row count must be 47,948. Any other count stops the job (no decision).
- `category_refined`: take it from `markets.parquet` of run 142082, NULL as `"Unknown"` (`code/common.py` 189).

### 2.2 Normalization

- `label_norm = lower(trim(label1))`, with runs of inner whitespace collapsed to one space.
- `trim` removes leading and trailing whitespace.
- No other change: no punctuation removal, no synonym map.

### 2.3 Yes-like

- Yes-like: `label_norm == "yes"`. Exactly that string.
- `"y"`, `"true"`, `"yes "` before trim, team names and player names are not special cases. Trim handles the last one.
- No-like (reported, not used in the rule): `label_norm == "no"`.
- Share Yes-like = (Yes-like markets) / (markets in the group).

### 2.4 Side checks (reported, not used in the rule)

- `n_distinct_label1`: distinct raw `outcome_label` values with `outcome_seq = 1`, per market. `max()` hides more than one. Count markets with a value above 1.
- `y_case_mismatch`: kept markets where `lower(trim(winning_outcome_label)) == label_norm` but the raw strings differ. `y` uses raw equality, so such markets would carry a wrong `y`.
- Which slot `outcome_seq = 1` is: run `runs/142123_robust_full_v4/r1_results.json` `agreement_index_primary` = 0.99917. So `y` matches payout index 0 (the first slot) in that share. This supports the wording "the first-listed outcome". This prereg does not re-measure it.

## 3. Outputs the job saves

- File: `label1_counts.json` in the new run folder. Also `label1_by_market.csv` (individual-level, `rules/measurement.md` §3).
- `label1_by_market.csv` columns: `market_id`, `label1`, `label_norm`, `is_yes_like`, `category_refined`, `p_1d`, `y`, `bin`.
- `bin` uses the Q1 rule: `min(int(p_1d * 10), 9)` (`code/q1_calibration.py` 41).

Expected keys of `label1_counts.json`:

| Key | Content |
| --- | --- |
| `n_markets` | must equal 47948 |
| `base_run` | `"142082_mvp1_full_v1r3"` |
| `normalization` | the rule text of §2.2 |
| `overall.top_labels` | list of `{label_norm, n, share}`, the 20 largest, by n descending |
| `overall.n_distinct_label_norm` | count of distinct normalized labels |
| `overall.n_yes_like`, `overall.share_yes_like` | Yes-like count and share |
| `overall.n_no_like`, `overall.share_no_like` | No-like count and share |
| `by_category.<category_refined>` | `n`, `n_yes_like`, `share_yes_like`, `top_labels` (5 largest) |
| `by_bin.<0..9>` | `n`, `n_yes_like`, `share_yes_like`. `n` must equal `q1_bins.csv` `n` per bin |
| `by_bin_yes_only.<0..9>` | Yes-like markets only: `n`, `n_y1`, `mean_price`, `observed_rate`, `diff_obs_minus_price`. Descriptive, no test |
| `checks.n_multi_label1` | markets with `n_distinct_label1` > 1 |
| `checks.n_y_case_mismatch` | count from §2.4 |
| `checks.n_p1d_on_inner_edge` | kept markets with `p_1d * 10` an integer in 1..9. Used in §5 |
| `checks.chi2_mirrored` | the Q1 chi-square recomputed on `1 − p_1d` and `1 − y`, same 10-bin rule. Used in §5 |
| `decision` | `"A"` or `"B"` by §4, computed by the job |

Q1 bins in `runs/142082_mvp1_full_v1r3/q1_bins.csv` (10 equal-width bins on `p_1d`):

| Bin | n | gap (observed − price) | off after BH |
| --- | --- | --- | --- |
| 0 | 18,209 | −0.0046 | yes |
| 1 | 2,703 | −0.0230 | yes |
| 6 | 2,553 | −0.0279 | yes |
| 7 | 2,301 | −0.0329 | yes |
| 8 | 2,133 | −0.0188 | yes |

- The "too high" reading rests on these 5 bins (`q1_results.json` `bins_reject_bh` = 5). Bins 2 to 5 and 9 are not off.

## 4. Decision rule (fixed now)

| Outcome | Condition | Wording action |
| --- | --- | --- |
| A | `overall.share_yes_like` ≥ 0.95 AND `by_bin.<b>.share_yes_like` ≥ 0.95 for each of bins 0, 1, 6, 7, 8 | Keep "Yes" wording. Add one line with the overall share, e.g. "The side coded 1 is labeled Yes in X% of kept markets" |
| B | any condition of A fails | Reword to "the first-listed outcome (outcome 1)" in paper 379, report Q1 "How to read", README 44 and 72. Optional: one line on `by_bin_yes_only`, marked descriptive, no new test |
| Stop | `n_markets` ≠ 47,948, or a `by_bin.n` differs from `q1_bins.csv` | No decision. Fix the join, re-run |

Reasons for the lines:

- 0.95 overall: the sentence names "Yes" flatly. It must hold for at least 19 of 20 kept markets. The same tolerance is the R1 agreement line (`analysis/prereg_robustness.md`, `robust_agree_min` 0.95).
- 0.95 in each off bin: Sports is 40.0% of kept markets. Team labels may sit in some price bins only. A good overall share could then hide a non-Yes bin that drives the result.
- Bins not off (2 to 5, 9) carry no line: the sentence does not rest on them.
- `share_no_like` and the side checks do not enter the rule. If `checks.n_y_case_mismatch` > 0, report it as a separate finding. It does not switch A and B.
- In A, if the job's share is below 1.0, the added line states it. It does not claim all markets.
- The category table is descriptive. It explains B if B occurs.

## 5. Effect on the MVP1 verdict

- The MVP1 verdict does not change under A or B.
- Why 1: this run recomputes no Q1 number. It only names what "1" means. The verdict rule (`analysis/prereg_mvp1.md`, lines 20-26) reads chi-square p and BH bin calls. Neither uses the label text.
- Why 2: the chi-square is symmetric to which side is coded 1, inside a fixed bin. Details below.

### 5.1 What the check of the code found

- Chi-square (`code/q1_calibration.py` 55-58): per bin, (O_yes − E_yes)²/E_yes + (O_no − E_no)²/E_no, with E_yes = n × mean price.
- Swap the coding: p becomes 1 − p, y becomes 1 − y. Then O_yes and O_no trade places. E_yes and E_no trade places. The two terms of the bin trade places. The bin sum is the same. Exact.
- df = number of bins = 10 (line 59). Unchanged.
- Per-bin binomial test (line 35): `binomtest(k, n, p)` and `binomtest(n − k, n, 1 − p)` give the same two-sided p. The distribution is the mirror image. So BH calls match too, bin for bin.
- Bin edges are not exactly symmetric. Bin = `min(int(p_1d * 10), 9)` (line 41) uses intervals closed on the left.
- Under 1 − p, a market with `p_1d` exactly on an inner edge (0.1, ..., 0.9) moves to a different mirrored bin. Example: `p_1d` = 0.5 is in bin 5. Its mirror 0.5 is also in bin 5, not bin 4.
- Ends are safe: p = 0 goes to bin 0, its mirror p = 1 goes to bin 9 by the clamp.
- So the claim holds exactly per bin. Over all bins it holds exactly only if no kept `p_1d` sits on an inner edge.
- `p_1d` is a mean of trade prices. Edge values are possible. No saved file counts them. `checks.n_p1d_on_inner_edge` and `checks.chi2_mirrored` report this. They are a check of the claim, not a verdict.
- The review's own sentence says the same with less detail: "the chi-square over mirrored bins does not depend on which leg is labeled 1" (V-1).
- `analysis/prereg_mvp1.md` names "observed Yes vs. n × mean price" (line 22). It defines no direction line. So no prereg line reads the sign of the gap. The direction sentence is descriptive under A and under B.
