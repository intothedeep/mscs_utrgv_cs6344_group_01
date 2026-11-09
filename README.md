# When Polymarket Says 70%, Does It Happen 70% of the Time?

**Group 1 | Team Brier**: Taek Lim, Zhugang Liu (Tony), Francisco Cortez
CS 6344 Introduction to Data Science, UTRGV

Do Polymarket prices behave like real probabilities? Who does the trading? What does the trading data look like? We answer these questions with statistics on Polymarket-v1.

The dataset paper (Qin & Yang, 2026) reports about 1.2 billion trades across 1.3 million markets, 2022–2026. Our runs use 688,131 markets in scope and keep 47,948 of them. Source: `runs/142082_mvp1_full_v1r3/tables_summary.json` (`n_markets_in_scope`, `n_kept`). The filter rules are in [How we filter the data](#how-we-filter-the-data).

This README is a step-by-step guide to MVP1 (minimum viable product 1: the smallest complete working version of the project). Start with [Current status](#current-status).

Scope: MVP1 only (Q1, Q2, Q3). MVP2 (Q1a, Q1b, Q1c) is out of scope, by the owner's choice on 2026-11-01 (D-016). Its files sit in `future_work/`.

## Current status

**The analysis is done. The paper, the 2-page course report and report v1 are built. Five owner text parts remain.**

```
 data --> runs --> Q1 --> Q2 --> Q3 --> checks --> paper --> course report
 done     done     done   done   done   done       built     built (2 pages)
```

| Part | State | Detail |
| --- | --- | --- |
| Data | Done | Downloaded to the cluster. 688,131 markets in scope |
| Main run | Done | `142082_mvp1_full_v1r3` |
| Q1 (is the crowd right?) | Done | Pre-registered verdict issued |
| Q2 (who is the crowd?) | Done | No pre-registered verdict. 80/20 and the power law are descriptive references (D-024, D-025) |
| Q3 (what does the data look like?) | Done | No verdict |
| Checks | Done | R1, R2 (run `142123_robust_full_v4`), M1 to M5, duplicate rows, peer asks (run `150310_r3_review_fixes_v6`) |
| Paper | Built | `papers/paper_mvp1/main.pdf`. Body in two columns, then References, then appendices A to G (D-042 to D-045). Page numbers: `papers/paper_mvp1/main.aux` |
| Course report | Built | `papers/course_report_mvp1/main.pdf`, 2 pages |
| Report v1 | Built | `reports/report_v1.html`. Owner review is open |
| Course deadline | 2026-11-15 | D-021 |

Terms: RQ means research question. The RQ list and its status are in `RQ.md`.

Source: `PLAN.md`, `STATUS.md`, `00.runs.md`, `DECISIONS.md`, `papers/paper_mvp1/main.aux`.

## Results so far

**Q1 says prices are not calibrated as a whole. The effect is small and runs one way: outcome 1 (the first-listed outcome) is priced too high. Q2 says the top wallets do most of the trading by USDC volume, far beyond the 80/20 reference. Q2 and Q3 have no pre-registered verdict.**

These results apply to the 47,948 kept markets only. For Q2, volume is in USDC. It sums every trade in those markets, including trades after T - 1 day. Rows are wallet and role. Trade counts were not measured. The kept markets are resolved Yes/No markets with a fresh price one day before the close and at least 10 trades.

| Question | Answer | File |
| --- | --- | --- |
| RQ1 / Q1: is the crowd right? | Verdict: "Prices are not calibrated as a whole at this n." | `runs/142082_mvp1_full_v1r3/verdicts.json` |
| RQ2 / Q2: who is the crowd? | Yes by USDC volume. The top 20% of wallets hold 98.9% (makers) and 98.0% (takers) of volume | `runs/142082_mvp1_full_v1r3/q2_results.json` |
| RQ3 / Q3: what does the data look like? | Described, no verdict. Prices are U-shaped. Sizes are right skewed | `runs/142082_mvp1_full_v1r3/q3_results.json` |

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
| Bins with the observed rate below the price | 9 of 10 (also without the minimum-trade filter and in equal-frequency bins) | `reports/lecture_numbers.json` `gap_direction.*.n_negative` |
| Net gap, all kept markets | -0.99 percent points, 475 fewer outcome-1 wins than the prices imply | `gap_direction.main.net_gap`, `n_yes_minus_expected` |
| Largest chi-square contributor | bin 0, 31.3% of the chi-square | `chi2_largest_contributor` |

How to read the effect:

- The effect is small, and it runs one way. In 9 of 10 bins the outcome-1 rate is below the price.
- The largest per-bin gap is 3.29 percent points (bin 7). Read the direction and the net gap with it.
- We set no size line before the results. So "small" is our reading.
- Read the gaps before the p-value.
- Why "outcome 1": outcome 1 is the leg coded `outcome_seq = 1`. Its label is "Yes" in 63.9% of kept markets (Sports 14.0%). So the paper says "outcome 1" (D-036, D-037, run `150296_v1label`).
- Among the 30,630 markets where outcome 1 is labeled Yes, the observed rate is below the mean price in bins 0 to 8. This is a description, with no new test (D-037).

Longshot statement. With the minimum-trade filter, the two cheapest bins pay off less than their price. Without the filter it holds only in part. Bin 0 flips to +0.0005 (BH p 0.6006). Bin 1 is -0.0093 (BH p 0.1362). Neither bin is off. File: `reports/lecture_numbers.json` `no_min_filter_longshot_bh`.

Limit. The tests assume independent markets. Markets on one event are not independent, so the p-values may be optimistic. Check M3 re-tests with proxy event keys (below).

Q2 numbers. A maker places a resting order. A taker fills it. A wallet is one address.

| Item | Makers | Takers | File and key |
| --- | --- | --- | --- |
| Wallets | 581,435 | 1,535,977 | `q2_results.json` `concentration.*.n_wallets` |
| Volume share of the top 1% of wallets | 86.1% | 75.9% | `q2_results.json` `concentration.*.top1_share` |
| Volume share of the top 20% of wallets | 98.9% | 98.0% | `q2_results.json` `concentration.maker.top20_share`, `concentration.taker.top20_share` |

There is no pre-registered test for Q2, so it has no verdict line. The 80/20 rule (Pareto principle: 20% of the units hold 80% of the total) is a descriptive reference (D-024). Both the 80/20 rule and the power law are lecture content (`notes/6_DataDistribution.pptx`, slide 19). The class post named 80/20 before any result (`proposal_md/polymarket_proposal_v3.md` line 12).

Pipeline check against the dataset paper: our top 1% maker share is 86.1%, and the paper's is 84.1% (Qin and Yang 2026, Table 5). The populations differ. The paper covers the full data, and our wallets come from the kept markets. We read the paper's value as a reference only.

The Lorenz curve is a full curve from all wallets (D-031). It is labeled as outside the lectures (D-028). Its use: the height shows the share of volume held by the lowest share of wallets, against the 80/20 reference. The Gini coefficient is removed (D-026).

The CCDF (complementary cumulative distribution function, the share of wallets above a volume) bends downward at the largest wallets. So it is not a straight line on log-log axes. Source: runs `145892_ccdf_v6` and `145893_walletdist_v7`.

Where the Q2 and Q3 figures sit in the paper (numbers from `main.aux`). Why: the body keeps one figure per question, and the rest sit in appendices (D-042, D-043).

| Figure | Place in the paper | File |
| --- | --- | --- |
| CCDF, ranks sampled from the top | Figure 4, Section 5.2 | `reports/figures/fig6_ccdf_top_sampled.png` |
| Maker and taker wallet and volume distributions, top 20% split | Figures 8 and 9, Appendix D.1 | `reports/figures/wallet_dist_*_count.png`, `wallet_dist_*_volume.png` |
| Lorenz curves, maker and taker | Figure 10, Appendix D.1 | `reports/figures/wallet_lorenz_maker.png`, `wallet_lorenz_taker.png` |
| QQ plot of trade size, raw and log | Figure 5, Section 5.3 | `reports/figures/qq_trade_size_raw_log.png` |
| Histograms of price and trade size | Figure 11, Appendix E | `reports/figures/hist_price_p1d.png`, `hist_trade_size.png` |
| QQ plot of wallet volume, raw and log | Figure 12, Appendix E | `reports/figures/qq_wallet_volume_raw_log.png` |

The trade-size histogram holds one trade fewer than the sample of 1,000,000. One sampled trade falls past the last bin edge by float rounding (`CHANGELOG.md`).

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
- Future work: compare the power law and lognormal on the same data, with the tail start estimated (D-027). No such analysis runs now.

Side analysis: k-means clusters against topic category (D-030, Lecture 12 chi-square of independence). It runs on the 200,000 sampled wallet-role rows. Chi-square 6,653.0 (df 21), p below 0.0001. The effect size is the largest observed minus expected share in one cell. That cell is cluster 2, Sports. It has 6.7% observed and 8.2% expected, a gap of -1.49%. No Cramér's V. Files: `reports/lecture_numbers.json` `cluster_category_gap`, `runs/145892_ccdf_v6/cluster_category_crosstab.csv`. k-means stays under 1/10 of the report (Appendix D.2 in the paper).

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

Trade size uses a fixed sample of 1,000,000 trades (`q3_results.json` `notes.trade_size_sample_rows`). The power law is a fit to the top 10% of values. Normal and exponential were fit on all data, so the fits are not like for like. We do not call the power law the best fit.

### Checks next to the Q1 verdict

Why: reviewers asked whether the Q1 result survives other choices (D-038). Each check adds a row next to the original Q1 row and never replaces it. Rules were fixed before the run (D-039, `analysis/prereg_review_fixes.md`). The paper lists every check in Table 4 (Section 5.4). Each check has an appendix section: R1 and R2 in Appendix F, the rest in Appendix G.

| Check | Key result | Same Q1 rule result? |
| --- | --- | --- |
| R1: drop unclear payouts (47,901 markets) | Chi-square 64.3, 4 bins off after BH | Yes |
| R2: price change before the close | Mean squared residual 0.107 at T - 1 day against 0.075 just before the close. So the T - 1 day price is not the close price | n/a |
| M1: VWAP (volume-weighted average price) | Net gap -1.20%, CI [-1.50%, -0.91%] | Yes |
| M2: markets labelled Yes/No (30,112) | Net gap -1.32%, CI [-1.61%, -1.03%]. Yes is priced above its observed rate (D-040) | Yes/No: yes. Other markets (17,836): no |
| M3: dependence between markets, first proxy key (16,161 clusters) | Net gap CI [-1.41%, -0.58%]. The proxies are not true event keys | Yes |
| M4: kept against dropped markets | Median volume before T - 1 day: 1,790.0 USDC kept, 69.0 USDC dropped | n/a |
| M5: practical size | Largest implied gap 2.22% against 1.57% (mean half spread). 0 of 7 grid prices pass the practical line | n/a |
| Duplicate rows (47,809 markets kept) | Net gap -0.99%, CI [-1.28%, -0.69%] | Yes |
| Peer a: volume terciles | High minus low net gap 0.71%, CI [0.01%, 1.40%], p = 0.046 | Low and mid: yes. High: no |
| Peer b: close period | 2022-2024 and 2025: yes. 2026: no, but its CI [-1.04%, -0.25%] excludes 0 | see left |

Equal-frequency bins: 7 of 10 bins off after BH. The z interval marks 8, because it also marks the lowest bin (1 outcome-1 win in 4,795). The z interval has no correction for ten bins and is unreliable when a bin has very few wins. File: `runs/142140_q1eqfreq_v5/q1_bins_eqfreq.csv` `reject_bh`.

Source: `runs/142082_mvp1_full_v1r3/verdicts.json`, `q1_results.json`, `q2_results.json`, `q3_results.json`, `tables_summary.json`, `runs/142123_robust_full_v4/`, `runs/142140_q1eqfreq_v5/q1_bins_eqfreq.csv`, `runs/150310_r3_review_fixes_v6/`, `papers/paper_mvp1/numbers.tex`.

## How we got here, step by step

Why this section exists: it shows what was done in what order, and why. The Q1 criteria were fixed before any Q1 result. That order protects the verdict.

```
1 download --> 2 pilot inspect --> 3 fix criteria --> 4 pilot end to end
                                                            |
 8 robustness <-- 7 final MVP1 run <-- 6 review, fix <-- 5 first full run
      |
 9 equal-frequency fix --> 10 report and paper --> 11 gate review
                                                            |
                                          12 scope: MVP1 only --> 13 third gate review
                                                            |
                                          14 lecture-method picks --> 15 project-end fixes
                                                            |
                          16 label check --> 17 two-reviewer checks --> 18 gate review r3
                                                            |
                                          19 paper restructure
```

### Step 1. Download data (D-003)

- What: download `daily_aligned/` (1,248 files) and `CTF/resolutions.parquet` to the cluster.
- Why: `daily_aligned/` is the analysis layer. Resolutions are the backup outcome source.
- Output file: data on the cluster, in `~/cs6344_polymarket/data/`. It is not in this repo. The size listing is `analysis/hf_daily_aligned_listing.txt`.

### Step 2. Pilot inspection, run 142041 (D-004, D-005)

- What: inspect one month of markets (`close_at` in 2025-06). Never pair a price with an outcome.
- Why: choose the close-time rule and the minimum-trade cutoff without seeing any Q1 result.
- Output file: `runs/142041_pilotA_2025_06/report_pilot_inspect.md`. It found 3,841 markets and 3,065,179 trades.

### Step 3. Fix the criteria before any Q1 result (D-007)

- What: set T to `close_at`, the minimum to 10 trades, and keep duplicate rows. Write the Q1 test and its lines.
- Why: a cutoff chosen after the result could follow the result.
- Output file: `analysis/prereg_mvp1.md`.

### Step 4. Pilot end to end, run 142056

- What: run the whole pipeline once on the pilot set.
- Why: find broken stages on a small set first.
- Output file: `runs/142056_mvp1b_pilot_2025_06/summary.md`. It kept 726 of 2,063 markets. This cycle gets no verdict.

### Step 5. First full run, 142057

- What: run all four stages on every market in `daily_aligned/`.
- Why: get the first full-data result.
- Output file: `runs/142057_mvp1_full_v1/summary.md`. It kept 47,948 of 688,131 markets.

### Step 6. Review and fix, code v3 (D-011)

- What: a reviewer checked the first full run. Fixes went into code v3, and the run was redone.
- Why: trades in one block have no order. So "last price" needed a tie rule, and the samples needed a fixed order.
- Output file: `analysis/review_mvp1_mvp2.md`.
- The tie rule changed after the first Q1 result. The verdict did not change. The amendment is in `analysis/prereg_mvp1.md`.

### Step 7. Final MVP1 run, 142082

- What: run build, Q3, Q1, Q2 and verdicts with code v3.
- Why: this run is the source of all MVP1 numbers.
- Output file: `runs/142082_mvp1_full_v1r3/` (see `verdicts.json` and `summary.md`).

### Step 8. Robustness, run 142123 (D-013)

- What: two descriptive checks on the kept markets. R1 looks at split payouts. R2 looks at the price path in the last day.
- Why: the class questions left both limits open.
- Output file: `runs/142123_robust_full_v4/report_r1_split_payout.md` and `report_r2_price_path.md`.

### Step 9. Equal-frequency correction, run 142140

- What: rerun Q1 only, so the BH p-values for equal-frequency bins are saved.
- Why: a paper review (F9) asked for a saved number, not a recomputed one.
- Output file: `runs/142140_q1eqfreq_v5/q1_bins_eqfreq.csv`.

### Step 10. Report v1 and the paper

- What: build the HTML report and the LaTeX paper from the saved runs.
- Why: the report and the paper are the deliverables (D-014).
- Output file: `reports/report_v1.html` and `papers/paper_mvp1/main.pdf`.

### Step 11. Gate review, 2026-11-01

- What: a reviewer checked whether MVP1 answers RQ1, RQ2 and RQ3, from saved outputs only.
- Why: the end of MVP1 is a gate.
- Output file: `analysis/review_mvp1_rq.md`. Result: ISSUE (0 blocker, 2 major, 9 minor). The Q1 verdict reproduces exactly.

### Step 12. Scope: MVP1 only (D-016 to D-020)

- What: the owner chose MVP1 only. MVP2 files moved to `future_work/`. A box plot closed the missing Q3 figure (D-018). The Mission names the markets actually tested (D-019).
- Why: the deadline is 2026-11-15 (D-021). These picks close or explain the two major findings.
- Output file: `DECISIONS.md`, `PLAN.md`.

### Step 13. Third gate review (D-022)

- What: a reviewer checked the four "MVP1 is done when" boxes again, from saved files.
- Why: the owner asked for a third review beyond the usual two (D-022).
- Output file: `analysis/review_mvp1_rq_r3.md`. Result: PASS (0 blocker, 0 major, 4 minor).
- Same day, the owner decided how RQ2 closes (D-024, D-025). The title stays. The 80/20 rule and the power law are descriptive references.

### Step 14. Lecture-method picks (D-025 to D-028)

- What: the owner picked from the lecture-method audit, and the picks went into the report and the paper. Chi-square goodness of fit stays. The Brier score is the mean squared residual of the price. Per-bin gaps replace Cohen's w. The z interval replaces the Wilson interval. The log10 mean difference replaces Cohen's d. Gini, the adjusted Rand index and Cohen's d_z are removed. Lorenz stays as a labeled figure (D-028).
- Why: the owner rule (D-025) says all analysis stays within lecture contents.
- Output file: `analysis/lecture_method_audit.md`, `reports/lecture_numbers.json`.
- The prereg files and `runs/` stay as committed. A dated note in `analysis/prereg_mvp1.md` records the departure. The verdict rule and sentence are unchanged.

### Step 15. Project-end fixes (D-029 to D-031)

- What: the project-end review found readings that went further than the numbers. Two cluster jobs redrew the figures. The report and the paper took the fixes.
- Why: the owner asked for the CCDF redraw (D-029), the cluster chi-square back with an effect size (D-030), and the full wallet distributions and Lorenz curve (D-031).
- Runs: `145892_ccdf_v6` and `145893_walletdist_v7`. Q3 figures were split in `145897_q3figs_v8` (D-032, D-033).
- Fixes in the paper:
  - The effect is small, runs one way, and has no size line set in advance.
  - The longshot statement holds with the minimum-trade filter only.
  - The CCDF tail bends. The exponent is reported with the KS rejection.
  - The Q2 answer is by USDC volume, in the kept markets, in wallet-role rows.
  - The independence limit covers the p-values and the z intervals (D-034).
- Output file: `analysis/review_project_end.md`.

### Step 16. Label check and "outcome 1" (D-035 to D-037)

- What: a gate review found one major issue (V-1): "Yes is priced too high" named a label no saved file showed. One cluster count of the label settled it, with the wording rule fixed first. Rule B applied: the paper says "outcome 1".
- Why: no measured number showed the label, and a rule fixed first keeps the result from picking the wording (D-036).
- Output file: `analysis/review_mvp1_gate_2026_11_07.md`, `analysis/prereg_v1_label_check.md`, `runs/150296_v1label/label1_counts.json`.

### Step 17. Two-reviewer checks, run 150310 (D-038, D-039)

- What: a conference reviewer and the course professor asked for more checks. One cluster job ran M1 to M5, duplicate rows and the two peer asks. Figure 3 has a gap panel, 3(b), next to the rate panel, 3(a).
- Why: the course grades responsiveness to feedback (D-038). New rows sit next to the original Q1 verdict.
- Output file: `analysis/review_paper_mvp1_two_reviewers.html`, `analysis/prereg_review_fixes.md`, `runs/150310_r3_review_fixes_v6/`.
- D-040: the paper adds one sentence that Yes is priced above its observed rate in the Yes/No markets (M2). The main result keeps "outcome 1".

### Step 18. Gate review r3 (D-041)

- What: a reviewer checked the paper and the report. Result: PASS (cycle 1/2). Fixes F1 to F14 are text, figure and format fixes with no new run.
- Why: it keeps the paper and report matching the runs.
- Output file: `analysis/review_gate_mvp1_r3.md`.
- The paper labels five methods outside the lectures: Lorenz curve, Wilson intervals, cluster bootstrap chi-square, logistic calibration, Brier skill score.

### Step 19. Paper restructure (D-042 to D-045)

- What: the checks, the extra Q2 and Q3 figures and the prereg table moved to appendices. Table 4 summarizes every check in Section 5.4. Figure 1 shows the core flow. The body is two columns.
- Why: the body should near conference length and keep Q1 as the focus (D-042). The core flow stays readable (D-043). Two columns and narrow margins fit that length (D-045).
- Output file: `papers/paper_mvp1/`, `analysis/design_paper_length_d042.md`, `paper_length.plan.md`.
- The 2-page course report did not change.

Rebuild after fetching new runs (`bash jobs/fetch_run.sh <run>`, from `cs6344_group_01/`):

```bash
OMP_NUM_THREADS=1 timeout 300 uv run python code/lecture_numbers.py --run runs/142082_mvp1_full_v1r3 --ccdf-run runs/145892_ccdf_v6
OMP_NUM_THREADS=1 timeout 300 uv run python code/make_report.py --run runs/142082_mvp1_full_v1r3 --version v1 --out reports/report_v1.html --q1eqfreq runs/142140_q1eqfreq_v5
```

Then regenerate `papers/paper_mvp1/numbers.tex` with the command in `papers/README.md`.

Source: `STATUS.md` log, `00.runs.md`, `DECISIONS.md`, `analysis/review_*.md`.

## What is left

State as read from `PLAN.md` and `STATUS.md`.

| Work | Who | Why |
| --- | --- | --- |
| Write or remove the 5 `\todo{owner: ...}` parts in the paper: related work, x_min choice, interpretation, wider implications, closing | Owner | The text is the owner's (D-044 keeps owner parts open) |
| Finish F5: no sentence over 15 words in the paper, after the owner text is in | Owner, with Claude Code | `rules/writing/style.md` §2 |
| Review report v1 and record notes in `STATUS.md` | Owner | Report v1 was built for the owner (D-016) |
| Compare the `markets.parquet` hash of run 142082 with run 142140 | Owner, on the cluster | Review item G11 |
| Split `code/make_report.py` (about 800 lines) in its own commit | Owner, with Claude Code | Kept as is for now (owner, 2026-10-19) |
| Pick the 3-person work split (`docs/team_split_design.html`) | Owner | Not yet decided (owner, 2026-11-01) |
| Redraw `fig5_ecdf_yes_no.png`: its inside text may still say Yes/No | Owner decides | One cluster job needed |
| Gate review of the restructured paper (PL-15) | Reviewer | Closes milestone M5 |

Course deadline: 2026-11-15 (D-021).

Source: `PLAN.md` "Open tasks", `paper_length.plan.md`, `STATUS.md`.

## How to read the outputs

Read in this order. Each step builds on the one before.

| Order | File | What it gives |
| --- | --- | --- |
| 1 | `papers/paper_mvp1/main.pdf` | The paper: body, References, appendices A to G |
| 2 | `papers/course_report_mvp1/main.pdf` | The 2-page course report |
| 3 | `reports/report_v1.html` | The full story in steps, with tables and figures |
| 4 | `runs/142082_mvp1_full_v1r3/summary.md` | Links to each stage report of the final run |
| 5 | `tips/index.html` | Explainer pages in English and Korean. Start with the Paper flow tab |

Open the HTML files in a browser. Numbers in the report and paper come from the saved run files. Do not retype them.

## Research questions

| | Question | MVP |
|---|---|---|
| Q1 | Is the crowd right? Do events priced at *p* happen with frequency *p*? | MVP1 |
| Q2 | Who is the crowd? Do a few wallets do most of the trading? | MVP1 |
| Q3 | What does the data look like? Trade sizes, wallet activity, prices | MVP1 |

The MVP2 questions (Q1a, Q1b, Q1c) are out of scope (D-016). They sit in [future_work/README.02.md](future_work/README.02.md).

## Where things are

| File | What it is |
|---|---|
| `proposal_md/polymarket_proposal_v3.md` | Class post (short proposal) |
| `tips/polymarket_plan_detailed.md` | MVP1 plan: questions, method, gate, risks |
| `docs/lecture_concept_map.md` | Lecture decks mapped to each question (section 6 = MVP1) |
| `polymarket_v1_paper.pdf` | Dataset paper (Qin & Yang, 2026) |
| `reports/` | HTML report v1 (`report_v1.html`) |
| `runs/` | One folder per cluster run: tables, figures, JSON results, stage reports |
| `analysis/` | Criteria fixed before results (`prereg_*`) and reviewer reports (`review_*`) |
| `papers/` | `paper_mvp1/` (full paper), `course_report_mvp1/` (2 pages). Guide: `papers/README.md` |
| `code/` | Python pipeline: build tables, Q1, Q2, Q3, robustness, report, paper numbers |
| `jobs/` | SLURM job scripts and the fetch script |
| `PLAN.md`, `STATUS.md`, `DECISIONS.md`, `00.runs.md` | Plan, progress log, decision log, run ledger |
| `tips/` | Explainer pages. Guide: `tips/README.md` |
| `archive/` | Earlier proposal drafts, kept for reference |
| `future_work/` | MVP2 files, out of scope (D-017) |

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
| Price (outcome 1 side) | `p_event` | Q1, Q3 |
| Outcome y (1 = outcome 1 won, 0 = it lost) | `winning_outcome_label` and the `outcome_seq = 1` leg's `outcome_label` | Q1 |
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

Without the 10-trade rule, 74,474 markets stay. Q1 is also reported on that set. Check M4 compares kept and dropped markets (Appendix G.4 in the paper).

| Filter (in order) | Rule | Why |
| --- | --- | --- |
| Up/Down | Drop a market if `market_slug` has `up-or-down` or `updown`. Also drop it if `category_refined` matches `up%down` or `updown` | Dataset paper: "fundamentally different settlement mechanics" (section 6), "should not be pooled" (limitation 5) |
| Not binary | Keep a market with at most 2 `outcome_seq` values and `neg_risk` not true | Dataset paper: Neg-Risk markets "require a separate normalization" (section 6) and "should not be pooled" (limitation 5) |
| No winner label | Drop a market with no usable y | We do not impute. The rule also drops a market whose outcome-1 label never traded |
| No price | Drop a market with no trade at or before T - 1 day | There is no price to test |
| Stale price | Drop a market if the price is older than 24 h | Plan rule: skip a price more than 24 h older than the evaluation time |
| Minimum trades | Drop a market with fewer than 10 trades before T - 1 day | A price from an almost empty market is not a crowd view |

Fixed values, set before any Q1 result:

| Item | Fixed value | Why |
| --- | --- | --- |
| Evaluation time T | `close_at` | 0.513 of pilot markets have a trade after `close_at` |
| Evaluation price | Mean `p_event` of the trades at the last timestamp at or before T - 1 day | Trades in one block have no order. The mean makes it deterministic |
| Minimum trades | 10 before T - 1 day | Chosen from the pilot (Job A) before any Q1 result |
| Duplicate rows | Kept | No row id tells a repeat fill from a copy. The pilot has 155,885 duplicate rows of 3,065,179. Check "duplicate rows" removes them as a test (Appendix G.6) |
| Stale price limit | 24 h | Plan rule |

Source run: `runs/142082_mvp1_full_v1r3`.

Source: `runs/142082_mvp1_full_v1r3/tables_summary.json`, `analysis/prereg_mvp1.md`, `analysis/prereg_mvp1_full.json`, `runs/142041_pilotA_2025_06/report_pilot_inspect.md`, `code/common.py`, `code/build_tables.py`, `DECISIONS.md` D-007, D-011.

## Criteria

We fixed the tests, the significance line and the effect size before we saw results. The files are `analysis/prereg_mvp1.md`, `analysis/prereg_robustness.md` and `analysis/prereg_review_fixes.md`.

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
- Departure from `analysis/prereg_mvp1.md` (D-026): the prereg names a Wilson interval, the Brier score and Cohen's w. The report and the paper use the z interval, the mean squared residual and the per-bin gaps. The verdict rule and the verdict sentence are unchanged.
- The pilot run is a first end-to-end cycle. It gets no verdict. The verdict applies to the full-data run.

Descriptive only, no verdict:

| Part | Status |
| --- | --- |
| Q2 and Q3 | No pre-registered test or verdict. The 80/20 rule and the power law are descriptive references (D-024, D-025) |
| R1, R2 | Descriptive. Add a sensitivity row next to Q1 and never replace it (D-013) |
| M1 to M5, duplicate rows, peer asks | Rules fixed before run 150310 (D-039). M1, M2, M3 and M5 have a pre-registered reading rule. The rest are tests without a reading rule, or descriptive |

Amendment, honest record:

- We changed the evaluation price rule after we saw the first full Q1 result (run 142057).
- Old rule: the last trade at or before T - 1 day. Trades in one block have no order, so this was undefined.
- New rule: the mean price at the last timestamp. The reason was determinism, not the result.
- The verdict did not change.

Source: `analysis/prereg_mvp1.md`, `analysis/prereg_robustness.md`, `analysis/prereg_review_fixes.md`, `DECISIONS.md` D-005, D-007, D-011, D-013, D-039.

## Constraints

| Constraint | Source |
| --- | --- |
| All analysis stays within lecture contents. k-means is a side analysis, under 1/10 of the report | owner, 2026-10-18; D-025, D-026 (2026-11-01); plan Q2 |
| A method outside the lectures is renamed or replaced, or labeled in the paper (five methods, D-041). The cluster chi-square test has a share-gap effect size (D-030) | D-026, D-028, D-041 |
| Every fact in a class post has a source. No source, no claim | owner, 2026-10-18; plan "Facts in the class post" |
| All data queries run on the cluster. The laptop only draws figures from saved outputs | root `CLAUDE.md`, 2026-10-18 |
| T, the minimum-trade cutoff and the Q1 criteria are fixed before any Q1 result | D-005, D-007 |
| Write "wallet" or "address", never "trader" or "person" | plan Q2 |
| Every test reports an effect size next to its p-value | plan "MVP1 is done when" |

Source: `STATUS.md` "Constraints" table.

## Tools

Python (pandas, NumPy, SciPy, statsmodels, scikit-learn, matplotlib) and DuckDB. The paper uses LaTeX (`latexmk`).

## Course assignment: proposal thread

One member of each team creates a thread with:

- Group number and team name
- Working title
- Brief description of the idea
- Description of the dataset
- Main question, hypothesis, problem, or objective
- Methods, tools, or approaches being considered

Each student responds to at least 4 classmates' threads. Responses cover what is interesting or promising about the idea, and suggestions for improvement or clarification.
