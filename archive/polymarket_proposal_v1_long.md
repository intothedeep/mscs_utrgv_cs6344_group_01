# Group [#] — Team Brier

## Working Title

**When Polymarket Says 70%, Does It Happen 70% of the Time?**

## Idea

Polymarket is the world's largest prediction market, where people bet real money on events such as elections, sports, and crypto prices. A share that pays $1 if the event happens and trades at $0.70 is read as a 70% chance. News outlets now quote these numbers as if they were facts. But are they? Since every market eventually ends with a known outcome, we can check: out of all events priced at 70%, did about 70% actually happen?

## Dataset

**Polymarket-v1** (Qin & Yang, 2026; free on Hugging Face). Every trade on Polymarket's first-generation exchange from November 2022 to April 2026: about 1.2 billion trades across 1.3 million markets. Each trade has a price, an implied probability, a timestamp, a category (politics, sports, crypto, etc.), and the market's final outcome. We will work with a manageable subset of resolved Yes/No markets.

- Paper: https://arxiv.org/abs/2606.04217
- Data: https://huggingface.co/datasets/TimeSeventeen/Polymarket-v1

## Main Question

**Can we trust Polymarket's probabilities?**

Two follow-ups:

1. **Are longshots overpriced?** Do events priced at 5–10% happen less often than the price suggests? (This "longshot bias" is well known in horse racing and sports betting.)
2. **Does the market get smarter over time?** Are prices one day before the end more accurate than prices one week before?

## Hypotheses

- H1: Overall, prices match real-world frequencies.
- H2: Cheap longshot bets win less often than their price implies.
- H3: Uncertainty drops and accuracy improves as the event gets closer.

## Story and Methods

The report is told in five steps. Each step uses techniques from the course.

### Step 1 — Meet the data
*Data, Data and Matrix, Basic Stats, Stats and Visualization*

- Reduce 1.2 billion trades to one table: one row per market, columns = category, total volume, number of trades, probability 7 days before close, probability 1 day before close, final outcome (1 = Yes, 0 = No).
- Summary statistics (mean, median, variance, quantiles) and bar charts: how many markets per category, how volume changed over time.

### Step 2 — What does the data look like?
*Data Distribution, QQ Plot and Normalization*

- Histogram of market probabilities: we expect a U-shape (many markets near 0% or 100%).
- Trading volume per market is expected to be extremely skewed. QQ plot against a normal distribution, then a log transform and a second QQ plot to show the effect.
- Use log-volume (and z-scores where needed) in later steps.

### Step 3 — Is the crowd right?
*Hypothesis Testing, P-value, Chi-Square Test*

- Group markets into 10 probability bins (0–10%, …, 90–100%).
- For each bin, compare the **expected** number of Yes outcomes (sum of the prices) with the **observed** number of Yes outcomes.
- Chi-square goodness-of-fit test across the 10 bins.
  - H0: the market is calibrated (observed = expected).
- Calibration chart: predicted probability vs. actual frequency, with a diagonal reference line.

### Step 4 — Where does it go wrong?
*Multiple Hypothesis Testing, Comparing Distributions*

- Longshot test: one-sided binomial test in each low-probability bin (H1: actual frequency < price).
- Repeat the bin-level tests within each category (e.g., 10 bins × 5 categories = 50 tests). Report raw p-values, Bonferroni, and Benjamini–Hochberg results, and show how many "significant" findings survive correction.
- Chi-square test of independence on a category × (favorite won / favorite lost) table: does accuracy depend on the category?
- Compare the distributions of prices for markets that ended Yes vs. No (Kolmogorov–Smirnov test), at 7 days and 1 day before close. A smart market should separate the two groups more clearly closer to the end.

### Step 5 — How does uncertainty disappear?
*Entropy, Pairwise Association*

- For each market, compute the binary entropy of its price: H(p) = −p log₂ p − (1−p) log₂(1−p). A 50% price has maximum uncertainty (1 bit); 0% or 100% has none.
- Compare average entropy at 7 days vs. 1 day before close: how much uncertainty does the market resolve in the final week?
- Score accuracy two ways: Brier score (squared error) and log loss (cross-entropy).
- Pairwise association: Spearman correlation and scatter plots between log-volume, number of trades, and prediction error. Are busier markets more accurate?

## Tools

Python (pandas, NumPy, SciPy, statsmodels, matplotlib) and DuckDB to query the large Parquet files.

## Planned Figures

1. Market count and volume by category (bar chart)
2. Volume before and after log transform (histograms + QQ plots)
3. Calibration chart: predicted vs. actual
4. Longshot zoom-in (0–20%) with confidence intervals
5. Price distributions of Yes vs. No markets, 7 days vs. 1 day before close
6. Average entropy and Brier score over time to close
7. Correlation heatmap: volume, trades, error
