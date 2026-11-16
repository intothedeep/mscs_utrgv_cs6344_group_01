# Lecture and homework method audit: MVP1 paper (D-050)

**Result: 44 methods in the current paper. 30 in lecture, 12 partly, 2 outside. 20 link to a homework: 18 computed directly, 2 by the parent method. The paper itself labels 4 methods outside (D-047). This audit classes 3 of those 4 as partly.**

Abbreviations: confidence interval (CI), standard deviation (SD), mean squared error (MSE), cumulative distribution function (CDF), empirical CDF (ECDF), complementary CDF (CCDF), Kolmogorov-Smirnov (KS), Benjamini-Hochberg (BH), sum of squares between and within groups (SSB, SSW), receiver operating characteristic (ROC), area under the curve (AUC), precision-recall (PR), k-nearest neighbors (KNN), principal component analysis (PCA), linear discriminant analysis (LDA), volume-weighted average price (VWAP).

- Date: 2026-11-16.
- Why: D-050 asks for a re-audit. D-025 says all analysis stays in the lecture contents.
- Scope: the current MVP1 paper, `papers/paper_mvp1/sections/` (03, 04, 06 to 09, app-b to app-g).
- This file replaces the counts of `analysis/lecture_method_audit.md` (2026-11-01, "52: 35 / 7 / 10"). That audit predates D-026, D-028 and D-047.
- Report only. No paper, README or tips edit. No code run.

## How to read this file

| Item | Rule |
| --- | --- |
| Deck key | `D6` = `6_DataDistribution.txt` in the extracted lecture text. There is no deck 8 file |
| Slide id | `s23` = the `=== s23` file id in the extracted text. It may differ from the shown slide number |
| Evidence | Every slide id below was seen in the extracted text in this session. Text in images is not extracted |
| in lecture | Deck text names the method, or a procedure that gives the same number |
| partly | Deck text names the parent method, not the variant, formula or resampling unit used |
| outside | No deck text names the method or its parent |
| Homework | "computed" means a homework file computes or plots it. A homework that only lists a method in a table does not count |
| Role | verdict input = reaches the Q1 rule branch. check = a robustness or review check (R1, R2, M1 to M5, peer). descriptive = all else |

Row rule (fixed before counting):

- One row per statistical method, plot type, score or model.
- Not counted (data rules): the T rule, staleness limit, minimum trades, Up/Down drop, missing-outcome drop, duplicate-row removal, payout classes.
- Not counted (price definitions in M1): volume-weighted mean price (VWAP), trade-based midpoint, half spread. Note: the words "weighted mean" are not in any deck text.
- Re-runs of the same test on a subset (R1, M2, M4, duplicate rows, peer b) count under the test they reuse.
- Volume terciles (peer a) count under equal-frequency bins.
- The Wald interval is its own row. The bootstrap band in M5 counts under the cluster bootstrap row.

## A. Methods in the current paper

| # | Method | Paper place (section/appendix, Q) | Lecture deck + slide id seen in text | Homework that practiced it | Class | Role | Note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Bernoulli and binomial model of outcome 1 | 4.2, Q1 | D6 s23 (Bernoulli), s26 (binomial), s29 (SD of binomial) | none | in lecture | verdict input | Prices vary inside a bin, so binomial is approximate |
| 2 | Equal-width price bins (10) | 4.2, 5.1, Q1 | D7 s13, s14 | none | in lecture | verdict input | |
| 3 | Equal-frequency bins, and volume terciles | 4.2, App C (Q1), App G peer a | D7 s13 to s15 | none | in lecture | check | |
| 4 | Exact binomial test per bin | 4.2, 5.1, Q1 | D10 s8 to s13 (coin example, "equally rare", "rarer") | none | in lecture | verdict input | The name "binomial test" is absent. The p rule is the same |
| 5 | Bonferroni correction | 4.2, 5.1, Q1 | D13 s16 | none. `hw05_clustering/report/hw5_taeklim_report.tex:1124` lists it, not computed | in lecture | descriptive | |
| 6 | Benjamini-Hochberg (BH) correction | 4.2, 5.1, Q1, App G (M2, peer a, peer b) | D13 s16, s18, s19 | none. Same hw05 line lists it only | in lecture | verdict input | Second branch of the Q1 rule |
| 7 | Chi-square goodness of fit, expected counts from prices | 4.2 eq. (1), 5.1, Q1, App F R1, App G (M2, M3, dup, peer b) | D12 s3 (observed against expected), s4 (expected counts). s5 to s9 show the independence form only. s7 gives df = (r-1)(c-1) | none. hw04 and hw05 practiced the independence form only (row 35) | partly | verdict input | Decides the Q1 verdict. D-026 keeps it, labeled as a form of the deck test |
| 8 | Per-bin gap (observed rate minus mean price), net gap, chi-square share per bin, longshot reading | 4.2, 5.1, Q1, App G | D12 s3 (observed against expected) | none | in lecture | descriptive | The effect size. The longshot check reads rows 4 and 8 in the two cheapest bins |
| 9 | 95% z interval with Bernoulli SD | 4.2, 5.1, App C, App G M2, Q1 | D5 s24 (Z value, 1.96, s, n), D6 s25 (Bernoulli SD) | none | partly | descriptive | D5 s24 is titled "Box Plots with Notch". Its formula is an image. Open check E1 |
| 10 | t interval for a mean (net gap CIs, R2 paired difference CI, M1) | App F R2, App G (M1, M2, M4, dup, peer), Q1 | D11 s9 (t table, n-1), D10 s19 (confidence interval), D5 s24 (z form) | none | partly | check | Code: `code/r3_common.py:55-61`. The paper never names the interval type (fix P5) |
| 11 | One-sample t-test on paired differences | App F R2, Q1 | D11 s3 (difference of means against mu0), s4 (single-sample t-test) | none. hw05 line 1108 lists it only | in lecture | check | The paper gives p but names no test (fix P4) |
| 12 | Mean squared residual of the price (pre-registration: Brier score) | 4.2, 5.1, App F R1 and R2, Q1 | D23 s3 (MSE), D20 s26 (sum of squared residuals) | `hw06_regression/report/hw6_taeklim_report.tex:137` (MSE) | in lecture | descriptive | D-026 renamed it. D23 s3 is a closer source than D20 |
| 13 | Log loss | 4.2, 5.1, Q1 | D15 s9 to s14 (surprise and its average) | none | partly | descriptive | The name "log loss" is absent |
| 14 | Mean binary entropy H(p) in bits | 4.2, 5.1, Q1 | D15 s15 to s21 | none. hw04 mutual information uses entropy, not H(p) of a price | in lecture | descriptive | |
| 15 | Accuracy, precision, recall at the 0.5 line | 4.2, 5.1, App G M5, Q1 | D23 s5 to s14, s22 (cutoff 0.5), D21 s20, s21 (t = 0.5), D16 s28 (confusion) | `hw07_classification/report/hw7_taeklim_report.tex` (confusion, precision, recall), `hw08_ml_dim_reduction/report/hw8_taeklim_report.tex` (accuracy) | in lecture | descriptive | |
| 16 | Majority-class accuracy | App G M5, Q1 | D23 s7 notes, s10 (high accuracy paradox) | `hw07_classification/report/hw7_taeklim_report.tex:529` (always-no baseline) | in lecture | check | |
| 17 | Two-sample Kolmogorov-Smirnov (KS) test | 4.2 (Q1 price by outcome), 4.3 (Q2 maker and taker) | D11 s2, s13, s21, s22 | `hw02_distribution/report/hw2_taeklim_report.tex:204` (`ks_2samp`) | in lecture | descriptive | |
| 18 | Empirical CDF (ECDF) plots | App C (Q1), App F R2 | D11 s13, s15, s17 (observed cumulative distribution) | `hw02_distribution/report/hw2_taeklim_report.tex:171` (CDF rows) | in lecture | descriptive | The word "ECDF" is absent |
| 19 | Calibration chart (rate against price, diagonal) and gap panel with intervals | 5.1 Fig. calib, App G M2, Q1 | D5 s15, s16 (error bar by group) | none | partly | descriptive | The diagonal reference is not in deck text |
| 20 | Top 1, 5, 10, 20% volume shares against 80/20 | 4.3, 5.2, App G dup, Q2 | D6 s19 (power law, Pareto, 80/20) | none | in lecture | descriptive | Main Q2 answer |
| 21 | Mean and median | 4.3, 4.4, 5.2, 5.3, App G M4, Q2, Q3 | D5 s2 (mean, median), D4 s18 (median) | `hw01_fastfood_nutrition/report/hw1_taeklim_report.tex:121`, `:129` | in lecture | descriptive | |
| 22 | CCDF on log-log axes | 4.3, 5.2, Q2 | D6 s21 (complementary CDF) | `hw02_distribution/report/hw2_taeklim_report.tex:78` | in lecture | descriptive | |
| 23 | Wallet share and volume share per decade of volume | App D.1, Q2 | D5 s12, s13 (histogram) | none. hw02 drew PDFs on log-log axes, not volume-weighted | partly | descriptive | A volume-weighted histogram is not in deck text. Repo rule `.claude/rules/visualization.md` §7 asks for it |
| 24 | Lorenz curve | 4.3, 5.2, App D.1, Q2 | not found. D25 s76 (Pareto chart) text has bars only | none | outside | descriptive | The paper labels it. D25 s76 image may show a cumulative line (open check E5) |
| 25 | Welch t-test | 4.3, 5.2 (Q2 roles), App G peer a (high minus low) | D11 s2 ("Student's"), s3, s6 (two-sample t-test) | none. hw05 line 1110 lists it only | partly | descriptive | The word "Welch" is absent. Peer a code: `code/r3_peer.py:45-46` (fix P6) |
| 26 | Difference of mean log10 volume (effect size) | 4.3, 5.2, Q2 | D11 s3 (difference between means) | none | in lecture | descriptive | Replaced Cohen's d (D-026) |
| 27 | Spearman correlation | 4.3, 5.2, Q2 | D14 s32, s33 | `hw04_pair_association/code/p2_correlation.py:43` | in lecture | descriptive | The hw04 report table leaves Spearman blank. The code computes it |
| 28 | Log transform | 4.4, App D.2, App E, Q2, Q3 | D7 s12, s22 | none. hw02 used log-log axes, not a transform | in lecture | descriptive | |
| 29 | z-score | App D.2, Q2 | D7 s17 | `hw05_clustering/report/hw5_taeklim_report.tex:122`, `hw06_regression/report/hw6_taeklim_report.tex:131` | in lecture | descriptive | |
| 30 | k-means | 4.3, App D.2, Q2 | D17 s23 to s34, s36 | `hw05_clustering/report/hw5_taeklim_report.tex` (k-means section), `hw08_ml_dim_reduction/report/hw8_taeklim_report.tex:102` | in lecture | descriptive | Side analysis |
| 31 | Elbow curve of inertia | App D.2, Q2 | D17 s39, s40 | `hw05_clustering/report/hw5_taeklim_report.tex:114`, `:196` | in lecture | descriptive | |
| 32 | Fixed elbow rule (farthest point from the chord) | App D.2, Q2 | D17 s39 (elbow method, "many heuristic methods", no fixed rule), s40 (inertia) | none | partly | descriptive | Our tie-breaker for a reproducible K |
| 33 | One-way ANOVA, printed as SSB / (SSB + SSW) | App D.2, Q2 | D11 s10 to s12 (SSB, SSW) | none. hw05 line 1114 lists it only | in lecture | descriptive | D-026 rename of eta squared, same number |
| 34 | Permutation test | App D.2, Q2 | D13 s20 to s33, D15 s26 | `hw04_pair_association/code/p1_association.py:45-47` | in lecture | descriptive | |
| 35 | Chi-square test of independence, with the largest observed minus expected cell | App D.2, Q2 | D12 s2 to s9 | `hw04_pair_association/report/hw4_taeklim_report.tex` Problem 1, `hw05_clustering/report/hw5_taeklim_report.tex:1118` ("used") | in lecture | descriptive | D-026 removed Cramér's V |
| 36 | Histograms | 4.4, 5.3, App E, Q3 | D5 s12, s13, D25 s68 | `hw01_fastfood_nutrition/report/hw1_taeklim_report.tex:150`, hw02 | in lecture | descriptive | |
| 37 | QQ plot before and after log | 4.4, 5.3, App E, Q3 | D7 s5, s11 | `hw02_distribution/report/hw2_taeklim_report.tex:80` | in lecture | descriptive | |
| 38 | Normal and exponential fit from mean and SD | 4.4, 5.3, Q3 | D6 s3 (list), s4 (normal), s15, s16 (exponential, mean = 1 / lambda), D7 s2 (normal, identify the parameters) | `hw02_distribution/grading_checklist.md:24`, `:26` (lambda, mu, sigma) | in lecture | descriptive | |
| 39 | Power-law exponent by maximum likelihood, tail above fixed x_min | 4.4, 5.2, 5.3, Q2, Q3 | D6 s19 (power law, 80/20), s20 (alpha, x_min), s21 (CCDF), s22 (Clauset notes) | `hw02_distribution/report/hw2_taeklim_report.tex:105` (sum of ln(x / x_min)), `grading_checklist.md:23` | partly | descriptive | The estimator is an image or absent in deck text. hw02 computed the same estimator. The fixed x_min is ours |
| 40 | One-sample KS against a fitted distribution | 4.4, 5.2, 5.3, Q2, Q3 | D11 s13, s15 to s19 | `hw02_distribution/report/hw2_taeklim_report.tex:192` (KS distance, data against a model sample. Same `ks_2samp` call as row 17) | in lecture | descriptive | |
| 41 | Cluster bootstrap (net gap interval, chi-square, M5 band) | App G M3, M5, Q1 | D5 s25, s26 (bootstrap CI, percentile bounds) | none | partly | check | The paper says "outside". Resampling whole clusters is not in deck text (fix P1) |
| 42 | Logistic calibration, logit P(y=1) = a + b logit(p) | App G M5, Q1 | D21 s15 to s19 (logistic regression, logit) | (parent) `hw07_classification/report/hw7_taeklim_report.tex:230-233` (logistic regression fit, not on logit(price)) | partly | check | The paper says "outside". The deck fits logistic regression. Using it on logit(price) is ours (fix P1) |
| 43 | Wald interval for a and b | App G M5, Q1 | not found | none | outside | check | The paper does not label it outside (fix P2) |
| 44 | Brier skill score against in-sample climatology | App G M5, Q1 | D23 s3 (R squared: 1 minus SSE over SS of the mean model, notes) | (parent) `hw06_regression/report/hw6_taeklim_report.tex:137` (R squared, not a skill score) | partly | check | `code/r3_m5.py:103`, `:108`: 1 - MSE / (ybar (1 - ybar)). This equals R squared with y hat = price. The paper says "outside" (fix P3) |

Counts (from the rows above):

| Class | Rows | Row numbers |
| --- | --- | --- |
| in lecture | 30 | all rows not listed below |
| partly | 12 | 7, 9, 10, 13, 19, 23, 25, 32, 39, 41, 42, 44 |
| outside | 2 | 24, 43 |
| homework, computed directly | 18 | 12, 15, 16, 17, 18, 21, 22, 27, 29, 30, 31, 34, 35, 36, 37, 38, 39, 40 |
| homework, parent method only | 2 | 42 (hw07 logistic regression), 44 (hw06 R squared) |

- Rows 17 and 40 rest on one hw02 call (`ks_2samp`, data against a model sample).

- Verdict-input rows: 1, 2, 4, 6, 7. None is outside. One is partly: row 7, the goodness-of-fit form.
- Evidence: every slide id was seen in the extracted text in this session (D4, D5, D6, D7, D10 to D25). D2, D3 and D9 back only data rules and are not cited.
- No homework practiced row 7. hw04 and hw05 practiced only the independence form.

## B. Homeworks hw01 to hw08

| HW | Main techniques practiced (evidence) | Paper methods that reuse them (Table A row) |
| --- | --- | --- |
| hw01 fast-food nutrition | Mean, median, SD, histograms, box plots (`report/hw1_taeklim_report.tex:121`, `:129`, `:150`, `:160`) | 21 mean and median, 36 histograms. Box plot: none (the paper has no box plot) |
| hw02 distribution | Power-law alpha with x_min, exponential lambda, uniform, normal fits. PDF, CDF, CCDF and QQ on linear and log-log axes. KS distance against each model. First-digit distribution (`grading_checklist.md:23-33`, `report/hw2_taeklim_report.tex:78`, `:80`, `:105`, `:192`, `:204`) | 17, 18, 22, 37, 38, 39, 40. The strongest link: Q3 and the Q2 tail reuse the hw02 workflow |
| hw03 word cloud | Text cleaning, language split, word counts, word clouds (report section headings, `report/hw3_taeklim_report.tex:63`, `:105`) | none reused. The paper has no text data |
| hw04 pair association | Contingency table with expected counts, chi-square, mutual information with a permutation null, Jaccard index, Pearson and Spearman correlation, scatter plots (`grading_checklist.md:14-21`, `code/p1_association.py:45-47`, `code/p2_correlation.py:43`) | 27 Spearman, 34 permutation test, 35 chi-square independence |
| hw05 clustering | z-score, k-means at two k, elbow and inertia, hierarchical clustering with two linkages, chi-square independence (`report/hw5_taeklim_report.tex:114`, `:122`, `:1118`) | 29 z-score, 30 k-means, 31 elbow, 35 chi-square independence. Hierarchical clustering: none |
| hw06 regression | Train and test split, z-score, linear, Ridge, Lasso and KNN regression, MSE, R squared (`report/hw6_taeklim_report.tex:131`, `:137`) | 12 mean squared residual, 29 z-score, 44 skill score (same form as R squared) |
| hw07 classification | Logistic regression, Naive Bayes, KNN, oversampling, confusion matrix, accuracy, precision, recall, F1, always-no baseline, ROC curves (`report/hw7_taeklim_report.tex:230-233`, `:529`, `:660`) | 15 accuracy, precision, recall, 16 majority-class accuracy, 42 logistic calibration |
| hw08 dimensionality reduction | Centering, principal component analysis (PCA), k-means on all columns and on two components, accuracy (`report/hw8_taeklim_report.tex:100-103`, `DESIGN.md` §2) | 30 k-means, 15 accuracy. PCA: none |

## C. Decks and methods with zero paper use

Never write these as used. Adopting one is an owner decision (D-025). Any new number needs a run on the cluster.

Decks with no paper use: D1 Syllabus (no method), D18 Hierarchical Clustering, D19 Recommendation Systems, D22 Classification, D24 Dimensionality Reduction. No deck 8 file exists in the extracted text. D2, D3 and D9 back only data rules and general testing terms, not a counted row.

Decks 23 and 25 are used (rows 12, 15, 16, 36, 44). README row 15 is stale on this point.

| Deck | Key methods (slide id) | Could apply (suggestion, to validate) | Reason |
| --- | --- | --- | --- |
| D22 Classification | KNN (s2 to s13), Naive Bayes (s14 to s36) | No, for Q1 to Q3 | No question asks to predict a label from features |
| D23 Model Evaluation | F1 (s17), specificity (s18, s19), ROC curve (s26 to s38), AUC (s39), PR curve (s42), ranked pairs, c-index (s45) | Q1: ROC curve and AUC of the price as a score of outcome 1 | It reads how well the price separates winners, beside the KS D (row 17). hw07 practiced ROC curves |
| D24 Dimensionality Reduction | PCA (s5 to s23), scale features first (s23), LDA (s25 to s33) | Q2: PCA view of the k-means wallet features | It shows whether the clusters separate in two dimensions. LDA needs a label, so no |
| D25 Visualization | Simpson's paradox (s43, s44), box plot (s67), Pareto chart (s76), color and accessibility (s20 to s38) | Q2: Pareto chart as a lecture view of the top shares. Q1 checks: Simpson's paradox as a framing for M2 and peer splits. Q3: box plot of trade size | The Pareto chart may replace or back the Lorenz curve (row 24) after the image check E5. Simpson's paradox asks whether a pooled gap hides subgroup gaps |
| D18 Hierarchical Clustering | Dendrogram (s2, s3), agglomerative steps (s8 to s14), linkages (s21, s22), against k-means (s29) | Q2: hierarchical clustering on the k-means sample | A second clustering checks the k-means side result. hw05 practiced it |
| D19 Recommendation Systems | User-item matrix (s6), collaborative filtering (s10), sparsity (s11), hierarchical cut at k (s27, s28) | No, for Q1 to Q3 | A wallet by market matrix answers no current question |
| D21 Logistic Regression (unused part) | Ridge, Lasso, Elastic Net (s10 to s14) | No | The logistic calibration has two parameters only |

## D. Fix list

### D.1 README, tips and slides (stale text)

| File | Line | Old text | Proposed new text |
| --- | --- | --- | --- |
| `README.md` | 59 | The audit counted 52 methods: 35 in a lecture, 7 partly, 10 not found. Ten were removed, renamed or labeled (D-026, D-028). | The 2026-11-16 audit counts 44 methods in the current paper: 30 in a lecture, 12 partly, 2 outside. 18 were also computed in a homework, and 2 more by their parent method (`analysis/lecture_hw_method_audit_2026_11_16.md`). |
| `README.md` | 67 | The audit lists five slides to open (D11 slides 3 and 6, D7 slide 2, D6 slide 20, D12 slides 5 to 9, D5 slide 24). | The audit lists six slides to open (D5 s24, D6 s20, D7 s2, D11 s3 and s6, D12 s5 to s9, D25 s76). |
| `README.md` | 74, 80, 84, 96 | "audit section 2", "audit section 3.3", `analysis/lecture_method_audit.md` | Keep these pointers, but name the file: "the 2026-11-01 audit (`analysis/lecture_method_audit.md`) section ...". Add the new file to line 96 |
| `README.md` | 76 | `D20 Regression, D15 Entropy` | `D23 Model Evaluation (s3), D20 Regression, D15 Entropy` |
| `README.md` | 77 | `D16 Intro to Machine Learning, D21 Logistic Regression, D11 Comparing Distributions, D9 and D10` | `D23 Model Evaluation (s5 to s14), D16 Intro to Machine Learning, D21 Logistic Regression, D11 Comparing Distributions, D10` |
| `README.md` | 82 | `Mean, median, histogram, violin plot, box plot` | `Mean, median, histogram` (the current paper has no violin or box plot) |
| `README.md` | 82 | `The Lecture 25 deck on visualization (25_Visualization.pptx, suggestion, to validate)` | `Box plot of trade size (D25 s67, suggestion, to validate)` |
| `README.md` | 85 | Row 15: `None. The audit did not map these decks` | `D23 and D25 are used (rows 6, 7, 12). D22 and D24 are not used. Candidates: ROC and AUC (D23 s26 to s39), PCA (D24 s5 to s23), Pareto chart (D25 s76), all suggestions to validate` |
| `README.md` | 87 | Four methods lie outside the lectures. The paper labels each one (D-028, D-041). D-047 removed the Wilson interval. | The paper labels four methods outside the lectures (D-028, D-041, D-047). Three have a lecture parent, so the audit classes them partly. The Wald interval in check M5 is outside and not labeled. |
| `README.md` | 94 | `Squared residual (D20)` | `R squared against the mean model (D23 s3). Same formula with the price as the prediction` |
| `tips/polymarket_lecture_rq_guide_tips.html` | 315 | ko: `그래도 이 넷은 부록에서 던져진 질문에 답하려고 남겼고` / en: `These four stay because they answer a question raised in review` | ko: `Lorenz 곡선은 소유자 결정(D-028)으로, 나머지 셋은 리뷰 질문에 답하려고 남겼다.` / en: `The Lorenz curve stays by an owner decision (D-028). The other three answer questions raised in review.` |
| `tips/polymarket_lecture_rq_guide_tips.html` | 327 | ko: `덱 22~25(...)는 감사가 매핑하지 않았다. 열어 보고 Q1~Q3에 더 맞는 방법이 있는지 본다 (제안, 확인 필요).` / en: `The audit did not map decks 22 to 25 (...). Open each deck and see whether a method fits Q1, Q2 or Q3 better (suggestion, to validate).` | ko: `덱 23과 25는 쓰였다 (MSE, 혼동 행렬, 히스토그램). 덱 22와 24는 쓰이지 않았다. 후보: ROC와 AUC(D23), PCA(D24), 파레토 차트(D25) (제안, 확인 필요).` / en: `Decks 23 and 25 are used (MSE, confusion matrix, histogram). Decks 22 and 24 are not used. Candidates: ROC and AUC (D23), PCA (D24), Pareto chart (D25) (suggestion, to validate).` |

Conditional (no edit now):

- `tips/polymarket_lecture_rq_guide_tips.html:112`, `:314` and `tips/presentation/deck/project/slides/methods.html:33` say "four methods outside". They match the paper label (`04-methods.tex:53`). Change them only if the owner changes that paper line (P1).
- `slides/backup-lorenz.html:6` and `slides/q2-why-how.html:28` call the Lorenz curve outside. Correct today. Revisit after check E5.
- `tips/polymarket_lecture_rq_guide_tips.html:221` says the Wilson interval became the z interval "in the main text". Since D-047 it is the z interval everywhere. Proposed en: "and the Wilson interval became the z interval (D-026, D-047)." Lines 221 and 325 also keep history (old names). The owner asked tips to show the current state only (memory note, 2026-11-08). Owner may drop them.

### D.2 Paper mismatches (for the owner, not fixed)

| # | Paper file and line | Mismatch | Option |
| --- | --- | --- | --- |
| P1 | `04-methods.tex:53` | It labels cluster bootstrap chi-square and logistic calibration "outside". Deck text has their parents: bootstrap CI (D5 s25, s26) and logistic regression (D21 s15 to s19) | (a) keep "outside" as a conservative label. (b) relabel "a variant of" the deck method |
| P2 | `04-methods.tex:54`, `app-g-review.tex:89-90` | "All other methods come from the CS 6344 course lectures." The Wald interval is outside and unlabeled. Twelve methods are only partly in the decks | (a) add the Wald interval to the outside list. (b) soften line 54 to "come from or build on the lectures" |
| P3 | `app-g-review.tex:94`, `:98` | The Brier skill score equals R squared of D23 s3 with the price as the prediction (`code/r3_m5.py:103`, `:108`). D-026 counts a rename with the same number as in lecture. Line 94 also prints "Brier", a name D-026 replaced | Rename to "R squared of the price against the base rate", then it is in lecture. Owner decision |
| P4 | `app-f-robust.tex:77-78` | A paired difference with CI and p. No test is named | Name it: one-sample t-test on paired differences, with a t interval |
| P5 | `app-g-review.tex:7-8`, `:29`, `:75`, `:126-128`, `:141-145` | Net gap CIs name no interval type. Code: t interval (`code/r3_common.py:55-61`, `:74`) | State "t interval" once in the checks summary (`09-res-checks.tex`) |
| P6 | `app-g-review.tex:129`, `:135` | "pre-registered difference test" is unnamed. Code: Welch t-test (`code/r3_peer.py:45-46`) | Name the Welch t-test |
| P7 | `app-d-q2.tex:57` | Typo: a space before the period, "independence ." | Remove the space |

## E. Open checks for teammates

| # | Check | What it settles |
| --- | --- | --- |
| E1 | Open D5 s24 (image) | The exact z interval form. If it is p ± 1.96 SD / sqrt(n), row 9 becomes in lecture |
| E2 | Open D12 s5 to s9 | Whether any goodness-of-fit form appears. If yes, row 7 becomes in lecture |
| E3 | Open D11 s3 and s6 | Whether the two-sample t uses unpooled variances. If yes, row 25 becomes in lecture |
| E4 | Open D6 s20 and D7 s2 | Whether the power-law estimator is on a slide. If yes, row 39 becomes in lecture (x_min choice stays ours) |
| E5 | Open D25 s76 | Whether the Pareto chart has a cumulative share line. If yes, it is a lecture parent of the Lorenz curve (row 24) |
| E6 | Closed: D17 s39 text calls the elbow one of "many heuristic methods" and gives no fixed rule | Row 32 stays partly |
| E7 | Check the log base of the log loss in `code/q1_calibration.py` against the paper text | D15 uses bits. The paper says bits for H(p) only (`04-methods.tex:77`) |
| E8 | Owner: P1, P2, P3 | Each changes the outside count (2) or the paper label (4) |
| E9 | hw03 | Checked: its report counts comments and words only. No paper reuse |
