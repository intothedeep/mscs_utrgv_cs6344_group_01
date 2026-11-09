# Sourced summaries of the 11 references in paper_mvp1 (2026-11-08)

- Purpose: one verified summary per reference cited in `papers/paper_mvp1/main.tex`.
- Inputs: `papers/paper_mvp1/references.bib` (11 entries), `papers/paper_mvp1/main.tex`.
- Reuse: R1 to R5 of `analysis/related_work_refs.md`, re-checked here.
- Tag: `PS`. Source IDs follow `[S-PS-n]`.
- Verification enum: `verified` (primary source or its abstract page read), `partial` (some field not checked, named in the entry), `unverifiable`.
- This file is a research output. It does not edit the paper or `references.bib`.

## Summary

- entries: 11 of 11
- verified: 9
- partial: 2 (brier1950verification, page2013prediction)
- unverifiable: 0
- sources: 16
- One wording mismatch in our paper, L963, fixed 2026-11-08: now "fall disproportionately into" (see entry 1).

## Key map

| key | topic group | our section(s), main.tex line | Q | verification |
| --- | --- | --- | --- | --- |
| qin2026polymarketv1 | Data source | Intro L123. Related Work L156, L162, L164. Data L197, L201. Results Q2 L589. Limitations L963 | data, Q1, Q2 | verified |
| polymarketv1data | Data source | Data, Source and scope L194, L199 | data | verified |
| snowberg2010favorite | Prediction-market calibration | Related Work L152. Results Q1 L462 | Q1 | verified |
| brier1950verification | Forecast scoring and calibration theory | Methods Q1 L337 | Q1 | partial |
| benjamini1995controlling | Statistical method | Methods Q1 L329 | Q1, methods | verified |
| raasveldt2019duckdb | Tool | Methods, Reproducibility L390 | methods | verified |
| gneiting2007strictly | Forecast scoring and calibration theory | Related Work L179 | Q1 | verified |
| wolfers2004prediction | Prediction-market calibration | Related Work L169 | Q1 | verified |
| clauset2009power | Distribution fitting | Related Work L182, Methods Q3 L382 | Q3 (also Q2 CCDF) | verified |
| le2026decomposing | Prediction-market calibration | Related Work L175 | Q1 | verified |
| page2013prediction | Prediction-market calibration | Related Work L172 | Q1 | partial |

## Sections that cite nothing

Found by a grep of `\cite` in `main.tex`.

| section | starts at main.tex line | note |
| --- | --- | --- |
| Data, Filters and drop reasons | L203 | own pipeline |
| Data, Market and wallet tables | L222 | own pipeline |
| Methods, Evaluation price and pre-registration | L235 | own rules |
| Methods, Q2 wallet concentration | L344 | 80/20, CCDF, Lorenz, Welch t, Spearman, k-means: no source |
| Methods, Q3 distributions | L373 | cites Clauset at L382 (added 2026-11-08). x_min fixed at top 10%, reason is an owner \todo at L384 |
| Results, Q3 | L622 | no citation |
| Results, Robustness | L690 | no citation |
| Results, Checks requested in review | L766 | no citation |
| Discussion | L917 | no citation |
| Conclusion | L1001 | no citation |

- Every Results Q3 claim rests on our own runs. No outside number is compared there. [inference]

## Entries

One block per reference. Each block was appended after it was checked.

### 1. qin2026polymarketv1

- Citation: Qin, B., and Yang, R. (2026). Polymarket-v1 Database. arXiv:2606.04217 [cs.CE], v2 (2026-06-08). https://doi.org/10.48550/arXiv.2606.04217
- Topic group: Data source.
- Problem: No complete on-chain trade archive of Polymarket existed with true trade direction. [S-PS-1]
- Data: 1.20 billion trades, 1.30 million markets, $61 billion nominal volume. [S-PS-1]
- Data period: 2022-11-21 to 2026-04-28, the first CTF Exchange on Polygon. [S-PS-1]
- Method:
  1. Read every fill from the on-chain settlement layer. [S-PS-1]
  2. Take the aggressor side from the chain, not from a heuristic. [S-PS-1]
  3. Benchmark trade classifiers (tick rule, bulk volume) against this truth. [S-PS-1]
  4. Relate microstructure measures (VPIN, Gibbs spread) to Brier scores on a panel. [S-PS-1] [S-PS-2]
- Key results:
  - Tick rule 49.83% and bulk volume classification 50.51% accuracy in aggregate. [S-PS-1]
  - True VPIN predicts Brier scores positively. Gibbs spread predicts them negatively. [S-PS-1]
  - Brier panel: 1,019 resolved Standard Binary markets with balanced monthly observations. [S-PS-2]
  - Table 3 mean return (payout minus price): 0.00 to 0.10 bin is -0.0023. [S-PS-2]
  - Table 3 mean return: 0.20 to 0.30 bin is -0.0032. [S-PS-2]
  - Table 3 mean return: 0.10 to 0.20 bin is -0.0019. [S-PS-2]
  - Table 3 counts trades per bin, for example 34,902,814 trades in the 0.00 to 0.10 bin. [S-PS-2]
  - Table 3: bins from 0.40 up have positive mean returns, up to +0.0098 at 0.80 to 0.90. [S-PS-2]
  - Table 5: top 1% of maker addresses control 84.1% of maker-side volume. [S-PS-2]
  - Table 5: maker Gini 0.9698. [S-PS-2]
  - Up-Down markets have "fundamentally different settlement mechanics" and "should not be pooled". [S-PS-2]
- Limitations: No off-chain order book. V1 exchange only. Preprint, not peer reviewed. [S-PS-1] [S-PS-3]
- How our paper uses it:
  - Introduction, L123: trade and market counts (data).
  - Related Work, L156 to L165: cheap-token bias (Q1), Brier panel (Q1), top-1% maker share (Q2).
  - Data, Source and scope, L197 and L201: Up/Down exclusion (data).
  - Results Q2, L589: pipeline check of the top-1% maker share (Q2).
  - Limitations, L963: Sports markets and Neg-Risk (data).
- Mismatch 1, L963 (fixed 2026-11-08): our text said "most Sports markets are Neg-Risk or Up/Down". It now says "fall disproportionately into". [inference]
  - The source says Sports markets "disproportionately fall into" Neg-Risk and Up-Down (limitation 7). [S-PS-2]
  - "Disproportionately" is not "most". The source gives no majority share in what was read.
- Note 2, L157 to L158: our text says "under 30 cents" and "0.2 to 0.3 cents less".
  - The three bins below 0.30 give -0.0023, -0.0019 and -0.0032. [S-PS-2]
  - In cents that is 0.19 to 0.32. "0.2 to 0.3" holds after rounding. [inference]
  - The source states no unit. Dollars per share is our reading. [inference]
  - The source cutoff is "price ≤0.30" (Figure 5 caption), not "under". [S-PS-2]
  - "Counted by trade" fits: Table 3 counts trades per bin. [S-PS-2]
- Why it matters to us: it is our data's own paper, so our numbers must agree with it.
- Verification: `verified`. Read: [S-PS-1] abstract page, [S-PS-2] HTML full text through a summarising fetch with targeted questions. Only the Sports wording at L963 disagrees with the source.

### 2. polymarketv1data

- Citation: Qin, B., and Yang, R. (2026). Polymarket-v1 (dataset). Hugging Face `TimeSeventeen/Polymarket-v1`, license CC-BY-4.0. https://huggingface.co/datasets/TimeSeventeen/Polymarket-v1
- Topic group: Data source.
- Problem: It releases the Polymarket-v1 archive as open Parquet files. [S-PS-3]
- Data: 2,786,380,324 rows, 52.7 GB in total. [S-PS-3]
- Data by layer: `orderfilled` about 1.2B rows, `ctf` about 839M, `daily_aligned` about 602M, `daily_aligned_multi` about 144M. [S-PS-3]
- Data period: 2022-11-21 to 2026-04-28. [S-PS-3]
- Method (layers):
  1. `OrderFilled/`: raw maker-taker fills, nominal, may include relayer records. [S-PS-3]
  2. `daily_aligned/`: Standard Binary markets, `neg_risk` always false, relayer records excluded. [S-PS-3]
  3. `daily_aligned/` adds `p_event` and `D`, one event-probability axis for both legs. [S-PS-3]
  4. `daily_aligned_multi/`: Neg Risk markets, same cleaning. [S-PS-3]
  5. `CTF/`: contract lifecycle events. [S-PS-3]
- Key result: the card states no trade or market total. It gives row counts only. [S-PS-3]
- Limitations: no order-book snapshots, v1 contracts only, static metadata snapshot. [S-PS-3]
- How our paper uses it:
  - Data, Source and scope, L194: relayer records removed in `daily_aligned/` (data).
  - Data, Source and scope, L199: data location and CC-BY-4.0 license (data).
- Why it matters to us: it is the exact layer we query, and it sets our license.
- Verification: `verified`. Dataset card read. [S-PS-3]

### 3. raasveldt2019duckdb

- Citation: Raasveldt, M., and Mühleisen, H. (2019). DuckDB: an Embeddable Analytical Database. SIGMOD '19, Amsterdam, 4 pages. https://doi.org/10.1145/3299869.3320212
- Page range 1981 to 1984 comes from our bib. The PDF read does not print it.
- Topic group: Tool.
- Problem: No purpose-built embedded database existed for analytical (OLAP) SQL. SQLite targets OLTP. [S-PS-4]
- Data: none (system demo). The demo uses TPC-H benchmark tables. [S-PS-4]
- Method:
  1. Run inside the host process through a C/C++ API. No server. [S-PS-4]
  2. Use a vectorized execution engine, 1024 values per vector by default. [S-PS-4]
  3. Use a cost-based optimizer and serializable MVCC. [S-PS-4]
  4. Store data column-wise in compressed blocks (DataBlocks layout). [S-PS-4]
- Key result: it ran all TPC-H queries and all but two TPC-DS queries at writing. [S-PS-4]
- Limitations: demo paper with no benchmark numbers. Buffer manager not yet built then. [S-PS-4]
- How our paper uses it: Methods, Reproducibility, L390. Tool for all data queries (methods).
- Why it matters to us: it lets one CPU node scan billions of Parquet rows with SQL.
- Verification: `verified`. Full paper PDF read, pages 1 to 4. [S-PS-4]

### 4. benjamini1995controlling

- Citation: Benjamini, Y., and Hochberg, Y. (1995). Controlling the False Discovery Rate: A Practical and Powerful Approach to Multiple Testing. *Journal of the Royal Statistical Society Series B*, 57(1), 289-300. https://doi.org/10.1111/j.2517-6161.1995.tb02031.x
- Topic group: Statistical method.
- Problem: Familywise error rate (FWER) control loses power when many hypotheses are tested. [S-PS-5]
- Data: none in the abstract. Simulations and examples only. Counts unknown. [S-PS-5]
- Method:
  1. Define the false discovery rate (FDR): expected share of false rejections. [S-PS-5]
  2. Use a sequential Bonferroni-type procedure to control it. [S-PS-5]
  3. Prove control for independent test statistics. [S-PS-5]
- Key result: FDR equals FWER when all nulls are true and is smaller otherwise. [S-PS-5]
- Key result: simulations show a substantial power gain. Exact numbers not in the abstract. [S-PS-5]
- Limitations: the proof covers independent test statistics only. [S-PS-5]
- How our paper uses it: Methods Q1, L329. It corrects the 10 per-bin tests (Q1, methods).
- Why it matters to us: it keeps 10 bin tests from giving false alarms by chance.
- Verification: `verified`. Abstract read via the Crossref record, publisher-deposited. Full text not read. [S-PS-5]

### 5. snowberg2010favorite

- Citation: Snowberg, E., and Wolfers, J. (2010). Explaining the Favorite-Long Shot Bias: Is It Risk-Love or Misperceptions? *Journal of Political Economy*, 118(4), 723-746. Working paper: NBER w15923, https://www.nber.org/papers/w15923
- DOI of the journal article: unknown (not in our bib, not read). NBER working paper DOI: 10.3386/w15923. [S-PS-6]
- Topic group: Prediction-market calibration.
- Problem: Is the favorite-longshot bias caused by risk-love or by misperceived probabilities? [S-PS-6]
- Data: all 6,403,712 US horse starts, 1992 to 2001, official jockey club data. [S-PS-7]
- Data subset: 206,808 races (1,485,112 starts) with exacta, quinella or trifecta payoffs. [S-PS-7]
- Data, other countries: 2,725,000 starts in Australia, 380,000 in Great Britain. [S-PS-7]
- Method:
  1. Plot the rate of return on win bets against odds, Lowess smoothed. [S-PS-7]
  2. Fit a risk-love model and a misperception model to win bets. [S-PS-7]
  3. Test which model also prices compound bets (exacta, quinella, trifecta). [S-PS-6]
- Key results:
  - Return on horses at 100/1 or longer is about -61%. [S-PS-7]
  - Random betting returns about -23%. Betting the favorite loses only 5.5%. [S-PS-7]
  - Odds 4/1 to 9/1 give a roughly constant return near -18%. [S-PS-7]
  - Misperceptions of probability drive the bias, as Prospect Theory suggests. [S-PS-6]
- Note: Figure 1 notes cite 5,610,580 starts. The text cites 6,403,712. Both are on the NBER PDF. [S-PS-7]
- Limitations: horse racing, not prediction markets. Numbers are from the 2010 working paper, not the JPE print. [inference]
- How our paper uses it:
  - Related Work, L152 to L154: longshots win less often than their odds say (Q1).
  - Results Q1, L462: our cheapest-bin gap has the same direction (Q1).
- Why it matters to us: it is the classic evidence that cheap bets are overpriced.
- Note: the JPE version was not opened. Its numbers and title wording are not checked.
- Verification: `verified`. NBER abstract page and working-paper PDF read. [S-PS-6] [S-PS-7]

### 6. brier1950verification

- Citation: Brier, G. W. (1950). Verification of Forecasts Expressed in Terms of Probability. *Monthly Weather Review*, 78(1), 1-3. https://doi.org/10.1175/1520-0493(1950)078<0001:VOFEIT>2.0.CO;2
- BibTeX caution: the DOI holds `<` and `>`. Our bib has no `doi` field, so no break today.
- Topic group: Forecast scoring and calibration theory.
- Problem: How to score forecasts stated as probabilities, such as chance of rain. [S-PS-9] [LOW-CONFIDENCE]
- Data: unknown. The paper was not read.
- Method, as a 1988 National Weather Service note describes the score: [S-PS-9]
  1. For each forecast i, take the forecast probability P_i. [S-PS-9]
  2. Set the outcome d_i to 1 if the event happens, else 0. [S-PS-9]
  3. Score B = (1/N) · sum of (P_i − d_i)². [S-PS-9]
  4. B runs from 0 (perfect) to 1 (totally bad). Lower is better. [S-PS-9]
- Caution: the same note calls this "a slightly modified version" of Brier's score (Sanders, 1963). [S-PS-9]
- Caution: Brier's original form may be twice the modern binary score, range 0 to 2. [S-PS-10] [LOW-CONFIDENCE]
- Key result: unknown. The paper was not read.
- Limitations: one number mixes calibration and sharpness. [inference]
- How our paper uses it: Methods Q1, L337. It names our mean squared residual of the price (Q1).
- Why it matters to us: it is the one-number accuracy score for our market prices.
- Verification: `partial`. Citation fields from Crossref [S-PS-8]. Content not read. AMS page returned HTTP 403. The formula comes from a secondary 1988 note [S-PS-9].

### 7. page2013prediction

- Citation: Page, L., and Clemen, R. T. (2013). Do Prediction Markets Produce Well-Calibrated Probability Forecasts? *The Economic Journal*, 123(568), 491-513. https://doi.org/10.1111/j.1468-0297.2012.02561.x
- Topic group: Prediction-market calibration.
- Problem: Are prediction-market prices calibrated probabilities, and when do they fail? [S-PS-11]
- Data: unknown. Market source and counts were not in the abstract read.
- Method: unknown in detail. The abstract read gives results only. [S-PS-11]
- Key results:
  - Markets "are reasonably well calibrated when time to expiration is relatively short". [S-PS-11]
  - "Prices are significantly biased for events farther in the future". [S-PS-11]
  - Favourite/longshot bias: low-likelihood events are over-priced. [S-PS-11]
- Limitations: unknown from the abstract. [inference]
- How our paper uses it: Related Work, L172 to L174. Calibration depends on time to expiry, plus longshot bias (Q1).
- Why it matters to us: it says when crowd prices are right, and when cheap bets mislead.
- Verification: `partial`. Abstract read on Duke Scholars, 2026-11-07, reused [S-PS-11]. Wiley page returned HTTP 403 today [S-PS-12]. Data and method not checked.

### 8. gneiting2007strictly

- Citation: Gneiting, T., and Raftery, A. E. (2007). Strictly Proper Scoring Rules, Prediction, and Estimation. *Journal of the American Statistical Association*, 102(477), 359-378. https://doi.org/10.1198/016214506000001437
- Topic group: Forecast scoring and calibration theory.
- Problem: Which scores reward an honest probabilistic forecast, and how should one build them? [S-PS-13]
- Data: none (theory and review). One case study on Pacific Northwest weather forecasts. Counts unknown. [S-PS-13]
- Method:
  1. Define proper: the true distribution maximizes expected score. Strictly proper: uniquely. [S-PS-13]
  2. Derive proper rules from convex functions. Link them to entropy and Bregman divergences. [S-PS-13]
  3. Review examples: logarithmic, spherical, pseudospherical, quadratic, continuous ranked probability score. [S-PS-13]
- Result: the goal is "to maximize the sharpness of the predictive distributions subject to calibration". [S-PS-13]
- Key result: the keywords list the Brier score among the scoring rules covered. [S-PS-13]
- Note: the paper treats scores as rewards (higher is better). The Brier score above is a loss. [S-PS-13]
- Limitations: theory paper. It gives no prediction-market evidence. [inference]
- How our paper uses it: Related Work, L179 to L181. The Brier score is a proper score (Q1).
- Why it matters to us: it shows our price score cannot be gamed by a dishonest forecast.
- Verification: `verified`. PDF page 1 read (abstract, keywords, introduction). [S-PS-13]

### 9. wolfers2004prediction

- Citation: Wolfers, J., and Zitzewitz, E. (2004). Prediction Markets. *Journal of Economic Perspectives*, 18(2), 107-126. https://doi.org/10.1257/0895330041371321
- Topic group: Prediction-market calibration.
- Problem: Can simple markets pool scattered information into good forecasts? [S-PS-14]
- Data: none of its own (review). It draws on many prediction settings. Counts unknown. [S-PS-14]
- Method:
  1. Review evidence from prediction markets in several settings. [S-PS-14]
  2. Explain contract types that reveal probabilities, means, medians and uncertainty. [S-PS-14]
  3. Discuss market design and the domains where markets help most. [S-PS-14]
- Key result: market forecasts are typically fairly accurate. [S-PS-14]
- Key result: they usually beat moderately sophisticated benchmarks. No numbers in the abstract. [S-PS-14]
- Limitations: conditional markets show correlation, not causation. [S-PS-14]
- How our paper uses it: Related Work, L169 to L171. Background claim that markets forecast well (Q1).
- Why it matters to us: it is the baseline claim that our calibration test checks on Polymarket.
- Verification: `verified`. AEA abstract page read. Full text not opened. [S-PS-14]

### 10. clauset2009power

- Citation: Clauset, A., Shalizi, C. R., and Newman, M. E. J. (2009). Power-Law Distributions in Empirical Data. *SIAM Review*, 51, 661-703. https://doi.org/10.1137/070710111 (arXiv:0706.1062)
- Topic group: Distribution fitting.
- Problem: least-squares fitting gives inaccurate exponents and no test of fit. [S-PS-15]
- Data: 24 real datasets from several fields, plus synthetic data. [S-PS-15]
- Method:
  1. Fit the power law by maximum likelihood. [S-PS-15]
  2. Test goodness of fit with the Kolmogorov-Smirnov (KS) statistic. [S-PS-15]
  3. Compare with other distributions by likelihood-ratio tests. [S-PS-15]
- Lower bound x_min: chosen as the value that minimizes the KS distance D (section 3.3, after eq. 3.9). Verified in the arXiv PDF 0706.1062 by the reviewer, 2026-11-08. [S-PS-17]
- Key result: the power law fits some of the 24 datasets and is ruled out for others. [S-PS-15]
- Key result: per-dataset counts are not in the abstract. Unknown.
- Limitations: the method needs enough tail data to tell a power law from alternatives. [inference]
- How our paper uses it: Related Work, L182 to L186. Power-law fit and KS check (Q3, Q2 CCDF).
- Note: Methods Q3 cites it at L382 (added 2026-11-08).
- Note: our x_min is fixed at the top 10%. No likelihood-ratio test is run (L186).
- Why it matters to us: it tells us a straight log-log line alone does not prove a power law.
- Verification: `verified`. arXiv abstract page read. [S-PS-15]

### 11. le2026decomposing

- Citation: Le, N. A. (2026). Decomposing Crowd Wisdom: Domain-Specific Calibration Dynamics in Prediction Markets. arXiv:2602.19520 [stat.AP], v2 (2026-08-04). https://doi.org/10.48550/arXiv.2602.19520
- Topic group: Prediction-market calibration.
- Problem: How does calibration change with event domain, time to resolution and trade size? [S-PS-16]
- Data: 353 million trades on 429,000 binary contracts, Kalshi and Polymarket (v2). Period not stated. [S-PS-16]
- Method:
  1. Fit logistic recalibration slopes per cell. [S-PS-16]
  2. Decompose the slopes descriptively by domain, time and trade size. [S-PS-16]
  3. Propagate first-stage error with a Bayesian measurement-error model. [S-PS-16]
  4. Check with market- and event-clustered bootstraps. [S-PS-16]
- Key results:
  - The decomposition explains 87.3% of in-sample variance on Kalshi, 71.5% out of sample. [S-PS-16]
  - Political markets are underconfident: prices compress toward 50%. This replicates on Polymarket. [S-PS-16]
  - Large political trades on Kalshi add compression. Not robust on Polymarket. [S-PS-16]
  - About half of the raw slope variation may be estimation noise. [S-PS-16]
- Limitations: preprint, not peer reviewed. The decomposition is descriptive. [S-PS-16]
- How our paper uses it: Related Work, L175 to L177. Calibration varies by domain and trade size (Q1).
- Why it matters to us: pooling all our markets may hide domain-level miscalibration.
- Verification: `verified`. arXiv abstract page read, v2. [S-PS-16]

## Selection log

- kept: all 11 keys in `references.bib`. The task fixes the set. No search for new papers.
- reused: R1 to R5 of `analysis/related_work_refs.md`. Each was re-read today, except Page and Clemen (Duke page reused).
- rejected source: Brier (1950) on AMS. Rule: HTTP 403.
- rejected source: Page and Clemen (2013) on Wiley. Rule: HTTP 403.
- rejected source: `https://sports-models-kb.pages.dev/brier-score-original-paper`. Rule: blog, below source rank, and its title wording differs.

## Sources

[S-PS-1] Polymarket-v1 Database | https://arxiv.org/abs/2606.04217 | published: 2026-06-08 (v2) | accessed: 2026-11-08 | type: paper | note: arXiv abstract page
[S-PS-2] Polymarket-v1 Database | https://arxiv.org/html/2606.04217 | published: 2026-06-08 (v2) | accessed: 2026-11-08 | type: paper | note: HTML full text, read through a summarising fetch with targeted questions
[S-PS-3] TimeSeventeen/Polymarket-v1 dataset card | https://huggingface.co/datasets/TimeSeventeen/Polymarket-v1 | published: 2026 | accessed: 2026-11-08 | type: official | note: dataset card read
[S-PS-4] DuckDB: an Embeddable Analytical Database | https://duckdb.org/pdf/SIGMOD2019-demo-duckdb.pdf | published: 2019-06 | accessed: 2026-11-08 | type: paper | note: full PDF read, 4 pages
[S-PS-5] Crossref record 10.1111/j.2517-6161.1995.tb02031.x | https://api.crossref.org/works/10.1111/j.2517-6161.1995.tb02031.x | published: 1995 | accessed: 2026-11-08 | type: aggregator | note: metadata and publisher-deposited abstract
[S-PS-6] Explaining the Favorite-Longshot Bias: Is it Risk-Love or Misperceptions? | https://www.nber.org/papers/w15923 | published: 2010-04 | accessed: 2026-11-08 | type: official | note: NBER abstract page
[S-PS-7] Explaining the Favorite-Longshot Bias: Is it Risk-Love or Misperceptions? (NBER WP 15923 PDF) | https://www.nber.org/system/files/working_papers/w15923/w15923.pdf | published: 2010-04 | accessed: 2026-11-08 | type: paper | note: PDF pages 1 to 6 read (cover, abstract, introduction, section 2)
[S-PS-8] Crossref record 10.1175/1520-0493(1950)078<0001:VOFEIT>2.0.CO;2 | https://api.crossref.org/works/10.1175/1520-0493(1950)078%3C0001:VOFEIT%3E2.0.CO;2 | published: 1950-01 | accessed: 2026-11-08 | type: aggregator | note: metadata only, no abstract
[S-PS-9] A New Measure of Forecast Skill Using the Brier Score (NWS Central Region Technical Attachment 88-26) | https://repository.library.noaa.gov/view/noaa/33800/noaa_33800_DS1.pdf | published: 1988-07 | accessed: 2026-11-08 | type: gov | note: secondary source, PDF pages 1 to 2 read
[S-PS-10] Brier score (Wikipedia mirror) | https://ipfs.ssi.eecc.de/ipns/en.wikipedia-on-ipfs.org/wiki/Brier_score | published: unknown | accessed: 2026-11-08 | type: aggregator | note: search snippet only, not opened
[S-PS-11] Do Prediction Markets Produce Well-Calibrated Probability Forecasts? | https://scholars.duke.edu/publication/765630 | published: 2013-05 | accessed: 2026-11-07 | type: official | note: abstract on author repository, read for analysis/related_work_refs.md, not re-read
[S-PS-12] Do Prediction Markets Produce Well-Calibrated Probability Forecasts? (Wiley) | https://onlinelibrary.wiley.com/doi/10.1111/j.1468-0297.2012.02561.x | published: 2013 | accessed: 2026-11-08 | type: official | note: HTTP 403, not read
[S-PS-13] Strictly Proper Scoring Rules, Prediction, and Estimation | https://sites.stat.washington.edu/raftery/Research/PDF/Gneiting2007jasa.pdf | published: 2007-03 | accessed: 2026-11-08 | type: paper | note: PDF page 1 read
[S-PS-14] Prediction Markets | https://www.aeaweb.org/articles?id=10.1257/0895330041371321 | published: 2004 | accessed: 2026-11-08 | type: official | note: publisher abstract page
[S-PS-15] Power-law distributions in empirical data | https://arxiv.org/abs/0706.1062 | published: 2009-02-02 (v2) | accessed: 2026-11-08 | type: paper | note: arXiv abstract page
[S-PS-16] Decomposing Crowd Wisdom: Domain-Specific Calibration Dynamics in Prediction Markets | https://arxiv.org/abs/2602.19520 | published: 2026-08-04 (v2) | accessed: 2026-11-08 | type: paper | note: arXiv abstract page
[S-PS-17] Power-law distributions in empirical data, full text | https://arxiv.org/pdf/0706.1062 | published: 2009-02-02 (v2) | accessed: 2026-11-08 | type: paper | note: section 3.3, after eq. 3.9: "Our estimate x_min is then the value of x_min that minimizes D". Read by the reviewer

open_questions:

- Closed 2026-11-08: main.tex L963 said "most Sports markets are Neg-Risk or Up/Down". The dataset paper says Sports markets "disproportionately fall into" them (limitation 7). Suggest "disproportionately". [S-PS-2]
- main.tex L157 says "under 30 cents". The dataset paper uses "price ≤0.30". Minor. [S-PS-2]
- Table 3 return unit is not stated in the dataset paper. Dollars per share is an inference. [S-PS-2]
- Brier (1950): content not read. AMS page returned HTTP 403. Access needed: https://doi.org/10.1175/1520-0493(1950)078<0001:VOFEIT>2.0.CO;2
- Brier (1950): the "original score is twice the binary score" claim is from a search snippet only. [LOW-CONFIDENCE] [S-PS-10]
- Page and Clemen (2013): data, counts and method not read. Wiley returned HTTP 403. Access needed: https://doi.org/10.1111/j.1468-0297.2012.02561.x
- Snowberg and Wolfers (2010): numbers are from NBER WP 15923. The JPE print and its DOI were not checked.
- Snowberg and Wolfers (2010): our bib prints "Favorite-Long Shot", NBER prints "Favorite-Longshot". JPE wording not checked.
- Clauset et al. (2009): x_min selection rule verified in the full PDF (minimize D), 2026-11-08.
- Gneiting and Raftery (2007): case-study data counts unknown. Only page 1 read.
- DuckDB (2019): page range 1981 to 1984 is from our bib. The PDF does not print it.
