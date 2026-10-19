# Pre-registration: MVP2 (written before any MVP2 result)

- Date: 2026-10-19. Extends `analysis/prereg_mvp1.md`. All MVP1 choices stay.
- Parameters: `analysis/prereg_mvp2.json`. New keys: `horizon_long_days` 7, `min_category_n` 30, `n_perm` 1000, `seed` 42.
- Population for every sub-question: markets kept WITH the min_trades filter (the Q1 main set).

## Choices

| Choice | Value |
| --- | --- |
| Category | `category_refined`. Missing = "Unknown". Fewer than 30 kept markets = merged into "Other" |
| Favorite | the side with p_1d >= 0.5. Favorite won = (p_1d >= 0.5 and y = 1) or (p_1d < 0.5 and y = 0) |
| Error of a market | Brier = (p − y)². p_1d for Q1a and Q1c. Both p_7d and p_1d for Q1b |
| p_7d | last `p_event` at or before T − 7 days, at most 24 h old |
| Q1b markets | kept, `opens_at` <= T − 7 days, fresh p_7d. The same markets at both horizons |
| Volume, trades | `volume_usdc` and `n_trades` over all trades of the market in scope |
| Tests | alpha 0.05. Permutation test: 1,000 permutations, seed 42 |

## Decision criteria (rules/measurement.md §1)

| Item | Q1a: topic | Q1b: deadline | Q1c: volume |
| --- | --- | --- | --- |
| Primary metric | chi-square test of independence, category × {favorite won, favorite lost} | one-sample t-test of the per-market Brier difference (7 d − 1 d) | Spearman rho of log1p(volume_usdc) vs per-market Brier error |
| Line | p < 0.05: accuracy depends on the topic | p < 0.05 and mean difference > 0: better near the deadline | p < 0.05 and rho < 0: busier is more accurate |
| Contrast | the categories against each other | the same markets at 7 d against 1 d | markets with low against high volume |
| Effect size | Cramér's V, reported next to p | mean difference with 95% CI, Cohen's d | rho with 95% CI |
| Failure condition | p >= 0.05: "no evidence that accuracy depends on the topic at this n" | p >= 0.05, or mean difference <= 0: "no evidence of a gain near the deadline at this n" | p >= 0.05, or rho >= 0: "no evidence that busier markets are more accurate at this n" |

## Secondary results (do not change the verdict)

| Sub-question | Secondary |
| --- | --- |
| Q1a | Bin tests per category (n >= 5 per bin), Bonferroni and BH over all category × bin tests. ANOVA and permutation test of Brier across categories, with eta squared |
| Q1b | KS test of p for Yes vs No at 7 d and at 1 d. Absolute-error difference. Mean H(p) at 7 d vs 1 d: the drop is expected by construction |
| Q1c | Spearman for log1p(n_trades). z-score and robust scaling of volume, trades and error |

- The three primary tests are each judged at 0.05. There is no adjustment across the three.
- The pilot run (`scope = pilot`) is the first end-to-end cycle of MVP2. It gets no verdict.
- The verdict applies to the full-data run with these same parameters.
- Q1a: report n per category. The plan expected Sports to be under-represented. The pilot had 921 Sports markets in scope (`runs/142041_pilotA_2025_06/value_counts.csv`), so the report states the real n.
