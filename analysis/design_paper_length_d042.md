# Design: paper length restructure (D-042)

- Author: system-architect, 2026-11-08. Design only. No LaTeX, no code.
- Serves: D-042 (owner, option 3), D-038, M4 in `PLAN.md`.
- Owner constraint added 2026-11-08: "we should have core flow in our paper body" (§4).
- Target: `papers/paper_mvp1/main.tex` (1,020 lines, 22 pages, `main.log` line 790).
- Language: English, like the other `analysis/*.md` design files.

## 0. Mission block (quoted from `PLAN.md`)

> - Mission: Test whether a Polymarket price can be read as a probability, using resolved Yes/No markets with a fresh price one day before the close and at least 10 trades, and only methods from our lectures. (owner, 2026-11-01; D-019; first set 2026-10-19)
> - Vision: A reader can look at a Polymarket price and know how far to trust it: which price ranges, topics and horizons are off, by how much, and who sets the prices. (owner, 2026-10-19)
> - Constraints: `STATUS.md` "Constraints" table (lecture methods only; k-means under 1/10 of the report; sourced facts only; cluster for all data queries; criteria fixed before results; "wallet", never "person"; effect size next to every p-value).
> - M4 → S1: paper v1 (D-014, D-023); exit: reviewer gate PASS, `papers/paper_mvp1` builds clean, every measured number is a `numbers.tex` macro.

How this design traces to the block:

| Design choice | Line served |
| --- | --- |
| Q1 stays in the body, in full | Mission (is the price a probability) |
| Checks summary table in the body | Vision ("how far to trust it") |
| k-means detail to the appendix | Constraint "k-means under 1/10 of the report" |
| Numbers only via macros, clean build | M4 exit |

## 1. Target structure

### 1.1 Result in one picture

```
BODY (target ~9-10 pages)                 APPENDIX (after References)
1 Introduction  [+ fig:flow, §4]
2 Related Work
3 Data          (counts stay)  ---------> A Data details: fig:drops [+ Sports para, F6]
4 Methods       (prereg text stays) ----> B Methods details: tab:prereg [+ Reproducibility, F3]
  4.1 timeline (fig:timeline stays)
5 Results
  5.1 Q1: tab:bins, fig:calib  ---------> C Q1 further results: fig:ecdf [+ eq-freq para, F4]
  5.2 Q2: tab:conc, fig:ccdf   ---------> D Q2 further results: fig:wd-maker, fig:wd-taker, fig:lorenz
                                                             [+ role tests F2, k-means F1]
  5.3 Q3: tab:fits, fig:qq-size --------> E Q3 further figures: fig:hist, fig:qq-wallet
  5.4 Checks: summary (NEW) tab:checks -> F Robustness R1, R2 (old 5.4)  [+ Limits R1/R2 para, F5]
                                   -----> G Checks requested in review (old 5.5)
6 Discussion
7 Limitations   (refs retargeted)
8 Conclusion
References
```

- Items in `[ ]` are the further moves of §2.3. They need the owner's pick.
- Every other move is fixed by D-042.

### 1.2 Kept figure for Q2 and Q3

D-042 keeps "one main figure and one table each" but does not name the figure.

| Question | Body table | Body figure (recommended) | Why this one | Alternative |
| --- | --- | --- | --- | --- |
| Q2 | `tab:conc` | `fig:ccdf` | Cited twice (lines 512, 600). The course report uses the same plot | `fig:lorenz` |
| Q3 | `tab:fits` | `fig:qq-size` | `tab:fits` reads with the normal fit. The course report uses the same plot | `fig:hist` |

- With `fig:qq-size`, the body sentence "Prices pile up near both ends" (line 644) points to an appendix figure.
- It gets a `\Cref{fig:hist-price}` pointer. Its words do not change.

### 1.3 Block map (source line ranges in the current `main.tex`)

| Block | Lines | Now | After | Bridge left in the body |
| --- | --- | --- | --- | --- |
| Drop counts text | 205-206, 209-213 | 3.2 | body | none needed |
| `fig:drops` + its two describing lines | 207-208, 215-220 | 3.2 | A | line 207 gets "(\Cref{sec:app-data})" |
| Pre-registration text and amendment | 269-271, 301-315 | 4.1 | body | none |
| `tab:prereg` | 273-299 | 4.1 | B.1 | line 270 points to B.1 |
| Q1 methods | 317-342 | 4.2 | body | none |
| Q2 methods, main | 346-359 | 4.3 | body | none |
| Q2 role-test methods (F2) | 360-362 | 4.3 | D.2 | one pointer sentence |
| k-means methods (F1) | 365-371 | 4.3 | D.3 | line 365 stays, with `\Cref{sec:app-kmeans}` |
| Q3 methods, incl. `\todo` at 384 | 375-385 | 4.4 | body | none |
| Reproducibility (F3) | 389-400 | 4.5 | B.2 | lines 389 and 391 stay, plus a pointer |
| Q1 verdict + gaps + `tab:bins` + `fig:calib` | 404-477 | 5.1 | body | none |
| `fig:ecdf` | 479-484 | 5.1 | C | line 491 keeps `\QOneKsD`, gets the pointer |
| Score measures | 486-491 | 5.1 | body | none |
| No-min result | 492-494 | 5.1 | body | none |
| Equal-frequency detail (F4) | 495-499 | 5.1 | C | one pointer sentence |
| Q2 answer + `tab:conc` + `fig:ccdf` | 503-538 | 5.2 | body | none |
| `fig:wd-maker`, `fig:wd-taker`, `fig:lorenz` | 540-586 | 5.2 | D.1 | lines 513-514 point to D.1 |
| Pipeline check vs dataset paper (F7) | 588-593 | 5.2 | body (D.2 if F7) | none |
| Power-law tail | 595-603 | 5.2 | body | none |
| Role tests results (F2) | 605-608 | 5.2 | D.2 | one pointer sentence |
| k-means results (F1) | 610-620 | 5.2 | D.3 | pointer kept at line 365 |
| Q3 text + `tab:fits` | 624-625, 643-648, 664-688 | 5.3 | body | none |
| `fig:hist` | 627-641 | 5.3 | E | line 625 points to E |
| `fig:qq-size` | 650-655 | 5.3 | body | none |
| `fig:qq-wallet` | 657-662 | 5.3 | E | line 647 splits into a body ref and an E ref |
| Robustness framing | 692-697 | 5.4 | NEW 5.4 body | moved, not copied |
| R1 text, `fig:r1`, `tab:r1` | 699-737 | 5.4 | F.1 | `tab:checks` row R1 |
| R2 text, `fig:r2` | 739-764 | 5.4 | F.2 | `tab:checks` row R2 |
| Review framing | 768-774 | 5.5 | NEW 5.4 body | moved, not copied |
| M1 to M5, duplicates, peer a, peer b | 776-915 | 5.5 | G.1-G.7 | one `tab:checks` row each |
| Discussion | 917-942 | 6 | body | none |
| Limitations, Sports (F6) | 956-964 | 7 | body (A.2 if F6) | one pointer sentence |
| Limitations, R1/R2 paragraph (F5) | 992-999 | 7 | F intro | one pointer sentence to `tab:checks` |
| Conclusion | 1001-1012 | 8 | body | none |

### 1.4 Appendix sections and new labels

- `\appendix` goes after the bibliography group (line 1017).
- Label prefix stays `sec:` (`latex.md` §10). The old labels `sec:res-robust` and `sec:res-review` keep their names.
- New headings are structure only. Each titles one check by its ID and short name.

| Appendix | Heading level | Label | Contents |
| --- | --- | --- | --- |
| A | `\section` | `sec:app-data` | `fig:drops`. A.2 `sec:app-sports` if F6 |
| B | `\section` | `sec:app-methods` | B.1 `sec:app-prereg` (`tab:prereg`). B.2 `sec:app-repro` if F3 |
| C | `\section` | `sec:app-q1` | `fig:ecdf`. F4 paragraph if picked |
| D | `\section` | `sec:app-q2` | D.1 `sec:app-q2-dist` (3 figures). D.2 `sec:app-q2-roles` (F2). D.3 `sec:app-kmeans` (F1) |
| E | `\section` | `sec:app-q3` | `fig:hist`, `fig:qq-wallet` |
| F | `\section` | `sec:res-robust` | F.1 `sec:app-r1`, F.2 `sec:app-r2` |
| G | `\section` | `sec:res-review` | G.1-G.5 `sec:app-m1`..`sec:app-m5`, G.6 `sec:app-dup`, G.7 `sec:app-peer` with `\subsubsection` `sec:app-peer-a`, `sec:app-peer-b` |

- The duplicate check has no figure. So rows must point to sections, not figures.
- Line 886 (the shared peer intro) opens G.7.
- Figure and table counters continue into the appendix. No counter reset (minimal diff).

### 1.5 Every `\Cref` whose direction changes

Moving a label never makes it undefined. `cleveref` prints the new number by itself.
"Direction change" here means body to appendix, appendix to body, or a retarget.

| Line | Target | Before | After | Action |
| --- | --- | --- | --- | --- |
| 207 | `fig:drops` | body → body | body → A | add `(\Cref{sec:app-data})` |
| 270 | `tab:prereg` | body → body | body → B.1 | add `in \Cref{sec:app-prereg}` |
| 491 | `fig:ecdf` | body → body | body → C | add `\Cref{sec:app-q1}` |
| 513 | `fig:wd-maker,fig:wd-taker` | body → body | body → D.1 | add `\Cref{sec:app-q2-dist}` |
| 514 | `fig:lorenz` | body → body | body → D.1 | same pointer as 513 |
| 600 | `fig:ccdf` | body → body | D → body if F2 moves 595-603 | no action (595-603 stays in body) |
| 625 | `fig:hist` | body → body | body → E | add `\Cref{sec:app-q3}` |
| 644 | none now | | body → E | add `(\Cref{fig:hist-price})`, words unchanged |
| 647 | `fig:qq-size,fig:qq-wallet` | body → body | split | `fig:qq-size` body. `fig:qq-wallet` → E pointer |
| 710, 711, 748 | R1, R2 floats | body → body | F → F | none |
| 787-908 | `fig:r3-*` | body → body | G → G | none |
| 970 | `sec:res-review` | body → body | body → G | retarget to `sec:app-m4` |
| 976 | `sec:res-review` | body → body | body → G | retarget to `sec:app-m3` |
| 988 | `sec:methods-prereg` | body → body | body → body | none |
| 992 | `sec:res-robust` | body → body | F → F if F5, else body → F | if F5: sentence moves into F intro. Body gets one pointer to `tab:checks` |
| NEW | `tab:checks` rows | | body → F, G | one `\Cref` per row (§3) |
| NEW | F and G openings | | appendix → body | one back-pointer: `\Cref{sec:res-checks}` and `\Cref{tab:checks}` |
| NEW | `fig:flow` (§4) | | body → body | one pointer sentence in the Introduction |

- Abstract: no `\Cref`. Its sentences stay true after the move. No change.
- Introduction: no `\Cref` to moved items today. Only the `fig:flow` pointer is added.
- Conclusion: line 1011 ("The payout check leaves the Q1 result in place") may get `(\Cref{tab:checks})`. Owner's call; default no change.
- Wording that assumes nearness: line 696 "The sensitivity row below". It moves into body 5.4 with the framing. "below" then refers to `tab:checks`. Check it reads true; else keep the sentence in F.1 with `tab:r1`.

## 2. Page budget

### 2.1 Where the 22 pages go now (from `main.aux` start pages)

```
p1   p2   p3   p4   p5   p6   p7   p8   p9   p10  p11  p12  p13  p14  p15  p16  p17  p18  p19  p20  p21  p22
|Intro+Rel|Data|  Methods  2.8  |  Q1 2.3   |    Q2 3.0    |  Q3 2.1  | R1,R2 1.8|   Review checks 5.1    |Disc+Lim+Concl+Refs
```

| Section | Start page (aux) | Pages now (est.) | Floats inside (est. pages) |
| --- | --- | --- | --- |
| Title, abstract, 1, 2 | 1 | 1.3 | none |
| 3 Data | 2 | 1.0 | `fig:drops` 0.45 |
| 4 Methods | 3 | 2.8 | `fig:timeline` 0.2, `tab:prereg` 0.5 |
| 5.1 Q1 | 6 | 2.3 | `tab:bins` 0.4, `fig:calib` 0.65, `fig:ecdf` 0.5 |
| 5.2 Q2 | 8 | 3.0 | `tab:conc` 0.2, `fig:ccdf` 0.5, 3 subfigure pairs 1.05 |
| 5.3 Q3 | 11 | 2.1 | `fig:hist` 0.35, 2 QQ plots 0.9, `tab:fits` 0.15 |
| 5.4 Robustness | 13 | 1.8 | `fig:r1`, `tab:r1`, `fig:r2` |
| 5.5 Review checks | 15 | 5.1 | 7 figures |
| 6 Discussion | 20 | 0.7 | none |
| 7 Limitations | 21 | 0.9 | none |
| 8 Conclusion + References | 22 | 0.85 | none |

- Robustness plus review checks are about 7 pages, not 15.
- Estimates use start pages and float sizes. Error is about ±1 page in total.
- Body length means page 1 to the end of the Conclusion. References are not counted.

### 2.2 After the D-042 moves only

| Section | Pages (est.) | Change |
| --- | --- | --- |
| Title, abstract, 1, 2 | 1.3 | 0 |
| 3 Data | 0.55 | −`fig:drops` |
| 4 Methods | 2.3 | −`tab:prereg` |
| 5.1 Q1 | 1.8 | −`fig:ecdf` |
| 5.2 Q2 | 1.95 | −3 figures |
| 5.3 Q3 | 1.2 | −`fig:hist`, −`fig:qq-wallet` |
| 5.4 Checks summary (new) | 0.6 | +table, +framing moved up |
| Bridges elsewhere | 0.1 | +pointers |
| 6, 7, 8 | 1.85 | 0 |
| **Body total** | **~11.6 (±1)** | from ~21.2 |

**Result: ~9 pages is not reachable by the D-042 moves alone.** The gap is about 2.5 pages.
With the core-flow figure (§4) the body is ~11.9.

### 2.3 Further moves that close part of the gap (moves, not deletions)

Ranked by pages saved, then by low cost to the core flow.

| Rank | ID | Move | Lines | Saves (est.) | Core-flow cost | Recommend |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | F1 | k-means methods and results → D.3 | 366-371, 610-620 | 0.4 | none. Side analysis. Serves the k-means constraint | yes |
| 2 | F3 | Reproducibility detail → B.2. Keep lines 389, 391 | 390, 392-400 | 0.3 | none | yes |
| 3 | F4 | Q1 equal-frequency detail → C. Lines 492-494 (no-min result) stay: line 252 and `tab:prereg` promise it | 495-499 | 0.15 | low | yes |
| 4 | F5 | Limitations R1/R2 paragraph → F intro | 992-999 | 0.2 | low. `tab:checks` carries R1, R2 | yes |
| 5 | F2 | Q2 role tests → D.2 | 360-362, 605-608 | 0.15 | low | optional |
| 6 | F6 | Limitations Sports paragraph → A.2 | 956-964 | 0.2 | medium. It is a real limitation | optional |
| 7 | F7 | Q2 pipeline check → D.2 | 588-593 | 0.1 | medium. Discussion line 933 repeats it | no |

| Scenario | Body pages (est., ±1) |
| --- | --- |
| D-042 moves only | 11.6 |
| + `fig:flow` | 11.9 |
| + F1, F3, F4, F5 | 10.85 |
| + F2, F6 too | 10.5 |
| + F7 too | 10.4 |

- Moves alone stop near **10.4 to 10.9 pages**.
- More moves would take Q1/Q2/Q3 results, Discussion or Limitations out. That breaks the core-flow rule (§4).
- The real number comes from the build after the last move step (§7, step S11).

### 2.4 Left for the owner to decide

| ID | Lever | Saves (est.) | Why it is the owner's |
| --- | --- | --- | --- |
| O1 | Accept ~10 to 10.5 pages as "nears ~9" | 0 | D-042 says "about 9". Reading it is the owner's |
| O2 | Conference layout: 10 pt, two columns, or a named template | ~30 to 40% of body | It is neither a move nor a cut. It changes the document class |
| O3 | Text cuts. Candidates: Discussion lines 919-927 repeat Q1 numbers from 5.1. Limitations lines 966-969 repeat Data counts | ~0.5 | Text cuts are the owner's (D-042: "no text deleted") |
| O4 | Smaller widths: `fig:ccdf` at 0.75 `\linewidth` | ~0.1 | Readability (memory "Figures stay readable") |

Also for the owner:

- Which of F1 to F7 to apply.
- Whether to add `fig:flow` (§4).
- The Q3 body figure: `fig:qq-size` (recommended) or `fig:hist`.
- `product-manager` logs each pick as a `DECISIONS.md` row before the step runs.

## 3. Checks summary table slot

### 3.1 Where it sits

- New `\subsection{Checks: summary}\label{sec:res-checks}`. It is 5.4, after Q3 results.
- It replaces old 5.4 Robustness and 5.5 Review checks in the body.
- Order inside 5.4:
  1. Framing sentences, moved from lines 692-697 and 768-774. Move, not copy.
  2. One pointer sentence: `\Cref{tab:checks}` lists every check. Details are in `\Cref{sec:res-robust,sec:res-review}`.
  3. The table `tab:checks`.

### 3.2 Interface for `analysis/table_design_checks_summary.md` (data-analyst)

| Item | Fixed by this design |
| --- | --- |
| Label | `tab:checks` |
| Float | `table` with `[H]`. `\caption` below, then `\label` (`latex.md` §14) |
| Rows, in order | R1, R2, M1, M2, M3, M4, M5, duplicates, peer a, peer b (10 rows) |
| Must per row | check ID, one pointer `\Cref{sec:app-...}` (table below), at least one existing macro |
| Numbers | existing `numbers.tex` macros only. No new macro in this restructure |
| Intervals | confidence interval (CI) bounds come from the existing `...CiLow` and `...CiHigh` macros |
| Width and size | `\linewidth`, at most ~0.5 page. `tabularx` and `booktabs` are loaded |
| Caption | two sentences, second starts "Why:". Source: runs `\RobustRun` and `\RThreeRun` |
| Column design | data-analyst's. Note: R2, M4 and duplicates have no "net gap with CI" shape. A single numeric schema will not fit every row |

Row to pointer map:

| Row | Pointer label | Source block now |
| --- | --- | --- |
| R1 | `sec:app-r1` | lines 699-737 |
| R2 | `sec:app-r2` | lines 739-764 |
| M1 | `sec:app-m1` | lines 776-794 |
| M2 | `sec:app-m2` | lines 796-811 |
| M3 | `sec:app-m3` | lines 813-835 |
| M4 | `sec:app-m4` | lines 837-851 |
| M5 | `sec:app-m5` | lines 853-873 |
| duplicates | `sec:app-dup` | lines 875-883 |
| peer a | `sec:app-peer-a` | lines 885-900 |
| peer b | `sec:app-peer-b` | lines 902-915 |

- The D-040 sentence ("Yes is priced above its observed rate", line 798) moves with M2 to G.2.
- D-041 F11 put it in the review-checks section. It stays in that section, which is now Appendix G.
- In the body, the M2 row of `tab:checks` carries it. No new body sentence is written (`book.md` principle 13).

## 4. Core flow in the body (owner, 2026-11-08)

### 4.1 Rule

The body must carry the whole flow. Each step must be readable without the appendix.

| Flow step | Body home | Key numbers that stay in the body | Moved out | Bridge |
| --- | --- | --- | --- | --- |
| Question | 1 Introduction | `\HookPct`, `\PaperTrades` | nothing | none |
| Data | 3 Data | `\NMarketsInScope`, `\NMarketsKept`, five drop counts | `fig:drops` | pointer at line 207 |
| Evaluation price and pre-registration | 4.1 | `\DaysShort`, `\MaxStaleHours`, `\MinTrades`, pilot shares, amendment | `tab:prereg` | pointer at line 270. Criteria stay in 4.2 text |
| Q1/Q2/Q3 methods | 4.2-4.4 | `\NBins`, `\Alpha`, eq. `eq:chisq` | k-means detail (F1), role tests (F2) | line 365 with pointer |
| Q1/Q2/Q3 results | 5.1-5.3 | `\VerdictQOne`, `\QOneChiSq`, `\GapNetDiffMain`, `tab:bins`, `tab:conc`, `tab:fits` | 6 figures, F1, F2, F4 | pointers, with the key macro kept in the sentence |
| Checks summary | 5.4 | `tab:checks` rows | R1, R2, review checks | the table itself |
| Discussion | 6 | unchanged | nothing | none |
| Limitations | 7 | unchanged, except F5/F6 | F5, F6 | one pointer each |
| Conclusion | 8 | unchanged | nothing | none |

Bridge rule (new text is limited, `book.md` principle 13):

- A bridge is a pointer: an existing sentence plus `\Cref`, or one new sentence of the form "X is in `\Cref{...}`."
- A bridge carries at most one existing macro. No adjective, no reading, no new claim.
- Where a moved block held the step's key number, the body sentence that already has that macro stays.
- New headings name a check by ID and short name only.

### 4.2 Does the body need a core-flow figure?

`fig:timeline` shows where the price sits in time. It does not show data → filters → Q1/Q2/Q3 → checks.

| Option | What | Page cost (est.) | Serves the owner's ask |
| --- | --- | --- | --- |
| A | Keep `fig:timeline` only | 0 | No. It shows one step |
| B | Add one single-row TikZ pipeline `fig:flow`. Keep `fig:timeline` | +0.25 to 0.35 | Yes |
| C | Merge the pipeline into `fig:timeline` as a second row | +0.2 | Partly. Time axis and process axis in one figure confuse |

**Recommendation: B**, at the end of the Introduction, after line 139.

```
[Polymarket-v1        ]   [filters: Up/Down,  ]   [kept \NMarketsKept ]   [Q1 calibration ]   [checks   ]
[daily_aligned        ]-->[no outcome, no     ]-->[markets, price \pOne]-+->[Q2 wallets     ]-->[R1, R2,  ]
[\NMarketsInScope     ]   [price, stale,      ]   [at T - \DaysShort  ] +->[Q3 distributions]   [M1-M5,   ]
[markets in scope     ]   [< \MinTrades trades]   [day                ]   (\Cref sec:res-q1..q3) [dup, peer]
```

- Height about 1.2 in, width `\linewidth`. TikZ, `[H]`, caption below with "Why:".
- Counts come from existing macros only. No literal digits.
- It partly carries what `fig:drops` showed, in the body.
- One pointer sentence in the Introduction: "`\Cref{fig:flow}` shows the study flow."
- A figure is Claude's to make (`book.md` principle 13). Adding it is still the owner's pick (§2.4).

## 5. Invariants and checks

Every step in §7 must pass all of these before it closes.

| ID | Invariant | Check |
| --- | --- | --- |
| I1 | Q1 verdict sentence unchanged and in the body | line "The pre-registered rule gives this verdict: `\VerdictQOne{}`" exists once, in the 5.1 file |
| I2 | All 5 owner `\todo` slots kept | `grep -c '\\todo{owner'` over `main.tex` and section files = 5 (now lines 187, 384, 928, 942, 1012) |
| I3 | No new `\todo` | same count, still 5 |
| I4 | No text deleted, only moved | sort every source line before and after, then `comm -23`. Removed lines may differ only by an added `\Cref` |
| I5 | Numbers only via macros | new or changed lines hold no literal digit outside labels, `\Cref`, and bin labels |
| I6 | `numbers.tex` and `figures/` untouched | `git diff --stat` shows neither |
| I7 | 0 undefined references | `main.log` has no "undefined" line. No "??" in `pdftotext` output. Appendix `\citep` calls sit after `\bibliography`. Only the full `latexmk` reruns resolve them. Judge the final pass only |
| I8 | 0 Overfull boxes | `grep -c Overfull main.log` = 0 |
| I9 | Appendix floats use `[H]` | every `\begin{figure}` and `\begin{table}` in appendix files has `[H]` |
| I10 | Captions below, `\label` after `\caption` | `latex.md` §14 grep |
| I11 | Real heading levels | no `\textbf{...}` fake headings (`latex.md` §15) |
| I12 | Core flow in the body (§4.1) | each flow step has its body home and key macro. Gate after step S9 |
| I13 | Pointers updated | every row of §1.5 done. Abstract, Introduction and Conclusion checked |
| I14 | Course report unchanged and 2 pages | `git diff` on `papers/course_report_mvp1/` empty. Its build gives 2 pages (final step only) |
| I15 | Outside-lecture labels stay true | line 314 lists five methods. Each moved method keeps its own label sentence |
| I16 | `% src:` comments travel with their text | each moved block keeps its `% src:` line |

Build per step: in `papers/paper_mvp1/`, `latexmk -C`, then the command in `papers/README.md` (`latex.md` §12).
A document build is allowed locally (`~/.claude/CLAUDE.md` "Allowed locally").

## 6. Risks

| Risk | Effect | Mitigation |
| --- | --- | --- |
| Page estimate is off | Body may land at 10 to 12 pages | Measure at S11. Owner then picks O1 to O4 |
| `[H]` floats leave white space at page ends | +0.1 to 0.3 page per break | Accept. `[H]` is a rule (`latex.md` §14) |
| Figure numbers shift | 51 hard-coded "Figure N" mentions in 9 `tips/` files go stale. Review HTML pages too | Out of scope. List them for a later task |
| Bridges read as new interpretation | Breaks `book.md` principle 13 | Bridge rule §4.1. Reviewer checks each new line |
| Framing sentences moved up read wrong (line 696 "below") | Misleading text | Check at S2/S3. Keep the sentence in F.1 if it does not fit |
| `cleveref` names in the appendix | "Section" vs "Appendix" | `\appendix` makes `cleveref` say "Appendix". Confirm in the S2 build |
| Split step changes the PDF | Hidden edits mixed with the split | S1 is its own commit. Same page count, same `\newlabel` lines, empty `pdftotext` diff |
| Another agent edits `main.tex` meanwhile | Lost edits | Do not split while another agent edits or reviews it (`.claude/CLAUDE.md` "Large source files") |
| `numbers.tex` regenerated mid-work | Course report and paper values change | Not part of this work. I6 |
| D-041 F11 location of the D-040 sentence | Reader may want it in the body | It stays in the review-checks section (now G). Body carries it through the M2 row |

## 7. Ordered steps for product-manager

Each step is one atomic change. Each ends in a clean build that passes §5.
Steps S2 to S8 do not wait on the data-analyst. S9 does.

| Step | Change | Depends on | Ends with |
| --- | --- | --- | --- |
| S0 | Owner picks logged as `DECISIONS.md` rows: F1 to F7, `fig:flow`, Q3 body figure | none | D-rows exist |
| S1 | Split `main.tex` into `sections/NN-slug.tex` via `\input`. Preamble and macros stay in `main.tex`. Own commit | none | PDF same: 22 pages, same `\newlabel` lines in `main.aux`, empty `pdftotext` diff |
| S2 | Add `\appendix` after the bibliography. Move 5.5 to Appendix G with subsections G.1 to G.7. Create body 5.4 `sec:res-checks` with the framing lines 768-774 and one pointer | S1 | build clean. G labels resolve |
| S3 | Move 5.4 R1, R2 to Appendix F with F.1, F.2. Move framing lines 692-697 to body 5.4 | S2 | build clean |
| S4 | Q1: `fig:ecdf` to C. F4 if picked. Pointer at line 491 | S1, S0 | build clean |
| S5 | Q2: three figures to D.1. F1 to D.3 and F2 to D.2 if picked. Pointers at 365, 513, 514 | S1, S0 | build clean |
| S6 | Q3: `fig:hist` and `fig:qq-wallet` to E. Pointers at 625, 644, 647 | S1, S0 | build clean |
| S7 | `tab:prereg` to B.1, `fig:drops` to A. F3 to B.2 if picked. Pointers at 207, 270 | S1, S0 | build clean |
| S8 | Limitations: retarget 970 to `sec:app-m4`, 976 to `sec:app-m3`. F5, F6 if picked | S2, S3 | build clean |
| S9 | Insert `tab:checks` in body 5.4, from `analysis/table_design_checks_summary.md` | S2, S3, analyst design | build clean. Gate for I12 core flow |
| S10 | Add `fig:flow` and its Introduction pointer, if picked | S0, S9 | build clean |
| S11 | Final: measure body pages (page where References starts). Build the course report once (2 pages). Run all §5 checks | S1 to S10 | page number reported to owner. Owner picks O1 to O4 if above ~9.5 |

S1 notes:

- The rule does not require the split. `main.tex` has 1,020 lines, below the 1,500 soft line.
- `latex.md` §13 forbids restructuring without an explicit request. This split is the main session's explicit request.
- Why it helps: every later step is a block move. Each block and its `% src:` line then move as one file cut.
- `\input` keeps the working directory. `figures/...` and `\input{numbers}` paths stay valid.
- Follow-up in S1: `papers/README.md` "Each folder holds" gets a `sections/` line.

- S4 to S7 touch different section files. They may run in any order after S1.
- Still one task at a time (`rules/core.md` Agent discipline).
- Reviewer gate after S11 (`.claude/CLAUDE.md` Workflow step 4). It is not a pm task row.
- Agents never commit. The main session commits after each step.
