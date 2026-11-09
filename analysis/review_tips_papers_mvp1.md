# Review: paper summaries tips page, review tips page, paper_mvp1 working tree

- Reviewer: `reviewer` agent. Date: 2026-11-08. Owner request: "review tip and paper mvp1".
- Baseline: commit 16b6661 (gate review cycles 1 and 2 PASS, `analysis/review_gate_mvp1_r3.md`). Only changes since then are re-checked.
- Mode: report only. No file under review was edited.
- Local runs: `latexmk` build, headless Chrome renders (Playwright, channel chrome, 1040 px), `grep`, one static check over the saved HTML (`uv run python -I`, one core), one `curl` of arXiv 0706.1062 to the scratchpad plus `pdftotext` (read of a saved file, no model, no dataset).

## Targets

| ID | Target | State vs 16b6661 |
| --- | --- | --- |
| A | `tips/polymarket_paper_summaries_tips.html` (+ `tips/index.html` tab `papers`, `tips/README.md` row) | new, untracked |
| B | `tips/polymarket_paper_review_tips.html` | unchanged (no diff). Checked against the paper's current state only |
| C | `papers/paper_mvp1/main.tex` | uncommitted edits: 380-382 (Clauset sentences, new `\todo`), 961 (Sports wording) |

## Verdict: **ISSUE** (A). B and C PASS.

- Why ISSUE: the new page fails two of its named acceptance checks on the file they name. (A1) The flowchart draws Methods Q3 as "cites nothing", but `main.tex:380` now cites Clauset there. (A2) English mode shows Korean in the tab group labels and panel badges. Both are text fixes. No re-run, no number changes, no verdict change.
- Why not worse: every number on the page matches `analysis/paper_summaries_refs.md`; partial marks (Brier 1950, Page and Clemen 2013) and `[LOW-CONFIDENCE]` are kept; all 12 subtabs open by hash in both languages at scrollWidth 1040; 63 of 63 term links resolve; 0 em dash, 0 semicolon, 0 "Abbreviations:" line.
- Root cause of A1 and the stale items: `paper_summaries_refs.md` was written against 16b6661. The paper then changed (Clauset citation added at 380, Sports wording fixed at 961). The page is faithful to its source file, and the source file is behind the paper.

## C. `papers/paper_mvp1/main.tex` (working tree)

| Check | Result | Evidence |
| --- | --- | --- |
| Build `latexmk -C && latexmk -xelatex main.tex` | PASS | exit 0, 22 pages (`main.log` "Output written on main.xdv (22 pages)") |
| Undefined refs or cites | PASS | 0 (`grep -ci undefined main.log`) |
| Overfull | PASS | 0 |
| `\todo` count | PASS | 5: lines 186, 382 (new), 926, 940, 1010 (line 39 is the macro definition) |
| Em dash, `---` | PASS | 0 hits (style.md §3 grep) |
| L961 Sports sentence | PASS | "Sports markets fall disproportionately into Neg-Risk or Up/Down" matches `paper_summaries_refs.md` entry 1 ("disproportionately fall into", [S-PS-2]). The earlier "most" overstatement is gone |
| L380-381 Clauset x_min sentence | PASS (verified) | arXiv 0706.1062 PDF, section 3.3 "Estimating the lower bound on power-law behavior", after eq. (3.9): "Here S(x) is the CDF of the data ... Our estimate x̂min is then the value of xmin that minimizes D." (`pdftotext` line 831). So "Unlike that method, we fix x_min at the top 10% and do not choose it by the smallest D" is a correct contrast. Fetched by `curl` to the scratchpad, not WebFetch |
| Every citation vs `paper_summaries_refs.md` | PASS, one note (C-1) | 20 `\cite` lines checked against the entries. 122 counts, 151-153 Snowberg, 155-157 Table 3 cheap tokens (refs Note 2: "under 30 cents" vs source "≤0.30", rounding holds), 161 Brier panel, 168 Wolfers, 171 Page, 174 Le counts, 178 Gneiting, 181-185 Clauset, 193/198 dataset card, 196/200 Up/Down, 328 BH, 336 Brier, 380 Clauset, 388 DuckDB, 460 Snowberg direction, 587 top 1% share, 961 Sports. No sentence overstates its source |

**C-1 (minor). The new Clauset sentences have no source row behind them.** Implementation issue (source-citation skill) → `sonnet-writer` (paper key) and `researcher` (refs file).
- `main.tex:373` is the `% src:` for the subsection: `S-PAPER-2, S-PAPER-5`. Neither covers Clauset. `analysis/paper_summaries_refs.md` is not in the paper's source key (lines 5-15), and its entry 10 says "Lower bound x_min: the abstract names the problem but not the selection rule. Not checked." The paper now states that rule (381).
- The claim is true (verified above). What is missing is the row: a new `[S-PS-17]` (arXiv PDF, section 3.3) in `paper_summaries_refs.md` entry 10 and `open_questions`, and a paper key line for `paper_summaries_refs.md` (same class as the closed F14). IDs are never renumbered.

## B. `tips/polymarket_paper_review_tips.html` (unchanged since 16b6661)

| Check | Result | Evidence |
| --- | --- | --- |
| Diff since 16b6661 | none | `git diff --stat 16b6661` lists only `main.tex`, `main.pdf`, `tips/README.md`, `tips/index.html` |
| Cycle-2 numbers (292.5, D-041, five outside-lecture methods, 22 pages) | PASS | unchanged, verified in `review_gate_mvp1_r3.md` cycle 2 and its addendum |
| Still matches the paper | PASS with one minor (B-1) | 22 pages still true. "Five references added. Two are only partly verified" (144, 228) matches `paper_summaries_refs.md` (partial 2) |

**B-1 (minor). The open `\todo` list undercounts.** Implementation issue → `sonnet-writer`.
- Lines 155, 187, 235, 280 describe the open `\todo` lines as "interpretation and conclusion lines". The paper now has a fifth `\todo` in Methods Q3 (`main.tex:382`, why x_min is fixed at the top 10%). Line 109 ("at review time: 4 `\todo`") is historical and stays correct.

## A. `tips/polymarket_paper_summaries_tips.html`

### Acceptance checks

| Check | Result | Evidence |
| --- | --- | --- |
| Claims and numbers match `paper_summaries_refs.md` | PASS | Read side by side, all 11 panels. Qin: 1.20 B / 1.30 M / $61 B, 2022-11-21 to 2026-04-28, 1,019 panel markets, 49.83% / 50.51%, −0.0023 / −0.0019 / −0.0032, +0.0098, 34,902,814, 84.1%, 0.9698. Dataset: 2,786,380,324 rows, 52.7 GB, 1.2 B / 839 M / 602 M / 144 M. Snowberg: 6,403,712, 206,808 / 1,485,112, 2,725,000 / 380,000, 5,610,580, −61%, −23%, 5.5%, 4/1 to 9/1 near −18%. Le: 353 M / 429,000, 87.3% / 71.5%. DuckDB: 1024, 1981 to 1984 caveat. BH: 10 tests. Bib fields (volumes, pages, DOIs) match. No number on the page is absent from the file |
| Partial and unknown marks kept | PASS | Brier 1950 and Page 2013: `.ver.part` badge, "partial" chip in the tab bar, yellow cells in the Step 2 table, "Unknown" for data, method, limitation. `[LOW-CONFIDENCE]` kept twice in Brier (483, 493). Header verdict "9 verified, 2 partial" matches the file Summary |
| Flowchart chips vs `\cite` grep of `main.tex` | **ISSUE (A1)** | 19 of 20 citation sites placed right: Intro Qin (122); Related Work Qin, Snowberg, Wolfers, Page, Le, Gneiting, Clauset (151-181); Data Qin ×2, dataset ×2 (193-200); Methods Q1 BH, Brier (328, 336); Repro DuckDB (388); Results Q1 Snowberg (460); Results Q2 Qin (587); Limitations Qin (961). Missing: Methods Q3 `\citet{clauset2009power}` at 380 |
| Chips link to the right subtab | PASS | 16 chip `href`s all resolve to a panel id (static check). Click on the Clauset chip opens `clauset2009power` (Playwright) |
| Legend explains every colour | PASS | 6 group colours (`--c-data`, `--c-cal`, `--c-score`, `--c-stat`, `--c-dist`, `--c-tool`) plus the dashed "cites nothing" box, all in the legend (139-147). Legend sits above the figure (figures.md §2) |
| No overlap in the SVG, ko and en | PASS | Bounding-box test over all visible `<text>` nodes: 0 overlaps in both languages, 0 chip labels wider than their rect. Screenshots `r_svg_ko.png`, `r_svg_en.png` in the scratchpad, looked at: clean |
| 12 subtabs open by hash, `?lang=ko` and `?lang=en` | PASS | All 12 ids × 2 languages: the right `.panel.on`, 3 steps (overview) or 8 steps (papers), eyebrows "k단계 / N" and "Step k of N" |
| scrollWidth ≤ 1040 at 1040 px | PASS | 1040 for all 24 loads, and for the page inside `index.html#papers` (ko and en, en via `localStorage`) |
| Renders inside `tips/index.html#papers` | PASS | iframe src `polymarket_paper_summaries_tips.html?lang=ko` / `?lang=en`, panel `overview`, no console or page errors. Note: `index.html` reads the language from `localStorage` only (lines 60-61), not from `?lang=`. Pre-existing, not part of this change |
| Korean: gloss and terms appendix links resolve | PASS | 63 `data-t` keys used, 63 defined in `TERMS`, 0 unresolved, 0 unused. `#term-ks` from a paper panel keeps that panel open and the target is visible |
| English: no Korean | **ISSUE (A2)** | see below. 0 Korean inside `<span lang="en">` and SVG `lang="en"` texts; the leak is in elements outside any lang span |
| English: abbreviations spelled out | minor (A5) | bare in English prose: VPIN, CTF, NBER, AMS, DOI, TPC-H, TPC-DS, CC-BY-4.0 |
| Sentence length ≤ 15 words | minor (A6) | 13 sentences over 15 words (12 en, 1 ko) |
| No em dash, no semicolon outside URLs | PASS | 0 and 0 in lines 100-624 (CSS and JS excluded) |
| tips-page.md structure | PASS | `<title>` starts with 6344; eyebrow, h1, lede, step boxes with "Step k of N"; per-panel numbered step list at the top (JS-built `steps-nav`); 0 "Abbreviations:" lines. Lede does not use the rule's "Lessons from our own runs" form, same as the other group pages; not flagged |
| `tips/index.html` tab, `tips/README.md` row | PASS | tab `papers` between `review` and `questions`; README row present; both notes match the page's h1 |

### Findings

**A1 (major). Methods Q3 is drawn and described as "cites nothing", but the paper now cites Clauset there.** Reasoning/consistency issue. Route: `researcher` updates `analysis/paper_summaries_refs.md` (Key map row clauset2009power, "Sections that cite nothing" table, entry 10 notes, open_questions), then `sonnet-writer` updates the page.
- `main.tex:380` `This follows the power-law method of \citet{clauset2009power}.` inside `\subsection{Q3: distributions}` (372-384).
- Page 195-197: Methods Q3 box has class `none` (dashed) with "cites nothing" and no chip. Page 265: "Clauset is cited only in Related Work". Page 261: "Methods: ... Q3 distributions (L372)" under "Sections that cite nothing". Page 248 and 581-582: Clauset "Our section: Related Work" only, "Methods Q3, L377 to L379, fits the power law but cites nothing there".
- `paper_summaries_refs.md:45` and 271 say the same. The file predates the edit.
- Fix: a Clauset chip (`cx`) in the Methods Q3 box, box no longer dashed, Step 3 and the Clauset panel text updated, refs file first.

**A2 (major). English mode shows Korean in the tab group labels and the panel badges.** Implementation issue → `sonnet-writer`.
- Page 126-131: `<div class="gl"><a class="t" data-t="datasrc"></a><span lang="en">Data source</span></div>`. The `a.t` term link (filled by JS with the Korean gloss) is not inside a `<span lang="ko">`, so it stays visible in English. Same pattern in every `.badge`: lines 271, 321, 356, 395, 424, 448, 479, 504, 532, 559, 592.
- Rendered English (screenshot `r_full_en_clauset2009power.png`, and inside `index.html` in English): "데이터 출처(data source)Data source", "분포 맞춤(distribution fitting)Distribution fitting".
- The legend (140-145) and the table (239-249) wrap the same link in `<span lang="ko">` and are correct. The static check scanned only `lang` spans, which is why it did not catch this.

**A3 (minor). The headline verdict and Mismatch 1 callout describe a paper state that no longer exists.** Reasoning issue (stale source) → `researcher` (refs file entry 1, open_questions), then `sonnet-writer`.
- Page 120: "One wording in our paper disagrees with its source (main.tex line 958)". Page 312: "Our text says 'most Sports markets are Neg-Risk or Up/Down' ... A change to 'disproportionately' is open."
- `main.tex:961` already reads "fall disproportionately into". `paper_summaries_refs.md:17, 89-91, 326` still list the mismatch as open.

**A4 (minor). Line pointers at or after L380 are off by 3.** Implementation issue → `sonnet-writer` (and `researcher` for the refs file, which carries the same numbers).
- Three lines were inserted at 380-382. Page and refs file: L385, L457, L584, L617, L685, L761, L912, L958, L996. Current file: 388, 460, 587, 620, 688, 764, 915, 961, 999. Lines before 380 (L122, L151, L155, L168, L171, L174, L178, L181, L193, L196, L198, L200, L202, L221, L234, L328, L336, L343, L372) are still right.
- Section labels (`sec:methods-q3`) would not drift. Suggestion only.

**A5 (minor). Abbreviations bare in English prose** (style.md §4, "full name (abbr)"). → `sonnet-writer`.
- VPIN (287, 292; the refs file says the full name was not read, so an honest parenthetical is "full name not given in the source"), CTF Exchange (279), NBER (390), AMS (499), DOI (496), TPC-H / TPC-DS (598, 607), CC-BY-4.0 (323). Korean side glosses VPIN and TPC in the terms appendix; the English side has no appendix by rule.

**A6 (minor). 13 sentences over 15 words.** Style → `sonnet-writer`, same treatment as F6.
- en: 228 (17), 265 (18, 19), 293 (25), 294 (17), 313 (17), 329 (19), 493 (16, 16), 547 (18), 578 (16), 581 (17). ko: 293 (16 어절).

**A7 (minor). Korean figure caption has four sentences** (figures.md §3: two or fewer, second starts "왜:"). → `sonnet-writer`.
- Page 228 ko: "그림 1: ... 붙였다. 왜: ... 보인다. 절 이름: ... 다. 출처: ...". The "절 이름" sentence is extra. The English caption is two sentences plus Source and passes.

**A8 (minor). Clauset x_min note is now stale on the page and in the refs file.** → `researcher`.
- Page 572 and `paper_summaries_refs.md:266, 334`: "the abstract names the problem but not the selection rule. Not checked." This review checked it (C above). A new `[S-PS-17]` row closes it; see C-1.

## Hierarchy check

| ID | Check | Result | Evidence |
| --- | --- | --- | --- |
| H1 | Mission block, milestone trace, counters | PASS (unchanged) | `PLAN.md` mission block and M4 counters verified at the gate (`review_gate_mvp1_r3.md`). This owner-requested review is not a new gate cycle |
| H2 | Decisions logged | PASS, note | No choice between options was made since D-041. The three `main.tex` edits follow the refs file's open_questions and book.md principle 13 (`\todo` to the owner). No D-row needed |

MVP ladder (L1 to L4): not applicable. Documents only.

## Not found (checked, clean)

- Em dash in `main.tex`, the new page, the review page: 0.
- Semicolons in the new page prose: 0.
- Unresolved term links, chip hrefs, tab buttons: 0.
- Console or page errors on any of the 24 page loads or the two index loads: 0.
- Overfull, undefined: 0 and 0.
- The new page adds no number that `paper_summaries_refs.md` does not hold (footer claim at 618 holds).

## Routing summary

| Finding | Class | Route |
| --- | --- | --- |
| A1, A3, A8, C-1 (refs rows) | reasoning / stale research file | `researcher` first (`analysis/paper_summaries_refs.md`), then `sonnet-writer` (page) |
| A2, A4, A5, A6, A7, B-1, C-1 (paper key line) | implementation (HTML text, paper comment) | `sonnet-writer` |

Scratchpad evidence: `/private/tmp/claude-501/-Users-tio-Documents-mscs-utrgv-mscs-utrgv-cs6344-intro-2-ds/9c98c4d5-9242-4444-8b45-6669d55f723e/scratchpad/` (`build.log`, `static_check.py`, `render_all.py`, `render_index_en.py`, `r_svg_ko.png`, `r_svg_en.png`, `r_full_en_clauset2009power.png`, `r_index_ko.png`, `r_index_en2.png`, `dl_clauset/clauset.txt`).

---

Verdict: **ISSUE** (A1, A2). B and C PASS.
