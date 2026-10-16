# When Polymarket Says 70%, Does It Happen 70% of the Time?

## Prediction Accuracy, Trading Concentration, and Statistical Distributions in Prediction Markets

**Group 1 | Team Brier**
Members: Taek Lim, Zhugang Liu (Tony), Francisco Cortez

## Project Description

On Polymarket, people trade contracts on future events such as elections, sports, and crypto prices. A contract pays $1 if the event happens. If it trades at $0.70, the price is read as a 70% chance. News outlets now quote these numbers as facts. Every market eventually resolves to a known outcome, so the claim can be checked: of all events priced near 70%, did about 70% actually happen?

We also look at who trades. A market price reflects all of its trades, but those trades may come from only a few wallets. Finally, we describe the shape of the data itself: trade sizes, wallet activity, and prices.

## Dataset

**Polymarket-v1** (Qin & Yang, 2026) is the on-chain trade record of Polymarket's first-generation exchange on Polygon, from November 2022 to April 2026. It holds about 1.2 billion trades across 1.3 million markets. Each trade record includes a timestamp, market and token identifiers, price, trade size, maker and taker wallet addresses, and the true trade direction. Market categories and outcomes come from a joined metadata snapshot.

- Paper: https://arxiv.org/abs/2606.04217
- Data: https://huggingface.co/datasets/TimeSeventeen/Polymarket-v1

We will work with resolved **standard binary (Yes/No) markets**. Multi-outcome markets are excluded because their legs are not independent: exactly one candidate wins. Platform relayer records are removed so that the same trade is not counted twice. NO-token prices are converted to the YES scale (1 − p).

## Research Questions

| # | Question | Statistical methods |
|---|---|---|
| 1 | **Prediction accuracy:** Do events priced at *p* happen with frequency *p*? | Probability bins, calibration curve, binomial confidence intervals, Brier score, log loss |
| 2 | **Trading concentration:** Do a few wallets account for most of the trading volume? | Top 1% / 5% / 10% volume share, Pareto chart, Lorenz curve, Gini coefficient |
| 3 | **Distributions:** What do trade sizes, wallet activity, and prices look like? | Histograms, ECDFs, quantiles, skewness, log transform, QQ plots |

## Approach

1. **Build the tables.** Turn trade-level records into (a) one row per market and (b) one row per wallet.
2. **Fix the evaluation time.** For each market, the predicted probability is the last traded price at a set time before the market's final trade, for example 1 day and 7 days before. This avoids using prices after the outcome was already known.
3. **Calibration.** Group markets into 10 probability bins and compare the average price with the observed Yes rate in each bin. The low-probability bins (0–10%) show whether "longshot" events are overpriced.
4. **Concentration.** Compute each wallet's lifetime trading volume, separately for makers and takers, then the Lorenz curve and Gini coefficient. We compare our numbers with those reported in the dataset paper as a check on our pipeline.
5. **Distributions.** Describe trade size and wallet volume on raw and log scales. These are expected to be heavily right-skewed.

## Tools

Python (pandas, NumPy, SciPy, statsmodels, matplotlib) and DuckDB to query the large Parquet files. No machine learning.

## Timeline (4 weeks)

| Week | Work |
|---|---|
| 1 | Data access, schema check, cleaning, market and wallet tables |
| 2 | Calibration and accuracy (Question 1) |
| 3 | Concentration and distributions (Questions 2–3) |
| 4 | Figures, report, presentation |

## Limitations

- A wallet is not a person. One trader can use many wallets, and one wallet (e.g., a market maker) can serve many people.
- Trading volume measures activity, not wealth or profit.
- With about a million markets, almost any difference becomes statistically significant. We therefore report effect sizes and confidence intervals, not only p-values.
