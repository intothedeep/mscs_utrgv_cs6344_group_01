# local_r3figs_v12

Print-size redraw of the seven r3 paper figures (gate review F4, F5). No model fit.

| Item | Value |
| --- | --- |
| Input | `runs/150310_r3_review_fixes_v6` (JSON and CSV only) |
| Output | `fig_r3_*.png`, same names as v10 |
| Used in | `papers/paper_mvp1/figures/` |
| Script | `code/fig_r3_paper.py` |
| Size | drawn at print width: 5.36 in (0.8 linewidth) and 3.685 in (M2, 0.55 linewidth); 300 dpi |
| Text | 7.5 pt everywhere, so printed text is 7.5 pt (7 pt or more, figures.md section 4) |

Changes from v10:
- F5: figsize equals print size, font 7.5 pt, dpi 300.
- F4: `fig_r3_m5_implied_gap.png` draws the practical line, plus and minus `mean_h` from `m1_results.json` (dotted, in the legend).

Re-run from `cs6344_group_01/`:

```bash
OMP_NUM_THREADS=1 timeout 300 uv run python code/fig_r3_paper.py \
  --r3 runs/150310_r3_review_fixes_v6 --macros papers/paper_mvp1/numbers.tex \
  --out runs/local_r3figs_v12
```

- The script checks 40 plotted numbers against the `RThree` macros in `numbers.tex` (40 of 40 equal).
- M5 and M2 notes are the same as in `runs/local_r3figs_v10/README.md`.
- Old copies in `papers/paper_mvp1/figures/` are renamed `x_<name>_v10.png`.

Update (same session): the M2 legend now reads "Markets labelled Yes/No" (F12). All seven PNGs were regenerated in place; only M2 differs from the first v12 write.
