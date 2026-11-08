# Stage report: r3_build

**What:** Gate and raw pass for the robustness v3 items.

**Why:** Every v3 item reads the kept set and p_1d of the base run. The gate proves the rebuild equals it before any item runs.

**Input data:** Raw trades (data/polymarket_v1/daily_aligned/*.parquet), base run markets.parquet (688131 markets). Real data.

**Output data:** r3_markets.parquet (688131 rows), r3_trades_window.parquet (4786979 rows), r3_gate.json

**Result:** | check | value |
| --- | --- |
| passed | True |
| n_in_scope | 688131 |
| n_kept_rebuilt | 47948 |
| n_kept_saved | 47948 |
| p_1d_null_mismatch | 0 |
| p_1d_max_abs_diff | 1.11e-16 |
| chi2_rebuilt | 67.99 |

**Status:** ran
