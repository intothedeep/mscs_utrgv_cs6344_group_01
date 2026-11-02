"""Job B stage 1: build the market table and the wallet table from the pilot (or full) set.

Parameters come from the prereg JSON (t_rule, min_trades, max_staleness_h, ...).
"""
import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from common import (build_market_set, connect, load_params, md_table, raw_glob, run_stage,
                    write_json, write_manifest)

STAGE = "build_tables"
SAMPLE_ROWS = 1_000_000   # trade-size sample for Q3 (fixed seed below)
SAMPLE_SEED = 42
REASON_ORDER = ["updown", "non_binary", "no_outcome", "no_price", "stale_price", "below_min_trades"]


def build_market_table(con, params: dict) -> None:
    """One row per market with T, p_1d, its age, y, and kept flags with and without min_trades."""
    t_expr = "s.last_ts" if params["t_rule"] == "last_trade" else "m.close_at"
    con.execute(f"""
        CREATE TABLE mk_stats AS
        SELECT m.condition_id AS market_id, m.category, m.category_refined, m.opens_at, m.close_at,
               m.is_updown, m.is_binary,
               CASE WHEN m.winning_outcome_label IS NULL OR m.label1 IS NULL THEN NULL
                    WHEN m.winning_outcome_label = m.label1 THEN 1 ELSE 0 END AS y,
               s.n_trades, s.volume_usdc, s.first_ts, s.last_ts, {t_expr} AS T
        FROM mkts m LEFT JOIN (
            SELECT condition_id, count(*) AS n_trades, sum(usdc_amount) AS volume_usdc,
                   min(ts) AS first_ts, max(ts) AS last_ts FROM tr GROUP BY 1) s USING (condition_id)""")
    # p_1d = last p_event at or before T - 1 day (p_event is already on the outcome_seq=1 YES scale).
    stale = float(params["max_staleness_h"])
    common_reason = f"""
        CASE WHEN is_updown THEN 'updown' WHEN NOT is_binary THEN 'non_binary'
             WHEN y IS NULL THEN 'no_outcome' WHEN p_1d IS NULL THEN 'no_price'
             WHEN p_age_h > {stale} THEN 'stale_price' {{extra}} END"""
    con.execute(f"""
        CREATE TABLE markets AS
        WITH base AS (
          SELECT k.*, p.p_1d, p.p_ts, coalesce(p.n_before, 0) AS n_trades_before_T1d,
                 epoch((k.T - INTERVAL 1 DAY) - p.p_ts) / 3600 AS p_age_h
          FROM mk_stats k LEFT JOIN (
              SELECT t.condition_id, arg_max(t.p_event, t.ts) AS p_1d, max(t.ts) AS p_ts, count(*) AS n_before
              FROM tr t JOIN mk_stats k ON t.condition_id = k.market_id
              WHERE t.ts <= k.T - INTERVAL 1 DAY GROUP BY 1) p ON p.condition_id = k.market_id)
        SELECT *,
               {common_reason.format(extra=f"WHEN n_trades_before_T1d < {int(params['min_trades'])} THEN 'below_min_trades'")} AS drop_reason,
               {common_reason.format(extra="")} AS drop_reason_no_min
        FROM base""")
    con.execute("ALTER TABLE markets ADD COLUMN kept BOOLEAN")
    con.execute("ALTER TABLE markets ADD COLUMN kept_no_min BOOLEAN")
    con.execute("UPDATE markets SET kept = (drop_reason IS NULL), kept_no_min = (drop_reason_no_min IS NULL)")
    add_long_horizon_columns(con, int(params["horizon_long_days"]))


def add_long_horizon_columns(con, days: int) -> None:
    """v2: append p_7d, p_age_7d_h, open_ge_7d (Q1b). Adds columns only: no existing column or drop rule changes.

    p_7d = last p_event at or before T - days. Its age is stored; Q1b applies the same max_staleness_h rule.
    open_ge_7d = opens_at <= T - days (NULL opens_at or T counts as FALSE).
    """
    con.execute(f"""
        CREATE TEMP TABLE p_long AS
        SELECT t.condition_id, arg_max(t.p_event, t.ts) AS p_7d, max(t.ts) AS p_ts
        FROM tr t JOIN mk_stats k ON t.condition_id = k.market_id
        WHERE t.ts <= k.T - INTERVAL {days} DAY GROUP BY 1""")
    con.execute("ALTER TABLE markets ADD COLUMN p_7d DOUBLE")
    con.execute("ALTER TABLE markets ADD COLUMN p_age_7d_h DOUBLE")
    con.execute("ALTER TABLE markets ADD COLUMN open_ge_7d BOOLEAN")
    con.execute(f"""
        UPDATE markets SET p_7d = l.p_7d, p_age_7d_h = epoch((markets.T - INTERVAL {days} DAY) - l.p_ts) / 3600
        FROM p_long l WHERE l.condition_id = markets.market_id""")
    con.execute(f"UPDATE markets SET open_ge_7d = coalesce(opens_at <= T - INTERVAL {days} DAY, FALSE)")


def build_wallet_table(con) -> None:
    """One row per wallet x role over the kept markets' trades. A wallet is one address, never a person."""
    con.execute("""
        CREATE TABLE side AS
        SELECT t.maker AS wallet, 'maker' AS role, t.condition_id, t.usdc_amount, t.p_event FROM tr t
        SEMI JOIN markets k ON k.market_id = t.condition_id AND k.kept
        UNION ALL
        SELECT t.taker, 'taker', t.condition_id, t.usdc_amount, t.p_event FROM tr t
        SEMI JOIN markets k ON k.market_id = t.condition_id AND k.kept""")
    # mean_trade_price uses p_event (YES scale) so prices of both legs share one axis.
    con.execute("""
        CREATE TABLE wallets AS
        WITH agg AS (
          SELECT wallet, role, sum(usdc_amount) AS volume_usdc, count(*) AS n_trades,
                 count(DISTINCT condition_id) AS n_markets, avg(p_event) AS mean_trade_price,
                 median(usdc_amount) AS median_trade_size
          FROM side GROUP BY 1, 2),
        cat AS (
          SELECT s.wallet, s.role, arg_max(k.category, s.v) AS dominant_category FROM (
            SELECT wallet, role, condition_id, sum(usdc_amount) AS v FROM side GROUP BY 1, 2, 3) s
          JOIN markets k ON k.market_id = s.condition_id GROUP BY 1, 2)
        SELECT a.*, c.dominant_category FROM agg a JOIN cat c USING (wallet, role)""")


def save_outputs(con, out: Path) -> None:
    con.execute(f"COPY (SELECT * FROM markets) TO '{out}/markets.parquet' (FORMAT PARQUET)")
    con.execute(f"COPY (SELECT * FROM markets) TO '{out}/markets.csv' (HEADER, DELIMITER ',')")
    con.execute(f"COPY (SELECT * FROM wallets) TO '{out}/wallets.parquet' (FORMAT PARQUET)")
    # Fixed-seed sample of kept-market trades for the Q3 trade-size histogram and fits.
    con.execute(f"""COPY (SELECT t.condition_id, t.usdc_amount, t.p_event FROM tr t
                          SEMI JOIN markets k ON k.market_id = t.condition_id AND k.kept
                          USING SAMPLE reservoir({SAMPLE_ROWS} ROWS) REPEATABLE ({SAMPLE_SEED}))
                    TO '{out}/trade_sizes_sample.parquet' (FORMAT PARQUET)""")


def summarize(con) -> dict:
    def counts(col: str) -> dict:
        rows = con.execute(f"SELECT coalesce({col}, 'kept') AS r, count(*) FROM markets GROUP BY 1").fetchall()
        return {r: n for r, n in rows}
    return {
        "n_markets_in_scope": con.execute("SELECT count(*) FROM markets").fetchone()[0],
        "n_kept": con.execute("SELECT count(*) FROM markets WHERE kept").fetchone()[0],
        "n_kept_no_min_filter": con.execute("SELECT count(*) FROM markets WHERE kept_no_min").fetchone()[0],
        "drop_reasons": counts("drop_reason"),
        "drop_reasons_no_min_filter": counts("drop_reason_no_min"),
        "reason_order": REASON_ORDER,
        "n_kept_open_ge_7d": con.execute("SELECT count(*) FROM markets WHERE kept AND open_ge_7d").fetchone()[0],
        "n_kept_with_p_7d": con.execute("SELECT count(*) FROM markets WHERE kept AND p_7d IS NOT NULL").fetchone()[0],
        "n_wallet_role_rows": con.execute("SELECT count(*) FROM wallets").fetchone()[0],
        "n_trades_in_kept_markets": con.execute(
            "SELECT count(*) FROM tr SEMI JOIN markets k ON k.market_id = tr.condition_id AND k.kept").fetchone()[0],
        "trade_size_sample_rows": SAMPLE_ROWS, "trade_size_sample_seed": SAMPLE_SEED,
    }


def draw_drop_reasons(summary: dict, out: Path) -> None:
    reasons = summary["drop_reasons"]
    labels = [r for r in REASON_ORDER if r in reasons] + ["kept"]
    fig, ax = plt.subplots(figsize=(7, 4), layout="constrained")
    ax.bar(labels, [reasons.get(r, 0) for r in labels], color="#555555")
    ax.set_ylabel("Markets (count)")
    ax.set_xlabel("Drop reason (first failing rule)")
    ax.tick_params(axis="x", rotation=30)
    ax.grid(axis="y", alpha=0.3)
    fig.savefig(out / "drop_reasons.png", dpi=150)
    plt.close(fig)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--params", required=True)
    ap.add_argument("--out", default=".")
    args = ap.parse_args()
    out, params = Path(args.out), load_params(args.params)

    def work() -> dict[str, str]:
        con = connect()
        build_market_set(con, params)
        build_market_table(con, params)
        build_wallet_table(con)
        save_outputs(con, out)
        summary = summarize(con)
        write_json(out / "tables_summary.json", summary)
        draw_drop_reasons(summary, out)
        write_manifest(out, params, summary, __file__, STAGE)
        table = md_table(pd.DataFrame({"reason": list(summary["drop_reasons"]),
                                       "markets": list(summary["drop_reasons"].values())}))
        return {
            "Why": "Q1, Q2 and Q3 all read these two tables. Drop reasons are counted, nothing is imputed.",
            "Input data": f"Real data, scope={params['scope']}, T rule={params['t_rule']}, min_trades={params['min_trades']}, "
                          f"{summary['n_markets_in_scope']} markets in scope ({raw_glob()}).",
            "Output data": f"markets.parquet/csv ({summary['n_markets_in_scope']} rows), wallets.parquet "
                           f"({summary['n_wallet_role_rows']} rows), trade_sizes_sample.parquet "
                           f"({SAMPLE_ROWS} rows max, seed {SAMPLE_SEED}), tables_summary.json",
            "Result": f"Kept {summary['n_kept']} markets with the min_trades filter and "
                      f"{summary['n_kept_no_min_filter']} without it. Of the kept, {summary['n_kept_open_ge_7d']} opened "
                      f"at least 7 days before T and {summary['n_kept_with_p_7d']} have a p_7d.\n\n{table}",
            "Figure": "![drop reasons](drop_reasons.png)  Caption: markets by first failing rule. "
                      "Why: it shows which rule removes the most markets. Source: this run folder.",
        }

    run_stage(out, STAGE, "Build the market table and the wallet table.", work)


if __name__ == "__main__":
    main()
