# Lecture method audit: MVP1 (D-025)

- Status: done, report only. Open: slide image checks and three owner questions (§4).
- Result: 52 methods. 35 in lecture, 7 partly, 10 not found. No not-found method feeds the Q1 verdict sentence.
- Date: 2026-11-01.
- Why: owner, 2026-11-01: "all analysis should be done in our lecture contents" (`DECISIONS.md` D-025).
- Scope: MVP1 only (Q1, Q2, Q3) and the robustness checks R1 and R2 in `papers/paper_mvp1/main.tex`.

## How to read this file

| Item | Rule |
| --- | --- |
| Evidence source | Slide text in `scratchpad/lecture_text/`. Deck key: `D6` = `6_DataDistribution.txt` |
| Slide id | `s23` = `slide23.xml`. It is the file id, and it may differ from the shown slide number |
| Limit | Text in images is not extracted. "Not found" means not found in slide text and notes |
| Book and homework | `book_intro_2_ds/` is not a deck. It appears in the note column only, tagged "book" |
| Fact | The evidence and where-used columns. Numbers come from the named saved file |
| Judgment | The class and role columns. Sections marked "Judgment" |

### Class rule (applied to every row)

| Class | Rule |
| --- | --- |
| in lecture | Deck text shows the method by name, or by a procedure that gives the same result |
| partly | Deck text names the method or its parent, but not the variant or formula used |
| not found | Neither. A general word such as "effect size" does not count |

- A named effect size counts as not found unless a deck names it. This applies to w, d, d_z, V and eta squared alike.
- Verdict input means the value reaches a branch of `code/verdicts.py` `q1()` (lines 31 to 36), directly or through a chain.
- Left out as data rules, not analysis methods: T rule, staleness limit, minimum trades, tie rule, payout classes, seeds, hash sample.

## 1. Method table

| # | Method | Where used | Role | Lecture evidence | Class | Note |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Bernoulli and binomial model (베르누이, 이항 모형) | `q1_calibration.py`, Q1 | verdict input | D6 s23, s26 to s29 | in lecture | Prices vary inside a bin, so binomial is approximate (`docs/lecture_concept_map.md` §2.1) |
| 2 | Equal-width bins (등간격 구간) | `q1_calibration.py:41`, Q1 | verdict input | D7 s13, s14 | in lecture | Also D5 s12 |
| 3 | Equal-frequency bins (등빈도 구간) | `q1_calibration.py:48`, run `142140_q1eqfreq_v5`, Q1 | pipeline check | D7 s13 to s15 | in lecture | |
| 4 | Exact two-sided binomial test per bin (이항 검정) | `q1_calibration.py:35`, Q1 | verdict input | D6 s26 to s28, D10 s8 to s12, D9 s11 to s13 | in lecture | The name is absent. D10 s10 gives the same p rule: observed + equally rare + rarer |
| 5 | Benjamini-Hochberg (BH, 거짓 발견율 보정) | `q1_calibration.py:44`, Q1 | verdict input | D13 s18, s19 | in lecture | Second branch only. It was not reached |
| 6 | Bonferroni correction (본페로니 보정) | `q1_calibration.py:43`, Q1 | secondary | D13 s15, s16 | in lecture | In `verdicts.json` `extra`, not in a branch |
| 7 | Chi-square goodness of fit, E = n × mean price, df = bins (카이제곱 적합도) | `q1_calibration.py:55-59`, `prereg_mvp1.md:22`, Q1, R1 | verdict input | D12 s3 (observed against expected). D12 s4 to s9 show independence only, with s7 df = (r-1)(c-1) | partly | The deciding test of the verdict. Concept map §2.5 already calls this form outside. Plan row 105 says only L12 |
| 8 | Cohen's w (코언의 w, 효과 크기) | `q1_calibration.py:80`, abstract `main.tex:94`, Q1, R1 | main result | not found. D10 s7 has the word "effect size" only | not found | In `verdicts.json` `effect_size`, not in a branch |
| 9 | Observed rate minus mean price (관측률과 가격의 차이) | `q1_bins.csv` `diff_obs_minus_price`, Q1 | main result | D12 s3, D10 s7 | in lecture | The effect size in `prereg_mvp1.md:25` |
| 10 | Wilson interval (윌슨 구간) | `q1_calibration.py:23-25`, `r1_split_payout.py:130`, `main.tex:288`, `:524`, Q1, R1 | main result | not found. D5 s23 to s26 give other methods: z interval and bootstrap | not found | Plan row 104 says "normal approximation or bootstrap". The code differs from the plan |
| 11 | Calibration chart: observed rate against mean price, with bars (보정 그림) | `fig4_calibration.png`, Q1 | main result | D5 s15, s16 (error bar by binning). Word "calibration" not found | partly | Deck bars are SD. The diagonal line is not in a deck |
| 12 | Brier score (브라이어 점수) | `q1_calibration.py:76`, `r2_price_path.py:97-98`, Q1, R1, R2 | secondary | not found. D20 s26 sums squared residuals, the same arithmetic without the division by n | not found | Plan row 107 marks it outside. Correct. It is the base of the R2 paired test |
| 13 | Log loss (로그 손실) | `q1_calibration.py:77`, `main.tex:298`, Q1 | secondary | D15 s10 to s14 (surprise and its average). Name not found | partly | Natural log in code. D15 uses bits. Plan row 107 is correct |
| 14 | Mean binary entropy H(p) (평균 엔트로피) | `q1_calibration.py:78`, Q1 | side | D15 s14 to s17 | in lecture | Mean over markets is our use |
| 15 | Confusion matrix, accuracy, precision, recall at 0.5 (혼동 행렬, 정밀도, 재현율) | `q1_calibration.py:61-63`, `:81-84`, Q1 | side | D16 s31, D21 s20, s21 (threshold 0.5) | in lecture | |
| 16 | Class balance, Yes rate (클래스 균형) | `q1_calibration.py:75`, Q1 | side | D16 s24 to s26, D6 s24 | in lecture | |
| 17 | Two-sample Kolmogorov-Smirnov test (KS, 두 표본 분포 비교) | `q1_calibration.py:64`, `q2_concentration.py:56`, Q1, Q2 | secondary | D11 s13, s21 to s23 | in lecture | |
| 18 | Empirical CDF plots (ECDF, 경험적 누적 분포) | `fig5_ecdf_yes_no.png`, `ecdf.png`, `fig_r2_price_path.png`, Q1, Q3, R2 | secondary | D11 s13, s15, s17, s22, D7 s4, D4 s9 | in lecture | Word miss only. Text says "observed cumulative distribution". Plan row 89 cites L4, L5. D11 is the better source |
| 19 | Longshot check: gap in the two cheapest bins (롱샷 점검) | `q1_calibration.py:65-73`, Q1 | secondary | D9 s11, D10 s8 to s12, D12 s3 | in lecture | Its interval is the Wilson interval (row 10) |
| 20 | Mean, median and their ratio (평균, 중앙값) | `q2_concentration.py:43-44`, Q2 | main result | D4 s13, s16, s18 | in lecture | |
| 21 | Top 1, 5, 10, 20% volume share (상위 지갑 몫) | `q2_concentration.py:34-36`, Q2 | main result | D5 s3, D6 s19 (80/20 rule) | in lecture | |
| 22 | Complementary CDF on log-log axes (CCDF, 여누적 분포) | `fig6_ccdf.png`, Q2 | secondary | D6 s21 | in lecture | |
| 23 | Lorenz curve (로렌츠 곡선) | `q2_concentration.py:150-162`, `fig7_lorenz.png`, `main.tex:124`, `:419`, Q2 | main result | not found | not found | Plan row 123 marks it outside. Correct. Plan row 116 calls it main, row 123 calls it a pipeline check |
| 24 | Gini coefficient (지니 계수) | `q2_concentration.py:28-31`, abstract `main.tex:97`, `tab:conc`, Q2 | main result | not found | not found | Same conflict as row 23. In the abstract, so it acts as a main result |
| 25 | Welch two-sample t-test (웰치 t검정) | `q2_concentration.py:54`, `main.tex:310`, `:451`, Q2 | secondary | D11 s2 ("Student's"), s3, s6 to s8, D10 s24, s25. Formulas are images | partly | Word "Welch" not found. Book `lec11:324` writes the deck statistic with unpooled variances. Then only df differs. Check the image. Plan row 124 says "t-test" |
| 26 | Cohen's d (코언의 d) | `q2_concentration.py:55`, `:57`, `main.tex:452`, Q2 | secondary | not found | not found | |
| 27 | Spearman correlation and its p-value (스피어만 상관) | `q2_concentration.py:187`, Q2 | secondary | D14 s32 to s35 | in lecture | Plan marks it "forced" |
| 28 | k-means (k-평균 군집) | `q2_concentration.py:110-113`, Q2 | side | D17 s24 to s33, s44 | in lecture | Plan: under 1/10 of the report |
| 29 | Elbow plot of inertia (엘보 그림, 관성) | `q2_concentration.py:110`, `fig8_elbow.png`, Q2 | side | D17 s39, s40 | in lecture | |
| 30 | Fixed elbow rule: farthest point from the chord (엘보 고정 규칙) | `q2_concentration.py:62-68`, Q2 | side | D17 s39 says to choose by eye. The rule is not found | partly | Our determinism device |
| 31 | z-score (표준 점수) | `q2_concentration.py:83`, Q2 | side | D7 s17, D14 s8 | in lecture | Search miss. The text has spaces: "z   -score" |
| 32 | Robust scaling, median and IQR (강건 스케일링) | `q2_concentration.py:77-83`, Q2 | pipeline check | D7 s21 | in lecture | |
| 33 | Log transform: log10, log1p, log (로그 변환) | `q2_concentration.py:52`, `:108`, `q3_describe.py:81`, Q2, Q3 | side | D7 s22 | in lecture | log1p is a small variant for zero safety |
| 34 | Chi-square test of independence (카이제곱 독립성) | `q2_concentration.py:121`, Q2 | side | D12 s2 to s9 | in lecture | Plan marks it "forced". `main.tex:460` prints only V, not this test |
| 35 | Cramér's V (크라메르 V) | `q2_concentration.py:122`, `main.tex:460`, Q2 | side | not found | not found | |
| 36 | One-way ANOVA (일원 분산 분석) | `q2_concentration.py:89`, Q2 | side | D11 s10 to s12 | in lecture | Plan marks it "forced" |
| 37 | Eta squared (에타 제곱) | `q2_concentration.py:90`, `main.tex:461`, Q2 | side | not found. D11 s11 has SSB and SSW, not the ratio | not found | Same number as SSB / (SSB + SSW) |
| 38 | Permutation test (순열 검정) | `q2_concentration.py:91-99`, Q2 | side | D13 s20 to s32 | in lecture | D13 s31 starts at 1000 permutations. Code uses 1000 |
| 39 | Adjusted Rand index (ARI, 군집 일치 지수) | `q2_concentration.py:131`, `main.tex:318`, `:459`, `:635`, Q2 | pipeline check | not found. D17 s22 has a stability check with a different procedure | not found | The concept is in D17. The measure is not |
| 40 | Summary statistics: mean, median, mode, range, variance, quantiles (요약 통계) | `q3_describe.py:20-28`, R2 shares of abs delta, Q3 | main result | D4 s15 to s21, D5 s3 to s8 | in lecture | Mode is the fullest of 50 bins, for continuous data |
| 41 | Histogram (히스토그램) | `q3_describe.py:51-60`, Q3 | main result | D5 s12 | in lecture | |
| 42 | Violin plot (바이올린 그림) | `q3_describe.py:91-106`, Q3 | secondary | D5 s17, s18 | in lecture | |
| 43 | Box plot (상자 그림) | `q3_box_p1d.py`, Q3 | secondary | D5 s20, s21 | in lecture | |
| 44 | Normal and exponential fit, from mean and SD (정규, 지수 적합) | `q3_describe.py:36-38`, Q3 | secondary | D7 s2, D6 s10, s15, s16 | in lecture | D6 s16: mean = 1 / lambda |
| 45 | Power-law exponent by maximum likelihood, xmin = 90% quantile (멱법칙 지수, 최대우도) | `q3_describe.py:39-41`, Q3 | secondary | D6 s19 to s22 (alpha, xmin, Clauset notes), D7 s2 (identify parameters). Formula not in text | partly | D-025 settled this: descriptive reference, no new run. Book `lec07:54` says D7 s2 shows the estimators. Check the image. The xmin choice is ours |
| 46 | One-sample KS against a fitted distribution (적합 분포 KS) | `q3_describe.py:37-42`, Q3 | secondary | D11 s13, s15 to s19 | in lecture | p-values are optimistic and the paper says so |
| 47 | QQ plot before and after log (QQ 그림) | `q3_describe.py:76-88`, Q3 | secondary | D7 s5, s6 | in lecture | |
| 48 | Drop rows with no outcome, no imputation (결측 행 제거) | `build_tables.py:41-44`, all | pipeline check | D7 s25, D2 s10 | in lecture | |
| 49 | Data matrix and variable types (데이터 행렬, 변수 유형) | `build_tables.py`, all | pipeline check | D3 s2, s3, s6 | in lecture | |
| 50 | One-sample t-test on paired differences (대응 차이 t검정) | `r2_price_path.py:43-56`, R2 | secondary | D11 s3 to s5 | in lecture | |
| 51 | t interval for the mean difference (t 구간) | `r2_price_path.py:50`, `prereg_robustness.md:89`, R2 | secondary | D5 s24 (z interval), D10 s19, s20, D11 s9 (t table) | partly | n is near 48,000, so t and z nearly match |
| 52 | Cohen's d_z (대응 효과 크기) | `r2_price_path.py:55`, `main.tex:577`, `:580`, R2 | secondary | not found | not found | Mean difference with interval is already printed |

### Counts

| Class | Rows | Row numbers |
| --- | --- | --- |
| in lecture | 35 | all others |
| partly | 7 | 7, 11, 13, 25, 30, 45, 51 |
| not found | 10 | 8, 10, 12, 23, 24, 26, 35, 37, 39, 52 |

### What this audit corrects

Keyword search (fact):

- z-score is in lecture: D7 s17. The search missed it because of spaces.
- ECDF is in lecture as a method. Only the word is absent.
- Welch, maximum likelihood and calibration: the word is absent, the parent method is present. They are partly.
- Brier, Lorenz, Gini, Wilson, Cohen, Cramér and Rand: the slide text search agrees. A wider search of `book_intro_2_ds/chapters/` (not the homework chapters) also has no hit.

Plan table (`tips/group_01/polymarket_plan_detailed.md`, row number = file line):

| Plan row | Plan says | Audit finds |
| --- | --- | --- |
| 104 | CI: normal approximation or bootstrap, L5, L10 | The plan is in lecture. The code uses Wilson, which is not |
| 105 | Chi-square goodness of fit, L12 | Partly. L12 text shows independence only |
| 107 | Brier, log loss, entropy: L15 + outside | Correct |
| 89 | ECDF, L4, L5 | L4 has CDF. L5 has none. L11 is the source |
| 90 | Fits, L6 | Add L7. The power-law estimator is partly |
| 55 | Minimum-activity filter, L7 | L7 has dropping of missing values, not an activity filter. It is a data rule |
| 116, 123 | Lorenz and Gini: main answer, and also a pipeline check | The roles conflict. The paper abstract uses Gini as a main result |
| 124 | t-test, L11 | The code and paper use Welch: partly |
| 135 | Every test has an effect size: difference, D, rho | The code adds w, d, d_z, V and eta squared. No plan row lists them, or ARI and Wilson |

## 2. Outside methods and the Q1 verdict

**Result: no not-found method feeds the Q1 verdict sentence. One partly method decides it: chi-square goodness of fit.**

The rule, from `analysis/prereg_mvp1.md`:

> | Primary metric | chi-square goodness of fit over the 10 bins (observed Yes vs. n × mean price) |
> | Line | p < 0.05 means the prices are not calibrated as a whole |
> | Per-bin call | binomial test per bin, BH-corrected at 0.05. A bin is off when its corrected p < 0.05 |
> | Effect size | observed rate − mean price per bin, with a 95% Wilson CI. Brier score next to it |
> | Failure condition | no bin off after BH, and chi-square p ≥ 0.05: "no evidence of miscalibration at this n" |

```
q1_results.json
   chi2_gof.p ---------> p < 0.05 ? --yes--> "Prices are not calibrated as a whole at this n."
   bins_reject_bh -----> elif == 0 ?  (not reached, because p = 1.08e-10)
   effect_w, brier ----> stored in verdicts.json. No branch reads them
Wilson interval -------> not in verdicts.json
```

Saved values, `runs/142082_mvp1_full_v1r3/verdicts.json`: chi-square 67.99, df 10, p 1.08e-10, Cohen's w 0.0377, n 47,948, BH bins off 5, Bonferroni bins off 4, Brier 0.1071. Sentence: "Prices are not calibrated as a whole at this n."

| Method | Class | Link to the sentence | Remove it: does the sentence change? |
| --- | --- | --- | --- |
| Chi-square goodness of fit | partly | Direct. First branch of `verdicts.py:31` | The rule cannot run. The prereg primary metric is gone. No sentence can be issued from the committed rule |
| Binomial test with BH | in lecture | Direct. Branches at `verdicts.py:33` | Listed for contrast. It was not reached |
| Cohen's w | not found | None. Stored as `effect_size` | No |
| Brier score | not found | None. Stored as `extra.brier` | No |
| Wilson interval | not found | None. Not in `verdicts.json` | No |
| Log loss | partly | None | No |
| Calibration chart | partly | None. It is a display | No |

Indirect paths (fact):

- R1 reuses the same rule through `verdicts.q1`. So R1 inherits the row above.
- R1 chooses its mapping from the agreement point value (`r1_split_payout.py:125`). The Wilson interval does not reach that choice.
- `r1_results.json`: `rule_results_same` is true.
- Lorenz, Gini, d, V, eta squared, ARI and d_z are in Q2 or R2. They have no path to Q1.

Judgment on the chi-square row:

- The degrees of freedom do not change the sentence. The deck rule gives df 9. The code uses df 10.
- Hand check, not for citation: the 5% critical values are 16.92 (df 9) and 18.31 (df 10). The statistic is 67.99.
- A 10 × 2 independence test is not a replacement. It tests "all bins share one rate", a different null.
- Removing Wilson and Brier does not change the sentence. But it departs from `prereg_mvp1.md:25`, which stays as committed. The report must state that departure, with a `DECISIONS.md` row.

## 3. Options for each method not in lecture (Judgment)

The final pick is the owner's. Option (b) needs the owner to allow an outside method.

Rules for every option:

- Prereg files stay as committed (`rules/measurement.md` §1). `runs/` folders and code snapshots stay as they are.
- A new number comes from a new script on saved outputs. It runs under `~/.claude/CLAUDE.md` "Allowed locally". The main session runs it.
- `wallets.parquet` is a saved run output, but "Allowed locally" lists CSV and JSON by name. The main session decides for rows marked "parquet".
- `make_report.py` regenerates `reports/report_v1.html`. `make_paper_numbers.py` regenerates `papers/paper_mvp1/numbers.tex`.
- Option (b) always has the fewest edits, because it only adds a label. But it leaves an outside method in place.
- So "Simplest" in §3.1 means the fewest edits among options that leave no outside method.
- "Simplest" in §3.3 means the fewest edits overall, because these methods already have a lecture parent.

### 3.1 Not found (10 rows)

| Method | (a) Lecture replacement and saved file | Cluster job for (a) | (b) Keep, labeled | Simplest |
| --- | --- | --- | --- | --- |
| Wilson interval | z interval, D5 s24, with Bernoulli SD, D6 s25. `q1_bins.csv` (`n`, `n_yes`), `r1_results.json` (`mapping`). Or bootstrap, D5 s25, s26 | No | Outside the lectures, named in prereg | (a) z interval |
| Cohen's w | Per-bin gap, already the prereg effect size. `q1_bins.csv` `diff_obs_minus_price` | No, already saved | Outside, with the gap beside it | (a) |
| Brier score | Rename only: mean squared residual of price, D20 s26. Same number, `q1_results.json` `brier` | No, already saved | Outside, named in prereg. Plan already says so | (a) rename, if a rename satisfies D-025 (§4 question 1). Removal breaks R2 |
| Lorenz curve | CCDF, D6 s21. `fig6_ccdf.png` | No, already saved | Pipeline check, outside | (c) with CCDF. See the rule conflict below |
| Gini | Top-k shares, D5 s3, D6 s19. `q2_concentration.csv` | No, already saved | Pipeline check only. Move out of the abstract | (c) with top shares |
| Cohen's d | Mean difference of log10 volume. `q2_results.json` `mean_log10_maker`, `mean_log10_taker` | No, already saved | Outside | (a) |
| Cramér's V | Normalized mutual information, D15 s25. Join `q2_kmeans_sample.csv` with `wallets.parquet` | No, if the parquet read is allowed. Else yes | Side analysis, outside | (c), and print the chi-square from `q2_results.json` instead |
| Eta squared | Print as SSB / (SSB + SSW), D11 s11. Same number, `q2_results.json` | No, already saved | Outside | (a) rename |
| Adjusted Rand index | Normalized mutual information, D15 s25, on `cluster_z` and `cluster_robust`. `q2_kmeans_sample.csv` | No. D17 s22 partition procedure would need a new fit: yes | Pipeline check, outside | (a) with the CSV, or (c) |
| Cohen's d_z | Mean difference with interval. `r2_results.json`, already printed | No, already saved | Outside | (c) |

Hand check for the Wilson row, not for citation, from `q1_bins.csv`:

- Over all 10 bins, the z and Wilson interval ends differ by about 0.0006 at most.
- Both leave the mean price outside in the same 5 bins: 0, 1, 6, 7, 8.
- Those are also the 5 bins off after BH in `q1_bins.csv`.
- A saved script must produce these numbers before any document uses them.

Replacement for the Gini pipeline check (fact):

- Dataset paper: top 1% of makers hold 84.1% (`main.tex:66`).
- Ours: 86.1% (`q2_results.json` `concentration.maker.top1_share`).
- So the check can use a lecture quantity. Populations differ, as `main.tex:449` says.

### 3.2 What option (c) removal touches

Every removal also needs a `DECISIONS.md` row. Line numbers come from the current files.

| Method | `papers/paper_mvp1/main.tex` lines | `numbers.tex` macros and `make_paper_numbers.py` | `make_report.py` lines | `README.md` lines | Other |
| --- | --- | --- | --- | --- | --- |
| Wilson | 262, 288, 400, 524, CI column of `tab:bins` | `RobROneAgreementLow`, `RobROneAgreementHigh`, bin CI macros | 345, 397 | 399 | `fig4_calibration.png` redraw, `references.bib` `wilson1927probable`, `prereg_robustness.md:56` stays |
| Cohen's w | 94, 293, 296, 349, 411, 530, 546 to 550, 587 | `QOneW`, `QOneNoMinW`, `RobROneSensW`, `RobROneDeltaW` | 394, 409 | 50, 57, 62, 395, 399 | `references.bib` `cohen1988statistical` if d and d_z go too. `prereg_robustness.md:59-60` stays |
| Brier | 120, 150, 262, 297, 405, 411, 546 to 550, 574 to 577 | `QOneBrier`, `QOneNoMinBrier`, `RobROneSensBrier`, `RobRTwo*Brier*` | 380, 394, 410, 588 | 50, 60, 392, 399 | Removes the base of the R2 paired test (`prereg_robustness.md:77`, `:88-90`). `references.bib` `brier1950verification` |
| Lorenz | 124, 308, 419, 438 to 443 | none | 82, 455 | none | `fig7_lorenz.png` out of the report and paper |
| Gini | 67, 68, 97, 124, 308, 309, 418, 429 to 433, 446 to 449, 593 | `MakerGini`, `TakerGini` (`make_paper_numbers.py:385`) | 237, 429 to 431, 449 to 451, 464, 604 | 64, 70 | Plan rows 116, 123 |
| Cohen's d | 452 | `RoleCohenD` (`:394`) | 434 | none | |
| Cramér's V | 460 | `KmeansCategoryV` (`:408`) | 442 | none | `references.bib` `cramer1946mathematical`. Add the chi-square result to line 460 |
| Eta squared | 461 | `KmeansPriceEtaSq` (`:400`) | 446 | none | |
| ARI | 317, 318, 459, 635 | `KmeansAri` (`:404`) | 422 | none | `references.bib` `hubert1985comparing` |
| Cohen's d_z | 577, 580 | `RobRTwoAllDz`, `RobRTwoTradedDz` (`:526`) | none found by this grep | none | `prereg_robustness.md:89`, `:94` stay |

Costs of removal:

- Plan row 135 (closed box) and `main.tex:134` promise an effect size next to every p-value. Removing w, d, V, eta squared or d_z without option (a) reopens that box.
- `main.tex:79` and `README.md:3` say "Team Brier". That is a team name, not a method. It can stay.

### 3.3 Partly (7 rows)

| Method | (a) Closer to the lecture | (b) Keep, labeled | (c) Remove touches | Simplest |
| --- | --- | --- | --- | --- |
| Chi-square goodness of fit | No like-for-like lecture test. The independence form has a different null | Keep. Label "goodness-of-fit form of L12". Fix plan row 105 | Breaks the prereg rule. Do not take it without an owner decision | (b). It is the only option that keeps the committed verdict |
| Calibration chart | Call it an error bar chart by bin, D5 s15 | Keep | Main Q1 figure. Do not remove | Rename |
| Log loss | Print average surprise in bits, D15 s14. From `q1_results.json` `log_loss` | Keep, plan already says L15 + outside | `main.tex:298`, `:405`, `QOneLogLoss`, `make_report.py:380`, `:394`, `:588` | (a), or (c). The prereg does not name it |
| Welch t-test | Student t from `wallets.parquet` (parquet). No cluster job if allowed | Name it "two-sample t, unequal variances" after the slide image check | `main.tex:310`, `:451`, `:452`, `RoleWelchT`, `RoleWelchP`, `make_report.py:434`, `:606` | (b). Saved p is 0.0 and t is 117.1, so the reading stays |
| Fixed elbow rule | Read the elbow by eye from `fig8_elbow.png` and `q2_results.json` `inertia` | Keep, labeled as our tie-breaker | `main.tex:316` wording only | (b) |
| Power-law exponent | D-025 already decided: descriptive reference, no new run | Already decided | Not needed | Keep as D-025 says. No new question |
| t interval | z interval from the saved mean and SD of the differences. n near 48,000 | Keep, labeled | `main.tex:577`, `:580` | (b) |

## 4. Questions for the owner

Only these need the owner. The rest follows from the option picked.

1. Does a rename satisfy D-025 when the number is the same (Brier as mean squared residual, eta squared as SSB ratio)?
2. May the verdict's chi-square goodness-of-fit form stay, labeled? No replacement keeps the committed rule.
3. If Lorenz goes, `.claude/rules/visualization.md` §7 asks for a Lorenz panel when a report shows "top x% holds y%". Which rule wins for this project? `.claude/rules/core.md` sends such a conflict to the owner.

Slide images to open, because the text cannot settle them:

| Slide | What it settles |
| --- | --- |
| D11 s3, s6 | Whether the two-sample t uses unpooled variances, and its df |
| D7 s2 | Whether the power-law estimator is on the slide |
| D6 s20 | Whether the exponent formula is on the slide |
| D12 s5 to s9 | Whether a goodness-of-fit form appears |
| D5 s24 | The exact form of the z interval |

## 5. Side notes (fact, outside this audit)

- `verdicts.json` has `criteria_sha256_12: null` for Q1. The criteria file hash was not recorded in that run.
- `code/r2_price_path.py:18` imports `q1a_category`. That file is not in `code/`. It is in `future_work/code/`.
