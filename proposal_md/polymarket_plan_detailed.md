# Project Plan: MVP1 and MVP2

**When Polymarket Says 70%, Does It Happen 70% of the Time?**
Group 1 | Team Brier: Taek Lim, Zhugang Liu (Tony), Francisco Cortez

- Class post: `polymarket_proposal_v3.md`
- Concept-by-concept detail: `../docs/lecture_concept_map.md` (sections 6 and 7)

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
| Inspect the data | List tables, columns, sizes, and the date range. Confirm the license | L2 |
| Build a pilot | Run the whole pipeline on **one monthly partition** first, then scale up | — |
| Keep only valid markets | Standard binary (Yes/No) markets with a winning-outcome label. Drop multi-outcome (neg-risk) and Up-Down markets | L2 |
| Remove duplicates | Drop relayer records | L2 |
| Put prices on one scale | Convert NO-token prices to the YES scale: p = 1 − price | — |
| Handle missing values | Drop markets with no outcome. Do not impute | L7 |
| Choose the evaluation price | The last traded price at or before T − 1 day, where T is the market's last trade. Skip a market if that price is more than 24 h older than the evaluation time | — |
| Build the tables | **Market table** and **wallet table**, each with its variable types listed | L3 |

**Market table** (one row per market):
- market_id, category, n_trades, volume_usdc
- p_1d (price 1 day before close), outcome y ∈ {0, 1}

**Wallet table** (one row per wallet):
- wallet, role (maker or taker), volume_usdc, n_trades, n_markets, mean_trade_price

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
| Longshot check: bins 0–10% and 10–20% | L9, L10 | Observed − expected, with CI |

### Q2. Who is the crowd? (Week 2)

| Method | Lecture | Output |
|---|---|---|
| Mean vs. median wallet volume (robustness) | L4 | Summary |
| Top 1%, 5%, 10% volume share (percentiles) | L5 | Table |
| Complementary CDF on log–log axes; test 80/20 rather than assume it | L4, L6 | Fig. 6 |
| Lorenz curve, Gini; compare with the dataset paper (maker 0.970, taker 0.943) | outside | Fig. 7, pipeline check |
| t-test and KS test on log-volume, makers vs. takers | L11 | Test results |
| k-means on z-scored wallet features; choose K by the elbow method | L7, L14, L17 | Fig. 8: elbow plot, cluster summary |
| *Forced:* chi-square test of independence on wallet cluster × market category | L12 | Contingency table |
| *Forced:* ANOVA and permutation test across clusters on mean trade price, a variable not used for clustering | L11, L13 | Test results |
| *Forced:* Spearman correlation between trade count and volume | L14 | ρ and p-value |

### MVP1 is done when

- [ ] The market table and the wallet table are built from the full data (or a documented subset).
- [ ] Figures 1–8 exist.
- [ ] Every row in the MVP1 tables above has a result.
- [ ] Every test reports an effect size (difference, D, ρ) next to its p-value.

## Gate: MVP1 → MVP2

Start MVP2 only if all of the following are true at the end of Week 2:

1. Every MVP1 box above is checked.
2. Queries on the full data finish in minutes, not hours.
3. The team agrees there is time left in Weeks 3 and 4.

If any condition fails, spend Week 3 polishing MVP1.

## MVP2: three sub-questions under Q1 (Week 3)

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
| Outcomes cannot be linked to markets | Q1 is not possible. Submit Q2 + Q3; neither needs outcomes |
| Full data too large for our machines | Use a documented random sample of markets, or a range of monthly partitions |
| Too few markets in a bin or category | Merge bins, and report n and the CI for every bin |
| Every test gives p ≈ 0 because n is about 10⁶ | Interpret effect sizes and CIs, not p-values alone (L10) |
| Clusters are unstable | Rerun with several seeds, and report the result as exploratory (L17) |

## Not in scope

These are left out because they need full position and cash-flow reconstruction:

- Wallet profit and loss
- Win rate per wallet
- Initial capital per wallet
