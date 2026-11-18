# Prediction-market size: Kalshi and Polymarket vs US peers

- Purpose: sourced numbers for one slide on prediction-market size.
- Compiled: 2026-11-17. Source ID tag: `MS`.
- Flag enum: `self-reported` / `third-party estimate` / `audited filing`.
- Verification enum: `verified` / `partial` / `unverifiable`.
- Rule: volume rows and revenue rows sit in separate tables. Never pair one firm's volume with another firm's revenue.
- Budget: pass 1 used the skill default of 15 web calls. Pass 2 (coordinator) used 30, counting 2 searches rejected with API 400 and failed fetches. Both budgets were reached. Rows marked `not collected (budget)` need a re-dispatch.
- Fetch access (2026-11-17): sec.gov, cftc.gov, cnbc.com, fool.com and q4cdn.com served pages. theblock.co, covers.com, casino.org, thedefiant.io, kalshi.com, help.kalshi.com reset the connection. americangaming.org, forbes.com, legalsportsreport.com returned HTTP 403. reuters.com is blocked for search.
- Volume caveat [UNVERIFIED]: per search summaries only, prediction-market volume may count both sides of a trade (Paradigm, Dec 2025), and sportsbook handle counts each bet once. Compare scale, not exact ratios.
- No figure in this file comes from an audited filing. Earnings releases are unaudited. The flag enum has no value for regulator records, so those rows use `self-reported`.
- `[UNVERIFIED]` rows come from search-result summaries only. Nobody read the claim in place. Do not put them on a slide yet.

## 1. Volume (amount traded or bet)

| ID | Entity | Metric | Value | Unit | Period | As of | Flag | Verification | Source | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V1 | DraftKings | Sportsbook handle (amount bet), up 11% YoY | 54 | USD billions | FY2025 | 2026-02-12 | self-reported | partial | [S-MS-2] | CFO Alan Ellingson on the Q4 2025 call. Not printed in the 8-K release [S-MS-1] |
| V2 | DraftKings | Sportsbook handle | 53.6 | USD billions | FY2025 | unknown | third-party estimate | unverifiable | none | [UNVERIFIED] search summary, link not identified. Differs from V1 by rounding or source |
| V3 | Kalshi | Notional trading volume, up 1,108% YoY | 23.8 | USD billions | CY2025 | 2026-01 | self-reported | unverifiable | [S-MS-6] | [UNVERIFIED] search summary only. Attributed to the KalshiData account. Other summaries say 24.2 and 22.88 |
| V4 | Polymarket | Nominal on-chain trading volume | 21.5 | USD billions | Jan to Nov 2025 | 2025-12-16 | third-party estimate | unverifiable | [S-MS-7], [S-MS-13] | [UNVERIFIED] search summary only. Keyrock and Dune report. Paradigm (Dec 2025) says trackers may double count both sides of a trade. Do not chart next to V3: different period and source |
| V5 | Kalshi | Trading volume | 17.1 | USD billions | Jan to Nov 2025 | 2025-12-16 | third-party estimate | unverifiable | [S-MS-7], [S-MS-13] | [UNVERIFIED] search summary only. Partial year, so not a conflict with V3 (full year) |
| V9 | Polymarket | Trading volume (Dune-based) | about 22.5 | USD billions | CY2025 | 2026-01 | third-party estimate | unverifiable | none | [UNVERIFIED] search summary, link not identified. DefiLlama DEX-only figure is about 10.5 per the same summary |
| V10 | Kalshi and Polymarket combined | Trading volume, above 44 | above 44 | USD billions | CY2025 | 2025-12-31 | third-party estimate | unverifiable | [S-MS-14] | [UNVERIFIED] The Block year-end article. Fetch failed (connection reset) |
| V11 | All prediction markets | Trading volume | 50.25 | USD billions | CY2025 | 2026-01 | third-party estimate | unverifiable | none | [UNVERIFIED] PredictionIndex.xyz via aggregator summary, link not identified |
| V6 | US legal sports betting (all operators) | Total handle, up 11% YoY | 166.94 | USD billions | CY2025 | 2026-02 | third-party estimate | unverifiable | [S-MS-8] | [UNVERIFIED] search summary only. The AGA page returned HTTP 403 |
| V7 | FanDuel (Flutter US) | US sportsbook handle, up 3% | 16,864 | USD millions | Q4 2025 only | 2026-02-26 | self-reported | verified | [S-MS-16] | Q4 2024: 16,379. Full release read (both parts): no full-year US handle printed. Do not chart against full-year rows |
| V8 | Kalshi, Polymarket | Volume 2024 | not collected (budget) | | | | | unverifiable | none | |
| V12 | All prediction markets | Total trading volume | 51 | USD billions | CY2025 | 2026-04-14 | third-party estimate | partial | [S-MS-17] | Bernstein (analyst Gautam Chhugani) via CNBC, read in place. No per-platform split. No double-counting caveat stated |
| V13 | Kalshi and Polymarket combined | Trading volume, year to date | about 60 | USD billions | 2026 YTD to mid-April | 2026-04-14 | third-party estimate | partial | [S-MS-17] | Bernstein via CNBC. No per-platform split |

## 2. Revenue and fees

| ID | Entity | Metric | Value | Unit | Period | As of | Flag | Verification | Source | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R1 | DraftKings | Total revenue (all products, not sportsbook only) | 6,054.5 | USD millions | FY2025 | 2026-02-12 | self-reported | verified | [S-MS-1] | SEC 8-K Ex. 99.1 earnings release, unaudited. Printed as 6,054,525 (thousands) |
| R2 | DraftKings | Total revenue | 4,767.7 | USD millions | FY2024 | 2026-02-12 | self-reported | verified | [S-MS-1] | Printed as 4,767,699 (thousands) |
| R3 | FanDuel (Flutter US) | US total revenue (sportsbook and iGaming), up 20% | 6.97 | USD billions | FY2025 | 2026-02-26 | self-reported | verified | [S-MS-16], [S-MS-9] | Printed in the guidance table as "US total revenue $6.97bn". FY2024 not printed. Sportsbook-only full-year revenue not printed |
| R3b | FanDuel (Flutter US) | US sportsbook revenue, up 35% | 1,497 | USD millions | Q4 2025 only | 2026-02-26 | self-reported | verified | [S-MS-16] | Q4 2024: 1,106 |
| R3c | Flutter (group) | Group revenue, up 17% | 16,383 | USD millions | FY2025 | 2026-02-26 | self-reported | verified | [S-MS-16] | FY2024: 14,048. Includes non-US |
| R4 | US legal sports betting (all operators) | Sports betting revenue | 16.96 (+22.8%); other summary: 16.89 (+22.6%) | USD billions | CY2025 | 2026-02 | third-party estimate | unverifiable | [S-MS-8], [S-MS-15] | [UNVERIFIED] [CONFLICT] two values in search summaries. AGA page HTTP 403. Not resolved |
| R5 | Kalshi | Non-sports annualized revenue run rate above 1 billion | above 1 | USD billions | run rate, 2026-10 | 2026-10-29 | self-reported | unverifiable | [S-MS-10] | [UNVERIFIED] search summary only. Run rate, not a reported annual figure. CNBC [S-MS-3] gave no revenue figure |
| R6 | Polymarket | Revenue or fees | not collected (budget) | | | | | unverifiable | none | |
| R8 | Robinhood | Prediction markets hub, annual recurring revenue | 350 | USD millions | run rate, 2026-04 | 2026-04-14 | third-party estimate | partial | [S-MS-17] | Per Bernstein via CNBC. Hub runs on Kalshi and is said to be about 30% of Kalshi volume. Run rate, not a reported annual figure |
| R7 | CME Group or Robinhood | Revenue | not collected (budget) | | | | | unverifiable | none | Optional row |

## 3. Valuation, regulation, fee model

| ID | Entity | Fact | As of | Flag | Verification | Source | Note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| F1 | Kalshi | Valuation USD 40 billion after a USD 1 billion round co-led by Sequoia Capital and Wellington Management. Prior round (May 2026): USD 22 billion | 2026-10-29 | self-reported | partial | [S-MS-3] | Company announcement as reported by CNBC. Read in place |
| F2 | Polymarket | ICE invested USD 1 billion (Oct 2025) and a further USD 600 million (2026-03-27), plus up to USD 40 million of secondary purchases | 2026-03-27 | self-reported | verified | [S-MS-4] | The release does not state the valuation of the 2026 tranche |
| F3 | Polymarket | Valuation about USD 9 billion post-money at the Oct 2025 ICE deal | 2025-10 | third-party estimate | unverifiable | none | [UNVERIFIED] search summary, link not identified |
| F4 | Polymarket | Reported talks to raise about USD 1 billion at about USD 21 billion post-money. Whether the round closed is disputed | 2026-09 to 2026-10 | third-party estimate | unverifiable | [S-MS-11] | [UNVERIFIED] [CONFLICT] a plan in talks, not an outcome. One summary says closed (Sep 2026). Another, link not identified, says still in talks in Oct 2026 |
| F5 | DraftKings | Runs DraftKings Predictions, a standalone app offering CFTC-regulated event contracts | 2026-02-12 | self-reported | verified | [S-MS-1] | Sportsbooks now enter the same market |
| F6 | Kalshi | [2020] CFTC "issued an Order of Designation to KalshiEX LLC, granting it status as a designated contract market (DCM)" | 2020-11-04 | self-reported | partial | [S-MS-21] | Regulator press release. Out of window; current status not re-read. Enum has no value for regulator records |
| F6b | Kalshi | Massachusetts won an injunction temporarily banning Kalshi from sports-related contracts there | 2026-02-14 | third-party estimate | partial | [S-MS-23] | CNBC, read in place |
| F7 | Polymarket | US entity "QCX LLC d/b/a Polymarket US" is a CFTC Designated Contract Market (DCM), designated 2025-07-09, status "Designated" | 2026-11-17 | self-reported | verified | [S-MS-18] | Regulator registry page, read live. Enum has no value for regulator records |
| F7b | Polymarket | Closed the QCX acquisition after CFTC staff gave a no-action position on event-contract swap data reporting. CEO said Polymarket had the "green light to go live in the USA". CFTC and DOJ had ended probes in July 2025 without charges | 2025-09-03 | self-reported | partial | [S-MS-19] | CNBC, read in place. Price not stated in the text (URL slug says 112 million, not confirmed) |
| F7c | Polymarket | US exchange launched in December 2025. CFTC investigation reported ongoing (per a source) | 2026-06-26 | third-party estimate | unverifiable | [S-MS-20] | [UNVERIFIED] CNBC search summary only |
| F8 | Kalshi | [2022] Fee schedule (2nd iteration, 2022-09-22): "fees = round up(0.07 x C x P x (1-P))", P = contract price in dollars, C = contracts. Charged only on orders that match immediately; resting orders pay no trading fee. No settlement fee. USD 2 per withdrawal. Table: USD 1.75 fee on 100 contracts at USD 0.50. S&P 500 and Nasdaq-100 markets use 0.035 | 2022-09-22 | self-reported | partial | [S-MS-28] | Read in place (filed on cftc.gov). Out of window: current schedule on kalshi.com reset the connection. Current maker fee (0.0175 on listed series) is [UNVERIFIED], search summary only [S-MS-24] |
| F8b | Polymarket | Fee model | | | unverifiable | none | not collected (budget) |
| F8c | Platforms in general | "a small fee on each trade", no amount given | 2026-02-14 | third-party estimate | partial | [S-MS-23] | CNBC, read in place |
| F10 | Polymarket | Fined USD 1.4 million by the CFTC in 2022 for operating an unregistered derivatives market. Forced to block US users. Later acquired QCEX and got US federal approval in November (2025). Relaunched US app in beta, waitlist rollout | 2026-02-14 | third-party estimate | partial | [S-MS-23] | CNBC, read in place |
| F11 | Polymarket | Settles in USDC (international exchange) | | | unverifiable | [S-MS-25] | [UNVERIFIED] only a Bloomberg headline ("USDC: Polymarket Election Bets...") seen. Not read in place |
| F9 | Kalshi | Legal pressure: Utah attorney general filed criminal charges against Kalshi and executives | 2026-10 | third-party estimate | unverifiable | none | [UNVERIFIED] search summary, link not identified |

## 4. Explainer facts

| ID | Fact | Verification | Source |
| --- | --- | --- | --- |
| E1 | DraftKings Predictions hit 3x its prior daily trading-volume record on Super Bowl Sunday 2026 (CEO Jason Robins). No dollar figure given | partial | [S-MS-2] |
| E2 | Contract price ranges "between $0 and $1". At settlement winning contracts went to "$1 per share", losing ones to "$0" (Super Bowl LX example: Patriots contracts "went to $0") | partial | [S-MS-23] |
| E3 | Kalshi vs Polymarket regulation: see F6, F7, F10. Currency: see E7 (Kalshi USD) and F11 (Polymarket USDC, [UNVERIFIED]) | partial | [S-MS-21], [S-MS-18], [S-MS-23] |
| E4 | Kalshi Super Bowl LX (2026-02-08) game day: "more than $1 billion in trading volume", a daily record, up 2,700% YoY. Company-stated (CEO Tarek Mansour on CNBC). Bad Bunny opening-song market above USD 100 million | partial | [S-MS-22]. Company claim; the Bank of America estimate in E5 is lower and unread |
| E5 | Kalshi and Polymarket combined about USD 1.2 billion on Super Bowl Sunday (Piper Sandler). Bank of America: Kalshi USD 871 million that Sunday | unverifiable | [S-MS-26]. [UNVERIFIED] search summary only. The $871 million (BofA) and ">$1 billion" (Kalshi) differ by source; not read in place |
| E6 | [2024] Polymarket 2024 US presidential race betting: "nearly $3.7 billion, according to the platform's tracker". Platform then "only available to customers outside of the United States" | partial | [S-MS-27]. Read in place. Self-reported count. An NBC News analysis (above USD 3.6 billion) is [UNVERIFIED], search summary only |
| E7 | Kalshi trades in US dollars (bank ACH deposits, USD 2 bank withdrawal fee) | partial | [S-MS-28]. [2022] fee schedule implies USD accounts. No current page read |
| E8 | Who can use it: Kalshi US users; Polymarket international vs US app eligibility, age limits | unverifiable | not collected (budget). Only partial: Polymarket US app in beta, waitlist (F10) |

## 5. Ready-to-plot table

Only `verified` or `partial` rows. Unit conversion only. No sums, no derived values.

| Name | Metric | USD billions | Year | Source ID |
| --- | --- | --- | --- | --- |
| DraftKings | volume (sportsbook handle) | 54 | 2025 | S-MS-2 |
| DraftKings | revenue (total company) | 6.05 | 2025 | S-MS-1 |
| DraftKings | revenue (total company) | 4.77 | 2024 | S-MS-1 |
| FanDuel (Flutter US) | revenue (US total, sportsbook and iGaming) | 6.97 | 2025 | S-MS-16 |
| All prediction markets (Bernstein estimate) | volume | 51 | 2025 | S-MS-17 |
| Kalshi and Polymarket combined (Bernstein estimate) | volume | about 60 | 2026 YTD to 2026-04-14 | S-MS-17 |

Read before plotting:
- The two prediction-market rows are third-party estimates. CNBC prints "volume" with no definition. They may count both sides of a trade ([UNVERIFIED] caveat).
- No per-platform 2025 volume for Kalshi or Polymarket was read in place. Bernstein's 51 is the only readable 2025 prediction-market number.
- The 2026 row covers only about 3.5 months. Label it as year to date.
- The DraftKings and FanDuel revenue rows include iGaming and other products, not sportsbook only.

Pending (not plottable until verified):
- Kalshi volume 2025 (V3 23.8, V5 17.1 Jan to Nov), Polymarket volume 2025 (V4 21.5 Jan to Nov, V9 about 22.5).
- US total handle (V6 166.94) and US sports betting revenue (R4 16.96 or 16.89).
- FanDuel full-year handle: not in the Flutter Q4 release (read in full). Only Q4 2025 (V7, 16.86) is verified.
- Kalshi revenue (R5 run rate), Polymarket revenue (R6), Robinhood hub run rate (R8 0.35, partial but a run rate).

## 6. Selection log

| Candidate source | Kept or rejected | Reason |
| --- | --- | --- |
| DraftKings 8-K Ex. 99.1 (SEC) | kept | first-party filing. Revenue read in place. No handle in it |
| Motley Fool Q4 2025 call transcript | kept | handle stated by the CFO, read in place |
| CNBC 2026-10-29 Kalshi round | kept | read in place. No revenue or volume figures |
| ICE release 2026-03-27 (PDF) | kept | first-party, read in place |
| AGA 2025 commercial gaming release | rejected as a read source | HTTP 403. Numbers held as [UNVERIFIED] from the search summary |
| Forbes 2025-12-16 (Keyrock and Dune volumes) | rejected as a read source | HTTP 403. Numbers held as [UNVERIFIED] from the search summary |
| Investegate Flutter FY2025 page | rejected | AI summary only, no release body. Rule: source hierarchy (aggregator restating) |
| KuCoin, Phemex, ChainCatcher, RootData Kalshi 2025 pages | rejected as a read source | aggregators restating the KalshiData post. Rule: follow to the original |
| X post (24.2B Kalshi) | rejected | anecdotal social post |
| KuCoin "2025 Prediction Market Review": Polymarket 220 to 250 billion | rejected | aggregator, about 10x every other source |
| "Kalshi CFO" quote on Robinhood share of volume | rejected | attribution garbled in the summary (Kalshi is private, no earnings call) |
| The Block, covers.com, casino.org, thedefiant.io, legalsportsreport.com, kalshi.com, help.kalshi.com | not read | fetch failed (connection reset or HTTP 403), 2026-11-17 |
| tsginvest, polycopy, startpolymarket, shattered.io | rejected | low-confidence aggregator or promotional pages |
| Flutter Q4 FY2025 Ex. 99.1 (SEC) | kept | first-party, read in place (first 100,000 characters) |
| CNBC Bernstein 2026-04-14 | kept | read in place |
| CFTC DCM registry (QCX LLC d/b/a Polymarket US) | kept | regulator page, read in place |
| CFTC press release 8302-20 (KalshiEX DCM) | kept | regulator page, read in place |
| CNBC 2025-09-03 Polymarket US launch | kept | read in place |
| CNBC 2026-02-10 Kalshi Super Bowl | kept | read in place |
| CNBC 2026-02-14 how prediction markets work | kept | read in place |
| CNBC 2024-11-07 Polymarket election article | kept | read in place |
| Kalshi fee schedule 2022 (cftc.gov PDF) | kept | first-party, read in place. [2022] out of window |
| Bloomberg Super Bowl and election articles | not read | budget reached. Values held as [UNVERIFIED] |

## Summary counts

- kept: 13
- rejected or not read: 10
- sources: 28
- unverified: 21

open_questions:

- V3, V4, V5, V9: Kalshi and Polymarket 2025 volume, search summaries only. V5 and V4 are Jan to Nov, V3 is full year. Next: Dune dashboard or Kalshi's own post, read in place.
- V4: Polymarket volume may be double counted (Paradigm, Dec 2025).
- V2: DraftKings 53.6 vs 54 (V1). Rounding or source; link not identified.
- V6, R4: AGA 2025 handle and revenue. AGA site returned 403. R4 [CONFLICT]: 16.96 vs 16.89. Next: AGA PDF via another host.
- V7: FanDuel full-year 2025 US handle. Not printed in the Flutter Q4 release (read in full). Next: the Flutter 10-K.
- F6, F8, E7: Kalshi DCM status, fee formula and USD accounts read only from 2020 and 2022 documents. Re-read current pages.
- V8, V10, V11: 2024 per-platform volume, combined 2025, PredictionIndex total.
- R5, R6, R7: Kalshi and Polymarket revenue, CME or Robinhood revenue.
- F3, F4: Polymarket valuations. F4 [CONFLICT]: closed round vs talks.
- F7c: Polymarket US launch date and CFTC investigation.
- F8b: Polymarket fee model not collected. Kalshi current maker fee [UNVERIFIED].
- F9: Utah charges against Kalshi.
- F11: Polymarket USDC settlement.
- E5: Super Bowl combined volume (Piper Sandler 1.2) and BofA Kalshi estimate (0.871).
- E6: NBC News 2024 election figure (above 3.6) unread; Polymarket tracker figure (nearly 3.7) read.
- E8: who can use each platform.

## Sources

[S-MS-1] DraftKings Inc. Form 8-K Exhibit 99.1: Q4 and fiscal year 2025 results | https://www.sec.gov/Archives/edgar/data/1883685/000188368526000011/q425-prx8kexx991.htm | published: 2026-02-12 | accessed: 2026-11-17 | type: official | note: full text read; revenue table and About section
[S-MS-2] DraftKings (DKNG) Q4 2025 Earnings Call Transcript | https://www.fool.com/earnings/call-transcripts/2026/02/13/draftkings-dkng-q4-2025-earnings-call-transcript | published: 2026-02-13 | accessed: 2026-11-17 | type: news | note: transcript read in place
[S-MS-3] Kalshi valuation jumps to $40 billion in latest funding round | https://www.cnbc.com/2026/10/29/kalshi-40-billion-valuation-funding-round.html | published: 2026-10-29 | accessed: 2026-11-17 | type: news | note: full text read
[S-MS-4] Intercontinental Exchange Announces New $600 Million Investment in Polymarket | https://s2.q4cdn.com/154085107/files/doc_news/Intercontinental-Exchange-Announces-New-600-Million-Investment-in-Polymarket-2026.pdf | published: 2026-03-27 | accessed: 2026-11-17 | type: official | note: PDF text read via fetch, not saved to the repo
[S-MS-5] DraftKings Delivers Super FY25 Fiscals, Predicts New Year Boom | https://igamingfuture.com/draftkings-delivers-super-fy25-fiscals-predicts-new-year-boom/ | published: 2026-02 | accessed: 2026-11-17 | type: news | note: search summary only
[S-MS-6] KalshiData: In 2025, Kalshi's trading volume reached $23.8 billion, a year-on-year increase of 1108% | https://www.chaincatcher.com/en/article/2234568 | published: 2026-01 | accessed: 2026-11-17 | type: aggregator | note: search summary only
[S-MS-7] How Prediction Markets Actually Grew In 2025 | https://www.forbes.com/sites/boazsobrado/2025/12/16/how-prediction-markets-actually-grew-in-2025/ | published: 2025-12-16 | accessed: 2026-11-17 | type: news | note: HTTP 403 on fetch (2026-11-17); search summary only
[S-MS-8] Commercial Gaming Revenue Hits $78.7 Billion in 2025, Driving Record $18.1 Billion in Gaming Taxes Nationwide | https://americangaming.org/commercial-gaming-revenue-hits-78-7-billion-in-2025-driving-record-18-1-billion-in-gaming-taxes-nationwide/ | published: 2026-02 | accessed: 2026-11-17 | type: official | note: HTTP 403; figures from search summary only (sportsbettingdime restatement)
[S-MS-9] US growth steadies Flutter after India shutdown dents FY25 | https://igamingbusiness.com/finance/full-year-results/us-growth-steadies-flutter-after-india-shutdown-dents-fy25/ | published: 2026-02 | accessed: 2026-11-17 | type: news | note: search summary only
[S-MS-10] Kalshi Valuation Jumps to $40B after Latest Funding Round | https://cointelegraph.com/news/kalshi-closes-1b-funding-round-at-40b-valuation-as-non-sports-revenue-run-rate-tops-1b | published: 2026-10 | accessed: 2026-11-17 | type: news | note: search summary only
[S-MS-11] Polymarket Funding Round Valued at $21 Billion | https://en.cryptonomist.ch/2026/09/01/polymarket-funding-round/ | published: 2026-09-01 | accessed: 2026-11-17 | type: news | note: search summary only
[S-MS-12] NYSE parent may invest again in Polymarket as valuation crosses $20B: report | https://crypto.news/nyse-parent-may-invest-again-in-polymarket-as-valuation-crosses-20b-report/ | published: 2026-10 | accessed: 2026-11-17 | type: news | note: search summary only
[S-MS-16] Flutter Entertainment Q4 and fiscal year 2025 results (Exhibit 99.1) | https://www.sec.gov/Archives/edgar/data/1635327/000119312526076569/d763070dex991.htm | published: 2026-02-26 | accessed: 2026-11-17 | type: official | note: first 100,000 characters read via fetch
[S-MS-17] Prediction markets will grow to $1 trillion by 2030, Bernstein estimates | https://www.cnbc.com/2026/04/14/prediction-markets-will-grow-to-1-trillion-by-2030-bernstein-says.html | published: 2026-04-14 | accessed: 2026-11-17 | type: news | note: full text read
[S-MS-18] Industry Filings: Designated Contract Markets (DCM), QCX LLC d/b/a Polymarket US | https://www.cftc.gov/IndustryOversight/IndustryFilings/TradingOrganizations/49571 | published: registry page | accessed: 2026-11-17 | type: gov | note: page read in place
[S-MS-19] Polymarket set for U.S. launch after getting green light from CFTC, CEO says | https://www.cnbc.com/2025/09/03/polymarket-set-for-us-launch-after-getting-green-light-from-cftc-ceo-says.html | published: 2025-09-03 | accessed: 2026-11-17 | type: news | note: full text read
[S-MS-20] CFTC is conducting an investigation into Polymarket, source says | https://www.cnbc.com/2026/06/26/cftc-is-conducting-an-investigation-into-polymarket-source-says.html | published: 2026-06-26 | accessed: 2026-11-17 | type: news | note: search summary only
[S-MS-21] CFTC Designates KalshiEX LLC as a Contract Market | https://www.cftc.gov/PressRoom/PressReleases/8302-20 | published: 2020-11-04 | accessed: 2026-11-17 | type: gov | note: full text read
[S-MS-22] Kalshi says Super Bowl trading volume surpassed $1 billion | https://www.cnbc.com/2026/02/10/kalshi-super-bowl.html | published: 2026-02-10 | accessed: 2026-11-17 | type: news | note: full text read
[S-MS-23] Polymarket is back in the U.S. with a free grocery store: what to know about it and other prediction markets | https://www.cnbc.com/2026/02/14/how-prediction-markets-work.html | published: 2026-02-14 | accessed: 2026-11-17 | type: news | note: full text read
[S-MS-28] Kalshi Fee Schedule: 2nd Iteration | https://cftc.gov/filings/orgrules/rule091222kexdcm003.pdf | published: 2022-09-22 | accessed: 2026-11-18 | type: official | note: PDF text read via fetch, not saved to the repo
[S-MS-24] Kalshi fee schedule | https://kalshi.com/docs/kalshi-fee-schedule.pdf | published: unknown | accessed: 2026-11-17 | type: official | note: fetch failed (connection reset); search summary only
[S-MS-25] Polymarket Election Bets Surge Toward $1 Billion Despite Bans | https://www.bloomberg.com/news/articles/2024-08-01/polymarket-rides-election-betting-frenzy-that-defies-a-us-ban | published: 2024-08-01 | accessed: 2026-11-17 | type: news | note: headline in search results only
[S-MS-26] Super Bowl Gives Prediction Bets Record $1.2 Billion Trading Day | https://www.bloomberg.com/news/articles/2026-02-10/super-bowl-gives-prediction-bets-record-1-2-billion-trading-day | published: 2026-02-10 | accessed: 2026-11-17 | type: news | note: search summary only
[S-MS-27] Polymarket plans U.S. return after signaling Trump election win, founder says | https://www.cnbc.com/2024/11/07/polymarket-plans-to-return-to-the-us-founder-says-.html | published: 2024-11-07 | accessed: 2026-11-18 | type: news | note: full text read
[S-MS-13] Prediction market 2025 growth report (Keyrock and Dune) | https://thedefiant.io/news/research-and-opinion/prediction-market-2025-growth-report-keyrock-dune | published: 2025-12 | accessed: 2026-11-17 | type: news | note: fetch failed (connection reset); search summary only
[S-MS-14] Prediction markets explode in 2025: Inside the Kalshi-Polymarket duopoly and challengers | https://www.theblock.co/post/383733/prediction-markets-kalshi-polymarket-duopoly-2025 | published: 2025-12-31 | accessed: 2026-11-17 | type: news | note: fetch failed (connection reset); search summary only
[S-MS-15] Sportsbooks Make More Money From Slower Betting Growth In 2025 | https://www.legalsportsreport.com/263300/sportsbooks-make-more-money-from-slower-sports-betting-growth-in-2025/ | published: 2026 | accessed: 2026-11-17 | type: news | note: HTTP 403; search summary only
