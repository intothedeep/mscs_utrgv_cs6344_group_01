# MVP2: Does Polymarket Accuracy Depend on Topic, Deadline and Volume?

MVP2 asks when the crowd is more right, by topic, by time to the deadline, and by market volume. It adds to MVP1 and does not repeat it. See [README.md](../README.md) for the project, the data layers, the funnel and the constraints.

## Research questions

| | Question | MVP |
|---|---|---|
| Q1a | Does accuracy depend on the topic? | MVP2 |
| Q1b | Does the market get smarter near the deadline? | MVP2 |
| Q1c | Are busier markets more accurate? | MVP2 |

## Data we use

MVP2 uses the same layers as MVP1 and the same kept markets. The kept set has 47,948 markets (10 or more trades). The layer table and the funnel from 688,131 markets are in [README.md](../README.md).

Which field carries the information each MVP2 question needs:

| Information | Source column | Used by |
| --- | --- | --- |
| Topic | `category_refined`, missing = "Unknown" | Q1a |
| Price at T - 1 day | `p_event` | Q1a, Q1b, Q1c |
| Price at T - 7 days | `p_event` | Q1b |
| Outcome y (1 = the Yes leg won, 0 = it lost) | `winning_outcome_label` and the `outcome_seq = 1` leg's `outcome_label` | Q1a, Q1b, Q1c |
| Close time T | `close_at` | Q1b |
| Market open time | `opens_at` | Q1b |
| Volume | `volume_usdc`, summed over all trades of the market in scope | Q1c |
| Trade count | `n_trades` | Q1c (secondary) |

`usdc_amount` is the trade size. USDC is a US-dollar stablecoin.

Source: `analysis/prereg_mvp2.md`, `runs/142083_mvp2_full_v2r3/tables_summary.json`, `../../tips/group_01/polymarket_plan_detailed.md` (section 0).

## How we filter the data

The population for every sub-question is the kept set above. It is the Q1 main set, with the 10-trade filter. Q1b and Q1a add filters.

```
47,948 markets kept (Q1a, Q1c use all of them)
  |-- opens_at at least 7 days before T     21,816 remain
  |-- fresh price at T - 7 days             14,169 remain
  v
 Q1b set
```

| Filter | Rule | Why |
| --- | --- | --- |
| Open at least 7 days | `opens_at` <= T - 7 days | The sources give no reason |
| Fresh 7-day price | `p_7d` is the mean `p_event` at the last timestamp at or before T - 7 days, at most 24 h old | Same staleness rule as T - 1 day |
| Same markets at both horizons | Q1b compares each market at 7 days and at 1 day | The sources state the choice and give no reason |
| Topic missing | Label the topic "Unknown" | The sources give no reason |
| Small topic | A topic with fewer than 30 kept markets joins "Merged" | The sources give no reason. 30 is `min_category_n` |

- Q1a and Q1c use the 47,948 kept markets, not the Q1b set.
- "Merged" is not a drop. Those markets stay in the test.
- The favorite is the side with a 1-day price of 0.5 or more. A favorite won when that side won.
- The 7-day price uses the same tie rule as the 1-day price: the mean `p_event` at the last timestamp.

Source: `runs/142083_mvp2_full_v2r3/tables_summary.json` (`n_kept`, `n_kept_open_ge_7d`, `n_kept_with_p_7d`), `analysis/prereg_mvp2.md`, `analysis/prereg_mvp2_full.json`, `../DECISIONS.md` D-011.

## Criteria

We fixed the three tests before any MVP2 result. The file is `analysis/prereg_mvp2.md` (D-010). This section lists criteria only.

Terms used below:

- Significance line: p below 0.05 (alpha, the false-alarm limit).
- Brier score: mean squared gap between price and outcome.
- CI (confidence interval): the range that likely holds the true value.
- Cramér's V: size of a chi-square effect on a table, from 0 to 1.
- Cohen's d: size of a mean difference, in standard deviations.
- Spearman rho: rank correlation, from -1 to 1.

| Question | Primary test | Significance line | Effect size | Counts as yes | Counts as no |
| --- | --- | --- | --- | --- | --- |
| Q1a: topic | Chi-square test of independence, topic by favorite won or lost | p < 0.05 | Cramér's V | p < 0.05: accuracy depends on the topic | p >= 0.05: no evidence at this n |
| Q1b: deadline | One-sample t-test of the Brier difference, 7 days minus 1 day | p < 0.05 | Mean difference with 95% CI, Cohen's d | p < 0.05 and mean difference > 0: better near the deadline | p >= 0.05 or difference <= 0: no evidence of a gain |
| Q1c: volume | Spearman rho of log1p(volume_usdc) against per-market Brier error | p < 0.05 | rho with 95% CI | p < 0.05 and rho < 0: busier is more accurate | p >= 0.05 or rho >= 0: no evidence |

- The error of a market is its Brier score (p - y)². Q1a and Q1c use the 1-day price. Q1b uses both prices.
- The three tests are each judged at 0.05. There is no adjustment across the three.
- Q1a reports n per category.
- The pilot run is a first end-to-end cycle. It gets no verdict. The verdict applies to the full-data run.

Secondary results never change a verdict:

| Question | Secondary |
| --- | --- |
| Q1a | Bin tests per category (n >= 5 per bin), with Bonferroni and BH corrections |
| Q1a | ANOVA and a permutation test of Brier across categories, with eta squared |
| Q1b | KS test of p for Yes against No, at 7 days and at 1 day |
| Q1b | Absolute-error difference |
| Q1b | Mean entropy H(p) at 7 days against 1 day. The drop is expected by construction |
| Q1c | Spearman for log1p(`n_trades`) |
| Q1c | z-score and robust scaling of volume, trades and error |

The permutation test uses 1,000 permutations and seed 42.

Amendments, honest record:

- The MVP1 evaluation-price amendment also covers the 7-day price (D-011). It came after the first full Q1 result. The MVP1 verdict did not change.
- The merge group for small topics was first named "Other". We renamed it "Merged" because "Other" is a real `category_refined` value.
- The rename came after review and before any v3 result. No criterion changed.

Source: `analysis/prereg_mvp2.md`, `analysis/prereg_mvp2_full.json`, `../DECISIONS.md` D-010, D-011.

## Constraints

The constraints in [README.md](../README.md) apply to MVP2 unchanged.

Source run: `runs/142083_mvp2_full_v2r3`.
