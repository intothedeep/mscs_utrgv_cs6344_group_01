# When Polymarket Says 70%, Does It Happen 70% of the Time?

### Prediction Accuracy, Trading Concentration, and Statistical Distributions in Prediction Markets

**Group 1 | Team Brier**: Taek Lim, Zhugang Liu (Tony), Francisco Cortez

On Polymarket, people bet real money on elections, sports, and crypto prices. A share that pays $1 if an event happens and trades at $0.70 is read as a "70% chance," and news outlets now quote these numbers as facts. Every market eventually ends with a known answer, so we can check this claim: of all the events priced at 70%, did about 70% actually happen? We will test it on **Polymarket-v1**, the full public record of Polymarket's first exchange: about 1.2 billion real trades across 1.3 million markets, from 2022 to 2026.

We ask three questions.

1. **Is the crowd right?** We treat every market as a coin flip whose probability is its price. We then group markets by price and compare predicted with actual outcomes using binomial tests, chi-square tests, confidence intervals, and the Brier score. We also check whether cheap "longshot" bets win less often than their price says.
2. **Who moves the market?** Using wallet addresses, we test whether a few big wallets do most of the trading (an 80/20 power law), with Lorenz curves, the Gini coefficient, and k-means clusters of wallet types.
3. **What does the data look like?** We expect trade sizes and wallet activity to be extremely skewed. We examine them with histograms, QQ plots, log transforms, and KS tests.

All analysis is in Python with DuckDB, without machine-learning models. If "70%" really means 70%, prediction markets are a free, real-time forecast anyone can use. If it does not, we show exactly where the numbers fail, and whether a handful of wallets are behind them.

Data: https://huggingface.co/datasets/TimeSeventeen/Polymarket-v1 · Paper: https://arxiv.org/abs/2606.04217
