"""Job A: inspect the pilot set. Fixes the Up/Down marking, close-time rule and activity cutoff.

HARD RULE: nothing here pairs a price with an outcome (no p_event/price grouped by winning label,
no Brier, no calibration). The only use of winning_outcome_label is the missing count.
"""
import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from common import (build_market_set, connect, load_params, md_table, raw_glob, run_stage,
                    write_json, write_manifest)

QUANTILES = [0, 0.05, 0.25, 0.5, 0.75, 0.95, 1]
CUTOFFS = [1, 5, 10, 20, 50]
STD = "is_binary AND NOT is_updown"  # Standard Binary set used by every check below


def write_schema(con, out: Path) -> None:
    con.execute("DESCRIBE raw").df()[["column_name", "column_type"]].rename(
        columns={"column_name": "column", "column_type": "type"}).to_csv(out / "schema.csv", index=False)


def write_value_counts(con, out: Path) -> None:
    parts = []
    for col in ["resolution_status", "category", "category_refined", "neg_risk"]:
        df = con.execute(f"SELECT '{col}' AS field, CAST({col} AS VARCHAR) AS value, "
                         f"count(*) AS n_markets FROM mkts GROUP BY 2 ORDER BY 3 DESC").df()
        parts.append(df)
    # Slug prefixes (first 3 words) of slugs that look like Up/Down: shows how they are marked.
    parts.append(con.execute("""
        SELECT 'slug_updown_prefix' AS field,
               array_to_string(list_slice(string_split(market_slug,'-'),1,3),'-') AS value,
               count(*) AS n_markets
        FROM mkts
        WHERE market_slug ILIKE '%up-or-down%' OR market_slug ILIKE '%updown%'
           OR market_slug ILIKE '%up-down%' OR market_slug ILIKE '%-up-%' OR market_slug ILIKE '%-down-%'
        GROUP BY 2 ORDER BY 3 DESC LIMIT 30""").df())
    pd.concat(parts).to_csv(out / "value_counts.csv", index=False)
    con.execute("""SELECT category, category_refined, count(*) AS n_markets, sum(is_updown::INT) AS n_flagged_updown
                   FROM mkts GROUP BY 1, 2 ORDER BY 3 DESC""").df().to_csv(out / "updown_check.csv", index=False)


def write_duplicates(con, out: Path) -> dict:
    total = con.execute("SELECT count(*) FROM tr").fetchone()[0]
    distinct = con.execute("""SELECT count(*) FROM (SELECT DISTINCT asset_id, ts, maker, taker, price,
                              usdc_amount, outcome_seq FROM tr)""").fetchone()[0]
    res = {"total_rows": total, "distinct_rows": distinct, "duplicate_rows": total - distinct,
           "key": "asset_id, block_timestamp, maker, taker, price, usdc_amount, outcome_seq"}
    write_json(out / "duplicates.json", res)
    return res


def write_close_time(con, out: Path) -> pd.DataFrame:
    df = con.execute(f"""
        WITH a AS (
          SELECT t.condition_id, min(t.ts) AS first_trade, max(t.ts) AS last_trade, count(*) AS n_trades,
                 count(*) FILTER (WHERE t.ts > m.close_at) AS n_trades_after_close,
                 sum(t.usdc_amount) AS volume, sum(t.usdc_amount) FILTER (WHERE t.ts > m.close_at) AS volume_after
          FROM tr t JOIN mkts m USING (condition_id) WHERE m.{STD} GROUP BY 1)
        SELECT a.condition_id, m.close_at, m.resolved_at, a.first_trade, a.last_trade, a.n_trades,
               a.n_trades_after_close, a.volume, coalesce(a.volume_after, 0) AS volume_after,
               epoch(a.last_trade - m.close_at) / 3600 AS last_minus_close_h,
               epoch(m.resolved_at - m.close_at) / 3600 AS resolved_minus_close_h
        FROM a JOIN mkts m USING (condition_id)""").df()
    df.drop(columns=["volume", "volume_after"]).to_csv(out / "close_time.csv", index=False)
    summary = {
        "n_markets": len(df),
        "quantiles": QUANTILES,
        "last_minus_close_h": df["last_minus_close_h"].quantile(QUANTILES).tolist(),
        "resolved_minus_close_h": df["resolved_minus_close_h"].quantile(QUANTILES).tolist(),
        "share_markets_trade_after_close": float((df["n_trades_after_close"] > 0).mean()),
        "share_volume_after_close": float(df["volume_after"].sum() / df["volume"].sum()),
    }
    write_json(out / "close_time_summary.json", summary)
    return df


def write_activity(con, out: Path) -> dict:
    df = con.execute(f"""
        SELECT t.condition_id,
               count(*) FILTER (WHERE t.ts <= lt.last_ts - INTERVAL 1 DAY) AS n_trades_last_rule,
               coalesce(sum(t.usdc_amount) FILTER (WHERE t.ts <= lt.last_ts - INTERVAL 1 DAY), 0) AS volume_last_rule,
               count(*) FILTER (WHERE t.ts <= m.close_at - INTERVAL 1 DAY) AS n_trades_close_rule,
               coalesce(sum(t.usdc_amount) FILTER (WHERE t.ts <= m.close_at - INTERVAL 1 DAY), 0) AS volume_close_rule
        FROM tr t JOIN mkts m USING (condition_id)
        JOIN (SELECT condition_id, max(ts) AS last_ts FROM tr GROUP BY 1) lt USING (condition_id)
        WHERE m.{STD} GROUP BY 1""").df()
    df.to_csv(out / "activity.csv", index=False)
    summary: dict = {"n_markets": len(df), "quantiles": QUANTILES, "cutoffs": CUTOFFS}
    for rule in ["last_rule", "close_rule"]:
        col = df[f"n_trades_{rule}"]
        summary[f"n_trades_{rule}_quantiles"] = col.quantile(QUANTILES).tolist()
        summary[f"volume_{rule}_quantiles"] = df[f"volume_{rule}"].quantile(QUANTILES).tolist()
        summary[f"kept_at_cutoff_{rule}"] = {str(c): int((col >= c).sum()) for c in CUTOFFS}
    write_json(out / "activity_summary.json", summary)
    return summary


def write_missing(con, out: Path) -> dict:
    res = {"markets_in_set": con.execute(f"SELECT count(*) FROM mkts WHERE {STD}").fetchone()[0],
           "markets_no_winning_label": con.execute(
               f"SELECT count(*) FROM mkts WHERE {STD} AND winning_outcome_label IS NULL").fetchone()[0],
           "markets_no_outcome_seq1_label": con.execute(
               f"SELECT count(*) FROM mkts WHERE {STD} AND label1 IS NULL").fetchone()[0],
           "markets_all_pilot_no_winning_label": con.execute(
               "SELECT count(*) FROM mkts WHERE winning_outcome_label IS NULL").fetchone()[0]}
    write_json(out / "missing.json", res)
    return res


def draw_close_hist(df: pd.DataFrame, out: Path) -> None:
    x = df["last_minus_close_h"].dropna().to_numpy()
    top = max(abs(x).max(), 10)
    pos = np.logspace(0, np.ceil(np.log10(top)), 40)
    edges = np.concatenate([-pos[::-1], [0], pos])
    fig, ax = plt.subplots(figsize=(7, 4), layout="constrained")
    ax.hist(x, bins=edges, color="#555555")
    ax.set_xscale("symlog", linthresh=1)
    ax.axvline(0, color="#aa0000", lw=1)  # 0 = last trade exactly at close_at; right of it = trades after close
    ax.set_xlabel("Last trade minus close_at (hours, symlog)")
    ax.set_ylabel("Markets (count)")
    ax.set_title("Pilot markets: last trade relative to close_at")
    ax.grid(alpha=0.3)
    fig.savefig(out / "close_time_hist.png", dpi=150)
    plt.close(fig)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--job", default="local")
    ap.add_argument("--out", default=".")
    ap.add_argument("--params", default=None)
    args = ap.parse_args()
    out = Path(args.out)
    params = load_params(args.params)
    params["scope"] = "pilot"  # Job A inspects the pilot set only

    def work() -> dict[str, str]:
        con = connect()
        build_market_set(con, params)
        write_schema(con, out)
        write_value_counts(con, out)
        dup = write_duplicates(con, out)
        ct = write_close_time(con, out)
        act = write_activity(con, out)
        missing = write_missing(con, out)
        draw_close_hist(ct, out)
        cts = json.loads((out / "close_time_summary.json").read_text())
        table = md_table(pd.DataFrame({"quantile": QUANTILES, "last_minus_close_h": cts["last_minus_close_h"],
                              "resolved_minus_close_h": cts["resolved_minus_close_h"]}))
        n_mk = con.execute("SELECT count(*) FROM mkts").fetchone()[0]
        n_tr = con.execute("SELECT count(*) FROM tr").fetchone()[0]
        write_manifest(out, params, {
            "n_markets_pilot_all": n_mk, "n_trades_pilot_all": n_tr, "duplicates": dup,
            "missing": missing, "close_time": cts, "kept_at_cutoff": {
                k: act[k] for k in ("kept_at_cutoff_last_rule", "kept_at_cutoff_close_rule")}},
            __file__)
        return {
            "Why": "Fix the Up/Down marking, the close-time rule T and the minimum-activity cutoff before any Q1 result is seen.",
            "Input data": f"Real data. Pilot = markets with close_at in {params['pilot_month']}: {n_mk} markets, {n_tr} trades "
                          f"(raw: {raw_glob()}). Standard Binary set: {missing['markets_in_set']} markets.",
            "Output data": "schema.csv, value_counts.csv, updown_check.csv, duplicates.json, close_time.csv, "
                           "close_time_summary.json, activity.csv, activity_summary.json, missing.json, "
                           "manifest.json, close_time_hist.png",
            "Result": f"Duplicate rows: {dup['duplicate_rows']} of {dup['total_rows']}. "
                      f"Markets with any trade after close_at: {cts['share_markets_trade_after_close']:.3f}. "
                      f"Volume after close_at: {cts['share_volume_after_close']:.3f}. "
                      f"No winning label: {missing['markets_no_winning_label']}.\n\n" + table,
            "Figure": "![close time](close_time_hist.png)  Caption: last trade minus close_at per market. "
                      "Why: trades after close_at would leak the outcome into p_1d. Source: this run folder.",
        }

    run_stage(out, "pilot_inspect", "Inspect the pilot set (schema, Up/Down marking, duplicates, close time, activity).", work)


if __name__ == "__main__":
    main()
