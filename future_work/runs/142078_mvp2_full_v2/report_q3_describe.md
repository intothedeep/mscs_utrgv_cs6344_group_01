# Stage report: q3_describe

**What:** Q3: summary statistics, histograms, ECDF, distribution fits, QQ plots, KS tests.

**Why:** Q3: describe price, trade size and wallet volume before Q1 and Q2 use them.

**Input data:** markets.parquet kept markets (47948), trade_sizes_sample.parquet (1000000 trades, fixed-seed sample), wallets.parquet (2117412 wallet x role rows).

**Output data:** q3_results.json, q3_summary.csv, fig1_fig2_hist.png, ecdf.png, fig3_qq.png

**Result:** Summary:

| index | n | mean | median | mode_50bin_mid | range | variance |
| --- | --- | --- | --- | --- | --- | --- |
| p_1d | 4.795e+04 | 0.3757 | 0.32 | 0.01098 | 0.998 | 0.1263 |
| trade_size_usdc | 1e+06 | 130.3 | 6.934 | 5762 | 5.762e+05 | 2.834e+06 |
| wallet_volume_usdc | 2.117e+06 | 7745 | 91.11 | 9.388e+05 | 9.388e+07 | 6.802e+10 |

Fits and KS (D is the effect size; p is optimistic because parameters are fitted on the same data; power law fitted on the top 10% tail with xmin = the 90% quantile):

| variable | model | KS D | KS p |
| --- | --- | --- | --- |
| trade_size_usdc | normal | 0.4691 | 0 |
| trade_size_usdc | exponential | 0.5352 | 0 |
| trade_size_usdc | power_law | 0.0384 | 1.204e-128 |
| wallet_volume_usdc | normal | 0.4882 | 0 |
| wallet_volume_usdc | exponential | 0.6745 | 0 |
| wallet_volume_usdc | power_law | 0.02392 | 1.152e-105 |

**Figure:** ![hist](fig1_fig2_hist.png) ![ecdf](ecdf.png) ![qq](fig3_qq.png)  Caption: price and trade-size histograms, ECDFs, and QQ plots before and after log. Why: a straight QQ line after log means the log-values are close to normal. Source: this run folder.

**Status:** ran
