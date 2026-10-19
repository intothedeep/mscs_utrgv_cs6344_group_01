# Stage report: q2_concentration

**What:** Q2: volume concentration, Gini, role tests, k-means side analysis.

**Why:** Q2: how concentrated is volume across wallets (addresses), and do wallet groups differ?

**Input data:** wallets.parquet: 2117412 wallet x role rows from kept markets. k-means on a fixed-seed sample of 200000 rows (a wallet in both roles has two rows).

**Output data:** q2_results.json, q2_concentration.csv, q2_clusters.csv, fig6_ccdf.png, fig7_lorenz.png, fig8_elbow.png

**Result:** | role | n_wallets | mean | median | top1_share | top5_share | top10_share | gini |
| --- | --- | --- | --- | --- | --- | --- | --- |
| maker | 5.814e+05 | 1.41e+04 | 101.2 | 0.8612 | 0.9465 | 0.9691 | 0.978 |
| taker | 1.536e+06 | 5339 | 86.57 | 0.759 | 0.904 | 0.9478 | 0.9625 |

Paper Gini (full data, reference only): maker 0.97, taker 0.943. Welch t on log10 volume: d=0.177, p=0. KS D=0.057. Spearman rho(n_trades, volume)=0.655. K=4. Chi-square cluster x category: Cramer's V=0.251, p=0. ANOVA on log median trade size: eta^2=0.012, permutation p=0.000999.

**Figure:** ![ccdf](fig6_ccdf.png) ![lorenz](fig7_lorenz.png) ![elbow](fig8_elbow.png)  Caption: wallet volume CCDF (log-log), Lorenz curves, and the k-means elbow (dashed line = chosen K). Why: a curve far below the equality line means few wallets hold most volume. Source: this run folder.

**Status:** ran
