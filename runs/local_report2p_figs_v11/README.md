# local_report2p_figs_v11

- What: three report figures redrawn at their exact printed size in papers/course_report_mvp1/main.tex (text 7.5 pt, no scaling).
- Why: the full-width originals printed at 4.5 to 5 pt, below the 7 pt rule (.claude/rules/figures.md section 4).
- Input (saved outputs only): runs/142082_mvp1_full_v1r3/q1_bins.csv and q1_bins_no_min.csv; runs/145892_ccdf_v6/ccdf_points.csv; runs/145897_q3figs_v8/qq_points.csv (Trade size rows).
- Output: fig4_calibration_gap_half.png (4.088 x 4.7 in), fig6_ccdf_top_sampled_half.png (3.504 x 2.3 in), qq_trade_size_raw_log_half.png (3.65 x 2.3 in). Copied to papers/paper_mvp1/figures/.
- Width rule: minipage fraction (0.56, 0.48, 0.50) x 7.3 in text width (letter, margin 0.6 in).
- Check: the QQ line and r match runs/145897_q3figs_v8/manifest_q3_figs.json (raw r 0.285, log r 0.994).
- Command: `OMP_NUM_THREADS=1 timeout 300 uv run python code/fig_report2p_half.py` (from cs6344_group_01).
- Used in: papers/course_report_mvp1/main.tex (Figures 1 to 3).
