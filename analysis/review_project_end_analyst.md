# Project-end review: data-analyst part (MVP1)

- Date: 2026-11-01.
- Scope: analysis method and number reading in `reports/report_v1.html`, `papers/paper_mvp1/main.tex`, `papers/paper_mvp1/numbers.tex`, `README.md`.
- Nothing was run. All inputs are saved outputs and code snapshots.
- Report locations use Table and Figure numbers. The HTML body is one minified line.

## 1. Result

**The Q1 verdict sentence stands. 0 blockers, 8 major, 7 minor. The numbers are correct. The readings go further than the numbers.**

| Rank | ID | Severity | Finding in one line |
| --- | --- | --- | --- |
| 1 | A3 | major | "The effect is small" rests on a maximum and hides a one-way bias of 0.99 points |
| 2 | A2 | major | "Cheap bets pay off less" holds for cheap Yes legs, main set only |
| 3 | A4 | major | README omits independence. The paper's "read the intervals first" does not escape it |
| 4 | A1 | major | The "long straight" CCDF tail is one drawn chord, a plotting artifact |
| 5 | A5 | major | "Close to a power law" conflicts with README, with the paper's own KS line and with Figure 9 |
| 6 | A6 | major | "Most of the trading" means volume. Scope and post-close trades are not stated |
| 7 | A7 | major | Paper says do not compare sizes. Report says compare the size |
| 8 | A8 | major | Report Table 11 still prints Wilson intervals, against D-026 |

Rank order: what changes a reader's conclusion on the verdict comes first. Q2 readings come next, then consistency. IDs follow the question order, not the rank.

Why this review: step 4 of the workflow cycle gives the analyst the numbers, tables and method at project end.

Data used:

- `runs/142082_mvp1_full_v1r3/`: bin CSVs, `q2_*`, `q3_results.json`, code snapshot, `fig6_ccdf.png`, `fig7_lorenz.png`.
- `runs/142123_robust_full_v4/report_r1_split_payout.md`, `runs/142140_q1eqfreq_v5/q1_bins_eqfreq.csv`, `reports/lecture_numbers.json`.
- `analysis/prereg_mvp1.md`, `analysis/lecture_method_audit.md`, `analysis/review_mvp1_rq_r3.md` G14, `DECISIONS.md` D-024 to D-028.

All data is real run output, with no generated data. D-024 to D-028 are the owner's picks. This memo does not reopen them.

What passed:

- `numbers.tex` bin, z, top-share and power-law macros match the saved files I compared.
- Maker and taker wallet counts sum to the 2,117,412 rows. So the `volume_usdc > 0` filter dropped nothing.
- Maker and taker total volume are equal, about 8.2 billion USDC. So no trade is double counted inside a role.
- The chi-square reproduces from `q1_bins.csv` (§7). The 5 z bins and 5 BH (Benjamini-Hochberg, 거짓 발견율 보정) bins match.
- "Wallet = address" appears in all three deliverables.

## 2. Q1: is "the effect is small" supported?

Signs of observed rate minus mean price (`-` below price, `+` above, `*` BH off):

```
bin set               0    1    2    3    4    5    6    7    8    9
main (47,948)         -*   -*   -    -    -    -    -*   -*   -*   +
no min filter (74,474)+    -    -    -    -    -    -*   -*   -*   -*
equal frequency       -    -*   -*   -*   -*   -*   -    -*   -*   +
```

Reading:

- 9 of 10 gaps are negative in all three bin sets.
- So the prices run above the outcomes, one way, and not as scatter.
- The exception moves. It is the top bin in the main set and bin 0 without the filter.
- The off bins also move: 0, 1, 6, 7, 8 become 6, 7, 8, 9.

### A3. Largest gap as the only size reading (major)

- Location: `main.tex` 92, 356, 608. `README.md` 43, 66. Report Table 1, Step 4 "How to read".
- Fact: no prereg line defines "small" (`prereg_mvp1.md` 18 to 26).
- Fact: the paper states the one-way direction (93, 384, 607).
- Fact: README and report do not state it. Report Table 8 shows signs, with no sentence.
- Fact: mean price 0.3757 against Yes rate 0.3658 is a net gap of 0.99 points. Both numbers are printed, and no text joins them.
- Fact: bin 7 has the largest gap in points. Bin 0 has the largest chi-square share, 21.3 of 68.0 (§7).
- Fact: the gap is bounded by price. In bin 0 it cannot pass 1.8 points downward, and 38% of markets sit there.
- Fact: per dollar of price, payout shortfall is 25% (bin 0), 15.5% (bin 1), 4.4% (bin 7) (§7).
- Judgment: the largest gap is a true number, but the wrong sole reading.
- Judgment: a maximum cannot show direction or count. "Small" in points is not small in relative terms for cheap bins.
- Judgment: "small" is a post-result word with no line. It should say so.
- Fix owner: owner picks the wording. `sonnet-writer` edits the paper and README. `developer` edits `make_report.py`.

| Option | Change | Gain | Cost |
| --- | --- | --- | --- |
| A | Add one sentence: prices sit above outcomes in 9 of 10 bins, net 0.99 points | Direction and size in one line, from the mean only | Adds a derived number. A saved script must produce it |
| B | A plus a shortfall column (gap / mean price) in Table 8 and `tab:bins` | Shows cheap bins fairly | Wider table. Low-price ratios are noisy |
| C | Keep "small", add "in percent points, with no size line set before the results" | Fewest edits | Direction still missing from README and report |

### A2. Longshot claim over-reaches (major)

- Location: `main.tex` 395, 396, 609, 680. Abstract has no longshot line.
- Fact, filter: without the minimum-trade filter, bin 0 is +0.05 points and bin 1 is -0.93 points. Neither is off (`q1_bins_no_min.csv`).
- Fact, disclosure: report Tables 10 and 12 show this. The paper (421) says only that chi-square also rejects. README shows no bin detail.
- Fact, range: bins 6, 7, 8 are also below price. Their YES price is high, so these are the favorites.
- Fact, complement: bin 7 YES at 0.746 happens 0.713 of the time. So No, near 0.254, happens 0.287 of the time.
- Judgment: "Cheap bets pay off less" fails for that cheap No leg, if No trades near 1 minus YES.
- Judgment: the data shows Yes overpriced across the range. That is not a longshot-only pattern.
- Judgment: "matches the horse-racing direction" is true for the two cheapest Yes bins only.
- Not verified: Snowberg and Wolfers also report favorites winning more than priced. That comes from memory. `researcher` should confirm it before any sentence uses it.
- Fix owner: owner, since the interpretation `\todo` at `main.tex` 610 is open. `sonnet-writer` applies it.

| Option | Change | Gain | Cost |
| --- | --- | --- | --- |
| A | "Cheap Yes legs pay off less in the main set. The gap disappears without the filter" | True to the saved numbers | Weaker headline |
| B | A plus "favorite Yes bins also sit below price, so this is not longshot-only" | Reads the full pattern | Needs owner words (`book.md` principle 13) |

### A9. Robustness wording (minor)

- Removing 47 of 47,948 markets drops one off bin, 5 to 4 (`report_r1_split_payout.md`). So bin calls are fragile. I did not read which bin.
- `main.tex` 562 explains "equal rows", and the two rows are not equal. No text reads the difference.
- Bin 8 is near the line: BH p 0.036, not off under Bonferroni.
- `main.tex` 132 promises an effect size next to every p-value. Lines 420 and 571 give p with no gap beside it.
- Judgment: the verdict is robust. Single bin calls are not. Say that.
- Fix owner: `sonnet-writer`.

### A10. Meaning of "Yes" cannot be checked here (minor, open)

- Fact: y = 1 when the winner equals the `outcome_seq = 1` label (`build_tables.py` 32, 33).
- Fact: Sports is 40.0% of kept markets (`numbers.tex`).
- Fact: no saved output lists label values, so I cannot say how many first labels are not "Yes".
- Judgment: A3 reads a bias of the first listed leg. "Yes" in the text assumes more than I can confirm.
- This data was not collected. I stop here. If the owner wants it, it is a cluster query. The main session decides.

## 3. Q2: where the z interval fails

| Bin set | Smallest n_yes, n_no | z interval state |
| --- | --- | --- |
| Main 10 bins | 249, 149 | Fine |
| No min filter | 550, 376 | Fine |
| Equal frequency, lowest | n_yes 1 | Fails. `z_low` is below 0 |
| Equal frequency, second | n_yes 6 | Weak |
| Equal frequency, top | n_no 24 | Weak |

### A11. Failure disclosed only in the prereg note (minor)

- Location: report Table 13. `main.tex` 422. `README.md` 122.
- Fact: lowest equal-frequency bin has 1 Yes in 4,795. `z_low` is -0.0002. Report Table 13 prints `[0, 0.0006173]`.
- Fact: its Wilson interval contains the price and binomial BH p is 0.129. Only z marks it off.
- Fact: report Table 13 gives 8 "yes" and no BH column. Paper and README give 7. Only `prereg_mvp1.md` §4 explains the gap.
- Fact: the Table 8 caption says ends are cut at 0 and 1. The Table 13 caption does not.
- Judgment: the main result is untouched. A reader comparing report and README sees 8 against 7.
- Fact: "same bins as BH" has thin margins. Bin 3 is inside by 0.0004 and bin 8 outside by 0.0027.
- Judgment: the agreement is an observation here, not a property. z is uncorrected and differs in its centre from the test.
- Dependency: the 7 comes from run 142140 and Table 13 from run 142082. `README.md` 265 keeps the hash comparison open.
- Fix owner: `developer` for Table 13. `sonnet-writer` for one sentence at `main.tex` 422.

| Option | Change | Cost |
| --- | --- | --- |
| A | Add BH p and call columns to Table 13, plus one note on the 1-Yes bin | Small edit, needs the v5 CSV as input |
| B | Note only, in the caption and at `main.tex` 422 | Reader still counts 8 in the table |

### A12. "Names" understates the change (minor)

- `main.tex` 277 and report Step 1 say "names" differ. A z interval is a different formula, with different ends.
- `README.md` 247 and 250 state it correctly.
- Fix owner: `sonnet-writer`.

### A8. Wilson left in the report (major)

- Location: report Table 11.
- Fact: bin 0 prints `[-0.006164, -0.002784]`. That equals `ci_low` and `ci_high` minus mean price in `q1_bins.csv`.
- Fact: Table 10, same bin, prints the z values `[-0.006263, -0.00289]`.
- Judgment: the size is tiny. But D-026 replaced Wilson and the method is not in lecture.
- Fix owner: `developer`. Table 11 in `make_report.py` (around 420) should read the z longshot rows in `lecture_numbers.json`.

## 4. Q3: the Lorenz picture, and a larger CCDF problem

### A1. CCDF tail is one straight chord (major)

- Location: `fig6_ccdf.png` in the report (Figure 9) and paper (`fig:lorenz`). Captions at `main.tex` 458 and report Figure 9.
- Fact: `q2_concentration.py` 140, 141 sorts volume ascending. It then picks 3,000 log-spaced positions from the low end.
- Fact: so points are dense at small wallets and sparse at large ones.
- Fact: the last gap skips the top 0.44% of makers and 0.47% of takers.
- Fact: Figure 9 shows the kink at those heights. The curve ends at 2/n, as the code predicts.
- Fact: the top 1% of wallets gets about 3 plotted points. Those wallets hold 86.1% and 75.9% of volume.

```
 log CCDF
 0.0044 + kink: last real plotted point before the top
        |\
        | \   one chord, no data drawn between the ends
        |  \
  2/n   +---\ second-largest wallet
        +------------------ log volume
```

- Judgment: the caption says "a long straight CCDF tail means a few wallets trade very large volumes". The straight part is made by the plot.
- Judgment: the chord connects two true points. So the figure is not false about those points, only about the shape between them.
- Judgment: the straight look also lends visual support to the power-law sentence (A5).
- Fix owner: `developer` for the drawing. Main session decides how it runs.

| Option | Change | Gain | Cost |
| --- | --- | --- | --- |
| A | Redraw with log-spaced ranks from the top | True tail shape | Needs `wallets.parquet`. Audit §3 sends that read to the main session. Else a cluster job |
| B | Keep the figure, change the caption: above the kink it is one chord, not measured shape | No new read | The best-known visual part stays uninformative |
| C | Mark the chord dashed from saved values | Honest look | Needs the same read for the kink location |

### A13. Lorenz picture (minor)

- Location: `main.tex` 313, 314, 458. Report Figure 10. `README.md` 80.
- Fact: points are x = 0, 0.80, 0.90, 0.95, 0.99, 1 (`lecture_numbers.py` 72).
- Judgment: a real Lorenz curve is convex, so each chord lies above it. Every segment understates concentration.
- Judgment: so the straight lines are not misleading on the claim. The error runs against it. The caption does not say so.
- Judgment: the 0.80 to 1 part, where the message lives, rests on measured points. The grey band is clear.
- Fact: "nothing was measured below 80%" is loose. `fig7_lorenz.png` drew the full curve from all wallets, and the numbers were not saved.
- Judgment: the caption is enough for honesty. It needs direction and one word changed.
- Fix owner: `sonnet-writer`, `developer` for the HTML caption.

| Option | Change | Cost |
| --- | --- | --- |
| A | Caption: "values below 80% were not saved. Straight lines lie above the true curve, so they understate concentration" | Small edit |
| B | A plus dashed lines for segments | Redraw from CSV. Allowed locally |
| C | Draw the full curve from `wallets.parquet`, no Gini | Best picture. Needs the parquet decision |

## 5. Q4: the 80/20 and power-law statements

Population, from code and manifest:

| Item | Value | Source |
| --- | --- | --- |
| Row | one wallet x role | `build_tables.py` 92 to 114 |
| Markets | kept markets only: 47,948 of 688,131 | `build_tables.py` 95, 98 |
| Trades | every trade in those markets, no time cut | `build_tables.py` 94 to 98 |
| Maker wallets | 581,435 | `q2_concentration.csv` |
| Taker wallets | 1,535,977 | `q2_concentration.csv` |
| Same address in both roles | two rows. Unique addresses not saved | `q2_concentration.py` 41 |
| Duplicate rows | kept | `manifest_q2_concentration.json` |

### A6. 80/20 sentence (major)

- Location: `main.tex` 94, 95, 426, 613, 681. `README.md` 26, 43, 50. Report Table 1.
- Supported: 98.9% and 98.0% against 80%, by role, inside kept markets. Direction is clear and D-024 sets it as descriptive.
- Over-reach 1: "do most of the trading" measures USDC volume only. Trade-count shares were not saved.
- Over-reach 2: "a few" is 116,287 makers and 307,196 takers at the top 20%. The top 1% is 5,815 and 15,360.
- Over-reach 3: the abstract (94) and answer (426, 613) omit "in the kept markets". Line 466 has it.
- Fact: kept markets hold about 13% of the dataset paper's $61 billion (§7). A wallet's rank uses only this part.
- Fact: post-close trades count, since no time cut applies. In the pilot they were 34.0% of volume.
- Fact: report says "after T - 1 day". Paper and README say nothing. The paper warns about these trades for price (206 to 211).
- Judgment: RQ2's title stays (D-024). The answer sentence should say "by volume" and "in the kept markets".
- Judgment: wallet against person is handled. The effect's direction is not measured, and the text claims none. That is right.
- Judgment: calling 86.1% against 84.1% a "pipeline check" says more than two different populations can. "Reference" already appears in the text. It is enough.
- Fix owner: `sonnet-writer`, `developer` for the report text.

| Option | Change | Cost |
| --- | --- | --- |
| A | "Yes by volume, in the kept markets", plus one limit line on post-close trades | Text only |
| B | A plus top 1% wallet counts in `tab:conc` | Derived from counts. Needs a saved script |
| C | Measure shares with post-close trades removed | Cluster job. Beyond MVP1 scope. Owner call |

### A5. Power-law sentence (major)

- Location: `main.tex` 469, 470, 503, 504. Report Table 1, Step 5. `README.md` 86, 88, 96.
- Fact: paper and report say "close to a power law". README says "we do not say wallet volume follows a power law".
- Fact: the paper relies on the KS p at 470. It says "we do not rely on them" at 504.
- Judgment: fitted parameters inflate p. So a rejection survives, and the two lines can be reconciled. The text does not do it.
- Fact: "close" has no line. D 0.024 is the only support.
- Fact: Figure 9's slope runs near 0.6 before the kink and near 1.3 after. The fit implies 0.788. This is read by eye (§7).
- Judgment: the tail bends. "Close" says more than D, with xmin fixed and lognormal not compared.
- Fact: the fit pools maker and taker rows (`q3_results.json` `notes`). Only report Step 3 says so. It is cited under Q2 as if wallet-level.
- Fact: README 88 labels 211,742 as "wallets". They are wallet x role rows.
- Fact: README 86 calls alpha "tail slope". `q3_describe.py` 41 is the density exponent. The CCDF slope is alpha minus 1.
- Fix owner: `sonnet-writer`, `developer` for the report text.

| Option | Change | Cost |
| --- | --- | --- |
| A | Use the README wording everywhere: alpha reported, KS rejects, we do not say it follows | Fewest words. Loses "close" |
| B | "D 0.024 on the top 10% of pooled rows, and we set no line for close" | Keeps the number. Adds a limit |

## 6. Q5 and Q6

### A4. Limits are not stated the same way (major)

| Limit | Report | Paper | README |
| --- | --- | --- | --- |
| Per-bin multiple tests | BH and Bonferroni, Table 7 | 291, 385, 386 | 53, 62, 63 |
| Independent markets | Step 1, Step 6. No direction | 650, 651. "p-values are optimistic" | **Absent** |
| Large n | Step 1: small effect, tiny p | 652: underflow only | 95: KS only. 66: "read the gaps first" |
| Scope to kept markets | Step 2 | 646 to 649 | 45 |

- Fact: only README lacks the independence limit, and it is the file a newcomer reads first.
- Fact: paper 652 gives underflow as the large-n issue. The real issue is that tiny gaps reach significance. Only the report says so.
- Judgment: paper 653 says "therefore read the effect sizes and the intervals first". z intervals use the same independence assumption, so they are also too narrow.
- Judgment: report Step 4 calls a gap "real but small". "Real" claims more than the optimistic p allows.
- Fact: no event-level count is saved, so the dependence size is unknown.
- Hand check: variance would need to grow about 3.7 times to lose the chi-square line (§7). This is not an estimate of the real factor.
- Fact: binomial(n, mean p) overstates variance when prices differ inside a bin. That works against the optimism. No text says so. `lecture_method_audit.md` row 1 notes the approximation.
- Fact: Welch and KS role tests compare groups that share addresses and trades. The stated limit covers markets only.
- Judgment: t 117.1 with p under 10^-300 beside a D of 0.057 is the large-n case, and the text does not read it.
- Fix owner: `sonnet-writer`, one shared limit block. The owner approves the wording.

| Option | Change | Cost |
| --- | --- | --- |
| A | One limit block, same sentences in all three | Three small edits |
| B | A plus a test by event group | New query. No event key was reviewed here. Owner call |

### A7. Compare sizes or not (major)

- Fact: `main.tex` 397, 398: "we do not compare their sizes".
- Fact: report under Table 11: "Compare the sign and the size, not the digits".
- Fact: bin 1 is -0.0230 ours against -0.0019 in the dataset paper. That is 12 times, on different units.
- Judgment: the paper is right. Per-market and per-trade gaps do not share a scale. Only the sign can be read.
- Fix owner: `developer` for `make_report.py`.

### A14. k-means after the removals (minor)

- Location: `main.tex` 324, 481, 482, 656, 657. Report Tables 17, 18.
- Fact: 324 announces a stability check. 656 says no agreement score is reported. No result appears.
- Fact: 657, "This does not make the clusters real", lost its referent when the ARI sentence left.
- Fact: SSB ratio 0.008 is printed with no reading. It means clusters barely differ on mean trade price.
- Fact: report Table 18 prints p 0.0010 with no floor note. The paper states the floor.
- Fact: report Table 17 says "wallets". They are wallet x role rows. The paper is correct at 478.
- Fact: paper 323, 477 say "elbow method". The K comes from a fixed chord rule, which only the report states.
- Fact: inertia falls smoothly, by 84,974, then 44,308, then 29,590. No sharp bend.
- Fact: median volume differs across clusters by construction, because volume is a feature.
- Judgment: the analysis is still honest. Paper 618 says it carries no claim, and no removed number leaks into a claim.
- Judgment: the dangling check is the one flaw. It implies stability evidence without showing it.
- Fix owner: `sonnet-writer`.

| Option | Change | Gain | Cost |
| --- | --- | --- | --- |
| A | Drop 324 and 656, 657 | Simplest. Removes the implied check | Stability goes unmentioned |
| B | Report the `cluster_z` x `cluster_robust` table from `q2_kmeans_sample.csv` | In lecture, CSV only | New output adds to the k-means share. The main session runs it |

### A15. The 1/10 limit (minor)

- Fact: `README.md` 235 cites 0.0974 and 0.0824. Those came from `review_mvp1_rq_r3.md` G14, before the D-026 removals.
- Estimate: the same text-character method now gives about 0.06. I counted the extracted text by eye. It is not for citation.
- Fact: by exhibit count it is 3 of 29 (Tables 17, 18, Figure 11), or 0.103.
- Fact: the paper's k-means text is about 3% of its source characters, also by eye.
- Judgment: within 1/10 by the only stated measure, characters. The owner's limit names no measure.
- Fix owner: main session measures and saves the number. README then cites that.

## 7. Hand checks

Done by hand from the named saved files. Not for citation. A saved script must produce any number before a deliverable uses it (`rules/answering.md` §3).

Source: `q1_bins.csv`.

| Bin | n | Chi-square share | Shortfall = gap / mean price |
| --- | --- | --- | --- |
| 0 | 18,209 | 21.3 | -25.1% |
| 1 | 2,703 | 11.3 | -15.5% |
| 2 | 2,543 | 1.4 | -4.0% |
| 3 | 2,769 | 3.6 | -4.9% |
| 4 | 3,859 | 2.4 | -2.7% |
| 5 | 4,240 | 0.6 | -1.1% |
| 6 | 2,553 | 8.7 | -4.3% |
| 7 | 2,301 | 13.1 | -4.4% |
| 8 | 2,133 | 5.8 | -2.2% |
| 9 | 6,638 | 0.0 | +0.0% |
| All | 47,948 | 68.0, saved 67.99 | |

Others:

- Net: 17,541 Yes against 18,016 expected, 475 short, 0.99 points.
- The net shortfall alone is about 6.6 SD. Its square is about 44 of the 68.0.
- Variance factor to lose the line: 68.0 / 18.31 = 3.7. The 18.31 is the df 10 value in `lecture_method_audit.md` §2.
- Volume share: maker mean x n is about 8.2 billion USDC, against $61 billion at `main.tex` 62.
- Plot gaps: 3,000 log-spaced positions give steps of 0.44% (maker) and 0.47% (taker) at the top.
- CCDF slopes are read from `fig6_ccdf.png` by eye, so they are rough.

## 8. Not checked

- Other figures against their code, except Lorenz, CCDF and calibration code.
- Which bin R1 drops.
- Every macro in `numbers.tex` against its source. I compared the ones this memo uses.
- Label values of `outcome_seq = 1` (A10).
- Whether No prices equal 1 minus YES in the kept markets (A2).

Terms (용어):

| English | 한국어 | Short meaning |
| --- | --- | --- |
| CCDF (complementary cumulative distribution function) | 여누적 분포 | Share of wallets above a volume |
| BH (Benjamini-Hochberg) | 거짓 발견율 보정 | Correction for many tests at once |
| z interval | z 구간 | Rate plus or minus 1.96 standard errors |
| Wilson interval | 윌슨 구간 | Another rate interval, outside the lectures |
| chord | 현 | Straight line between two curve points |
| SSB (between-group sum of squares) | 집단 간 제곱합 | Spread of group means |
| ARI (adjusted Rand index) | 군집 일치 지수 | Agreement of two clusterings, removed by D-026 |
| KS (Kolmogorov-Smirnov) | 분포 거리 검정 | Largest gap between two CDFs |
