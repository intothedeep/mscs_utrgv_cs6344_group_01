# Project Plan: Phase 1 (MVP1) and Phase 2 (MVP2)

**When Polymarket Says 70%, Does It Happen 70% of the Time?**
Group 1 | Team Brier: Taek Lim, Zhugang Liu (Tony), Francisco Cortez

- Class post: `../proposal_md/polymarket_proposal_v3.md`
- Concept-by-concept detail: `../docs/lecture_concept_map.md` (sections 6 and 7)

## Facts in the class post and their sources

Rule: every fact in the class post has a source. If we cannot cite it, we do not write it (owner, 2026-10-18).

| Fact | Source |
|---|---|
| 1.2 billion trades, 1.3 million markets, $61 billion nominal volume, Nov 2022 to Apr 2026 | Dataset paper, abstract |
| Only a small subset of markets lacks a known winner | Dataset paper, limitation 4 |
| In our full run, 62,718 of 688,131 markets (9.1%) have no usable winner label. Our rule is wider than the paper: it also drops markets whose Yes-side label never traded | `runs/142082_mvp1_full_v1r3/tables_summary.json` (`no_outcome`) |
| Cheap tokens (price under 0.30) pay out 0.2 to 0.3 cents less than their price, counted by trade | Dataset paper, Table 3 (payout − price per token) |
| The paper's Brier panel has 1,019 markets | Dataset paper, Brier panel |
| Top 1% of maker addresses hold 84.1% of maker volume (Gini 0.970) | Dataset paper, Table 5 |
| In horse racing, longshots are overbet, so they win less often than their odds say | Snowberg and Wolfers (2010), abstract, checked on NBER w15923 |

- The dataset paper calls its Table 3 result a "reversal" of the horse-racing bias. Snowberg and Wolfers say longshots are overbet. So the Polymarket result is the same direction. Do not copy the paper's "reversal" wording.
- Removed as unsourced: "news headlines quote the odds as facts" and "nobody checks the odds afterward".
- Posting: the class forum uses a proportional font. Do not use column-aligned tables in the `.txt`. Use one fact line, then one "→" line.

## Strategy

| | MVP1 | MVP2 |
|---|---|---|
| Research questions | Q1, Q2, Q3 (the three in the class post) | Q1–Q3 plus sub-questions Q1a, Q1b, Q1c |
| Lecture coverage | All lecture concepts. Three are used in a forced way (see below) | All lecture concepts, each used naturally |
| Deadline | End of Week 2 | End of Week 3 |
| Start condition | — | MVP1 is done (see the gate) |

MVP1 is the report we can always submit. MVP2 only adds to it. Nothing in MVP1 is thrown away.

The three forced uses in MVP1 are the chi-square test of independence, ANOVA with a permutation test, and Spearman correlation. In MVP1 they enter Q2 through the wallet clusters. In MVP2 they move to Q1a–Q1c, where they answer real questions.

## 0. Shared data foundation (Week 1)

Everything else depends on this step.

| Task | Rule | Lecture |
|---|---|---|
| Compute | The pilot and all full-data queries run on the cluster (owner, 2026-10-18). A pass over raw parquet does not run on a laptop | — |
| Inspect the data | List tables, columns, sizes, and the date range. Confirm the license. List the values of `resolution_status`. Confirm how Up-Down markets are marked (`category_refined` or `market_slug`) | L2 |
| Build a pilot | Run the whole pipeline on **one month of daily partitions** of `daily_aligned/` first, then scale up | — |
| Keep only valid markets | Use `daily_aligned/` (`neg_risk = false`). Keep markets with a `winning_outcome_label`. Drop Up-Down markets via `category` / `category_refined` | L2 |
| Remove duplicates | `daily_aligned/` already has relayer records removed. Check this on the pilot | L2 |
| Put prices on one scale | Use the `p_event` column (YES-scale price). Do not recompute it | — |
| Handle missing values | Drop markets with no outcome. Do not impute. Report the number dropped | L7 |
| Check the close time (pilot) | Measure (last `block_timestamp` − `close_at`) and (`resolved_at` − `close_at`). If many markets trade after `close_at`, set T = `close_at`. Why: trades after the event make p_1d look perfect | — |
| Choose the evaluation price | The last traded price at or before T − 1 day, where T is the market's last trade, or `close_at` if the pilot check says so. Skip a market if that price is more than 24 h older than the evaluation time | — |
| Set a minimum-activity filter | Drop markets with too few trades before T − 1 day. Why: a price from a nearly empty market is not a crowd view. Fix the cutoff from the pilot, before any Q1 result is seen. Report Q1 with and without the filter | L7 |
| Build the tables | **Market table** and **wallet table**, each with its variable types listed | L3 |

**Market table** (one row per market):
- market_id, category, n_trades, volume_usdc
- p_1d (price 1 day before close), outcome y ∈ {0, 1}

**Wallet table** (one row per wallet):
- wallet, role (maker or taker), volume_usdc, n_trades, n_markets, mean_trade_price
- A wallet is one address. One person can own many addresses, so "wallet" never means "person"

**Where each field comes from** (`daily_aligned/` columns, checked against the dataset card on 2026-10-17):

| Field | Source column | Needed by |
|---|---|---|
| market_id | `condition_id` | all |
| category | `category`, `category_refined` | Q1a, Q2 |
| price p | `p_event` | Q1, Q3 |
| outcome y | 1 if `winning_outcome_label` = the `outcome_seq = 1` leg's `outcome_label`, else 0 | Q1 |
| close time T | last `block_timestamp`, or `close_at` (decided by the pilot check above) | Q1, Q1b |
| market open time | `opens_at` (Q1b keeps markets open ≥ 7 days) | Q1b |
| trade size | `usdc_amount` | Q1c, Q3 |
| wallet, role | `maker`, `taker` (taker = aggressor) | Q2, Q3 |
| trade time | `block_timestamp` | Q1b |

The dataset has no order-book snapshots and no oracle events in the trade layer. Outcomes are in `winning_outcome_label`, and `CTF/resolutions.parquet` is the backup source.

## MVP1: three questions

### Q3. What does the data look like? (Week 1)

| Method | Lecture | Output |
|---|---|---|
| Mean, median, mode, range, variance, quantiles | L4, L5 | Summary table for price, trade size, wallet volume |
| Histogram, box plot, violin plot by category, ECDF | L4, L5 | Fig. 1: price histogram (expected U shape). Fig. 2: trade size |
| Fit normal, exponential, and power law to trade size and wallet volume | L6 | Fitted parameters |
| QQ plot before and after a log transform | L7 | Fig. 3 |
| KS test of each fitted distribution against the data | L11 | D statistic and p-value |
| z-score and robust scaling | L7 | Inputs for the Q2 clustering |

### Q1. Is the crowd right? (Week 2)

**Caution: the close time decides whether Q1 is valid.** Trades can continue after the outcome is known. Then the price "1 day before close" already contains the answer, and calibration looks perfect. Do not run Q1 until the pilot close-time check (section 0) has set T.

| Method | Lecture | Output |
|---|---|---|
| Treat each outcome as Bernoulli(p); count Yes outcomes per bin, approximately binomial | L6 | Model statement |
| 10 equal-width bins; equal-frequency bins as a check | L7 | Bin table |
| H0: observed Yes rate = average price. Binomial test per bin | L9, L10 | p-value per bin |
| 95% CI per bin (normal approximation or bootstrap) | L5, L10 | Fig. 4: calibration chart with CIs |
| Chi-square goodness of fit on the bin × {Yes, No} table | L12 | χ², degrees of freedom, p-value |
| Bonferroni and BH corrections over the 10 bin tests | L13 | Table: raw vs. corrected |
| Brier score; log loss read as average surprise; H(p) as market uncertainty | L15 + outside | Scores |
| Market as a p > 0.5 classifier: confusion matrix, precision, recall, class balance of Yes vs. No | L16 | Confusion matrix |
| KS test: price distribution of Yes-resolved vs. No-resolved markets | L11 | Fig. 5: two ECDFs |
| Longshot check: bins 0–10% and 10–20%. Compare with the paper (Table 3: payout − price per token, counted per trade, so it differs from our per-market count) | L9, L10 | Observed − expected, with CI |

### Q2. Who is the crowd? (Week 2)

**Caution: a wallet is one address, not one person.** One person can own many addresses. Write "wallet" or "address" in every result, never "trader" or "person".

**Scope: k-means is a side analysis, not a main result.** It takes less than 1/10 of the report (owner, 2026-10-18). The main Q2 answer comes from the shares, the Lorenz curve, and Gini.

| Method | Lecture | Output |
|---|---|---|
| Mean vs. median wallet volume (robustness) | L4 | Summary |
| Top 1%, 5%, 10% volume share (percentiles) | L5 | Table |
| Complementary CDF on log–log axes; test 80/20 rather than assume it | L4, L6 | Fig. 6 |
| Lorenz curve, Gini; compare with the dataset paper (maker 0.970, taker 0.943) | outside | Fig. 7, pipeline check |
| t-test and KS test on log-volume, makers vs. takers | L11 | Test results |
| k-means on wallet features: log-transform the heavy-tailed ones, then z-score; choose K by the elbow method | L7, L14, L17 | Fig. 8: elbow plot, cluster summary |
| *Forced:* chi-square test of independence on wallet cluster × market category | L12 | Contingency table |
| *Forced:* ANOVA and permutation test across clusters on mean trade price, a variable not used for clustering | L11, L13 | Test results |
| *Forced:* Spearman correlation between trade count and volume | L14 | ρ and p-value |

### MVP1 is done when

- [x] The market table and the wallet table are built from the full data (or a documented subset).
- [x] Figures 1–8 exist.
- [x] Every row in the MVP1 tables above has a result.
- [x] Every test reports an effect size (difference, D, ρ) next to its p-value.

## Gate: MVP1 → MVP2

Start MVP2 only if all of the following are true at the end of Week 2:

1. Every MVP1 box above is checked.
2. Queries on the full data finish in minutes, not hours.
3. The team agrees there is time left in Weeks 3 and 4.

If any condition fails, spend Week 3 polishing MVP1.

## MVP2: three sub-questions under Q1 (Week 3)

**Caution for Q1a: Sports mostly drops out.** Sports is the largest category by market count. Most Sports markets are Neg-Risk (multi-outcome) or Up-Down, so they are not in the Standard Binary sample (paper, limitation 7). Report n per category, and state that Sports is under-represented.

**Caution for Q1b:** it uses the same close time T as Q1 (section 0).

| Sub-question | Method | Lecture | Output |
|---|---|---|---|
| **Q1a. Does accuracy depend on the topic?** | Chi-square test of independence: category × {favorite won, favorite lost} | L12 | Table |
| | Bin tests within each category (10 × 5 = 50), Bonferroni and BH | L13 | Fig. 9: calibration by category |
| | ANOVA and permutation test of Brier score across categories | L11, L13 | Test results |
| **Q1b. Does the market get smarter near the deadline?** | Add p_7d to the market table | — | Data |
| | KS test: Yes vs. No price distributions at 7 days and at 1 day | L11 | Fig. 10 |
| | One-sample t-test on per-market (error at 7 days − error at 1 day) | L11 | Test result |
| | Mean H(p) at 7 days vs. 1 day. The drop is expected by construction; the error change is the real test | L15 | Table |
| **Q1c. Are busier markets more accurate?** | Spearman correlation: log-volume vs. per-market error, with significance | L14 | Fig. 11 |
| | z-score and robust scaling of volume, trade count, and error | L7 | Inputs |

In MVP2 the three forced Q2 tests stay in the report as secondary results. The natural versions in Q1a and Q1c become the main ones.

## Backlog: open after MVP1 is done (owner, 2026-10-18)

Do not start these before the MVP1 gate passes.

| Item | Data | Lecture | Priority |
|---|---|---|---|
| Did trading change after the 2026 taker fee started? Fees started by category: Crypto Jan, Sports Feb, others Mar | `fee_usdc`, `taker_base_fee`, `block_timestamp`, `category` | L11 (t-test), L13 (permutation test) | After MVP1 |
| Does trade direction persist? Autocorrelation of `D` within a market | `D`, `block_timestamp` | L14 | After MVP1 |
| Reword "no machine-learning models" in the class post. k-means (L17) is unsupervised learning. Example: "lecture methods only, no model training" | — | L17 | Done 2026-10-18: "using only methods from our lectures". k-means stays as a side analysis (owner) |

## Timeline

| Week | MVP1 track | MVP2 track |
|---|---|---|
| 1 | Data foundation, Q3 | — |
| 2 | Q1, Q2; the gate decision at the end of the week | — |
| 3 | If the gate failed: polish MVP1 | If the gate passed: Q1a, Q1b, Q1c |
| 4 | Report, slides, presentation | Same |

## Risks and fallbacks

| Risk | Fallback |
|---|---|
| Some markets have no `winning_outcome_label` (paper, limitation 4) | Drop them and report the count. Use `CTF/resolutions.parquet` as a backup source |
| Sports is the largest category but is mostly Neg-Risk or Up-Down (paper, limitation 7) | Q1a under-represents Sports. Report n per category and state this in the report |
| Full data too large for our machines | Use a documented random sample of markets, or a range of monthly partitions |
| Too few markets in a bin or category | Merge bins, and report n and the CI for every bin |
| Every test gives p ≈ 0 because n is about 10⁶ | Interpret effect sizes and CIs, not p-values alone (L10) |
| Markets on one event are not independent (e.g. many markets on one election). The binomial and chi-square tests assume independence | Run the tests per category (Q1a), and state this limit in the report |
| Clusters are unstable | Rerun with several seeds, and report the result as exploratory (L17) |

## Not in scope

These are left out because they need full position and cash-flow reconstruction:

- Wallet profit and loss
- Win rate per wallet
- Initial capital per wallet
