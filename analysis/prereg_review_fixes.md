# Pre-registration DRAFT: robustness v3 (review fixes M1 to M5, minor 4, peer asks)

- Status: DRAFT, 2026-11-07. Written before any v3 result. Not yet a committed prereg.
- Decision: pending. The main session logs a `DECISIONS.md` row before the job is written.
- Owner instruction: "go" on the review fixes (2026-11-07). Review: `analysis/review_paper_mvp1_two_reviewers.html` tab 1 (M1 to M7), tab 3.
- Parameters: `analysis/prereg_review_fixes.json`. All keys of `analysis/prereg_robustness.json` stay.
- Base run: `runs/142082_mvp1_full_v1r3`. Population: the 47,948 kept markets (`q1_results.json` `main_with_min_filter.n_markets`), unless an item names another set.
- Format model: `analysis/prereg_robustness.md` (R1, R2, run 142123). Label prior work: `analysis/prereg_v1_label_check.md`, run 150296, D-036, D-037.
- One cluster job: UTRGV Cradle, SLURM, CPU only (`-p kimq`, 8 CPU, 64G). Nothing here runs locally (`~/.claude/CLAUDE.md` "No local execution: cluster first").
- Every row in this file is a descriptive sensitivity row. It sits next to the Q1 row. It never replaces the Q1 verdict (`runs/142082_mvp1_full_v1r3/verdicts.json`).
- Every printed p-value has its effect size next to it (Cohen's w, net gap with CI, or a difference with CI).
- Wording: "outcome 1" is the side coded `outcome_seq = 1` (D-037). A wallet is one address, never a person.

## 0. Items and feasibility

| Item | Feasible | Reason |
| --- | --- | --- |
| M1 price definition | yes, partly | `taker_direction` and `outcome_seq` give the aggressor side per trade. No quote or order book, so the midpoint is a trade-based proxy |
| M2 Yes-oriented calibration | yes | Run 150296: outcome 1 is "Yes" in 30,630 kept markets and "No" in 0. The recode is the identity on Yes/No markets |
| M3 event dependence | proxy only | The 24 raw columns hold no event id, event slug or group key. Neg-Risk bundles (the native event groups) are dropped by the binary rule |
| M4 kept vs dropped table | yes | `markets.parquet` of 142082 holds all 688,131 markets with `drop_reason`. Volume before T − 1 day needs a raw pass |
| M5 practical size | yes | Saved `p_1d`, `y`. Logistic fit runs on the cluster |
| Minor 4 duplicates | yes | Exact duplicates are found by DISTINCT over all raw columns |
| Peer (a) volume tercile | yes | Volume before T − 1 day from the raw pass |
| Peer (b) close period | yes | `close_at` is in `markets.parquet` |
| T − 7 day horizon | pending owner | MVP2 Q1a, out of scope (D-016, D-020) |

### 0.1 Raw columns the job reads

Source: `data/polymarket_v1/daily_aligned/*.parquet`. Schema: `runs/142041_pilotA_2025_06/schema.csv`.

| Column | Used by |
| --- | --- |
| `condition_id`, `asset_id`, `outcome_seq` | all |
| `block_timestamp` | M1, peer (a), minor 4 |
| `price`, `p_event` | M1, minor 4 |
| `taker_direction`, `D` | M1 |
| `usdc_amount` | M1 (volume-weighted average price), M4, peer (a), minor 4 (Q2) |
| `maker`, `taker` | minor 4 (Q2) |
| `outcome_label`, `winning_outcome_label` | M2 (label of outcome 2) |
| `market_slug`, `category_refined`, `close_at` | M3 proxies |
| all 24 columns | minor 4 (exact-duplicate key) |

Saved inputs: `runs/142082_mvp1_full_v1r3/markets.parquet`, `q1_bins.csv`, `q1_results.json`, `q2_results.json`, `runs/150296_v1label/label1_by_market.csv`.

### 0.2 Gate before any item (job stops on failure)

- The rebuilt kept set equals the `market_id` list where `kept` is true in 142082 `markets.parquet`. Count 47,948.
- The rebuilt `p_1d` equals the saved `p_1d` per market (absolute difference ≤ 1e-12).
- The Q1 chi-square on the rebuilt set equals 67.99 (`verdicts.json`) to 4 decimals.
- Failure: no item is computed. The report says "gate failed" and names the check.

### 0.3 Shared definitions

| Name | Definition |
| --- | --- |
| T | `close_at` (as in MVP1) |
| Bin | `min(int(p * 10), 9)`, 10 equal-width bins (`code/q1_calibration.py` 41) |
| Q1 analysis | `q1_calibration.py` logic: per-bin exact binomial test, Benjamini-Hochberg (BH) at 0.05, chi-square goodness of fit with E = n × mean price, df 10, Cohen's w |
| Q1 rule text | the verdict sentence that `prereg_mvp1.md` lines 20 to 26 produce from chi-square p and BH bin calls |
| Net gap | mean(y − p) over markets. Equals the n-weighted mean of per-bin (observed − mean price). Main value −0.0099 (`reports/lecture_numbers.json` `gap_direction.main.net_gap`) |
| Net gap CI | 95% t interval of mean(y − p). Effect size d_z = mean / sd of (y − p) |
| Row agreement | "same" if the Q1 rule text is identical to the main row, else "different". The change in w and in net gap is reported either way (as in R1) |

## 1. M1: price definition

Why: `p_1d` is the mean trade price at the last timestamp at or before T − 1 day. A taker who buys pays the ask. Then the trade price sits above the midpoint. The reviewer says half the bid-ask spread could explain the −0.99 percentage point (pp) net gap.

### 1.1 What the data has

| Need | In the data | Note |
| --- | --- | --- |
| Trade direction | yes: `taker_direction` (BUY or SELL, values to be confirmed by the job) | Taker is always the aggressor |
| Maker and taker | yes: `maker`, `taker` | Wallets, not used in M1 |
| Leg traded | yes: `outcome_seq`, `asset_id` | `price` is the leg token price. `p_event` is on the outcome 1 scale |
| Direction flag | yes: `D` (TINYINT, dataset paper) | Meaning not documented locally. The job cross-tabulates it |
| Order book, best bid, best ask, quote midpoint | no | Only fills exist |

### 1.2 Choices

| Choice | Value |
| --- | --- |
| Aggressor side on the outcome 1 scale, `s` | +1 if (`outcome_seq` = 1 and BUY) or (`outcome_seq` = 2 and SELL). −1 if (`outcome_seq` = 1 and SELL) or (`outcome_seq` = 2 and BUY). Other values: `s` = 0, counted |
| Why this mapping | buying outcome 2 at price q is selling outcome 1 at 1 − q. So both are on one axis, the axis of `p_event` |
| Window W | T − 2 days ≤ ts ≤ T − 1 day (closed at both ends). The stale rule keeps `p_age_h` ≤ 24, so every kept market has its `p_ts` trade in W |
| Shares per trade | `usdc_amount / price`, only for `price` > 0. Rows with `price` ≤ 0 are counted and excluded |
| p_vwap (PRIMARY) | volume-weighted average price (VWAP) over W: Σ(`p_event` × shares) / Σ shares |
| p_ask | mean `p_event` of `s` = +1 trades at the last timestamp in W with an `s` = +1 trade (same tie rule as `p_1d`) |
| p_bid | the same for `s` = −1 |
| p_mid | (p_ask + p_bid) / 2. Defined only when both exist. Set S_both = kept markets with p_mid |
| Half-spread proxy h | per market (p_ask − p_bid) / 2 on S_both. Report mean, median, 95% t interval of the mean |
| Taker-buy price only, taker-sell price only | the Q1 analysis on p_ask and on p_bid (each on its own defined set). Shows the direction of the price-rule effect |

- Why VWAP is the primary: it keeps the population at exactly 47,948. It mixes both sides by volume, so a one-sided last fill weighs less.
- p_mid is the price the reviewer names. It is a trade-based proxy, not a quote midpoint. Its set S_both is a subset, so it is secondary.

### 1.3 Sign gate (fixed now, as the R1 index check)

| Median over S_both of (p_ask − p_bid) | Mapping |
| --- | --- |
| > 0 | `s` as defined (validated) |
| < 0 | `s` flipped (validated as flipped). Both medians reported |
| = 0 | no mapping. p_ask, p_bid, p_mid rows skipped, flagged "side not validated". p_vwap still runs |

- Side checks, reported, not in the rule: crosstab of `taker_direction` × `outcome_seq` × `D`. Share of trades where `p_event` = `price` (outcome 1) or 1 − `price` (outcome 2), tolerance 1e-9.

### 1.4 Outputs

| Item | Value |
| --- | --- |
| `m1_prices_by_market.csv` | `market_id`, `p_1d`, `p_vwap`, `p_ask`, `p_bid`, `p_mid`, `h`, `n_trades_W`, `y`, bins under each price |
| Rows next to Q1 | per price: n, chi-square, df, p, w, BH bins off, net gap with CI and d_z, Q1 rule text, row agreement |
| Same-set row | the Q1 analysis on `p_1d` restricted to S_both. p_mid is compared with this row, not with the full Q1 row |
| Paired difference | net gap(p_vwap) − net gap(p_1d) on 47,948, and net gap(p_mid) − net gap(p_1d) on S_both. Mean of per-market (p_1d − p_alt) with 95% t interval and d_z |
| Coverage | n and share of S_both, of p_ask only, of p_bid only |

### 1.5 Reading rule (fixed now)

| Outcome | Condition |
| --- | --- |
| A: not a price-rule artifact | net gap CI under p_vwap is entirely below 0, AND net gap CI under p_mid (S_both) is entirely below 0 |
| B: consistent with a price-rule artifact | net gap CI under p_mid covers 0 or is above 0, AND the same-set `p_1d` CI is below 0 |
| C: mixed | any other case. The report names which price disagrees |
| VWAP only | the sign gate skipped p_mid (§1.3). A if the p_vwap net gap CI is entirely below 0, else B. Row labeled "VWAP only" |

- Side line, reported, not in the rule: |net gap(p_1d)| against the mean of h. If |net gap| ≤ mean h, the paper says "the gap is within half the trade-based spread proxy".
- Why the CI and not a fixed pp line: the net gap is a mean over markets. Its t interval is the noise line (`rules/measurement.md` §1).
- Coverage caveat: if S_both < 50% of 47,948, outcome A or B is stated "on the subset with trades on both sides".

## 2. M2: Yes-oriented calibration

Why: in kept markets, outcome 1 is "Yes" in 63.9% (run 150296, `label1_counts.json` `overall.share_yes_like` 0.6388). "Outcome 1 is priced too high" mixes Yes/No markets with team-name markets.

### 2.1 Choices

| Choice | Value |
| --- | --- |
| Label 2 | `max(outcome_label) FILTER (WHERE outcome_seq = 2)`, rebuilt from raw. Normalized as in `prereg_v1_label_check.md` §2.2 |
| Yes/No market | {label1_norm, label2_norm} = {"yes", "no"} |
| p_yes, y_yes | if label1_norm = "yes": p_yes = `p_1d`, y_yes = y. If label2_norm = "yes": p_yes = 1 − `p_1d`, y_yes = 1 − y |
| Expected | run 150296 has `n_no_like` 0. So p_yes = `p_1d` on every Yes/No market. The job reports the count of each case |
| Sets | Y = Yes/No markets. N = all other kept markets (team, player, Over/Under labels) |
| Statistic | the Q1 analysis on Y with p_yes, y_yes. The same on N with `p_1d`, y |

- Why only the set matters: the chi-square is symmetric to the coding inside a bin (`prereg_v1_label_check.md` §5.1). So the recode cannot move it. Set membership can.
- Inner-edge markets: `checks.n_p1d_on_inner_edge` is reported again for Y.

### 2.2 Outputs

| Item | Value |
| --- | --- |
| `m2_yes_by_market.csv` | `market_id`, `label1_norm`, `label2_norm`, `is_yes_no`, `p_yes`, `y_yes`, `bin_yes` |
| Rows next to Q1 | Y and N: n, chi-square, df, p, w, BH bins off, net gap with CI, d_z, per-bin gap with Wilson and z 95% CI, row agreement |
| Check | n(Y) must be ≥ 30,630 − (markets whose label 2 is not "no"). Count of label2 values for label1 = "yes" is reported |
| Figure | reliability diagram for Y, y axis "Observed Yes rate". It fixes the axis label issue of `fig4_calibration_z.png` |

### 2.3 Reading rule (fixed now)

| Outcome | Condition | Wording proposal |
| --- | --- | --- |
| Yes-bias | Y: chi-square p < 0.05 AND net gap CI entirely below 0 | the paper may add "In Yes/No markets, Yes is priced above its observed rate" |
| No Yes-bias shown | any condition above fails | the paper keeps "outcome 1" only |

- M2 makes a wording proposal only. D-037 is an owner decision. This rule cannot revert it. A change goes to the owner.

## 3. M3: dependence between markets of one event

Why: markets on one event move together. The binomial and chi-square tests assume independent markets (D-034).

### 3.1 Key search

| Source | Event key |
| --- | --- |
| `runs/142041_pilotA_2025_06/schema.csv` (24 columns) | none. No event id, event slug, group id, question id |
| `code/common.py` `mkts_raw` | none. `market_slug` is read but not saved |
| `markets.parquet` of 142082 | none. `market_slug` is not in `mk_stats` |
| `analysis/hf_daily_aligned_listing.txt` | file listing only |
| `CTF/resolutions.parquet` (R1) | `condition_id`, `outcome_slot_count`, `payout_numerators`. No event key |
| `neg_risk` | marks Neg-Risk event bundles. They are dropped by the binary rule, so it groups no kept market |

- Result: no event key exists in our data. The job uses proxies.

### 3.2 Proxy keys

| Proxy | Definition | Weakness |
| --- | --- | --- |
| K1 slug stem | `lower(market_slug)` split on "-". Keep the first 3 tokens, joined by "-". No other stripping. NULL slug: own cluster | ad hoc text rule. Slugs of one event may differ in the first 3 tokens (under-merge). Unrelated slugs may share them, e.g. "will-trump-say" (over-merge) |
| K2 category × close hour | (`category_refined`, `close_at` truncated to the hour, UTC) | merges unrelated markets that close in the same hour (over-merge). Misses events whose markets close at different hours (under-merge) |
| K0 market | `market_id` (iid bootstrap) | method check, not a dependence proxy |

- Error direction: over-merge widens the CI (conservative). Under-merge leaves the CI too narrow.
- Read rule: the proxy with the wider net gap CI is read. Both are reported.
- Cluster counts reported per proxy: number of clusters, median and maximum cluster size, share of markets in clusters of size 1.

### 3.3 Cluster bootstrap

| Choice | Value |
| --- | --- |
| Resampling | draw clusters with replacement, as many as there are clusters. Take all markets of each drawn cluster |
| B | 2,000 |
| Seed | 20261107, `numpy.random.default_rng` |
| Per replicate | per-bin gap (observed − mean price), net gap, chi-square |
| Per-bin CI | percentile 2.5 and 97.5 of the per-bin gap |
| Net gap CI | percentile 2.5 and 97.5 |
| Design effect per bin | deff_b,K = Var_boot,K(gap_b) / Var_boot,K0(gap_b). Cluster bootstrap against the iid market bootstrap |
| Cluster chi-square | X²_cl,K = Σ_b (gap_b / SE_boot,K,b)², df 10. Computed for K0, K1, K2 |
| Cluster BH bins | per-bin z = gap_b / SE_boot,K,b, two-sided normal p, BH at 0.05 |

- Method check: SE_boot,K0,b must lie within ±5% of the analytic sd(y − p | bin b) / sqrt(n_b), for every bin.
- Why ±5%: the Monte Carlo error of a bootstrap SE at B = 2,000 is about 1 / sqrt(2B) = 1.6%. Three times that, rounded, is 5%.
- If any bin fails the check, the K1 and K2 rows are flagged "method check failed". Their numbers are still printed.
- Why not the binomial SE: the iid bootstrap estimates the observed variance of y − p. The binomial SE uses the price p̄(1 − p̄). They differ where a bin is miscalibrated. Example: bin 0 has p̄(1 − p̄) = 0.0179 and ȳ(1 − ȳ) = 0.0135 (`q1_results.json` longshot "0.0-0.1").
- So X²_cl,K0 does not reproduce the main 67.99. The comparison that reads dependence is K1 or K2 against K0, not against 67.99.
- Limit: X²_cl ignores covariance between bins inside one cluster. It is an approximation, stated as such.

### 3.4 Outputs and reading rule

| Item | Value |
| --- | --- |
| `m3_clusters.csv` | `market_id`, `k1`, `k2` |
| `m3_bootstrap.json` | per proxy: cluster counts, per-bin gap with CI and deff, net gap CI, X²_cl, df, p, w_cl = sqrt(X²_cl / n), BH bins off |
| Row next to Q1 | per proxy: X²_cl, df, p, w_cl, BH bins off, net gap CI, row agreement |

| Outcome | Condition |
| --- | --- |
| Robust to the proxy | the read proxy: X²_cl p < 0.05 AND net gap CI entirely below 0 |
| Not robust | X²_cl p ≥ 0.05, or net gap CI covers 0 |

- The Q1 verdict stays as committed. The paper adds the read row and its proxy weakness.

## 4. M4: kept vs dropped markets

Why: 47,948 of 688,131 markets (7.0%) stay. 215,289 have no price at T − 1 day (README filter tree). The kept set may differ from the rest.

### 4.1 Choices

| Choice | Value |
| --- | --- |
| Groups | kept, and each `drop_reason`: updown, non_binary, no_outcome, no_price, stale_price, below_min_trades |
| Main contrast | kept vs eligible-but-dropped (no_price, stale_price, below_min_trades). Up/Down and no_outcome are dropped by design |
| Category | `category_refined`, NULL = "Unknown". Share of the 8 largest kept categories, rest "Other" |
| Volume total | `volume_usdc` (saved) |
| Volume before T − 1 day | Σ `usdc_amount` with ts ≤ T − 1 day (raw pass). Why: pilot volume after `close_at` is 0.340 of all volume |
| Duration | `close_at` − `opens_at` in days. NULL counted |
| Trade count | `n_trades` (all) and `n_trades_before_T1d` (saved) |
| Outcome 1 rate | mean y where y is defined |

### 4.2 Outputs

| Item | Value |
| --- | --- |
| `m4_kept_vs_dropped.csv` | per group: n, share of 688,131, category shares, median and interquartile range (IQR) of each numeric column, outcome 1 rate |
| Main contrast row | kept vs eligible-but-dropped pooled: the same columns. Medians and interquartile range (IQR) carry the comparison |
| Calibration of priced dropped markets | stale_price and below_min_trades have `p_1d` and y. Per group: net gap with t CI, mean squared residual. The Q1 analysis on stale_price |

- M4 is descriptive. No p-value is printed, except the stale_price Q1 row, which carries w next to p.

## 5. M5: practical size

Why: the chi-square p is 1.08e-10 at n 47,948, but w is 0.0377. The reviewer asks how large the miscalibration is in usable terms.

### 5.1 Choices

| Choice | Value |
| --- | --- |
| Model | logit(P(y = 1)) = a + b × logit(p), p = `p_1d`, maximum likelihood, `statsmodels.Logit` |
| Clip | p clipped to [0.001, 0.999] before logit. n clipped is reported |
| CI | Wald 95% from the fit. Also the cluster bootstrap 95% (read proxy of M3, same B and seed) |
| Reading of a, b | b = 1 and a = 0 is calibrated. b < 1: prices too extreme. b > 1: prices not extreme enough. a < 0: outcome 1 less often than priced |
| Implied gap | Δ(p) = expit(a + b × logit(p)) − p at p = 0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95, with bootstrap CI |
| Mean squared residual (Brier) | 0.1071 (saved). Climatology reference = ȳ(1 − ȳ), ȳ = 0.3658 (`class_balance_yes`), in sample |
| Brier skill score | 1 − Brier / climatology. Printed with the note "in-sample climatology" |
| Majority baseline accuracy | max(ȳ, 1 − ȳ) = 0.6342, next to the saved accuracy at 0.5, 0.8343 |

### 5.2 Practical-size line (fixed now)

- Practical line: the mean half-spread proxy h from M1.
- Why: a gap smaller than half the spread cannot be traded against. This line comes from the data, not from a round number.
- Rule: the gap is "practically sized" at price p if |Δ(p)| CI lies entirely above mean h. Else "below the trade-cost line".
- If M1 skips h (sign gate fails), the line is not applied. The report gives Δ(p) only.

### 5.3 Outputs

- `m5_calibration_fit.json`: a, b, Wald CI, bootstrap CI, n clipped, Δ(p) table, climatology, Brier skill score, majority accuracy, saved accuracy.
- Per-market predictions are not new: `p_1d`, y are in `markets.parquet`.

## 6. Minor 4: duplicate rows

Why: the pilot has 155,885 duplicate rows of 3,065,179 (`runs/142041_pilotA_2025_06/duplicates.json`). MVP1 keeps them (README "Fixed values").

### 6.1 Choices

| Choice | Value |
| --- | --- |
| Exact duplicate | rows identical on all raw columns (`SELECT DISTINCT *`) |
| Also reported | count under the pilot 7-column key (`asset_id`, `block_timestamp`, `maker`, `taker`, `price`, `usdc_amount`, `outcome_seq`) |
| Market scope | the 47,948 kept markets. Why: removing exact copies removes no timestamp. So `p_ts` and staleness cannot change. Only the last-timestamp mean and `n_trades_before_T1d` can, and the count only falls. So the new kept set is a subset of the old one |
| Rebuild | `p_1d`, `n_trades_before_T1d`, kept flag, on deduplicated trades |
| Q1 | the Q1 analysis on the new kept set |
| Q2 | top 1% and top 20% volume shares, maker and taker, over the new kept set's deduplicated trades, as `q2_concentration.py` |

### 6.2 Outputs and reading

| Item | Value |
| --- | --- |
| `minor4_dedup.json` | duplicate counts (both keys), share of trades, kept-set change (n in, n out), Q1 row, Q2 shares, deltas in pp |
| Q1 row | chi-square, df, p, w, BH bins off, net gap with CI, row agreement |
| Q2 | descriptive. Delta in pp next to each saved share. No verdict |

## 7. Peer asks

### 7.1 (a) Volume tercile (Hameem Gorabi, "volume x odds")

| Choice | Value |
| --- | --- |
| Volume | volume before T − 1 day (§4.1). Why not `volume_usdc`: it holds trades after T − 1 day, so it looks ahead |
| Terciles | cut points at the 1/3 and 2/3 quantiles over the 47,948 markets, reported. Ties go to the lower tercile |
| Per tercile | the Q1 analysis: n, chi-square, df, p, w, BH bins off, net gap with t CI |
| Volume × odds table | 3 terciles × 10 bins: n, gap, z 95% CI. Cells with n < 30 are shown, marked "small" |
| High vs low | net gap(high) − net gap(low), Welch t 95% interval and p, d next to it |
| Multiplicity | BH over the 3 tercile chi-square p-values |

### 7.2 (b) Close period (Robert Molina, "periods")

| Choice | Value |
| --- | --- |
| Period | calendar year of `close_at`, UTC |
| Small years | a year with fewer than 1,000 kept markets merges into the next later year. Repeat until each group has 1,000 or more. The last group merges backward |
| Per period | the Q1 analysis plus net gap with t CI |
| Multiplicity | BH over the period chi-square p-values |

- Both peer items are descriptive. No verdict.

## 8. Methods and lecture status

Source of status: `analysis/lecture_method_audit.md`, `docs/lecture_concept_map.md`. Constraint: `STATUS.md` Constraints row 1, D-025, D-026.

| Method | Item | Status | Basis |
| --- | --- | --- | --- |
| Exact binomial test per bin, BH | M1, M2, M4, minor 4, peer | in lecture | audit rows 4, 5 |
| Chi-square goodness of fit | same | partly | audit row 7 (already the Q1 form) |
| Mean, quantiles, terciles, median, IQR | M1, M4, peer | in lecture | audit row 40 |
| Volume-weighted mean (VWAP) | M1 | partly | mean is in D4. Weighting by shares is our data rule |
| t interval of a mean | net gap CI | in lecture | D5 s24 (z interval), L11 t-test |
| Welch t interval | peer (a) | partly | audit row 124 |
| Bootstrap percentile CI | M3, M5 | in lecture | D5 s25, s26, concept map §2.4 |
| Cluster resampling | M3 | partly | bootstrap in D5. Resampling clusters is not |
| Chi-square with bootstrap SE (X²_cl) | M3 | not found | our construction |
| Logistic regression | M5 | partly | logistic regression in L21. Calibration use is ours |
| Mean squared residual (Brier) | M5 | not found | audit row 12. D20 s26 has the arithmetic |
| Brier skill score | M5 | not found | depends on Brier |
| Accuracy, majority baseline | M5 | in lecture | audit row 15 |
| Wilson interval | M2 per-bin | not found | audit row 10. The z interval is printed next to it |

## 9. Cost and job shape [estimate]

| Item | Value |
| --- | --- |
| Job | one SLURM job, `-p kimq`, 8 CPU, 64G, no GPU, time limit 3 h |
| Raw passes | build gate (as 142082), one trade pass over the kept markets (about 63,023,987 kept-market trades, `tables_summary.json`), market-level slug and label 2. M4 volume before T − 1 day sums over all in-scope trades, inside the build pass |
| Bootstrap | 3 proxies × 2,000 replicates over 47,948 markets, bincount per bin |
| Logistic fit | one fit plus 2,000 bootstrap refits on 47,948 rows |
| Estimate | 60 to 90 minutes [estimate]. Basis: run 142123 did build, q1, r1, r2 in about 42 minutes (`00.runs.md`) |

## 10. Not in scope

| Item | Status |
| --- | --- |
| T − 7 day horizon | pending owner. MVP2 Q1a (D-016, D-020) |
| M5 fee-adjusted strategy return | not designed. Not in lecture (review tab 3) |
| M6 literature, M7 focus, Vuong test | not a run |

## 11. Open questions for the owner

1. Methods not found in lecture (X²_cl, Brier skill score): keep labeled, or drop (D-025, D-026)?
2. M3: proxy keys only, or fetch event slugs from the Polymarket Gamma API (a new data source)?
3. M2: may a "Yes-bias" outcome lead to a new owner question on D-037 wording?
4. T − 7 day horizon: stays out of scope?

## Owner answers (2026-11-07, D-039)

- Methods outside the lectures (bootstrap chi-square interval, Brier skill score): keep, labeled "outside the lectures" in the paper.
- M3 grouping key: proxies only (first 3 words of `market_slug`; topic × close hour). Report the wider interval. No Gamma API.
- M2: report as a sensitivity row. If Yes is priced too high in Yes/No markets, ask the owner before any D-037 wording change.
- T − 7 day horizon: out of scope (D-020 holds).
