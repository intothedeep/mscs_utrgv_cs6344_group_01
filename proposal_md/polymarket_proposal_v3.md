# When Polymarket Says 70%, Does It Happen 70% of the Time?

### Prediction Accuracy, Trading Concentration, and Statistical Distributions in Prediction Markets

**Group 1 | Team Brier**: Taek Lim, Zhugang Liu (Tony), Francisco Cortez

**The hook.** News headlines now quote Polymarket odds as if they were facts: "70% chance of X." Those numbers come from people betting real money, but almost nobody checks the scoreboard afterward. We will. **Polymarket-v1** records every trade on Polymarket's first exchange: 1.2 billion trades across 1.3 million markets from 2022 to 2026. Every one of those markets ended with a known answer.

**Three questions.**

- **Is the crowd right?** If we collect every event priced at 70%, about 70% should have happened. We test this one price range at a time with binomial and chi-square tests, confidence intervals, and the Brier score. We also ask whether cheap "longshot" bets are a trap.
- **Who is the crowd?** Does a small group of wallets do most of the trading? We look for an 80/20 power law with Lorenz curves and the Gini coefficient, and group wallets into types with k-means.
- **What does betting look like?** We examine trade sizes and wallet activity with histograms, QQ plots, log transforms, and KS tests.

**Why it matters.** If 70% really means 70%, anyone gets a free, live forecast. If it does not, we will show where the odds break, and who is behind them.

*Tools:* Python and DuckDB, with no machine-learning models.
*Data:* https://huggingface.co/datasets/TimeSeventeen/Polymarket-v1
*Paper:* https://arxiv.org/abs/2606.04217
