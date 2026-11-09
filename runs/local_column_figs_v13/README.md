# local_column_figs_v13

Column-width redraw of three body figures for the two-column paper (D-045, PL-12a). No model fit.

| Item | Value |
| --- | --- |
| Input | saved outputs read by `code/fig_report2p_half.py`: `q1_bins.csv`, `q1_bins_no_min.csv` (run 142082), `ccdf_points.csv` (run 145892), `qq_points.csv` (run 145897) |
| Output | `fig4_calibration_gap_col.png`, `fig6_ccdf_top_sampled_col.png`, `qq_trade_size_raw_log_col.png` |
| Used in | `papers/paper_mvp1/figures/` (same names). The `*_half.png` files of the 2-page course report are untouched |
| Script | `code/fig_column_widths.py` (reuses the draw functions of `code/fig_report2p_half.py`) |
| Size | width 3.425 in = (8.5 - 2 x 0.7 - 0.25) / 2; heights 4.6 (calibration), 2.5 (CCDF), 2.6 (QQ); 300 dpi |
| Text | 7.5 pt everywhere, drawn at print size |
| Not redrawn | `fig:timeline`: it is TikZ in `04-methods.tex`, not an image |

Change in shared code: `draw_calibration` got a `legend_ncol` argument (default 3, so the half figure is unchanged). The column figure uses 2 so the legend fits.

Re-run from `cs6344_group_01/`:

```bash
OMP_NUM_THREADS=1 timeout 300 uv run python code/fig_column_widths.py
```
