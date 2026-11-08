# When Polymarket Says 70%, Does It Happen 70% of the Time?

**Group 1 | Team Brier**: Taek Lim, Zhugang Liu (Tony), Francisco Cortez
CS 6344 Introduction to Data Science, UTRGV

Do Polymarket prices behave like real probabilities? Who does the trading? What does the trading data look like? We answer these questions with statistics on Polymarket-v1.

The dataset paper (Qin & Yang, 2026) reports about 1.2 billion trades across 1.3 million markets, 2022–2026. Our runs use 688,131 markets in scope and keep 47,948 of them. Source: `runs/142082_mvp1_full_v1r3/tables_summary.json` (`n_markets_in_scope`, `n_kept`). The filter rules are in [How we filter the data](#how-we-filter-the-data).

This README is a step-by-step guide to MVP1 (minimum viable product 1: the smallest complete working version of the project). Start with [Current status](#current-status).

## Current status

As of 2026-11-02: **the analysis is done. The project-end fixes are applied. The owner parts remain.**

```
 data --> runs --> Q1 --> Q2 --> Q3 --> robustness --> report v1 --> paper v1
 done     done     done   done   done   done           done          4 owner parts open
```

| Part | State | Detail |
| --- | --- | --- |
| Data | Done | Downloaded to the cluster. 688,131 markets in scope |
| Runs | Done | Final MVP1 run is `142082_mvp1_full_v1r3` |
| Q1 (is the crowd right?) | Done | Pre-registered verdict is issued |
| Q2 (who is the crowd?) | Done | Yes. Far beyond the 80/20 reference. No pre-registered verdict. The 80/20 rule and the power law are descriptive references (D-024, D-025) |
| Q3 (what does the data look like?) | Done | Box plot added 2026-11-01 (D-018) |
| Robustness | Done | Run `142123_robust_full_v4` and run `142140_q1eqfreq_v5` |
| Lecture-method picks | Applied 2026-11-01 | D-026 to D-028. Report v1 and the paper text use them. See step 14 |
| MVP1 gate review | Passed 2026-11-01 | Third review: 0 blocker, 0 major, 4 minor (`analysis/review_mvp1_rq_r3.md`) |
| Project-end fixes | Applied 2026-11-02 | D-029 to D-031. Report v1 and the paper match. See step 15 |
| Report v1 | Built, project-end fixes done | File: `reports/report_v1.html`. Owner review is open |
| Paper v1 | Built, owner text open | 4 `\todo{owner: ...}` parts remain. The new text is in |
| Course deadline | 2026-11-15 | D-021 |

MVP2 is out of scope until the owner goes for it (D-016, D-020). Its files are in `future_work/`.

Terms: RQ means research question. The RQ list and its status are in `RQ.md`.

Source: `PLAN.md`, `STATUS.md`, `00.runs.md`, `DECISIONS.md` D-016, D-017, D-020 to D-031, `analysis/review_mvp1_rq_r3.md`, `analysis/review_project_end_analyst.md`, `analysis/review_project_end_reviewer.md`.

## Results so far

**Q1 says prices are not calibrated as a whole. The effect is small and runs one way: outcome 1 (the first-listed outcome) is priced too high. Q2 says the top wallets do most of the trading by USDC volume, far beyond the 80/20 reference. Q2 and Q3 have no pre-registered verdict.**

These results apply to the 47,948 kept markets only. For Q2, volume is in USDC. It sums every trade in those markets, including trades after T - 1 day. Rows are wallet and role. Trade counts were not measured. They do not cover the other markets in scope. The kept markets are resolved Yes/No markets with a fresh price one day before the close and at least 10 trades.

| Question | Answer | Key numbers | File |
| --- | --- | --- | --- |
| RQ1 / Q1: is the crowd right? | Verdict: "Prices are not calibrated as a whole at this n." | See the Q1 table below | `runs/142082_mvp1_full_v1r3/verdicts.json` |
| RQ2 / Q2: who is the crowd? | Yes by USDC volume, far beyond the 80/20 reference. The top 20% of wallets hold 98.9% (makers) and 98.0% (takers) of volume. No pre-registered verdict | See the Q2 table below | `runs/142082_mvp1_full_v1r3/q2_results.json` |
| RQ3 / Q3: what does the data look like? | Described, no verdict. Prices are U-shaped. Sizes are right skewed | See the Q3 table below | `runs/142082_mvp1_full_v1r3/q3_results.json` |

Q1 numbers. Chi-square is the goodness-of-fit form of the Lecture 12 test: observed counts against the counts the prices predict. The effect size is the per-bin gap, the observed rate minus the mean price. The z interval (Lecture 5) is the 95% range around each observed rate. BH (Benjamini-Hochberg) is a correction for many tests at once. The mean squared residual of the price is the mean squared gap between price and outcome. The pre-registration calls it the Brier score.

| Item | Value | File and key |
| --- | --- | --- |
| Markets tested (n) | 47,948 | `verdicts.json` `comparisons.Q1.n` |
| Chi-square (df 10) | 67.99 | `verdicts.json` `comparisons.Q1.statistic.value` |
| p-value | 1.08e-10 | `verdicts.json` `comparisons.Q1.p` |
| Largest per-bin gap | -0.0329 (bin 7, counting from 0) | `reports/lecture_numbers.json` `largest_gap.diff_obs_minus_price`, `largest_gap.bin` |
| Bins where the 95% z interval leaves the mean price outside | 5 of 10: bins 0, 1, 6, 7, 8. The same bins as BH | `reports/lecture_numbers.json` `z_interval_95.n_outside`, `bins_outside`, `same_bins` |
| Bins off after BH correction | 5 of 10 | `verdicts.json` `comparisons.Q1.extra.bins_off_bh` |
| Bins off after Bonferroni correction | 4 of 10 | `verdicts.json` `comparisons.Q1.extra.bins_off_bonferroni` |
| Mean squared residual of the price | 0.1071 | `verdicts.json` `comparisons.Q1.extra.brier` |
| Bins with the observed rate below the price | 9 of 10 (the same count without the minimum-trade filter and in equal-frequency bins) | `reports/lecture_numbers.json` `gap_direction.*.n_negative` |
| Net gap, all kept markets | -0.99 percent points, 475 fewer Yes outcomes than the prices imply | `gap_direction.main.net_gap`, `n_yes_minus_expected` |
| Largest chi-square contributor | bin 0, 31.3% of the chi-square | `chi2_largest_contributor` |

How to read the effect:

- The effect is small, and it runs one way. In 9 of 10 bins the outcome-1 rate is below the price, so outcome 1 (the first-listed outcome) is priced too high.
- The largest per-bin gap is 3.29 percent points (bin 7). It is only one number, so read the direction and the net gap with it.
- We set no size line before the results. So "small" is our reading.
- Read the gaps before the p-value.

Longshot statement. With the minimum-trade filter, the two cheapest bins pay off less than their price. Without the filter it holds only in part. Bin 0 flips to +0.0005 (BH p 0.6006). Bin 1 is -0.0093 (BH p 0.1362). Neither bin is off. File: `reports/lecture_numbers.json` `no_min_filter_longshot_bh`.

Limit. The tests assume independent markets. Markets on one event are not independent, so the p-values are optimistic. The z intervals use the same assumption, so they may be too narrow. No event-level count is saved, so the size of this effect is unknown.

Q2 numbers. A maker places a resting order. A taker fills it. A wallet is one address.

| Item | Makers | Takers | File and key |
| --- | --- | --- | --- |
| Wallets | 581,435 | 1,535,977 | `q2_results.json` `concentration.*.n_wallets` |
| Volume share of the top 1% of wallets | 86.1% | 75.9% | `q2_results.json` `concentration.*.top1_share` |
| Volume share of the top 20% of wallets | 98.9% | 98.0% | `q2_results.json` `concentration.maker.top20_share`, `concentration.taker.top20_share` |

There is no pre-registered test for Q2, so it has no verdict line. The 80/20 rule (Pareto principle: 20% of the units hold 80% of the total) is a descriptive reference (D-024). Both the 80/20 rule and the power law are lecture content (`notes/6_DataDistribution.pptx`, slide 19). The class post named 80/20 before any result (`proposal_md/polymarket_proposal_v3.md` line 12).

Pipeline check against the dataset paper: our top 1% maker share is 86.1%, and the paper's is 84.1% (Qin and Yang 2026, Table 5). The populations differ. The paper covers the full data, and our wallets come from the kept markets. We read the paper's value as a reference only.

The Lorenz curve is now a full curve, drawn from all wallets (D-031). It is labeled as outside the lectures. Its use: area and height show the share of wallets against the share of volume, against the 80/20 reference. The Gini coefficient is removed (D-026).

Figures for Q2 (cluster runs `145892_ccdf_v6` and `145893_walletdist_v7`, drawn from `wallets.parquet` of run 142082). Pairs share a row in the paper when both stay readable at half width (D-033):

| Figure | Layout in the paper | File |
| --- | --- | --- |
| CCDF (complementary cumulative distribution function, the share of wallets above a volume), ranks sampled from the top | full width | `reports/figures/fig6_ccdf_top_sampled.png` |
| Maker: wallet distribution, top 20% split | pair (a) | `reports/figures/wallet_dist_maker_count.png` |
| Maker: volume distribution, top 20% split | pair (b) | `reports/figures/wallet_dist_maker_volume.png` |
| Taker: wallet distribution, top 20% split | pair (a) | `reports/figures/wallet_dist_taker_count.png` |
| Taker: volume distribution, top 20% split | pair (b) | `reports/figures/wallet_dist_taker_volume.png` |
| Lorenz curve, maker | pair (a) | `reports/figures/wallet_lorenz_maker.png` |
| Lorenz curve, taker | pair (b) | `reports/figures/wallet_lorenz_taker.png` |

Figures for Q3 (run `145897_q3figs_v8`, redrawn from saved points):

| Figure | Layout in the paper | File |
| --- | --- | --- |
| Histogram of the price p_1d | pair (a) | `reports/figures/hist_price_p1d.png` |
| Histogram of trade size. One sampled trade falls past the last bin edge by float rounding, so the plot holds one trade fewer than the sample | pair (b) | `reports/figures/hist_trade_size.png` |
| QQ plot of trade size, raw and log side by side (a comparison) | full width | `reports/figures/qq_trade_size_raw_log.png` |
| QQ plot of wallet volume, raw and log side by side (a comparison) | full width | `reports/figures/qq_wallet_volume_raw_log.png` |

The CCDF tail bends downward at the largest wallets. So it is not a straight line on log-log axes. The earlier "long straight tail" was a plotting artifact of the old sampling (`analysis/review_project_end_analyst.md` A1).

Power law on the top 10% tail of wallet volume (D-025). No new run. The numbers come from the saved fit.

| Item | Value | File and key |
| --- | --- | --- |
| alpha (power-law exponent of the density, not the CCDF slope) | 1.788 | `runs/142082_mvp1_full_v1r3/q3_results.json` `fits.wallet_volume_usdc.power_law.alpha` |
| xmin (tail starts at) | 3,450 USDC | `fits.wallet_volume_usdc.power_law.xmin` |
| n_tail (wallet-role rows in the tail, both roles pooled) | 211,742 | `fits.wallet_volume_usdc.power_law.n_tail` |
| D (KS distance) | 0.0239 | `fits.wallet_volume_usdc.power_law.D` |
| p (KS) | 1.15e-105 | `fits.wallet_volume_usdc.power_law.p` |

Limits:

- We ran no p-value test for the 80/20 comparison.
- The KS test rejects an exact power law. Large samples also reject small gaps.
- Fitted parameters make the KS p too large. So the rejection stands.
- So we do not say wallet volume follows a power law, and we set no line for how close it is.
- We do not say the power law fits best. Normal and exponential were fit on all data. The power law was fit on the tail only. Lognormal was not compared.
- Future work could compare the power law and lognormal on the same data, with the tail start estimated (D-027). No such analysis runs now.

Side analysis: k-means clusters against topic category (D-030, Lecture 12 chi-square of independence). It runs on the 200,000 sampled wallet-role rows. Chi-square 6,653.0 (df 21), p below 0.0001. The effect size is the largest observed minus expected share in one cell. That cell is cluster 2, Sports. It has 6.7% observed and 8.2% expected, a gap of -1.49%. No Cramér's V. Files: `reports/lecture_numbers.json` `cluster_category_gap`, `runs/145892_ccdf_v6/cluster_category_crosstab.csv`. k-means stays a short side analysis.

Q3 numbers. USDC is a dollar-pegged token. The price column is the price one day before the close.

| Item | Value | File and key |
| --- | --- | --- |
| Price, median | 0.32 | `q3_results.json` `summary.p_1d.median` |
| Price, mean | 0.376 | `q3_results.json` `summary.p_1d.mean` |
| Price, 25th and 75th percentile | 0.015 and 0.66 | `q3_results.json` `summary.p_1d.q25`, `q75` |
| Trade size, median | 6.93 USDC | `q3_results.json` `summary.trade_size_usdc.median` |
| Trade size, mean | 129.8 USDC | `q3_results.json` `summary.trade_size_usdc.mean` |
| Wallet volume, median | 91.1 USDC | `q3_results.json` `summary.wallet_volume_usdc.median` |
| Wallet volume, mean | 7,745 USDC | `q3_results.json` `summary.wallet_volume_usdc.mean` |
| Power law fit, trade size | alpha 1.875 | `q3_results.json` `fits.trade_size_usdc.power_law` |
| Power law fit, wallet volume | alpha 1.788 | `q3_results.json` `fits.wallet_volume_usdc.power_law` |

Trade size uses a fixed sample of 1,000,000 trades (`q3_results.json` `notes.trade_size_sample_rows`). The power law is a fit to the top 10% of values. Normal and exponential were fit on all data, so the fits are not like for like. Lognormal was not compared. We do not call the power law the best fit.

Robustness checks leave the Q1 verdict unchanged:

| Check | Result | File |
| --- | --- | --- |
| No minimum-trade filter (74,474 markets) | Same verdict. Chi-square 214.2 | `runs/142082_mvp1_full_v1r3/q1_results.json` `no_min_filter` |
| Drop the markets with unclear payouts (47,901 left) | Same verdict. 4 bins off after BH | `runs/142123_robust_full_v4/r1_results.json` `q1_sensitivity` |
| Equal-frequency bins | 7 of 10 bins off after BH. The z interval marks 8, because it also marks the lowest bin (1 Yes in 4,795). It has no correction for ten bins. It is unreliable when a bin has very few Yes outcomes | `runs/142140_q1eqfreq_v5/q1_bins_eqfreq.csv` `reject_bh`. `reports/lecture_numbers.json` `z_interval_95.bins_equal_frequency` |

The reviewer's reading is in `analysis/review_mvp1_rq.md`. It recomputed the Q1 verdict from saved files. The numbers above come from the run files.

Source: `runs/142082_mvp1_full_v1r3/verdicts.json`, `q1_results.json`, `q2_results.json`, `q3_results.json`, `tables_summary.json`, `runs/142123_robust_full_v4/r1_results.json`, `runs/142140_q1eqfreq_v5/q1_bins_eqfreq.csv`.

## How we got here, step by step

Why this section exists: it shows what was done in what order, and why. The Q1 criteria were fixed before any Q1 result. That order protects the verdict.

```
1 download --> 2 pilot inspect --> 3 fix criteria --> 4 pilot end to end
                                                            |
 8 robustness <-- 7 final MVP1 run <-- 6 review, fix <-- 5 first full run
      |
 9 equal-frequency fix --> 10 report v1, paper v1 --> 11 gate review: ISSUE
                                                            |
                                          12 target narrowed to MVP1
                                                            |
                                          13 third gate review: PASS
                                                            |
                                          14 audit picks applied
                                                            |
                                          15 project-end fixes
```

Steps 1 to 10 happened on 2026-10-19. Steps 11 to 14 happened on 2026-11-01. Step 15 happened on 2026-11-02.

### Step 1. Download data (D-003)

- What: download `daily_aligned/` (1,248 files) and `CTF/resolutions.parquet` to the cluster.
- Why: `daily_aligned/` is the analysis layer. Resolutions are the backup outcome source.
- Output file: data on the cluster, in `~/cs6344_polymarket/data/`. It is not in this repo. The size listing is `analysis/hf_daily_aligned_listing.txt`.
- Status: done.

### Step 2. Pilot inspection, run 142041 (D-004, D-005)

- What: inspect one month of markets (`close_at` in 2025-06). Never pair a price with an outcome.
- Why: choose the close-time rule and the minimum-trade cutoff without seeing any Q1 result.
- Output file: `runs/142041_pilotA_2025_06/report_pilot_inspect.md`. It found 3,841 markets and 3,065,179 trades.
- Status: done.

### Step 3. Fix the criteria before any Q1 result (D-007)

- What: set T to `close_at`, the minimum to 10 trades, and keep duplicate rows. Write the Q1 test and its lines.
- Why: a cutoff chosen after the result could follow the result.
- Output file: `analysis/prereg_mvp1.md`.
- Status: done.

### Step 4. Pilot end to end, run 142056

- What: run the whole pipeline once on the pilot set.
- Why: find broken stages on a small set first.
- Output file: `runs/142056_mvp1b_pilot_2025_06/summary.md`. It kept 726 of 2,063 markets.
- Status: done. Stage q3 failed on a SciPy call and was fixed. This cycle gets no verdict.

### Step 5. First full run, 142057

- What: run all four stages on every market in `daily_aligned/`.
- Why: get the first full-data result.
- Output file: `runs/142057_mvp1_full_v1/summary.md`. It kept 47,948 of 688,131 markets.
- Status: done. Superseded by run 142082.

### Step 6. Review and fix, code v3 (D-011)

- What: a reviewer checked the first full runs. Fixes went into code v3, and the runs were redone.
- Why: trades in one block have no order. So "last price" needed a tie rule, and the samples needed a fixed order.
- Output file: `analysis/review_mvp1_mvp2.md`. It found 0 blockers, 8 major and 16 minor findings.
- Status: done. The tie rule changed after the first Q1 result. The verdict did not change. The amendment is in `analysis/prereg_mvp1.md`.

### Step 7. Final MVP1 run, 142082

- What: rerun build, Q3, Q1, Q2 and verdicts with code v3.
- Why: this run is the source of all MVP1 numbers.
- Output file: `runs/142082_mvp1_full_v1r3/` (see `verdicts.json` and `summary.md`).
- Status: done.

### Step 8. Robustness, run 142123 (D-013)

- What: two descriptive checks on the kept markets. R1 looks at split payouts. R2 looks at the price path in the last day.
- Why: the class questions left both limits open.
- Output file: `runs/142123_robust_full_v4/report_r1_split_payout.md` and `report_r2_price_path.md`.
- Status: done. The Q1 verdict is the same without the split-payout markets.

### Step 9. Equal-frequency correction, run 142140

- What: rerun Q1 only, so the BH p-values for equal-frequency bins are saved.
- Why: a paper review (F9) asked for a saved number, not a recomputed one.
- Output file: `runs/142140_q1eqfreq_v5/q1_bins_eqfreq.csv`.
- Status: done.

### Step 10. Report v1 and paper v1

- What: build the HTML report and the LaTeX paper from the saved run.
- Why: the report and the paper are the deliverables.
- Output file: `reports/report_v1.html` and `papers/paper_mvp1/main.pdf`.
- Status: built. A paper review passed (`analysis/review_papers.md`). Report gate fixes are done (step 12). Paper text is still open. See [What is left](#what-is-left).

### Step 11. Gate review, 2026-11-01

- What: a reviewer checked whether MVP1 answers RQ1, RQ2 and RQ3, from saved outputs only.
- Why: the end of MVP1 is a gate.
- Output file: `analysis/review_mvp1_rq.md`.
- Status: result ISSUE (0 blockers, 2 major, 9 minor).
- The Q1 verdict reproduces exactly.
- Major G1: the Q3 plan row names a box plot, and none exists.
- Major G3: the Mission said "every resolved market", but we test the kept markets.
- Minor: the k-means block takes 10.03% of the report text, against a limit of under 1/10.
- Minor: RQ2 is a yes/no question with no pre-registered line.

### Step 12. Target narrowed to MVP1 (D-016, D-017, D-018, D-019, D-020)

- What: the owner chose MVP1 only. MVP2 files moved to `future_work/`. The box plot was drawn locally from saved files. The Mission now names the markets actually tested. The Vision line stays.
- Why: these picks close or explain G1 and G3 and set the scope.
- Output file: `DECISIONS.md`, `PLAN.md`.
- Status: decided. The box plot and the report fixes are done. The k-means share is below the 0.100 limit, not remeasured after D-026. The limit is 1/10 of the report text. The earlier measure counted characters of the extracted report text (`analysis/review_mvp1_rq_r3.md` G14).

### Step 13. Third gate review, 2026-11-01 (D-022)

- What: a reviewer checked the four "MVP1 is done when" boxes again, from saved files.
- Why: the owner asked for a third review beyond the usual two (D-022). The second review had found an ISSUE (step 11).
- Output file: `analysis/review_mvp1_rq_r3.md`.
- Status: PASS (0 blocker, 0 major, 4 minor). The Q1 verdict reproduces. The four minor findings are record gaps (G14 to G17). They are rows in [What is left](#what-is-left).
- Same day, the owner decided how RQ2 closes (D-024, D-025). The title stays. The 80/20 rule and the power law are descriptive references.

### Step 14. Lecture-method picks applied (D-026, D-027, D-028)

- What: the owner picked from the lecture-method audit, and the picks went into report v1 and the paper text. Chi-square goodness of fit stays, labeled as a form of the Lecture 12 test. The Brier score is now the mean squared residual of the price. Eta squared is now SSB/(SSB+SSW). Per-bin gaps replace Cohen's w. The z interval replaces the Wilson interval. The log10 mean difference replaces Cohen's d. Gini, Cramér's V, the adjusted Rand index and Cohen's d_z are removed. The cluster chi-square was removed here and returned in step 15 (D-030). Lorenz stays as a labeled figure, now a full curve (D-031).
- Why: the owner rule (D-025) says all analysis stays within lecture contents. Owner, with Claude Code, applied the picks.
- Output file: `reports/lecture_numbers.json`, `reports/report_v1.html`, `papers/paper_mvp1/main.tex`, `papers/paper_mvp1/numbers.tex`. The audit is `analysis/lecture_method_audit.md`.
- Status: done for report v1 and the paper text. The prereg files and `runs/` stay as committed. A dated note in `analysis/prereg_mvp1.md` records the departure. It adds lines and changes no rule. No numbers changed. Only names, intervals and the removed methods changed.
- The paper text says the departure in one sentence. The verdict rule and the verdict sentence are unchanged.
- Two picks changed on 2026-11-02: the cluster chi-square returned (D-030) and Lorenz became a full curve (D-031). See step 15.

### Step 15. Project-end fixes (D-029, D-030, D-031)

- What: the project-end review (`analysis/review_project_end_analyst.md` A1 to A7, `analysis/review_project_end_reviewer.md` G18 to G28) found readings that went further than the numbers. Two cluster jobs redrew the figures. The main session submitted them. Report v1 and the paper then took the fixes.
- Why: the owner asked for the CCDF redraw (D-029), the cluster chi-square back with an effect size (D-030), and the full wallet distributions and Lorenz curve (D-031).
- Runs: `145892_ccdf_v6` (CCDF with ranks sampled from the top, cluster by category crosstab) and `145893_walletdist_v7` (wallet and volume distributions, full Lorenz curve, no Gini).
- Fixes now in the report, the paper and this README:
  - A3: the effect is small, runs one way, and has no size line set in advance.
  - A2: the longshot statement holds with the minimum-trade filter only.
  - A4: the independence limit covers the p-values and the z intervals.
  - A1, A5: the CCDF tail bends. The exponent is reported with the KS rejection. We do not say it follows a power law.
  - A6: the Q2 answer is by USDC volume, in the kept markets, in wallet-role rows, with trades after T - 1 day.
  - A7: the size comparison with the dataset paper is direction only.
  - Equal-frequency bins: the z interval marks 8, BH marks 7, and the extra bin has 1 Yes in 4,795.
- G7 closes by a ledger line. `verdicts.json` stays as committed (D-031).
- Output file: `reports/report_v1.html`, `papers/paper_mvp1/main.tex`, `papers/paper_mvp1/numbers.tex`, `reports/lecture_numbers.json`.
- Status: done. The paper builds with 0 errors. The paper puts pairs in one row where both stay readable (D-032, D-033). One older PNG still holds two panels: `fig_r1_split_payout.png`. Its right panel compares calibration with and without the unclear markets.

Rebuild after fetching the two new runs (`bash jobs/fetch_run.sh 145892_ccdf_v6` and `bash jobs/fetch_run.sh 145893_walletdist_v7`, from `cs6344_group_01/`):

```bash
OMP_NUM_THREADS=1 timeout 300 uv run python code/lecture_numbers.py --run runs/142082_mvp1_full_v1r3 --ccdf-run runs/145892_ccdf_v6
OMP_NUM_THREADS=1 timeout 300 uv run python code/make_report.py --run runs/142082_mvp1_full_v1r3 --version v1 --out reports/report_v1.html --q1eqfreq runs/142140_q1eqfreq_v5
```

Then regenerate `papers/paper_mvp1/numbers.tex` with the command in `papers/README.md`.

Source: `STATUS.md` log, `00.runs.md`, `DECISIONS.md`, `analysis/review_mvp1_mvp2.md`, `analysis/review_mvp1_rq.md`, `analysis/review_mvp1_rq_r3.md`, `analysis/review_papers.md`.

## What is left

State as read from `PLAN.md` on 2026-11-01, updated on 2026-11-02 for the project-end fixes. Rows under "MVP1 gate 2026-11-01" are the open work.

| Work | Who | State |
| --- | --- | --- |
| Fill the null `criteria_sha256_12` in `verdicts.json` (G7) | Owner | Done 2026-11-02 by a ledger line. `verdicts.json` stays as committed (D-031) |
| Redraw the CCDF with the top tail sampled (A1) | Main session, cluster job | Done 2026-11-02. Run `145892_ccdf_v6` (D-029) |
| Draw the wallet and volume distributions and a full Lorenz curve | Main session, cluster job | Done 2026-11-02. Run `145893_walletdist_v7` (D-031) |
| Apply the project-end text fixes A1 to A7 to report v1, the paper and this README | Owner, with Claude Code | Done 2026-11-02 (D-029, D-030, D-031) |
| Add a citation note to the Up/Down row of `analysis/prereg_mvp1.md` (G5) | Owner, with Claude Code | Done 2026-11-01 |
| Edit `papers/paper_mvp1/main.tex` for the Up/Down reason and build warnings (G5, G13) | Owner, with Claude Code | Done 2026-11-01 |
| Update `00.runs.md` with partition, CPU count and env (G11, G12) | Owner, with Claude Code | Done 2026-11-01 |
| Compare the `markets.parquet` hash of run 142082 with run 142140 | Owner, on the cluster | Open |
| Review report v1 and record notes in `STATUS.md` | Owner | Open |
| Split `code/make_report.py` (about 800 lines) in its own commit | Owner, with Claude Code | Open |
| Add the 80/20 and power law comparison to `reports/report_v1.html` and `papers/paper_mvp1/main.tex` | Owner, with Claude Code | Done 2026-11-01 |
| Add a note in `analysis/prereg_mvp1.md` for the 80/20 reference, the Up/Down citation and the departures (D-026, D-028) | Owner, with Claude Code | Done 2026-11-01 |
| Fix the report wording "Closest of the three fits" | Owner, with Claude Code | Done 2026-11-01. The fits are not ranked |
| Update `docs/team_split_design.html`: deadline, Mission wording, `paper_mvp2` (review G16) | Owner, with Claude Code | Done 2026-11-01. The 3-person split stays "Not yet" |
| Note that the box plot's input comes from `jobs/fetch_run.sh` (review G17) | Owner, with Claude Code | Done 2026-11-02 |
| Lecture-method audit: `analysis/lecture_method_audit.md`. Owner rule (D-025): all analysis stays within lecture contents. Of 52 methods, 35 are in lecture, 7 partly, 10 not found. None of the 10 feeds the Q1 verdict. The owner's picks are applied to MVP1 (D-026 to D-028) | Owner, with Claude Code | Done 2026-11-01 |

The audit picks are applied. The paper's 4 `\todo{owner: ...}` parts and the 3-person work split are "Not yet" (owner, 2026-11-01).

The paper milestone (M4) now needs `paper_mvp1` only (D-023). The `paper_mvp2` files stay in `future_work/`.

Decisions still open:

| Decision | State |
| --- | --- |
| The 3-person work split | Not yet (owner, 2026-11-01) |
| Whether team text may fill the owner `\todo` parts | Not yet (owner, 2026-11-01) |

Decided on 2026-11-01: how RQ2 closes (D-024, D-025). The title stays. The 80/20 rule and the power law are descriptive references.

Course deadline: 2026-11-15 (D-021).

The split options A (stable), B (scalable) and C (cutting-edge) are a proposal only. See `docs/team_split_design.html`.

The paper has 4 `\todo{owner: ...}` parts in `papers/paper_mvp1/main.tex`:

| Part | State |
| --- | --- |
| Related work | Open |
| Interpretation | Open |
| Wider implications | Open |
| Closing | Open |

The new lines of 2026-11-02 keep sentences to 15 words or fewer. After the owner text is in, the paper still needs a pass on the older long sentences (F5).

Source: `PLAN.md` "Open tasks" and "MVP1 gate 2026-11-01", `analysis/review_mvp1_rq.md`, `analysis/review_mvp1_rq_r3.md`, `DECISIONS.md` D-021 to D-028, `docs/team_split_design.html`.

## How to read the outputs

Read in this order. Each step builds on the one before.

| Order | File | What it gives |
| --- | --- | --- |
| 1 | `reports/report_v1.html` | The full story in steps, with tables and figures |
| 2 | `papers/paper_mvp1/main.pdf` | The paper draft with the same numbers |
| 3 | `runs/142082_mvp1_full_v1r3/summary.md` | Links to each stage report of the final run |
| 4 | `tips/polymarket_mvp1_preprocessing_tips.html` | Why each filter exists |

Open the HTML file in a browser. The PDF is a draft with open text parts. Numbers in the report and paper come from the saved run files. Do not retype them.

## Research questions

| | Question | MVP |
|---|---|---|
| Q1 | Is the crowd right? Do events priced at *p* happen with frequency *p*? | MVP1 |
| Q2 | Who is the crowd? Do a few wallets do most of the trading? | MVP1 |
| Q3 | What does the data look like? Trade sizes, wallet activity, prices | MVP1 |

The MVP2 questions (Q1a, Q1b, Q1c) are in [future_work/README.02.md](future_work/README.02.md).

## Where things are

| File | What it is |
|---|---|
| `proposal_md/polymarket_proposal_v3.md` | **Current class post** (short proposal) |
| `tips/polymarket_plan_detailed.md` | **Current plan**: MVP1, gate, MVP2, timeline, risks |
| `docs/lecture_concept_map.md` | Lecture decks mapped to each question (section 6 = MVP1, section 7 = MVP2) |
| `polymarket_v1_paper.pdf` | Dataset paper (Qin & Yang, 2026) |
| `reports/` | HTML report v1 (`report_v1.html`) |
| `runs/` | One folder per cluster run: tables, figures, JSON results, stage reports |
| `analysis/` | Criteria fixed before results (`prereg_*`) and reviewer reports (`review_*`) |
| `papers/` | LaTeX paper v1 in `paper_mvp1/`, with `numbers.tex` made from run files |
| `code/` | Python pipeline: build tables, Q1, Q2, Q3, robustness, report, paper numbers |
| `jobs/` | SLURM job scripts and the fetch script |
| `PLAN.md`, `STATUS.md`, `DECISIONS.md`, `00.runs.md` | Plan, progress log, decision log, run ledger |
| `archive/` | Earlier proposal drafts, kept for reference |
| `future_work/` | MVP2 files, kept for later if time allows (D-017) |

## Data we use

We read trades, prices and outcomes from the Polymarket-v1 dataset. The runs use real data, not generated data.

- Dataset: https://huggingface.co/datasets/TimeSeventeen/Polymarket-v1
- Paper: https://arxiv.org/abs/2606.04217

```
Polymarket-v1 (Hugging Face)
 |-- daily_aligned/       USED    1,248 files, 13.2 GB. One row per trade.
 |-- CTF/resolutions.parquet  USED    backup outcome source. Robustness check only.
 `-- OrderFilled/         NOT USED  raw tape with relayer records
```

| Layer or file | Used? | What it gives us | Why |
| --- | --- | --- | --- |
| `daily_aligned/*.parquet` | Yes | Trades, prices, outcomes, topics, wallets | The plan names it the analysis layer |
| `CTF/resolutions.parquet` | Yes, robustness only | Payout numbers per market | Backup outcome source. It checks for split payouts |
| `OrderFilled/` | No | Raw tape with relayer records | Rejected in D-003. `daily_aligned/` has relayer records removed |

Where it lives: the UTRGV Cradle cluster, in the project folder `~/cs6344_polymarket/data/`. All data queries run there. The laptop only draws figures from saved outputs.

Sizes of the real runs:

| Item | Value | Where it comes from |
| --- | --- | --- |
| Markets in scope, full run | 688,131 | `tables_summary.json` `n_markets_in_scope` |
| Markets kept (10 or more trades) | 47,948 | `tables_summary.json` `n_kept` |
| Trades in kept markets | 63,023,987 | `tables_summary.json` `n_trades_in_kept_markets` |
| Wallet rows (wallet and role) | 2,117,412 | `tables_summary.json` `n_wallet_role_rows` |
| Pilot markets (`close_at` in 2025-06) | 3,841 | `report_pilot_inspect.md` |
| Pilot trades | 3,065,179 | `report_pilot_inspect.md` |
| Pilot Standard Binary markets | 2,063 | `report_pilot_inspect.md` |

Which field carries the information each question needs:

| Information | Source column | Used by (MVP1 question) |
| --- | --- | --- |
| Market id | `condition_id` | all |
| Topic | `category`, `category_refined` | Q2 |
| Price (Yes side) | `p_event` | Q1, Q3 |
| Outcome y (1 = the Yes leg won, 0 = it lost) | `winning_outcome_label` and the `outcome_seq = 1` leg's `outcome_label` | Q1 |
| Close time T | `close_at` | Q1 |
| Trade size | `usdc_amount` | Q3 |
| Wallet and role | `maker`, `taker` | Q2, Q3 |

A wallet is one address. It is never one person.

Source: `tips/polymarket_plan_detailed.md` (section 0), `DECISIONS.md` D-003, `runs/142082_mvp1_full_v1r3/tables_summary.json`, `runs/142082_mvp1_full_v1r3/report_build_tables.md`, `runs/142041_pilotA_2025_06/report_pilot_inspect.md`, `analysis/hf_daily_aligned_listing.txt`, `code/common.py`, `CLAUDE.md` (repo root).

## How we filter the data

We filter to keep one clean price per market. Each market counts once, at its first failing rule.

```
688,131 markets in scope
  |-- Up/Down market          drop 255,420
  |-- not binary              drop       0
  |-- no winner label         drop  62,718
  |-- no price at T - 1 day   drop 215,289
  |-- price older than 24 h   drop  80,230
  |-- under 10 trades         drop  26,526
  v
 47,948 markets kept
```

In the full run, "in scope" means every market in `daily_aligned/`.

The not-binary rule dropped no market. The file lists no count for it, and the other counts sum to 688,131.

Without the 10-trade rule, 74,474 markets stay. Q1 is also reported on that set.

| Filter (in order) | Rule | Why |
| --- | --- | --- |
| Up/Down | Drop a market if `market_slug` has `up-or-down` or `updown`. Also drop it if `category_refined` matches `up%down` or `updown` | Dataset paper: "fundamentally different settlement mechanics" (section 6), "should not be pooled" (limitation 5) |
| Not binary | Keep a market with at most 2 `outcome_seq` values and `neg_risk` not true | Dataset paper: Neg-Risk markets "require a separate normalization" (section 6) and "should not be pooled" (limitation 5) |
| No winner label | Drop a market with no usable y | We do not impute. The rule also drops a market whose Yes-side label never traded |
| No price | Drop a market with no trade at or before T - 1 day | There is no price to test |
| Stale price | Drop a market if the price is older than 24 h | Plan rule: skip a price more than 24 h older than the evaluation time |
| Minimum trades | Drop a market with fewer than 10 trades before T - 1 day | A price from an almost empty market is not a crowd view |

Fixed values, set before any Q1 result:

| Item | Fixed value | Why |
| --- | --- | --- |
| Evaluation time T | `close_at` | 0.513 of pilot markets have a trade after `close_at` |
| Evaluation price | Mean `p_event` of the trades at the last timestamp at or before T - 1 day | Trades in one block have no order. The mean makes it deterministic |
| Minimum trades | 10 before T - 1 day | Chosen from the pilot (Job A) before any Q1 result |
| Duplicate rows | Kept | No row id tells a repeat fill from a copy. The pilot has 155,885 duplicate rows of 3,065,179 |
| Stale price limit | 24 h | Plan rule |

The MVP2 sub-questions add their own filters. See [future_work/README.02.md](future_work/README.02.md).

Source run: `runs/142082_mvp1_full_v1r3`.

Source: `runs/142082_mvp1_full_v1r3/tables_summary.json`, `analysis/prereg_mvp1.md`, `analysis/prereg_mvp1_full.json`, `runs/142041_pilotA_2025_06/report_pilot_inspect.md`, `code/common.py`, `code/build_tables.py`, `DECISIONS.md` D-007, D-011.

## Criteria

We fixed the tests, the significance line and the effect size before we saw results. The files are `analysis/prereg_mvp1.md` and `analysis/prereg_robustness.md`. This section lists criteria only. The MVP2 criteria are in [future_work/README.02.md](future_work/README.02.md).

Terms used below:

- Significance line: p below 0.05 (alpha, the false-alarm limit).
- Mean squared residual of the price: mean squared gap between price and outcome. The pre-registration calls it the Brier score.
- BH (Benjamini-Hochberg): a correction for many tests at once.
- CI (confidence interval): the range that likely holds the true value.
- Per-bin gap: the observed rate minus the mean price in one price bin. It is the effect size.
- z interval: the observed rate plus or minus 1.96 standard errors (Lecture 5).

| Question | Primary test | Significance line | Effect size | Counts as yes | Counts as no |
| --- | --- | --- | --- | --- | --- |
| Q1: is the crowd right? | Chi-square goodness of fit over 10 equal-width price bins | p < 0.05 | Observed rate minus mean price per bin, with a 95% z interval. Mean squared residual of the price | p < 0.05: prices are not calibrated as a whole | No bin off after BH and p >= 0.05: no evidence of miscalibration at this n |

- Q1 also checks each bin with a binomial test, corrected by BH at 0.05. A bin is off when its corrected p is below 0.05.
- Departure from `analysis/prereg_mvp1.md` (D-026): the prereg names a Wilson interval, the Brier score and Cohen's w. Report v1 and the paper use the z interval, the mean squared residual and the per-bin gaps. The verdict rule and the verdict sentence are unchanged. The prereg file stays as committed.
- The pilot run is a first end-to-end cycle. It gets no verdict. The verdict applies to the full-data run.

Descriptive only, no verdict:

| Part | Status |
| --- | --- |
| Q2 and Q3 | No pre-registered test or verdict in the prereg files. The 80/20 rule and the power law are descriptive references, not verdict lines (D-024, D-025) |
| R1: split payouts | Descriptive. Adds a sensitivity row next to Q1 and never replaces it |
| R2: price path in the last day | Descriptive. No new primary test |

R1 and R2 check Q1. They come from run `142123_robust_full_v4`. R2 groups topics with fewer than 30 kept markets as "Merged".

Amendment, honest record:

- We changed the evaluation price rule after we saw the first full Q1 result (run 142057).
- Old rule: the last trade at or before T - 1 day. Trades in one block have no order, so this was undefined.
- New rule: the mean price at the last timestamp. The reason was determinism, not the result.
- The verdict did not change.

Source: `analysis/prereg_mvp1.md`, `analysis/prereg_robustness.md`, `DECISIONS.md` D-005, D-007, D-011, D-013.

## Constraints

| Constraint | Source |
| --- | --- |
| All analysis stays within lecture contents. k-means is a side analysis, under 1/10 of the report | owner, 2026-10-18; D-025, D-026 (2026-11-01); plan Q2 |
| A method outside the lectures is renamed or replaced. Lorenz is a labeled figure, now a full curve (D-028, D-031). The cluster chi-square test returned with a share-gap effect size (D-030) | D-026, D-028 |
| Every fact in a class post has a source. No source, no claim | owner, 2026-10-18; plan "Facts in the class post" |
| All data queries run on the cluster. The laptop only draws figures from saved outputs | root `CLAUDE.md`, 2026-10-18 |
| T, the minimum-trade cutoff and the Q1 criteria are fixed before any Q1 result | D-005, D-007 |
| Write "wallet" or "address", never "trader" or "person" | plan Q2 |
| Every test reports an effect size next to its p-value | plan "MVP1 is done when" |

Source: `STATUS.md` "Constraints" table.

## Tools

Python (pandas, NumPy, SciPy, statsmodels, scikit-learn, matplotlib) and DuckDB.

## Course assignment: proposal thread

One member of each team creates a thread with:

- Group number and team name
- Working title
- Brief description of the idea
- Description of the dataset
- Main question, hypothesis, problem, or objective
- Methods, tools, or approaches being considered

Each student responds to at least 4 classmates' threads. Responses cover what is interesting or promising about the idea, and suggestions for improvement or clarification.

