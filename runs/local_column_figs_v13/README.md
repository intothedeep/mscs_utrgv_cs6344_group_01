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

Update: the combined calibration figure is also split in two, for the column layout (same 3.425 in width, 300 dpi, 7.5 pt):
- `fig4_calibration_rate_col.png`, 3.425 x 2.7 in: rate against price, legend on top.
- `fig4_calibration_gap_panel_col.png`, 3.425 x 2.1 in: per-bin gap with 95% z intervals. It has its own legend (zero gap, two series) and the same x range (0 to 1) as the rate figure.
- Same bins, colours and x shift as `fig4_calibration_gap_col.png`, which is unchanged (md5 equal before and after the re-run).
- Both are copied to `papers/paper_mvp1/figures/`.
