# When Polymarket Says 70%, Does It Happen 70% of the Time?

### Prediction Accuracy, Trading Concentration, and Statistical Distributions in Prediction Markets

**Group 1 | Team Brier**: Taek Lim, Zhugang Liu (Tony), Francisco Cortez

**The hook.** News headlines now quote Polymarket odds as if they were facts: "70% chance of X." Those numbers come from people betting real money, but almost nobody checks the scoreboard afterward. We will. **Polymarket-v1** records every trade on Polymarket's first exchange: 1.2 billion trades across 1.3 million markets from 2022 to 2026. Almost every one of those markets ended with a known answer.

**Three questions.**

- **Is the crowd right?** If we collect every event priced at 70%, about 70% should have happened. We test this one price range at a time with binomial and chi-square tests, confidence intervals, and the Brier score. We also ask whether cheap "longshot" bets are a trap.
- **Who is the crowd?** Does a small group of wallets do most of the trading? We look for an 80/20 power law with Lorenz curves and the Gini coefficient, and group wallets into types with k-means.
- **What does betting look like?** We examine trade sizes and wallet activity with histograms, QQ plots, log transforms, and KS tests.

**Why it matters.**

*Why is the hypothesis interesting?*

- Our hypothesis is simple: a price of 70% means a 70% chance.
- Many people already act as if this is true. News sites quote the odds as facts.
- But nobody promised it. Prices come from bettors, not from a forecasting model.
- Betting research shows a known gap. In horse racing, longshots win less often than their odds suggest (Snowberg and Wolfers, 2010).
- Polymarket is a newer and much larger crowd. Does the same gap exist there?
- The dataset paper sees a small gap of the same kind (Qin and Yang, 2026, Table 3).
- On average, tokens priced under 30% paid out 0.2 to 0.3 cents less than their price.
- But the paper counts trades. We count markets, so our answer can differ.

*What will we test?*

- **Calibration:** do events priced at p happen with frequency p?
- **Longshots:** are cheap bets overpriced?
- **Concentration:** do a few wallets do most of the trading?
- **Distributions:** what do trade sizes look like?

*How will we test it?*

- Resolved markets have a known answer. So we can check each price against what happened.
- We group markets by price, count how many events happened, and compare with the price.
- Statistical tests and confidence intervals tell us if a gap is real or only noise.

*Why is it important?*

- **For readers:** it shows when to trust a headline that quotes the odds.
- **For bettors:** it shows which price ranges lose money on average.
- **For research:** a large, open dataset gives a clean test of the "wisdom of crowds".
- If a few wallets set most prices, the "crowd" is a small group. Then the odds may reflect only a few views.

**Bottom line:** if 70% really means 70%, anyone gets a free, live forecast. If it does not, we will show where the odds break, and who is behind them.

*Tools:* Python and DuckDB, using only methods from our lectures.
*Data:* https://huggingface.co/datasets/TimeSeventeen/Polymarket-v1
*Paper:* https://arxiv.org/abs/2606.04217
