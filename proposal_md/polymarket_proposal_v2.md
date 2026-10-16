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

1. **Prediction accuracy.** Do events priced at *p* happen with frequency *p*?
2. **Trading concentration.** Do a few wallets account for most of the trading volume?
3. **Distributions.** What do trade sizes, wallet activity, and prices look like?

## Approach

Each step lists the course lectures it uses (L = lecture deck number).

### Step 1: Build the data (L2, L3, L7)

- Turn the trade-level records into two data matrices: a **market table** (one row per market) and a **wallet table** (one row per wallet). Classify each variable by type: price and trade size are ratio-scaled, category is nominal, and the outcome is binary (L3).
- Handle the data issues: duplicated rows (relayer records), missing values (markets without an outcome label are dropped, not imputed), and a biased sample (only resolved markets) (L2, L7).
- Fix the evaluation time. For each market, the predicted probability is the last traded price at a set time before the market's final trade, for example 1 day and 7 days before. This avoids using prices after the outcome was already known.

### Step 2: Describe the data (Q3; L4, L5, L6, L7)

- Report mean, median, mode, range, variance, and quantiles. Compare the mean with the median to show how much a few large values pull the mean (robustness; L4, L5).
- Plot histograms, box plots, and violin plots by category, and ECDFs (L4, L5). We expect the price histogram to be U-shaped.
- Fit candidate distributions to trade size and wallet volume: normal, exponential, and power law (L6). Check the fit with QQ plots before and after a log transform, and with a KS test against the fitted distribution (L7, L11).
- Use z-scores and robust scaling (median, IQR) wherever variables on different scales are compared (L7).

### Step 3: Is the crowd right? (Q1; L6, L7, L9, L10, L12, L15, L16)

- Model each outcome as a Bernoulli trial with probability *p*. Within a probability bin, the number of Yes outcomes is then approximately binomial (L6).
- Group markets into 10 equal-width probability bins, and into equal-frequency bins as a robustness check (L7).
- In each bin, test H0: the observed Yes rate equals the average price, using a binomial test and its p-value. Report a 95% confidence interval for each bin, from the normal approximation or a bootstrap (L5, L9, L10).
- Run a chi-square test on the bin × {Yes, No} table of observed and expected counts (L12).
- Score accuracy with the Brier score and log loss. Log loss is the average *surprise* of the outcome that actually happened, and the binary entropy H(p) of a price measures how uncertain the market is (L15).
- Treat the market as a classifier that predicts Yes when *p* > 0.5. Report the confusion matrix, accuracy, precision, and recall, and check for class imbalance between Yes and No outcomes (L16). No model is trained.
- The low-probability bins (0–10%) show whether "longshot" events are overpriced.

### Step 4: Where does it go wrong? (Q1; L11, L12, L13, L14, L15)

- Repeat the bin tests within each category (10 bins × 5 categories = 50 tests). Correct for multiple testing with Bonferroni and Benjamini–Hochberg (L13).
- Test whether accuracy depends on category, using a chi-square test of independence on a category × {favorite won, favorite lost} table (L12) and normalized mutual information with a permutation test (L15).
- Compare Brier scores across categories with ANOVA and with a permutation test that makes no normality assumption (L11, L13).
- Compare the price distributions of markets that resolved Yes and No with a KS test, at 7 days and at 1 day before close. Test whether the per-market error shrinks from 7 days to 1 day with a one-sample t-test on the per-market differences (L11).
- Measure the association between log-volume and per-market error with Spearman correlation, which is robust to outliers, and report its significance (L14).

### Step 5: Who trades? (Q2; L4, L5, L6, L11, L14, L17)

- Compute each wallet's lifetime trading volume, separately for makers and takers. Report the share of volume held by the top 1%, 5%, and 10% of wallets, using percentiles (L5).
- Plot the complementary CDF on log–log axes to check for a power law, and test whether the 80/20 rule holds rather than assuming it (L4, L6).
- Draw the Lorenz curve and compute the Gini coefficient. Compare our values with those reported in the dataset paper as a check on our pipeline.
- Compare the maker and taker volume distributions with a KS test (L11).
- Cluster wallets with k-means on z-normalized features (log-volume, trade count, mean price, number of markets), choosing K with the elbow method. K-means is sensitive to outliers, so the result is treated as exploratory (L14, L17).

## Lecture Coverage

| Lecture | Concepts used | Step |
|---|---|---|
| L2 Data | Data issues: duplicates, missing values, sample bias | 1 |
| L3 Data and Matrix | Data matrix, variable types | 1 |
| L4 Basic Stats | Random variable, PMF/PDF, CDF, robustness | 2, 5 |
| L5 Stats and Visualization | Quantiles, histogram, box/violin plot, CI, bootstrap | 2, 3, 5 |
| L6 Data Distribution | Normal, exponential, power law, Bernoulli, binomial | 2, 3, 5 |
| L7 QQ Plot and Normalization | QQ plot, binning, z-score, robust scaling, log transform, missing values | 1, 2, 3 |
| L9 Hypothesis Testing | Null and alternative hypotheses | 3 |
| L10 P-value | P-value, CI vs. p-value, effect size | 3 |
| L11 Comparing Distributions | t-test, ANOVA, KS test | 2, 4, 5 |
| L12 Chi-Square Test | Contingency table, chi-square test | 3, 4 |
| L13 Multiple Hypothesis Testing | Bonferroni, Benjamini–Hochberg, permutation test | 4 |
| L14 Pairwise Association | Scaling, Pearson vs. Spearman, significance of correlation | 4, 5 |
| L15 Entropy | Surprise, entropy, mutual information (NMI) | 3, 4 |
| L16 Intro to ML | Confusion matrix, precision, recall, class imbalance | 3 |
| L17 Clustering | K-means, elbow method, outlier sensitivity | 5 |

Methods from outside the lectures: calibration curve, Brier score, Lorenz curve, and Gini coefficient. These are cited separately in the report.

## Tools

Python (pandas, NumPy, SciPy, statsmodels, scikit-learn for k-means, matplotlib) and DuckDB to query the large Parquet files. No predictive model is trained.

## Timeline (4 weeks)

| Week | Work |
|---|---|
| 1 | Data access, schema check, cleaning, market and wallet tables (Steps 1–2) |
| 2 | Calibration, accuracy, and tests (Steps 3–4) |
| 3 | Concentration and clustering (Step 5) |
| 4 | Figures, report, presentation |

## Limitations

- A wallet is not a person. One trader can use many wallets, and one wallet (e.g., a market maker) can serve many people.
- Trading volume measures activity, not wealth or profit.
- With about a million markets, almost any difference becomes statistically significant. We therefore report effect sizes and confidence intervals, not only p-values.
