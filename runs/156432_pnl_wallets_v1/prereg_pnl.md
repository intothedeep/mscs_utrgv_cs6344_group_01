# Pre-registration: wallet profit and loss (written before the run)

- Date: 2026-11-16. Owner request: compute it on the cluster. Do not put it in the report or the paper. The results go to a tips page later.
- Code: `code/pnl_wallets.py`. Job: `jobs/pnl_wallets.slurm`.
- Descriptive only. No hypothesis test, no verdict.
- A "wallet" is one address, never a person.

## Question

How much money did each wallet win or lose on resolved markets, and how is it spread across wallets?

## Scope

| Scope | Markets |
| --- | --- |
| `all` | every market in the saved `markets.parquet` with a usable winner |
| `non_updown` | `all`, without Up/Down markets (`is_updown` from `build_tables`) |
| `kept` | the `kept` flag of `build_tables` (47,948 markets in the MVP1 full run) |

- Source of flags: `markets.parquet` of run `142123_robust_full_v4`. It is the same build as `142082_mvp1_full_v1r3`.
- Usable winner: all rows of the market have one `winning_outcome_label`, and some `outcome_label` of the market equals it.
- Every `kept` market must be usable. Checked below.

## Accounting rule

| Step | Rule |
| --- | --- |
| Fill | one raw row. Rows with `price` <= 0 or null, `usdc_amount` null, `taker_direction` not BUY or SELL, or a null wallet are excluded and counted |
| Taker BUY | cash -`usdc_amount`, shares +`usdc_amount` / `price` on the row's outcome |
| Taker SELL | cash +`usdc_amount`, shares -`usdc_amount` / `price` |
| Maker | the opposite leg of the same fill, same outcome |
| Payout | shares x 1 if the outcome equals the winning label, else 0 |
| `pnl_gross` | cash + payout, summed over the wallet's legs in the scope |
| `fees` | `fee_usdc` of the fill, charged to the taker leg only. Null counts as 0 |
| `pnl_net` | `pnl_gross` - `fees` |
| Winner, loser, zero | `pnl_net` > 1e-6 USDC, < -1e-6 USDC, else zero |

Per leg, `pnl_gross = sign x usdc_amount x (won / price - 1)`. It is linear, so no per-market netting is needed.

### Assumptions (not verified from repo files)

1. `usdc_amount` is the cash of the fill on the row's outcome, and `price` is that outcome's price.
2. `taker_direction` is the taker's side on the row's outcome (`r3_side_check` tests the values, not this meaning).
3. `fee_usdc` is the fee the taker paid on that fill. The maker pays none. The schema also has `taker_base_fee` and `maker_base_fee`. Their meaning is not documented here.
4. The maker is the exact counterparty on the same outcome. A fill matched by a mint or a merge (a split of 1 USDC into both outcomes) breaks this. Then the real counterparty is not a wallet holding the other side.
5. Duplicate raw rows stay (`keep_duplicate_rows` true in the earlier runs). Both legs double together, so market sums still cancel. A wallet's volume and profit include the repeats.
6. Trades after `close_at` count. Every position is held to resolution. No wallet sells after resolution.
7. Redemption value is exactly 1 or 0. A split payout market counts as a win for the winning label only (R1 showed how many markets are split).
8. A wallet that is both maker and taker in one fill (self trade) nets to zero cash and pays the fee. It is counted.
9. A market with more than two outcomes is handled the same way. Neg-Risk markets are not in `daily_aligned/`.

## Sanity checks and pass criteria

| Check | Pass | If it fails |
| --- | --- | --- |
| Market identity: per usable market, `abs(sum of gross pnl over all wallets)` <= 1e-6 x fill volume | 0 failures | report the count, find the cause before any number is read |
| Row count and volume of each market equal the saved `n_trades` and `volume_usdc` of `markets.parquet` | 0 mismatches | the raw read or the join differs from `build_tables` |
| Sum of `pnl_net` over wallets = -(sum of fees), within 1e-6 x volume, per scope | pass in all three scopes | accounting bug |
| Every `kept` market is usable | 0 kept markets unusable | the usable rule differs from `y` in `build_tables` |
| Excluded rows (price, direction, nulls) in usable markets | reported. Under 1% of rows is clean | say how many and read with care |
| Markets with conflicting winner labels | reported | those markets are unusable |
| Share of positions that are short, in the `kept` set | reported, no pass line | a high share means mint and merge matter and assumption 4 is weak |

- The first three checks are bookkeeping identities. They find code errors, not data errors. They do not test assumptions 1 to 4.
- The pass lines are rounding limits. They are not derived from noise because the run is descriptive.

## Outputs (run folder)

| File | Content |
| --- | --- |
| `wallet_pnl.parquet` | long table: `wallet`, `scope`, `n_markets`, `n_trades` (legs), `volume_usdc` (both roles), `pnl_gross`, `fees`, `pnl_net` |
| `pnl_summary.json` | per scope: wallet counts, winners, losers, zero, total won, total lost, sum of `pnl_net`, quantiles (1, 5, 25, 50, 75, 95, 99%), median, top shares, histogram counts. Plus all checks |
| `market_check.csv` | per usable market: identity and count checks |
| `report_pnl_wallets.md`, `fig_pnl_distribution.png` | stage report and one figure |

Definitions of the top shares (p = 1 and 10):

- `top_pct_of_all_wallets_share_of_won`: the top p% of all wallets by `pnl_net`. Their positive profit over total won.
- `top_pct_of_winners_share_of_won`: the top p% of winners over total won.
- `top_pct_of_losers_share_of_lost`: the top p% of losers (largest losses) over total lost.
- Histogram: symmetric-log bins. One centre bin (-1, 1) USDC, half-decade bins to 1e8, one open tail each side.
