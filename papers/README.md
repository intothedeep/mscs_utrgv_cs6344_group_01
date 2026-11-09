# papers

Two LaTeX documents for MVP1 (scope: root `CLAUDE.md`, D-016). Every number is a macro from `numbers.tex`.

MVP2 is out of scope. Its papers sit in `../future_work/papers/` (D-016, D-017).

| Folder | What it is | Run |
| --- | --- | --- |
| `paper_mvp1/` | Full paper. Body in two columns, then References, then appendices A to G | `runs/142082_mvp1_full_v1r3` |
| `course_report_mvp1/` | 2-page course report. It reuses the figures of `paper_mvp1/figures/` | same run |
| `references_verified.bib` | Citations checked against their sources | |

## Layout of `paper_mvp1`

Why this layout: the body stays near conference length and keeps the core flow, Question to Conclusion (D-042, D-043, D-045).

| Part | Layout | Why |
| --- | --- | --- |
| Sections 1 to 8, Introduction to Conclusion | Two columns, article class, 10 pt, margins 0.7 in, column gap 0.25 in | Body figures are drawn at column width |
| Wide floats `fig:flow` and `tab:checks` | Span both columns | They need the full width |
| Section 9, References | One column, own page | Owner request, 2026-11-09 |
| Appendices A to G | One column, each on a new page | Their figures are drawn for full width and `[H]` needs one column |

Read the page numbers from `main.aux`. They change when the text changes.

## Source files

`main.tex` holds the preamble, the title and the abstract. It `\input`s one file per section from `sections/`.

| Files | Content |
| --- | --- |
| `01-intro.tex` to `13-conclusion.tex` | Body sections 1 to 8 (Introduction, Related Work, Data, Methods, Results, Discussion, Limitations, Conclusion) |
| `05-results.tex` to `09-res-checks.tex` | Results: Q1, Q2, Q3, and the summary table `tab:checks` |
| `app-a-data.tex` to `app-g-review.tex` | Appendices A to G, one file each |

The `\appendix` block of `main.tex` starts every appendix section on a new page.

## Figures

`figures/` holds PNG copies from the run folders. The paper uses the files named in `\includegraphics`. Other files in the folder are unused copies. `fig:flow` and `fig:timeline` are TikZ and have no PNG.

## Regenerate numbers.tex

Run from `cs6344_group_01/`. The script reads saved JSON and CSV only.

```bash
OMP_NUM_THREADS=1 timeout 300 uv run python code/make_paper_numbers.py \
  --run runs/142082_mvp1_full_v1r3 --pilot runs/142041_pilotA_2025_06 \
  --robust runs/142123_robust_full_v4 --q1eqfreq runs/142140_q1eqfreq_v5 \
  --r3 runs/150310_r3_review_fixes_v6 --out papers/paper_mvp1/numbers.tex
```

| Option | What it adds |
| --- | --- |
| `--pilot <dir>` | Pilot close-time macros |
| `--robust <dir>` | `Rob*` macros from `r1_results.json` and `r2_results.json`, the robustness code version, and the per-category scope table from `markets.csv`. Without it the paper does not compile |
| `--q1eqfreq <dir>` | `p_bh` and `reject_bh` of the equal-frequency bins (run 142140). Without it the script computes the BH count itself |
| `--r3 <dir>` | `RThree*` macros for checks M1 to M5, duplicate rows and peer asks (run 150310, code v6, D-038, D-039) |

- `numbers.tex` is generated. Do not edit it by hand.
- `CodeSha` is the hash of `q1_calibration.py`. `CodeSetSha` and `RobustCodeSha` hash the run's `code.sha256`.
- Macro names use letters only. Numbers are spelled, for example `\BinTenTwentyObs`.
- A comment above each macro names its source file and key.
- Number formats come from the rule table at the top of `code/make_paper_numbers.py`.

## Build

Run inside a paper folder.

```bash
latexmk -pdf main.tex
```

Clean build: `latexmk -C && latexmk -pdf main.tex`.

`x_base_d042/` is a gitignored scratch copy of the pre-restructure paper (D-042). Do not read from it.
