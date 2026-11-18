# local_r2close_v14

- What: Q1 calibration repeated with the last price before the close (p_T), next to p_1d.
- Why: tests the timing hypothesis on the tips page (step 14, part 10). Owner request 2026-11-18.
- Input: runs/142123_robust_full_v4/r2_markets.csv (47,948 kept markets: p_1d, p_T, outcome y). Saved outputs only.
- Method: same as code/q1_calibration.py. 10 equal-width bins, chi-square goodness of fit (df 10), exact two-sided binomial test per bin, BH and Bonferroni at 0.05.
- Gate: p_1d must reproduce run 142082 (chi-square 67.99, 5 BH bins). It does.
- Output: results.json, bins_p_1d.csv, bins_p_T.csv.
- Result: p_T chi-square 53.6, p 5.7e-8, 5 BH bins (0, 6, 7, 8, 9), 3 Bonferroni, 9 of 10 bins negative, net gap -0.65% (p_1d: 68.0, 5, 4, 9, -0.99%).
- Command: `OMP_NUM_THREADS=1 timeout 300 uv run python code/r2_close_calibration.py` (from cs6344_group_01). Local, 1 core.
- Used in: tips/polymarket_lecture_rq_guide_tips.html only. Not in the paper.
