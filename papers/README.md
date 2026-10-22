# papers

Two LaTeX papers (DECISIONS D-014). Every number is a macro from `numbers.tex`.

| Folder | Scope | Run |
| --- | --- | --- |
| `paper_mvp1/` | MVP1 | `runs/142082_mvp1_full_v1r3` |
| `paper_mvp2/` | MVP1 + MVP2 | `runs/142083_mvp2_full_v2r3` |

Each folder holds:

- `numbers.tex`: generated macros, one `\newcommand` per number. Do not edit by hand.
- `figures/`: PNG copies from the run folder, same names.
- `figkit.sty`: copy of `.claude/skills/latex-figkit/figkit.sty`.

## Regenerate numbers.tex

Run from `cs6344_group_01/`. The script reads saved JSON and CSV only.

```bash
OMP_NUM_THREADS=1 timeout 300 uv run python code/make_paper_numbers.py \
  --run runs/142082_mvp1_full_v1r3 --pilot runs/142041_pilotA_2025_06 \
  --robust runs/142123_robust_full_v4 --q1eqfreq runs/142140_q1eqfreq_v5 --out papers/paper_mvp1/numbers.tex
OMP_NUM_THREADS=1 timeout 300 uv run python code/make_paper_numbers.py \
  --run runs/142083_mvp2_full_v2r3 --pilot runs/142041_pilotA_2025_06 \
  --robust runs/142123_robust_full_v4 --q1eqfreq runs/142140_q1eqfreq_v5 --out papers/paper_mvp2/numbers.tex
```

- `--pilot <dir>` adds the pilot close-time macros. `--robust <dir>` adds `Rob*` macros from `r1_results.json` and `r2_results.json` (a stage whose file is absent is skipped), the robustness code version, and the per-category scope table from the run's `markets.csv` (three columns, checked against the main run's counts).
- Omitting `--robust` drops every `Rob*` macro and the per-category scope macros, so the papers will not compile.
- `CodeSha` is the hash of `q1_calibration.py` alone. `CodeSetSha` and `RobustCodeSha` hash the run's `code.sha256`, which lists every script.
- `--q1eqfreq <run dir>` (code v5 run of `jobs/q1_only.slurm`) reads `p_bh` and `reject_bh` of the equal-frequency bins. Both commands use run 142140. Without it, the script computes the BH count itself and says so in the macro comment.
- Number formats are set by the rule table at the top of `code/make_paper_numbers.py`.
- Macro names use letters only. Numbers are spelled, for example `\BinTenTwentyObs`.
- A comment above each macro names its source file and key.
- `paper_mvp1` defines the MVP1 macros. `paper_mvp2` defines the same names plus the MVP2 macros.

## Build

Run inside a paper folder. The main file name is chosen when the text is written.

```bash
latexmk -pdf main.tex
```
