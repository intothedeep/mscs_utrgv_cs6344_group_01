# Related work references for paper_mvp1 (2026-11-07)

- Purpose: add 6-10 verified references to the related work of `papers/paper_mvp1/main.tex`.
- Dedup: `papers/paper_mvp1/references.bib` already holds Snowberg and Wolfers (2010) and Brier (1950). They are not repeated here.
- Tag: `RW`. Source IDs follow `[S-RW-n]`. Sources for each entry sit in its block and repeat in the Sources section.
- Verification enum: `verified` (first-party page or the paper itself read), `partial` (secondary page read, or metadata only), `unverifiable`.
- This file is a research output. It does not edit the paper or `references.bib`.

## Summary

- kept: 8
- rejected: 6
- sources: 11
- unverified: 0 (4 partial)

| # | key | supports | verification |
| --- | --- | --- | --- |
| R1 | gneiting2007strictly | scoring rules | verified |
| R2 | wolfers2004prediction | Q1 calibration | verified |
| R3 | clauset2009power | Q3 power-law fitting | verified |
| R4 | le2026decomposing | Q1 calibration | verified |
| R5 | page2013prediction | Q1 calibration, longshot bias | partial |
| R6 | murphy1973new | scoring rules | partial |
| R7 | gomezcram2026prediction | Q2 concentration | partial |
| R8 | sirolly2025network | Q2 concentration | partial |

## References

One block per reference. Each block was appended after it was checked.

### R1. gneiting2007strictly

- Citation: Gneiting, T., and Raftery, A. E. (2007). Strictly proper scoring rules, prediction, and estimation. *Journal of the American Statistical Association*, 102(477), 359-378. https://doi.org/10.1198/016214506000001437
- Finding: The paper states that the goal of probabilistic forecasting is "to maximize the sharpness of the predictive distributions subject to calibration", and it lists the Brier score among proper scoring rules (keywords and introduction, p. 359). [S-RW-1]
- Supports: scoring rules.
- Verification: `verified`. Page 1 of the paper PDF read (title, abstract, keywords, introduction). Citation fields match Crossref. [S-RW-1] [S-RW-2]

```bibtex
@article{gneiting2007strictly,
  author  = {Gneiting, Tilmann and Raftery, Adrian E.},
  title   = {Strictly Proper Scoring Rules, Prediction, and Estimation},
  journal = {Journal of the American Statistical Association},
  volume  = {102},
  number  = {477},
  pages   = {359--378},
  year    = {2007},
  doi     = {10.1198/016214506000001437}
}
```

### R2. wolfers2004prediction

- Citation: Wolfers, J., and Zitzewitz, E. (2004). Prediction markets. *Journal of Economic Perspectives*, 18(2), 107-126. https://doi.org/10.1257/0895330041371321
- Finding: Across many settings, market-generated forecasts are typically fairly accurate and usually beat moderately sophisticated benchmarks (abstract). [S-RW-3]
- Supports: Q1 calibration (background on prediction-market accuracy).
- Verification: `verified`. Publisher (AEA) abstract page read. Free full-text PDF is linked there but was not opened. [S-RW-3]

```bibtex
@article{wolfers2004prediction,
  author  = {Wolfers, Justin and Zitzewitz, Eric},
  title   = {Prediction Markets},
  journal = {Journal of Economic Perspectives},
  volume  = {18},
  number  = {2},
  pages   = {107--126},
  year    = {2004},
  doi     = {10.1257/0895330041371321}
}
```

### R3. clauset2009power

- Citation: Clauset, A., Shalizi, C. R., and Newman, M. E. J. (2009). Power-law distributions in empirical data. *SIAM Review*, 51, 661-703. https://doi.org/10.1137/070710111 (preprint: arXiv:0706.1062)
- Finding: The paper fits power laws by maximum likelihood and tests them with Kolmogorov-Smirnov goodness-of-fit and likelihood-ratio tests against alternatives. Applied to 24 real datasets, the power law fits some and is ruled out for others (abstract). [S-RW-4]
- Supports: Q3 power-law fitting.
- Verification: `verified`. arXiv abstract page read, journal reference and DOI taken from it. Issue number not shown there, so it is left out of the BibTeX. [S-RW-4]

```bibtex
@article{clauset2009power,
  author  = {Clauset, Aaron and Shalizi, Cosma Rohilla and Newman, M. E. J.},
  title   = {Power-Law Distributions in Empirical Data},
  journal = {SIAM Review},
  volume  = {51},
  pages   = {661--703},
  year    = {2009},
  doi     = {10.1137/070710111},
  eprint  = {0706.1062},
  archivePrefix = {arXiv}
}
```

### R4. le2026decomposing

- Citation: Le, N. A. (2026). Decomposing crowd wisdom: Domain-specific calibration dynamics in prediction markets. arXiv:2602.19520 [stat.AP], v2 (2026-08-04). https://doi.org/10.48550/arXiv.2602.19520
- Finding: Using 353 million trades on 429,000 binary contracts from Kalshi and Polymarket, calibration varies by event domain, time to resolution and trade size. Political markets show persistent underconfidence (prices compressed toward 50%), and this replicates on Polymarket (abstract, v2). [S-RW-5]
- Supports: Q1 calibration (Polymarket, recent).
- Verification: `verified`. arXiv abstract page read. Preprint, not peer reviewed. Version note: v1 (2026-02-23) reported 292 million trades on 327,000 contracts per a search snippet. Cite v2 numbers. [S-RW-5]

```bibtex
@misc{le2026decomposing,
  author        = {Le, Nam Anh},
  title         = {Decomposing Crowd Wisdom: Domain-Specific Calibration Dynamics in Prediction Markets},
  year          = {2026},
  eprint        = {2602.19520},
  archivePrefix = {arXiv},
  primaryClass  = {stat.AP},
  doi           = {10.48550/arXiv.2602.19520},
  url           = {https://arxiv.org/abs/2602.19520},
  note          = {Version 2, 4 August 2026}
}
```

### R5. page2013prediction

- Citation: Page, L., and Clemen, R. T. (2013). Do prediction markets produce well-calibrated probability forecasts? *The Economic Journal*, 123(568), 491-513. https://doi.org/10.1111/j.1468-0297.2012.02561.x
- Finding: Prediction markets "are reasonably well calibrated when time to expiration is relatively short", but "prices are significantly biased for events farther in the future", with a favourite/longshot bias in which low-likelihood events are over-priced (abstract). [S-RW-6]
- Supports: Q1 calibration and longshot bias.
- Verification: `partial`. Abstract read on the author's institutional repository (Duke Scholars). Publisher page not opened. [S-RW-6]

```bibtex
@article{page2013prediction,
  author  = {Page, Lionel and Clemen, Robert T.},
  title   = {Do Prediction Markets Produce Well-Calibrated Probability Forecasts?},
  journal = {The Economic Journal},
  volume  = {123},
  number  = {568},
  pages   = {491--513},
  year    = {2013},
  doi     = {10.1111/j.1468-0297.2012.02561.x}
}
```

### R6. murphy1973new

- Citation: Murphy, A. H. (1973). A new vector partition of the probability score. *Journal of Applied Meteorology*, 12(4), 595-600. https://doi.org/10.1175/1520-0450(1973)012<0595:ANVPOT>2.0.CO;2
- Finding: The paper partitions the probability (Brier) score into three parts: the uncertainty of the events, the reliability of the forecasts, and a new resolution measure. [S-RW-8] [LOW-CONFIDENCE]
- Supports: scoring rules (Brier decomposition into reliability, resolution, uncertainty).
- BibTeX caution: the DOI contains `<` and `>`. A style that prints DOIs may break on them. When copying, drop `doi` or escape the brackets.
- Verification: `partial`. Citation fields from Crossref metadata [S-RW-7]. The finding comes from a search snippet only. The publisher (AMS) and Scilit pages returned HTTP 403. [S-RW-8]

```bibtex
@article{murphy1973new,
  author  = {Murphy, Allan H.},
  title   = {A New Vector Partition of the Probability Score},
  journal = {Journal of Applied Meteorology},
  volume  = {12},
  number  = {4},
  pages   = {595--600},
  year    = {1973},
  doi     = {10.1175/1520-0450(1973)012<0595:ANVPOT>2.0.CO;2}
}
```

### R7. gomezcram2026prediction

- Citation: Gómez-Cram, R., Guo, Y., Jensen, T. I., and Kung, H. (2026). Prediction market accuracy: Crowd wisdom or informed minority? Working paper, SSRN abstract 6617059. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6617059
- Finding: On two years of Polymarket data (1.72 million accounts, 210,322 markets, $13.76 billion volume), about 3% of accounts are skilled. Skilled traders plus market makers, "fewer than 3.5% of all accounts", capture "over 30% of total gains". [S-RW-9]
- Supports: Q2 concentration.
- Verification: `partial`. Yale School of Management Insights article (2026-06-10) read. SSRN page returned HTTP 403. Working paper, not peer reviewed. [S-RW-9]

```bibtex
@techreport{gomezcram2026prediction,
  author      = {G{\'o}mez-Cram, Roberto and Guo, Yunhan and Jensen, Theis Ingerslev and Kung, Howard},
  title       = {Prediction Market Accuracy: Crowd Wisdom or Informed Minority?},
  institution = {SSRN},
  type        = {Working paper},
  number      = {6617059},
  year        = {2026},
  url         = {https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6617059}
}
```

### R8. sirolly2025network

- Citation: Sirolly, A., Ma, H., Kanoria, Y., and Sethi, R. (2025). Network-based detection of wash trading. Working paper, SSRN abstract 5714122. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5714122
- Finding: A network method flags wallets that repeatedly close positions against each other. On Polymarket, a cluster of 200 wallets traded more than $113 million in volume almost only among themselves, for a total loss of $57.86. [S-RW-10]
- Supports: Q2 concentration (caveat: raw wallet volume can include wash trading).
- Verification: `partial`. Co-author Rajiv Sethi's post (2025-11-12) read. SSRN page not opened. The "about 25% of Polymarket volume" figure appears only in press snippets and is not recorded as a finding here. [S-RW-10] [S-RW-11] [LOW-CONFIDENCE]

```bibtex
@techreport{sirolly2025network,
  author      = {Sirolly, Allen and Ma, Hongyao and Kanoria, Yash and Sethi, Rajiv},
  title       = {Network-Based Detection of Wash Trading},
  institution = {SSRN},
  type        = {Working paper},
  number      = {5714122},
  year        = {2025},
  url         = {https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5714122}
}
```

## Selection log

- kept: gneiting2007strictly, wolfers2004prediction, clauset2009power, le2026decomposing, page2013prediction, murphy1973new, gomezcram2026prediction, sirolly2025network.
- rejected: snowberg2010favorite. Rule: dedup, already in `references.bib`.
- rejected: brier1950verification. Rule: dedup, already in `references.bib`.
- rejected: Akey, Grégoire, Harvie, Martineau (2026), "Who Wins and Who Loses In Prediction Markets? Evidence from Polymarket", SSRN. Rule: not opened (search snippet only, budget reached).
- rejected: Nechepurenko, arXiv 2605.02287 (critique of Gómez-Cram et al.). Rule: not opened (budget reached).
- rejected: Princeton senior thesis "The Price is (Almost) Right" (2026). Rule: not opened, and a thesis ranks below peer-reviewed or preprint work.
- rejected: LessWrong "Empirical calibration of Polymarket" post, Medium and dev.to posts. Rule: blog, below source rank (`anecdotal`).

## Sources

[S-RW-1] Strictly Proper Scoring Rules, Prediction, and Estimation | https://sites.stat.washington.edu/raftery/Research/PDF/Gneiting2007jasa.pdf | published: 2007-03 | accessed: 2026-11-07 | type: paper | note: PDF page 1 read
[S-RW-2] Crossref record 10.1198/016214506000001437 | https://api.crossref.org/works/10.1198/016214506000001437 | published: 2007 | accessed: 2026-11-07 | type: aggregator | note: metadata only
[S-RW-3] Prediction Markets | https://www.aeaweb.org/articles?id=10.1257/0895330041371321 | published: 2004 | accessed: 2026-11-07 | type: official | note: publisher abstract page
[S-RW-4] Power-law distributions in empirical data | https://arxiv.org/abs/0706.1062 | published: 2009-02-02 (v2) | accessed: 2026-11-07 | type: paper | note: arXiv abstract page
[S-RW-5] Decomposing Crowd Wisdom: Domain-Specific Calibration Dynamics in Prediction Markets | https://arxiv.org/abs/2602.19520 | published: 2026-08-04 (v2) | accessed: 2026-11-07 | type: paper | note: arXiv abstract page
[S-RW-6] Do Prediction Markets Produce Well-Calibrated Probability Forecasts? | https://scholars.duke.edu/publication/765630 | published: 2013-05 | accessed: 2026-11-07 | type: official | note: abstract on author institutional repository
[S-RW-7] Crossref record for Murphy (1973) | https://api.crossref.org/works/10.1175/1520-0450(1973)012%3C0595:ANVPOT%3E2.0.CO;2 | published: 1973 | accessed: 2026-11-07 | type: aggregator | note: metadata only, no abstract
[S-RW-8] A New Vector Partition of the Probability Score (Scilit listing) | https://scilit.com/publications/33f100f3485bed290b76f75810285843 | published: 1973 | accessed: 2026-11-07 | type: aggregator | note: search snippet only, page returned HTTP 403
[S-RW-9] Wisdom of the Few: Prediction Markets Are Driven by Small Number of Skilled Traders | https://insights.som.yale.edu/insights/wisdom-of-the-few-prediction-markets-are-driven-by-small-number-of-skilled-traders | published: 2026-06-10 | accessed: 2026-11-07 | type: official | note: institutional summary of the working paper
[S-RW-10] The Detection of Wash Trading | https://rajivsethi.substack.com/p/the-detection-of-wash-trading | published: 2025-11-12 | accessed: 2026-11-07 | type: blog | note: co-author post, full post read
[S-RW-11] Polymarket wash trading inflated volume (Fortune) | https://fortune.com/2025/11/07/polymarket-wash-trading-inflated-prediction-markets-columbia-research | published: 2025-11-07 | accessed: 2026-11-07 | type: news | note: search snippet only, not opened

open_questions:

- Murphy (1973): finding not read in the paper. AMS page `https://doi.org/10.1175/1520-0450(1973)012<0595:ANVPOT>2.0.CO;2` returned HTTP 403.
- Gómez-Cram et al. (2026): SSRN 6617059 returned HTTP 403. Author order differs: Yale page lists Gómez-Cram, Guo, Jensen, Kung; press lists Kung before Jensen. One press source gives the subtitle "Crowd Wisdom or Informed Traders?".
- Sirolly et al. (2025): SSRN 5714122 not opened. Title comes from search results and press, the co-author post does not name it. A 2026-01-17 version may exist. The 25% volume share is press-only.
- Page and Clemen (2013): publisher page not opened. Citation and abstract from Duke Scholars only.
