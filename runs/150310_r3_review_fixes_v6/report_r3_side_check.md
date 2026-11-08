# Stage report: r3_side_check

**What:** Check the side columns before M1.

**Why:** M1 maps (taker_direction, outcome_seq) to the aggressor side on the outcome 1 scale. The mapping needs BUY and SELL.

**Input data:** Raw trades (data/polymarket_v1/daily_aligned/*.parquet), 601934424 trades with outcome_seq 1 or 2. Real data.

**Output data:** r3_side_crosstab.csv, r3_side_check.json

**Result:** taker_direction values ['BUY', 'SELL']. D values [-1, 1] (meaning not documented, not tested). p_event equals price or 1 - price in 1.000000 of trades.

| taker_direction | outcome_seq | D | n | n_p_event_consistent |
| --- | --- | --- | --- | --- |
| BUY | 1 | 1 | 40610027 | 4.061e+07 |
| BUY | 2 | -1 | 41669117 | 4.167e+07 |
| SELL | 1 | -1 | 260565063 | 2.606e+08 |
| SELL | 2 | 1 | 259090217 | 2.591e+08 |

**Status:** ran
