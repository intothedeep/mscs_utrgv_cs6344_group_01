# local_r3figs_v13

Redraw of the seven r3 paper figures after D-047 (M2 uses the z interval, not Wilson). No model fit.

| Item | Value |
| --- | --- |
| Input | `runs/150310_r3_review_fixes_v6` (JSON and CSV only) |
| Output | `fig_r3_*.png`, same names as v12 |
| Used in | `papers/paper_mvp1/figures/` (M2 only) |
| Script | `code/fig_r3_paper.py` |

Change from v12: M2 error bars end at `mean_price + z_low` and `mean_price + z_high` from `m2_bins_yes_no.csv`. Legend: "95% z interval". The other six PNGs are byte-identical to v12.

Re-run from `cs6344_group_01/`:

```bash
OMP_NUM_THREADS=1 timeout 300 uv run python code/fig_r3_paper.py \
  --r3 runs/150310_r3_review_fixes_v6 --macros papers/paper_mvp1/numbers.tex \
  --out runs/local_r3figs_v13
```

- The script checks 40 plotted numbers against the `RThree` macros (40 of 40 equal).
- The old paper copy is renamed `x_fig_r3_m2_yes_reliability_v12.png`.
