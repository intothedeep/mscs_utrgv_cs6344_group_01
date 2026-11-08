# Lecture Concept Map for the Polymarket Project

This file maps each lecture deck in `mscs_utrgv_cs6330_intro_2_ds/notes/` (decks 1–17) to the three research questions in `proposal_md/polymarket_proposal_v3.md` (the class post). The step-by-step plan is in `tips/polymarket_plan_detailed.md`.

Sections 2–5 list every concept that could be used. Section 6 (**MVP1**) places each concept inside the current three questions. Section 7 (**MVP2**) adds three sub-questions under Q1. The schedule and the gate between them are in `tips/polymarket_plan_detailed.md`.

- **Q1:** Prediction accuracy (calibration)
- **Q2:** Wallet trading concentration
- **Q3:** Distributions of trade size, wallet activity, and prices

**Source rule.** A concept marked **[deck N]** appears in that lecture deck. A concept marked **[outside]** is not in any deck, and the report must cite a separate source for it. Deck 8 is not in the `notes/` folder.

## 1. Coverage at a glance

| Deck | Topic | Q1 | Q2 | Q3 | Use in this project |
|---|---|:-:|:-:|:-:|---|
| 2 | Data, data issues | ● | ● | ● | Duplicates (relayer rows), missing outcomes, biased sample |
| 3 | Data and matrix, variable types | ● | ● | ● | Market table and wallet table as n × d matrices |
| 4 | Basic stats, CDF, robustness | | ● | ● | Mean vs. median of wallet volume; CDF |
| 5 | Quantiles, plots, CI, bootstrap | ● | ● | ● | Top-k% shares as percentiles; box/violin plots; bootstrap CI |
| 6 | Distributions (Bernoulli, binomial, power law) | ● | ● | ● | Outcome ~ Bernoulli(p); Pareto 80/20; heavy tails |
| 7 | QQ plot, binning, normalization, log, missing values | ● | ● | ● | Probability bins; log-volume; QQ plots; z-scores |
| 9 | Hypothesis testing | ● | | ● | H0: "a bin is calibrated" |
| 10 | P-value, CI vs. p-value | ● | | ● | Binomial p-value per bin; effect size ≠ p-value |
| 11 | t-test, ANOVA, KS test | ● | ● | ● | Yes vs. No price distributions; maker vs. taker volume |
| 12 | Chi-square test | ● | | ● | Observed vs. expected counts; category × outcome table |
| 13 | Multiple testing, permutation test | ● | | ● | Bonferroni / BH over bins × categories; permutation test |
| 14 | Pairwise association | ● | ● | ● | Spearman: log-volume vs. prediction error |
| 15 | Entropy, mutual information | ● | | ● | Log loss = average surprise; binary entropy of price |
| 16 | Intro to ML | ● | | | Market as a p > 0.5 classifier: confusion matrix, precision, recall, class imbalance (no model training) |
| 17 | Clustering (k-means) | | ● | | Wallet segmentation (exploratory) |

● = core use, ○ = optional

## 2. Q1: Prediction accuracy

### 2.1 Outcome as a Bernoulli trial [deck 6]

- **What.** Each resolved market is one trial with Y ∈ {0, 1}. Its price p is the claimed P(Y = 1).
- **Why.** This states "70% means 70%" as a probability model that can be tested.
- **How.** Within a bin of n markets with mean price p̄, the number of Yes outcomes is approximately Binomial(n, p̄) under H0. This is approximate because prices vary inside a bin; the exact count follows a Poisson-binomial distribution **[outside]**.
- **When.** Use this model whenever the outcome is binary and independent across units. That is why multi-outcome (neg-risk) markets are excluded.
- **Example.** The 0.60–0.70 bin has n = 2,000 markets with p̄ = 0.65. Expected Yes count = 1,300.

### 2.2 Binning: equal-width vs. equal-frequency [deck 7]

- **What.** Discretization turns the continuous price into bins.
- **Why.** Each bin needs enough markets for a stable observed rate.
- **How.** Equal-width bins (0–10%, …, 90–100%) are easy to read. Equal-frequency bins (deciles of price) give every bin the same n. Prices pile up near 0 and 1, so equal-width bins have uneven sizes. Report n per bin either way.
- **When.** Use equal-width for the main chart and equal-frequency as a robustness check.

### 2.3 Hypothesis test and p-value per bin [decks 9, 10]

- **What.** H0: the observed Yes rate in the bin equals p̄. Ha: it does not.
- **How.** Use a binomial test. The deck builds the p-value as P(observation) + P(equally rare) + P(rarer).
- **Example.** Bin 0–10%: n = 10,000, p̄ = 0.05, expected 500 Yes, observed 430. A two-sided binomial test gives p ≪ 0.05, so reject "calibrated" for this bin. The effect is −0.7 percentage points.
- **Caution [deck 10, slide 7].** A small p-value does not mean a large effect. With about 10⁶ markets, almost every bin will be "significant". Always report observed − expected.

### 2.4 Confidence interval and bootstrap [decks 5, 10]

- **What.** Put a 95% CI around each bin's observed rate.
- **Why [deck 10, slide 19].** A CI is more informative than a p-value. The calibration chart shows whether the diagonal falls inside each CI.
- **How.** Use the normal approximation (±1.96 SE), or a bootstrap: resample markets, recompute the bin rate, and take the 2.5th and 97.5th percentiles.

### 2.5 Chi-square test [deck 12]

- **What.** Compare observed and expected counts in a table.
- **How (calibration).** Build a 10 × 2 table: bins × {Yes, No}. The expected Yes count in bin b is the sum of prices; the expected No count is the sum of (1 − prices). χ² = Σ (O − E)² / E over **all 20 cells**. Deck 12 shows the independence version only; this goodness-of-fit form is **[outside]**. Using only the Yes cells is wrong.
- **How (independence).** Build a category × {favorite won, favorite lost} table. H0: accuracy is independent of category. Degrees of freedom = (rows − 1)(cols − 1).

### 2.6 Multiple testing [deck 13]

- **What.** 10 bins × 5 categories = 50 tests.
- **Why.** With m = 50 and α = 0.05, P(at least one false positive) = 1 − 0.95⁵⁰ ≈ 0.92.
- **How.** Report raw p-values, Bonferroni (α / m), and Benjamini–Hochberg (FDR) results side by side.

### 2.7 Entropy and log loss [deck 15]

- **Surprise.** Deck 15 defines the surprise of an event as log(1/p). Log loss is the average surprise of the outcome that actually happened: LL = −(1/N) Σ log p(yᵢ). This places log loss inside the deck's framework. The name "log loss" and its use as a forecast score are **[outside]**.
- **Binary entropy of a price.** H(p) = −p log₂ p − (1 − p) log₂(1 − p) [deck 15, Bernoulli entropy curve] measures how uncertain the market is. H(0.5) = 1 bit; H(0.95) ≈ 0.29 bit.
- **Brier score** BS = mean (pᵢ − yᵢ)² and the **calibration curve** are **[outside]**. Cite Brier (1950) or the dataset paper.

### 2.8 Comparing distributions: KS test [deck 11]

- **What.** Compare the price distribution of markets that resolved Yes with that of markets that resolved No.
- **Why.** A useful market separates the two groups. The KS statistic D is the maximum gap between the two ECDFs.
- **When.** Use KS to compare whole distributions, not just means.

### 2.9 Pairwise association: Spearman [deck 14]

- **What.** Spearman correlation between log(1 + volume) and the per-market squared error (pᵢ − yᵢ)².
- **Why Spearman over Pearson [deck 14, slides 23, 32].** Pearson is sensitive to outliers and assumes linearity. Volume is heavy-tailed.
- **Caution [deck 13, spurious correlations].** Correlation is not causation.

## 3. Q2: Wallet trading concentration

### 3.1 Power law and the 80/20 rule [deck 6]

- **What.** Deck 6 introduces the Pareto distribution and the 80/20 rule: a few items hold most of the mass.
- **How.** Plot the complementary CDF of wallet volume on log–log axes (deck 6, slide 21). A straight line is consistent with a power law.
- **Caution [deck 6, slide 22].** Distinguish a power law from an exponential tail. Do not assume 80/20 in advance.

### 3.2 Quantiles and top-k% shares [deck 5]

- **What.** The "top 1% of wallets" are the wallets above the 99th percentile of volume.
- **How.** S₁ = (volume above the 99th percentile) / (total volume). Repeat for 5% and 10%.

### 3.3 Robustness: mean vs. median [deck 4]

- **What.** The mean is not robust; the median is (deck 4, slides 16, 18).
- **Example.** If the mean wallet volume is far above the median, a few large wallets dominate. Report both.

### 3.4 CDF → Lorenz curve, Gini [deck 4 + outside]

- The CDF is in deck 4. The **Lorenz curve and Gini coefficient are [outside]**.
- A Lorenz curve plots the cumulative share of wallets (sorted from smallest to largest) against the cumulative share of volume.
- Gini = 1 − 2 × (area under the Lorenz curve).
- The dataset paper reports a maker Gini of 0.970 and a taker Gini of 0.943 (Table 5). Use these to check the pipeline.

### 3.5 Log transform and QQ plot [deck 7]

- **How.** Plot a histogram of log₁₀(volume). Compare it with a normal distribution on a QQ plot. Points on the line mean the volume is approximately log-normal.
- **When.** Use a log scale for any heavily right-skewed positive variable.

### 3.6 Maker vs. taker distributions [deck 11]

- **What.** Use a two-sample KS test on log-volume of makers vs. takers.
- **Caution.** With very large n, D matters more than the p-value.

### 3.7 Optional: k-means wallet segments [deck 17]

- **Features.** Log-volume, trade count, mean trade price, and number of markets traded. Z-normalize first (deck 7; deck 14, slide 8: scaling matters).
- **How.** Choose K with the elbow method (deck 17, slide 40).
- **Caution [deck 17, slides 41, 46].** K-means fails with outliers and with clusters of unequal density, and wallet data has both. Treat the result as exploratory only.

## 4. Q3: Distributions

### 4.1 Variable types [deck 3]

| Variable | Type |
|---|---|
| Price p ∈ [0, 1] | Numeric, ratio |
| Trade size (USDC) | Numeric, ratio |
| Category | Categorical, nominal |
| Outcome Y | Binary (Bernoulli) |
| Timestamp | Numeric, interval |

### 4.2 Data matrices [deck 3]

- **Market table:** n markets × d features (category, volume, trade count, p at 7 days before close, p at 1 day before close, Y).
- **Wallet table:** n wallets × d features (volume, trade count, maker share).

### 4.3 Data-quality issues [deck 2, slides 10–11]

| Deck issue | Instance in this data |
|---|---|
| Duplicated rows | Relayer records (about 53% of nominal trades) |
| Missing values | Markets with no winning-outcome label |
| Biased sample | Only resolved, standard binary markets are kept |
| Categories badly chosen | Category labels come from a single metadata snapshot |

Handle missing values by dropping them (deck 7, slide 25). Imputing an outcome is not valid.

### 4.4 Descriptive statistics and plots [decks 4, 5]

- Report mean, median, mode, variance, range, and quantiles (25th, 50th, 75th, 90th, 99th).
- **Histogram** of prices: expect a U shape, with mass near 0 and 1.
- **Box plot or violin plot** of log trade size by category.
- **ECDF**: the empirical version of the CDF [deck 4].

### 4.5 Normalization [deck 7]

- **z-score:** for comparing variables on different scales.
- **Robust scaling (median, IQR):** for heavy-tailed variables.
- **Log transform:** to reduce skew before plotting or correlating.

### 4.6 Comparing groups [decks 11, 13]

- **What.** Do Brier scores differ by category?
- **How.**
  - ANOVA compares group means (deck 11).
  - A permutation test makes no normality assumption (deck 13): shuffle the category labels and recompute the statistic. 1,000 shuffles give a minimum p-value of 0.001.
- **When.** Prefer the permutation test because Brier scores are not normally distributed.

### 4.7 Mutual information (optional) [deck 15]

- **What.** NMI between category and outcome correctness.
- **How.** Use a permutation test for significance (deck 15, slide 26).

## 5. Concepts the report needs from outside the decks

| Concept | Where it is used | Suggested source |
|---|---|---|
| Brier score | Q1 | Brier (1950), *Monthly Weather Review* |
| Calibration curve / reliability diagram | Q1 | Any forecast-verification text |
| Log loss as a forecast score | Q1 | Link to deck 15 surprise; cite a scoring-rule reference |
| Chi-square goodness of fit (both cells) | Q1 | Standard statistics text |
| Poisson-binomial distribution | Q1 | Standard probability text |
| Lorenz curve, Gini coefficient | Q2 | Standard inequality-measurement reference |
| Favorite–longshot bias | Q1 | Snowberg & Wolfers (2010); dataset paper, Table 3 |

## 6. MVP1: coverage with the current three questions only

The current Q1–Q3 can cover every lecture concept without new research questions, provided the methods are chosen on purpose. Most concepts fit naturally. Three can only enter Q2 by way of the k-means wallet clusters (deck 17).

**Fit:** *natural* means the concept answers the question directly. *Moderate* means it works but is not the obvious choice. *Forced* means it is added mainly to cover the concept.

| Concept | Deck | Where | Fit | Concrete use |
|---|---|---|---|---|
| Hypothesis test, H0/Ha, p-value | 9, 10 | Q1 | natural | H0: "the bin's observed Yes rate = its average price"; binomial test per bin |
| Chi-square goodness of fit | 12 | Q1 | natural | Bin × {Yes, No} table, observed vs. expected counts |
| Multiple testing (Bonferroni, BH) | 13 | Q1 | natural | 10 bins = 10 tests, even without categories |
| KS test | 11 | Q1, Q3 | natural | Q1: price distributions of Yes vs. No markets. Q3: fitted vs. empirical distribution |
| Entropy | 15 | Q1 | natural | Log loss as the average surprise of the outcome that happened; H(p) as market uncertainty |
| Mean vs. median, robustness | 4 | Q2 | natural | Mean wallet volume far above the median is a sign that a few wallets dominate |
| z-score, robust scaling | 7 | Q2, Q3 | natural | Normalize k-means inputs. Deck 14: an unscaled large variable dominates the distance |
| Variable types, data matrix | 3 | Data preparation | natural | Define the market table and the wallet table |
| t-test | 11 | Q2 | moderate | Mean log-volume of makers vs. takers |
| Chi-square test of independence | 12 | Q2 | forced | Wallet cluster × market category: which markets do the big wallets trade? |
| ANOVA, permutation test | 11, 13 | Q2 | forced | Compare clusters on a variable **not** used to build them (e.g., mean trade price), to avoid circular results. Deck 17, slide 21 recommends reviewing clusters with such variables |
| Spearman correlation | 14 | Q2 | forced | Wallet trade count vs. volume. A strong positive correlation is expected, so the finding adds little |

## 7. MVP2: add three sub-questions under Q1

The concepts marked *forced* in Section 6 become natural if Q1 gains three sub-questions. Q1b and Q1c revive H3 and Step 5 of the first proposal (`archive/polymarket_proposal_v1_long.md`).

| Sub-question | Concept | Deck | Concrete use |
|---|---|---|---|
| **Q1a. Does accuracy depend on the topic?** (politics, sports, crypto, …) | Chi-square test of independence | 12 | Category × {favorite won, favorite lost} table |
| | Multiple testing | 13 | 10 bins × 5 categories = 50 tests |
| | ANOVA, permutation test | 11, 13 | Brier score by category. Brier scores are not normal, so the permutation test fits better |
| **Q1b. Does the market get smarter near the deadline?** (7 days vs. 1 day before close) | KS test | 11 | How far apart the Yes and No price distributions are at each time point |
| | t-test | 11 | One-sample t-test on per-market (error at 7 days − error at 1 day) |
| | Entropy | 15 | Drop in mean H(p) from 7 days to 1 day |
| **Q1c. Are busier markets more accurate?** | Spearman, significance of correlation | 14 | Log-volume vs. per-market error |
| | z-score, robust scaling | 7 | Comparing volume, trade count, and error on one scale |

**Cautions.**

- In Q1b the drop in entropy is expected by construction: prices move toward 0 or 1 as resolution nears. The test that matters is whether the error (Brier score, log loss) falls.
- In Q1c a correlation is not causation (deck 13, spurious correlations). Category and market duration are possible confounders.

### Comparison

| Criterion | Current Q1–Q3 only | Add Q1a–c |
|---|---|---|
| Lecture coverage | All | All |
| Number of questions | 3 | 6 |
| Class post (v3) | Unchanged | Unchanged if Q1a–c stay in the detailed plan only |
| Forced methods | 3 (chi-square independence, ANOVA/permutation, Spearman) | None |
| Spearman result | Trade count vs. volume: expected, little new | Volume vs. error: answers "are busier markets more accurate?" |

### Applies to both options

With about 10⁶ markets, the t-test, ANOVA, and chi-square tests will almost always give p ≈ 0. Always report an effect size next to the p-value: the mean difference, the KS statistic D, or the correlation coefficient.
