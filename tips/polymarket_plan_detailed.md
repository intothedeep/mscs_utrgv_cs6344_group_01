# Project Plan: MVP1

**When Polymarket Says 70%, Does It Happen 70% of the Time?**
Group 1 | Team Brier: Taek Lim, Zhugang Liu (Tony), Francisco Cortez

- Class post: `../proposal_md/polymarket_proposal_v3.md`
- Concept-by-concept detail: `../docs/lecture_concept_map.md` (section 6)
- Scope: MVP1 only (Q1, Q2, Q3). MVP2 (Q1a, Q1b, Q1c) is out of scope since 2026-11-01. Reason: the owner set the target to MVP1 before the 2026-11-15 deadline (D-016, D-021). Its files are in `../future_work/`.

## Facts in the class post and their sources

Rule: every fact in the class post has a source. If we cannot cite it, we do not write it (owner, 2026-10-18).

| Fact | Source |
|---|---|
| 1.2 billion trades, 1.3 million markets, $61 billion nominal volume, Nov 2022 to Apr 2026 | Dataset paper, abstract |
| Only a small subset of markets lacks a known winner | Dataset paper, limitation 4 |
| In our full run, 62,718 of 688,131 markets (9.1%) have no usable winner label. Our rule is wider than the paper: it also drops markets whose outcome-1 label never traded | `runs/142082_mvp1_full_v1r3/tables_summary.json` (`no_outcome`) |
| Cheap tokens (price under 0.30) pay out 0.2 to 0.3 cents less than their price, counted by trade | Dataset paper, Table 3 (payout − price per token) |
| The paper's Brier panel has 1,019 markets | Dataset paper, Brier panel |
| Top 1% of maker addresses hold 84.1% of maker volume (Gini 0.970) | Dataset paper, Table 5 |
| In horse racing, longshots are overbet, so they win less often than their odds say | Snowberg and Wolfers (2010), abstract, checked on NBER w15923 |

- The dataset paper calls its Table 3 result a "reversal" of the horse-racing bias. Snowberg and Wolfers say longshots are overbet. So the Polymarket result is the same direction. Do not copy the paper's "reversal" wording.
- Posting: the class forum uses a proportional font. Do not use column-aligned tables in the `.txt`. Use one fact line, then one "→" line.

## Strategy

MVP1 is the report we submit: Q1, Q2 and Q3 on one price per market, with only methods from our lectures (D-025).

| Part | Rule |
|---|---|
| Research questions | Q1, Q2, Q3 (the three in the class post) |
| Lecture coverage | Goodness-of-fit form of the L12 chi-square. Other L12 uses stay in the Q2 cluster side analysis only (D-026, D-030) |
| Deadline | 2026-11-15 (D-021) |
| Outputs | Paper (`../papers/paper_mvp1`), 2-page course report (`../papers/course_report_mvp1`), report v1 (`../reports/report_v1.html`) |

## 0. Shared data foundation

Everything else depends on this step.

| Task | Rule | Lecture |
|---|---|---|
| Compute | The pilot and all full-data queries run on the cluster (owner, 2026-10-18). A pass over raw parquet does not run on a laptop | none |
| Inspect the data | List tables, columns, sizes, and the date range. Confirm the license. List the values of `resolution_status`. Confirm how Up-Down markets are marked (`category_refined` or `market_slug`) | L2 |
| Build a pilot | Run the whole pipeline on **one month of daily partitions** of `daily_aligned/` first, then scale up | none |
| Keep only valid markets | Use `daily_aligned/` (`neg_risk = false`). Keep markets with a `winning_outcome_label`. Drop Up-Down markets via `category` / `category_refined` | L2 |
| Remove duplicates | `daily_aligned/` already has relayer records removed. Duplicate rows stay (D-007). The paper tests their removal (Appendix G, duplicate rows) | L2 |
| Put prices on one scale | Use the `p_event` column. Do not recompute it | none |
| Handle missing values | Drop markets with no outcome. Do not impute. Report the number dropped | L7 |
| Close time | T = `close_at`. Why: the pilot shows 51.3% of markets trade after `close_at`, and trades after the outcome is known make p_1d look perfect (D-007) | none |
| Evaluation price | The mean `p_event` at the last timestamp at or before T − 1 day. Skip a market if that price is more than 24 h older than T − 1 day. Why: trades in one block have no order (D-011) | none |
| Minimum-activity filter | Drop markets with fewer than 10 trades before T − 1 day. Why: a price from a nearly empty market is not a crowd view. The cutoff came from the pilot, before any Q1 result (D-007). Report Q1 with and without the filter | L7 |
| Build the tables | **Market table** and **wallet table**, each with its variable types listed | L3 |

**Market table** (one row per market):
- market_id, category, n_trades, volume_usdc
- p_1d (price 1 day before close), outcome y ∈ {0, 1}, where y = 1 means outcome 1 won

**Wallet table** (one row per wallet and role):
- wallet, role (maker or taker), volume_usdc, n_trades, n_markets, mean_trade_price
- A wallet is one address. One person can own many addresses, so "wallet" never means "person"

**Where each field comes from** (`daily_aligned/` columns, checked against the dataset card on 2026-10-17):

| Field | Source column | Needed by |
|---|---|---|
| market_id | `condition_id` | all |
| category | `category`, `category_refined` | Q2 |
| price p | `p_event` | Q1, Q3 |
| outcome y | 1 if `winning_outcome_label` = the `outcome_seq = 1` leg's `outcome_label`, else 0 | Q1 |
| close time T | `close_at` | Q1 |
| trade size | `usdc_amount` | Q3 |
| wallet, role | `maker`, `taker` (taker = aggressor) | Q2, Q3 |

The dataset has no order-book snapshots and no oracle events in the trade layer. Outcomes are in `winning_outcome_label`, and `CTF/resolutions.parquet` is the backup source (check R1).

## MVP1: three questions

### Q3. What does the data look like?

| Method | Lecture | Output in the paper |
|---|---|---|
| Mean, median, mode, range, variance, quantiles | L4, L5 | Summary of price, trade size, wallet volume |
| Histogram, box plot by category, ECDF | L4, L5 | Histograms: Figure 11 (Appendix E). ECDF: Figure 7 (Appendix C) |
| Fit normal, exponential, and power law to trade size and wallet volume | L6 | Table 3 (Section 5.3) |
| QQ plot before and after a log transform | L7 | Figure 5 (trade size), Figure 12 (wallet volume, Appendix E) |
| KS test of each fitted distribution against the data | L11 | D statistic and p-value in Table 3 |
| z-score and robust scaling | L7 | Inputs for the Q2 clustering |

### Q1. Is the crowd right?

**Caution: the close time decides whether Q1 is valid.** Trades can continue after the outcome is known. Then the price "1 day before close" already contains the answer, and calibration looks perfect. T = `close_at` was fixed before any Q1 result (D-007).

| Method | Lecture | Output in the paper |
|---|---|---|
| Treat each outcome as Bernoulli(p); count outcome-1 wins per bin, approximately binomial | L6 | Model statement |
| 10 equal-width bins; equal-frequency bins as a check | L7 | Table 1 |
| H0: observed outcome-1 rate = average price. Binomial test per bin | L9, L10 | p-value per bin |
| 95% z interval per bin, with Bernoulli SD (D-026) | L5, L6, L10 | Figure 3(a), the rate panel |
| Chi-square goodness of fit on the bin × {win, loss} table (D-026) | L12 | χ², degrees of freedom, p-value (the verdict) |
| Bonferroni and BH corrections over the 10 bin tests | L13 | Table 1, corrected p |
| Per-bin gap, observed rate minus mean price (D-026) | L5 | Figure 3(b), the gap panel |
| Mean squared residual of the price (the pre-registration calls it the Brier score); log loss; entropy of p | L15 | Scores in Section 5.1 |
| Market as a p > 0.5 classifier: confusion matrix, precision, recall | L16 | Section 5.1 |
| KS test: price distribution of outcome-1 wins vs. losses | L11 | Figure 7 (Appendix C) |
| Longshot check: bins 0 to 10% and 10 to 20%. Compare with the dataset paper (Table 3 counts per trade, so it differs from our per-market count) | L9, L10 | Section 5.1 |
| Sensitivity checks: R1, R2, M1 to M5, duplicate rows, peer asks (D-013, D-038, D-039) | L9 to L13 | Table 4, Appendix F and G |

### Q2. Who is the crowd?

**Caution: a wallet is one address, not one person.** Write "wallet" or "address" in every result, never "trader" or "person".

**Scope: k-means is a side analysis.** It takes less than 1/10 of the report (owner, 2026-10-18). The main Q2 answer comes from the volume shares. The Lorenz curve is a labeled picture of those shares, outside the lectures (D-028). Gini is removed (D-026).

| Method | Lecture | Output in the paper |
|---|---|---|
| Mean vs. median wallet volume | L4 | Summary |
| Top 1%, 5%, 10%, 20% volume share (percentiles) | L5 | Table 2 |
| Complementary CDF on log–log axes; 80/20 as a descriptive reference (D-024) | L4, L6 | Figure 4 |
| Wallet and volume distributions, top 20% split | L4 | Figures 8 and 9 (Appendix D.1) |
| Lorenz curve | outside | Figure 10 (Appendix D.1) |
| t-test and KS test on log-volume, makers vs. takers | L11 | Test results in Section 5.2 |
| k-means on wallet features: log-transform the heavy-tailed ones, then z-score; choose K by the elbow method | L7, L14, L17 | Appendix D.2 |
| Chi-square test of independence on wallet cluster × market category. Effect size: observed share minus expected share (D-030) | L12 | Appendix D.2 |
| ANOVA and permutation test across clusters on mean trade price, a variable not used for clustering | L11, L13 | Appendix D.2 |
| Spearman correlation between trade count and volume | L14 | Section 5.2 |

### MVP1 is done when

- [x] The market table and the wallet table are built from the full data.
- [x] Every row in the MVP1 tables above has a result. The Q3 box plot is `cs6344_group_01/reports/figures/box_p1d_by_category_group.png` (D-018).
- [x] Every test reports an effect size (difference, D, ρ) next to its p-value.
- [x] The paper's floats match `main.aux`: body Figures 1 to 5 and Tables 1 to 4, appendix Figures 6 to 21 and Tables 5 and 6.

## Gate

The MVP1 gate passed (`../analysis/review_mvp1_rq_r3.md`, `../analysis/review_gate_mvp1_r3.md`). The gate for the restructured paper is `../analysis/review_gate_paper_length.md` (PL-15, D-042).

## Risks and fallbacks

| Risk | Fallback |
|---|---|
| Some markets have no `winning_outcome_label` (paper, limitation 4) | Drop them and report the count. Use `CTF/resolutions.parquet` as a backup source (R1) |
| Too few markets in a bin | Merge bins, and report n and the CI for every bin |
| Every test gives p ≈ 0 because n is about 10⁵ | Interpret effect sizes and CIs, not p-values alone (L10). Check M5 compares the gap with a practical line |
| Markets on one event are not independent. The binomial and chi-square tests assume independence | Check M3 re-tests with a cluster bootstrap over proxy event keys. The proxies are not true event keys. State this limit in the paper (D-039) |
| Clusters are unstable | Rerun with several seeds, and report the result as exploratory (L17) |

## Not in scope

These are left out because they need full position and cash-flow reconstruction:

- Wallet profit and loss
- Win rate per wallet
- Initial capital per wallet

## Future work

- Compare the power law and lognormal on the same data, with the tail start estimated (D-027).
- Did trading change after the 2026 taker fee started? Data: `fee_usdc`, `taker_base_fee`, `block_timestamp`, `category`.
- Does trade direction persist? Autocorrelation of `D` within a market.
