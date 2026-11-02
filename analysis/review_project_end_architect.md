Verdict: the design holds, and every number traces to a saved run. Clean-clone rebuild fails today. Four plan lines lag D-024 to D-028, and one open task contradicts D-026.

# Project-end review: system-architect part

- Date: 2026-11-01. Scope: MVP1 (D-016). Deadline: 2026-11-15 (D-021).
- Remit: does what was built match the design and the plan's contract?
- Nothing ran. I read files only, and edited only this file.
- Marks: **[F]** fact from a named file. **[J]** my judgment. **[?]** needs an answer.
- Git state comes from reading the submodule index file, `.git/modules/.../cs6344_group_01/index`.
- That index stores full paths: the byte before each path is its length. So absence is meaningful.
- The main session confirms it with `git status`. The index shows staged paths, not commits.
- `analysis/review_mvp1_rq_r3.md` line 11 reports the same uncommitted state.
- Options serve M1 and M4 under S1 and RQ1 to RQ3. No option changes a number.
- "Plan line N" means `../tips/group_01/polymarket_plan_detailed.md`. `PLAN.md` is named in full.

Terms: index (스테이징 목록), snapshot (스냅샷: the code copy in a run folder), manifest (실행 기록 파일), provenance (출처 추적), gitignored (git 제외).

## 1. Reproducibility

**Answer: not today. It works after one commit and one environment file, without the cluster, for a rebuild from committed inputs.**

```
runs/142082 (tracked) ─► lecture_numbers.py* ─► lecture_numbers.json*, z PNG*, Lorenz PNG*
runs/142123 r2_markets.csv (gitignored, fetch) ─► q3_box_p1d.py* ─► box PNG*
all of the above ─► make_report.py ─► report_v1.html

runs/142082, 142041, 142140 (tracked)  ┐
runs/142123 results (tracked)          ├► make_paper_numbers.py ─► numbers.tex
runs/142123 markets.csv (gitignored)   ┘
numbers.tex + figures/ (copied by hand, 3*) ─► latexmk ─► main.pdf

* = on disk, not in the index
```

### Missing inputs

| Item | State | Effect on a clean clone |
| --- | --- | --- |
| `code/lecture_numbers.py` | [F] not in index | Cannot regenerate the JSON or 2 figures |
| `code/q3_box_p1d.py` | [F] not in index | Cannot regenerate the box plot |
| `reports/lecture_numbers.json` | [F] not in index | `make_report.py` v1 exits, line 831 |
| `reports/figures/*.png` | [F] not in index | The report prints a skip note for each |
| `papers/paper_mvp1/figures/fig4_calibration_z.png` | [F] not in index | The paper shows a dashed box |
| `papers/paper_mvp1/figures/lorenz_top_shares.png` | [F] not in index | The paper shows a dashed box |
| `papers/paper_mvp1/figures/fig6_ccdf.png` | [F] not in index | The paper shows a dashed box |
| `runs/142123_robust_full_v4/r2_markets.csv` | [F] gitignored by design | Needs fetch to redraw the box plot |
| `runs/142123_robust_full_v4/markets.csv` | [F] gitignored by design | Needs fetch to regenerate `numbers.tex` |
| `pyproject.toml`, `uv.lock`, `.python-version` | [F] at the course repo root, not in the group repo | [J] A clone of the group repo alone gets no dependencies from `uv run` |
| `../tips/group_01/polymarket_plan_detailed.md` | [F] in the parent repo, modified and uncommitted | M1 exit cites a file outside the group repo |

### Traps

- [F] `\figorbox` draws a dashed box and the build still exits 0 (`figkit.sty` line 51).
- [F] So the plan's build AC (0 errors, 0 overfull) passes with a figure missing.
- [F] `Page.figure` skips a missing PNG and the report still writes (`make_report.py` lines 191, 192).
- [F] `add_categories` is skipped when `markets.csv` is absent (`make_paper_numbers.py` line 620).
- [F] Then the 4 `main.tex` lines that use those macros fail at build. That failure is loud.
- [F] `fetch_run.sh` line 12 uses `~/cs6344_polymarket/runs` on the remote host.
- [J] The `~` is the owner's home only. A teammate's account would not resolve it.
- [?] Do teammates have Cradle access? The script needs an answer, or a stated owner-only fetch.
- [F] No rebuild order exists. `papers/README.md` covers `numbers.tex` and the build only.
- [F] `papers/README.md` line 13 says figures come from the run folder. Two come from `reports/figures/`.
- [F] No script copies figures into `papers/paper_mvp1/figures/`.

### Is `reports/lecture_numbers.json` tied to the run?

- [F] By a name only: `source_run` = `142082_mvp1_full_v1r3`.
- [F] It stores its own `code_sha` `d553342cb0d7`, which equals the `CHANGELOG.md` value.
- [F] It stores no input-file hash and no pointer to the run's `code.sha256`.
- [F] `make_report.py` line 830 and `make_paper_numbers.py` line 443 compare the name only.
- [J] Once committed, the git commit pins both sides, because `runs/` stays as committed (D-026).
- [J] So the gap is low risk after the commit, and real before it.

### Paper v1 spans four runs

| Input | Run | Tie that is checked |
| --- | --- | --- |
| Main numbers | 142082 | Run name macro |
| Box plot, category macros | 142123 | [F] Row counts match `tables_summary.json` |
| Equal-frequency BH count | 142140 | [F] `binom_p` compared, stops on a difference |
| Close-time macros | 142041 | [F] None |

- [F] The 142083 and 142082 table match is "by construction". Byte equality is not measured (`00.runs.md`).
- [F] The open G11 row closes that gap.

### Options for the rebuild path (owner picks)

| | What | Gain | Cost |
| --- | --- | --- | --- |
| A stable | Commit derived files, add `pyproject.toml` and `uv.lock`, write one "Rebuild v1" section, tag the submitted commit | A teammate builds with no cluster. The commit is the pointer | [J] About one hour. No input-file hashes |
| B scalable | A, plus `jobs/rebuild_v1.sh` and `reports/manifest_v1.json` with run, input hashes, script hashes, output hashes. Stop on a missing figure | One command, and drift is caught | New code and a new contract, 2 weeks before the deadline |
| C cutting-edge | Content-addressed pipeline (Make or DVC) with a shared store for individual-level files | Full rebuild for anyone | Needs storage and access rules. Individual-level data leaves the cluster |

- [J] All three keep the `.gitignore` individual-level rows unchanged. C alone strains the reason for them.

## 2. Separation of MVP1 and `future_work/`

**Answer: the boundary is clean and one-way. MVP2 should still run. It has not run since the move, and its record would break.**

```
future_work/code/q1a,q1b,q1c ──PYTHONPATH──► code/common.py, code/q1_calibration.py
code/*.py ──────────────────────────────────► nothing in future_work/
```

### What crosses the boundary

| Importer | Imported | Source |
| --- | --- | --- |
| `q1a_category.py`, `q1b_deadline.py`, `q1c_volume.py` | `common`: 5 helpers | [F] import lines |
| `q1a_category.py` | `q1_calibration.bin_table` | [F] exists, line 28 |
| `q1b_deadline.py` | `q1_calibration.LOG_CLIP` | [F] exists, line 20 |
| Any file in `code/` | nothing from `future_work/` | [F] grep is empty, the r2 import is fixed |

### Code in `code/` that serves MVP2

| File | Part | Keep? |
| --- | --- | --- |
| `build_tables.py` | `add_long_horizon_columns`, `p_7d` | [J] Keep. Removal changes the table a rerun builds |
| `verdicts.py` | `q1a`, `q1b`, `q1c`, `CRITERIA` rows | [J] Keep. Skipped when result files are absent |
| `make_summary.py` | `MVP2_STAGES` | [J] Keep. Listed only when a report exists |
| `make_report.py` | `sec_q1a`, `sec_q1b`, `sec_q1c`, `sec_compare`, `--version v2` | [J] Keep. D-017 and D-020 require a way back |
| `make_paper_numbers.py` | `add_q1a`, `add_q1b`, `add_q1c`, unused macros | [J] Keep. Additive by design |
| `common.py` | `horizon_long_days`, `min_category_n`, `n_perm`, `seed` | [F] Not MVP2 only. `q3_describe.py` line 128 and `r2_price_path.py` line 98 read `min_category_n` |

### Can MVP2 run if the owner goes for it (D-020)?

- [F] `future_work/jobs/mvp2.slurm` sets `PYTHONPATH`, snapshots both code folders, and calls the moved files.
- [J] So it should run. It is unproven: no run has used the moved layout.
- [?] Is `future_work/` on the cluster? A pilot job proves this at low cost.
- [F] `verdicts.py` `CRITERIA` points to `analysis/prereg_mvp2.md`. D-017 moved the file to `future_work/analysis/`.
- [F] `sha12` returns null without error (line 19). So Q1a to Q1c would repeat the G7 defect.
- [F] The job writes to `runs/`, and `fetch_run.sh` fetches into `runs/`. The ledger keeps MVP2 runs in `future_work/runs/`, so a hand move follows.
- [F] `future_work/code/q1a_category.py` line 27 keeps its own `group_categories`, and `common.py` has a second copy.
- [J] That copy is the price of "leave MVP2 unchanged" (D-017). Drift risk is low while MVP2 sleeps.
- [F] D-026 applies to MVP1. `future_work/README.02.md` still names Cramér's V, Cohen's d and eta squared.
- [J] Going back to MVP2 therefore means a second lecture-method audit, because the Constraint holds there too.
- [J] Unused macros in `numbers.tex` are harmless. `main.tex` does not use them (AC in `PLAN.md`).

## 3. Code version

**Answer: the run-to-code link holds by snapshot and hash. The labels no longer identify code. The derived layer has only a partial link.**

### Layer 1: cluster runs. The link holds.

- [F] 142082, 142123 and 142140 each track `code_snapshot/` and `code.sha256`.
- [F] `verdicts.json` `verdicts_py_sha256_12` `fdcca90b6588` equals the 142082 `code.sha256` row.
- [J] `code/` moving past the snapshots harms nothing. The snapshot answers "which code made this number".

### Layer 2: derived files. The link is partial.

| Script | Label | Sha recorded where | Gap |
| --- | --- | --- | --- |
| `lecture_numbers.py` | `lecture-v1` | [F] In its JSON and `CHANGELOG.md`, equal | Script not in the index |
| `make_report.py` | `v3` | [F] In the report and `CHANGELOG.md`, equal: `ec268fd9c4d6` | Label misleads, see below |
| `make_paper_numbers.py` | none | [F] `CHANGELOG.md` only | `numbers.tex` does not stamp it |
| `q3_box_p1d.py` | none | [F] Nowhere | No sha on file for the box plot |

### Labels that no longer identify code

- [F] `make_report.py` says `v3` at sha `c37079965d60` in all three snapshots and `ec268fd9c4d6` now.
- [F] `common.py` gained `group_categories` under a "no version bump" row, and it still says `v5`.
- [F] The v5 snapshot in 142140 has sha `61557c0422c3`. It lacks the moved function.
- [J] Any new cluster run would stamp `v5` on different code. This repeats the F6 retro-note pattern.
- [J] The move is safe in effect. The `CHANGELOG.md` row states "moved unchanged", with no hash comparison.
- [F] `rules/measurement.md` §2.2 asks for invariance evidence with each change.
- [F] `jobs/mvp1_b.slurm` now names `kimq` and 8 CPUs. Run 142082 used `gpul40q` and 16 CPUs (`00.runs.md`).
- [F] `common.py` line 84 ties thread count to the v1 and v2 non-determinism.
- [J] A full rerun may not match bytes. No plan row needs one, so do not rerun.

### Options (owner picks)

| | What | Gain | Cost |
| --- | --- | --- | --- |
| A stable | Add two `CHANGELOG.md` lines: the `q3_box_p1d.py` sha, and "labels of derived scripts do not identify code, use the sha". Bump `common.py` before any cluster run | Honest record, no code change | Labels stay loose |
| B scalable | A, plus `make_paper_numbers.py` and `q3_box_p1d.py` stamp their own sha, with a run-style manifest beside the outputs | Every derived file names its code | Small code change, then regenerate |
| C cutting-edge | Stamp a git commit id into every output | One id for everything | Needs a clean tree before each build, which this shared checkout lacks |

## 4. Decision hierarchy against D-025 to D-028

**Answer: no owner line is broken in substance. One open task contradicts D-026. Four lower lines lag the decisions.**

| Line | Says | Decision | Finding |
| --- | --- | --- | --- |
| `PLAN.md` G7 row | [F] "re-issue verdicts for run 142082" | [F] D-026: "`runs/` stay as committed" | **Real conflict.** Task against an owner decision. Goes to the owner. See options below |
| Plan line 118 | [F] Main Q2 answer comes from "the shares and the Lorenz curve" | [F] D-028: a picture of the top shares. README line 488: "a labeled figure, not an analysis" | Wording conflict. Lorenz cannot be a main source and also only a picture |
| Plan line 124 | [F] "test 80/20 rather than assume it" | [F] D-024: descriptive reference, not a verdict line | Wording conflict |
| Plan line 32 | [F] "All lecture concepts" | [F] D-026 removes the independence test | [J] Holds at lecture level, since L12 stays through goodness of fit. The line 40 note is enough until the owner edits |
| Plan lines 32, 38 | [F] "three forced uses" | [F] D-026 removes one | [F] Row 128 shows two remain: ANOVA with permutation, Spearman. One owner edit |
| Plan line 169 | [F] "three forced Q2 tests stay" in MVP2 | [F] v2 is unchanged | [J] Still true of report v2. No action |
| Mission, `STATUS.md` Constraints | [F] "only methods from our lectures", no exception | [F] D-028 keeps Lorenz, labeled outside | [J] The owner's later word governs. The text lacks the exception, which only README line 488 states |
| Constraint: effect size next to every p-value | [F] D-026 removes w, d, V, d_z | [F] Box 4 names "difference, D, ρ" | [J] Consistent in form. The chi-square p now has per-bin gaps. `reviewer` and `data-analyst` check each row |
| Vision: "topics and horizons" | [F] Kept by D-020 | [F] MVP1 does not answer them | [J] No conflict, since a Vision has no date. But the paper states no gap |
| `RQ.md`: 6 answered | [F] RQ4 to RQ6 cite `future_work/runs/` | [F] D-016: not a target | [J] True, evidence exists. Only the owner edits RQ rows. No action |
| `.claude/rules/visualization.md` §7 | [F] Asks for three panels: f(x), x f(x), Lorenz | [F] D-026: "D-025 wins" here. D-028 restores Lorenz only | [F] The audit put this to the owner (line 248). Resolved. The exception sits only in a D-row |

Notes on the rows above:

- [F] The only place for the Vision gap sentence is `main.tex` line 684, an owner todo on future work.
- [J] If the owner deletes that todo with no text, the paper never names the gap.
- [F] `fig7_lorenz.png` prints Gini in its legend. So the 4-point redraw has a reason, and it is not a defect.
- [J] §7 protects against reading an area as a share. CCDF plus Lorenz has no such area, so no harm remains.
- [F] Panels 1 and 2 of §7 are absent from the `main.tex` figure list.
- [J] Drawing them needs wallet rows, so a job.
- [J] A later reviewer will flag §7 again unless the exception is written where rules live.
- [F] `rules/docs.md` §6: repo exceptions belong in the owner's section of root `CLAUDE.md`. Agents never write there.

### Options for G7 (owner picks)

Facts first:

- [F] The Q1 hash is null (`verdicts.json` line 29).
- [F] `verdicts.py` hashes the working file. The prereg note has changed that file.
- [F] So a plain re-issue cannot meet the AC, which needs the hash from `f78de3e`.
- [F] `prereg.json` is in the run folder, so the numeric criteria are pinned already.

| | What | Keeps D-026? | Cost |
| --- | --- | --- | --- |
| A stable | Leave `verdicts.json`. Record prereg commit and hash in the `00.runs.md` row. Rewrite the G7 AC | Yes | One edit. The file itself keeps a null |
| B scalable | Write `analysis/verdict_criteria_pin.json`: run, file, commit, hash. Rewrite the AC | Yes | One small file. A second place to look |
| C cutting-edge | Change `verdicts.py` to take a pinned hash, bump the version, re-issue into the run | No. The owner lifts D-026 for this file | Code change. The verdict file changes after citation |

- [F] `verdicts.py` reads saved JSON only, so C may fit "Allowed locally". The main session decides.

## 5. Before 2026-11-15, ranked

### Must change

| Rank | Item | Who | Why this rank |
| --- | --- | --- | --- |
| 1 | Commit today's state: `code/`, `reports/`, `papers/paper_mvp1/figures/`, `analysis/`, living docs. Also commit the parent repo's plan file | Main session | [J] A lost checkout loses everything. It unblocks a clone, at low cost |
| 2 | Write or remove 4 owner todos, then finish F5. State the Vision gap in the closing text if wanted | Owner, then `sonnet-writer` | [F] Open rows. The paper cannot ship with them |
| 3 | Pick the 3-person split | Owner | [F] Open row. Teammates wait on it |
| 4 | Pick the rebuild option (§1), and answer Cradle access | Owner, then `developer` | [J] Without it, teammates depend on the owner's laptop |
| 5 | Pick the G7 option (§4) | Owner | [F] The open row contradicts D-026 |
| 6 | Add a missing-figure check to the final build AC: every `\figorbox` target exists | `product-manager` | [F] Today's build AC cannot catch it |
| 7 | Run the G11 parquet hash compare | Main session, cluster | [F] Open row. It proves the 142140 tie. Not equal stops work |
| 8 | Owner edits plan lines 32, 38, 118, 124, and the `STATUS.md` Constraint row | Owner | [J] No number depends on them. The next reader will trip on them |
| 9 | Record the derived-layer sha gap and the v5 label (§3) | Main session | [J] Record only. Bump `common.py` before any cluster run |
| 10 | Clean stale text, listed below | Main session or `sonnet-writer` | [J] Cosmetic |

Stale text for rank 10:

- [F] README line 272 shows the G17 note as open. `PLAN.md` closed it.
- [F] `papers/README.md` line 3 says "Two LaTeX papers", against D-023.
- [F] `make_paper_numbers.py` lines 7 and 8 show old MVP2 paths.
- [F] Plan line 153 cites `papers/paper_mvp2/numbers.tex`, which moved.
- [J] Add one note to `future_work/README.02.md`: the `CRITERIA` path, and the second audit.

### Should not change

| Item | Why |
| --- | --- |
| `runs/` and the prereg files | [F] D-026. They are the evidence |
| `q1_calibration.py`, `r1_split_payout.py`, `q2_concentration.py` outside methods | [J] They match the snapshots. `lecture_numbers.py` is the right layer for lecture names |
| `common.py` defaults | [F] MVP1 reads `min_category_n` |
| Extra macros in `numbers.tex` | [F] By design, and the paper does not use them |
| MVP2 paths in `make_report.py` and `make_paper_numbers.py` | [F] D-017, D-020 |
| `verdicts.py` `CRITERIA` code | [J] Note it only. Fixing it now touches a cited stage for no target |
| `.gitignore` individual-level rows | [F] Deliberate |
| `future_work/` contents | [F] D-017 |
| Any new cluster analysis, power-law test or lognormal run | [F] D-025, D-027 |
| Full rerun of 142082 | [J] Different partition and CPU count. It risks numbers for no gain |

### Do not do before the deadline

- The `make_report.py` split row.
- [F] Its AC asks for byte-equal HTML, but the page prints the script's own sha (lines 789, 802).
- [F] So that AC cannot pass as written. `product-manager` rewrites it if the row stays open.
- [J] The `code.md` 400-line review line is passed by a wide margin. That is debt, not risk.

## Unverified

- [?] Current sha of `code/*.py` against `CHANGELOG.md`. Checking needs a hash run, and I ran nothing.
- [?] k-means share since D-026. The `PLAN.md` value 0.0974 came before the lecture edits. `reviewer` re-measures.
