# local_r3figs_v10

Plain-word redraw of the seven r3 paper figures. No model fit.

| Item | Value |
| --- | --- |
| Input | `runs/150310_r3_review_fixes_v6` (JSON and CSV only) |
| Output | `fig_r3_*.png`, same names as the run folder |
| Used in | `papers/paper_mvp1/figures/` |
| Script | `code/fig_r3_paper.py` |

Re-run from `cs6344_group_01/`:

```bash
OMP_NUM_THREADS=1 timeout 300 uv run python code/fig_r3_paper.py \
  --r3 runs/150310_r3_review_fixes_v6 --macros papers/paper_mvp1/numbers.tex \
  --out runs/local_r3figs_v10
```

- The script checks 40 plotted numbers (gaps, interval ends, n) against the `RThree` macros in `numbers.tex`.
- M5: the run did not save the bootstrap fits. The grey bars are the saved 95% intervals at the 7 grid prices (`m5_calibration_fit.json: delta_table`). The line is expit(a + b logit p) - p from the saved a and b. The cluster figure showed a smooth band.
- M2: saved Wilson ends are on the gap scale, so the plot adds `mean_price` to them.
- Old copies in `papers/paper_mvp1/figures/` are renamed with an `x_` prefix.
