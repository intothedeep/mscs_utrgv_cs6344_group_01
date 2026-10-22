# When Polymarket Says 70%, Does It Happen 70% of the Time?

**Group 1 | Team Brier**: Taek Lim, Zhugang Liu (Tony), Francisco Cortez
CS 6344 Introduction to Data Science, UTRGV

Do Polymarket prices behave like real probabilities? Who does the trading? What does the trading data look like? We answer these questions with statistics on Polymarket-v1: about 1.2 billion trades across 1.3 million markets, 2022–2026.

## Research questions

| | Question | MVP |
|---|---|---|
| Q1 | Is the crowd right? Do events priced at *p* happen with frequency *p*? | MVP1 |
| Q2 | Who is the crowd? Do a few wallets do most of the trading? | MVP1 |
| Q3 | What does the data look like? Trade sizes, wallet activity, prices | MVP1 |
| Q1a | Does accuracy depend on the topic? | MVP2 |
| Q1b | Does the market get smarter near the deadline? | MVP2 |
| Q1c | Are busier markets more accurate? | MVP2 |

MVP1 is due at the end of Week 2. MVP2 starts only if MVP1 passes the gate described in the plan.

## Where things are

| File | What it is |
|---|---|
| `proposal_md/polymarket_proposal_v3.md` | **Current class post** (short proposal) |
| `tips/polymarket_plan_detailed.md` | **Current plan**: MVP1, gate, MVP2, timeline, risks |
| `docs/lecture_concept_map.md` | Lecture decks mapped to each question (section 6 = MVP1, section 7 = MVP2) |
| `polymarket_v1_paper.pdf` | Dataset paper (Qin & Yang, 2026) |
| `archive/` | Earlier proposal drafts, kept for reference |

## Data

- Dataset: https://huggingface.co/datasets/TimeSeventeen/Polymarket-v1
- Paper: https://arxiv.org/abs/2606.04217

## Tools

Python (pandas, NumPy, SciPy, statsmodels, scikit-learn, matplotlib) and DuckDB.

## Course assignment: proposal thread

One member of each team creates a thread with:

- Group number and team name
- Working title
- Brief description of the idea
- Description of the dataset
- Main question, hypothesis, problem, or objective
- Methods, tools, or approaches being considered

Each student responds to at least 4 classmates' threads. Responses cover what is interesting or promising about the idea, and suggestions for improvement or clarification.
