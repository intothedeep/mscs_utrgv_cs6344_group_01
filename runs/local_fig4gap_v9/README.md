# local_fig4gap_v9

- What: calibration figure with a second panel, gap = observed rate minus mean price (percentage points), 95% z interval.
- Input: runs/142082_mvp1_full_v1r3/q1_bins.csv (with filter, 10 bins), q1_bins_no_min.csv (without filter). Saved outputs only.
- Interval: rate +- 1.96 sqrt(rate (1 - rate) / n). The gap interval uses the same half-width around the gap.
- Output: fig4_calibration_gap.png (copied to papers/paper_mvp1/figures/fig4_calibration_gap.png).
- Command: `OMP_NUM_THREADS=1 timeout 300 uv run python code/fig_calibration_gap.py` (from cs6344_group_01).
- Check: the script compares the 10 main gaps and 2 no-filter gaps with papers/paper_mvp1/numbers.tex. All matched.
- Used in: paper_mvp1 Figure for Q1 calibration (to replace fig4_calibration_z.png; main.tex not edited).
