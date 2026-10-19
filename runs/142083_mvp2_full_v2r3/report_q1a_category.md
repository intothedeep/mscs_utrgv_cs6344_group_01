# Stage report: q1a_category

**What:** Q1a: does accuracy depend on the topic?

**Why:** Q1a: does the favorite win equally often in every topic, and is the price equally calibrated?

**Input data:** markets.parquet: 47948 kept markets (with min_trades filter), real data. Category = category_refined, categories under 30 markets merged into 'Merged'. Favorite = side with p_1d >= 0.5.

**Output data:** q1a_contingency.csv, q1a_bins_by_category.csv, q1a_markets.csv, q1a_results.json, fig9_calibration_by_category.png

**Result:** Chi-square of independence: chi2=3203.8056862450953, df=7, p=0.0, Cramer's V=0.2584924337963562 (min expected count 109.76253441227998).

Bin tests (n >= 5): 80 of 80 category x bin cells tested. Rejected: Bonferroni 2, BH 9.

Brier across categories: ANOVA F=837.6878226514474, p=0.0, eta squared=0.10898511164820039, permutation p=0.000999000999000999 (1000 perms, seed 42).

Under-represented: merged into 'Merged': none. Sports: {'Sports': 19162}.

n per category, favorite win rate and mean Brier:

| category | won | lost | n | favorite_win_rate | mean_brier |
| --- | --- | --- | --- | --- | --- |
| Sports | 13832 | 5330 | 19162 | 0.7218 | 0.1736 |
| Crypto | 11264 | 624 | 11888 | 0.9475 | 0.03733 |
| Politics | 5991 | 931 | 6922 | 0.8655 | 0.09169 |
| Finance | 4664 | 482 | 5146 | 0.9063 | 0.06652 |
| Other | 1946 | 328 | 2274 | 0.8558 | 0.09594 |
| Culture | 971 | 103 | 1074 | 0.9041 | 0.06615 |
| Sci-Tech | 726 | 93 | 819 | 0.8864 | 0.07893 |
| Price Action | 616 | 47 | 663 | 0.9291 | 0.04927 |

**Figure:** ![calibration by category](fig9_calibration_by_category.png)  Caption: observed Yes rate against mean price per bin, one panel per category, shared axes. Why: a panel off the diagonal shows a topic where the price is miscalibrated. Source: this run folder.

**Status:** ran
