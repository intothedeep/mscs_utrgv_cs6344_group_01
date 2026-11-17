"""Robustness v3, minor 4: exact duplicate rows (prereg_review_fixes.md section 6).

Duplicates = rows identical on all raw columns (SELECT DISTINCT *), over the trades of the kept markets. Rebuilds p_1d and
the trade count before T - 1 day on the deduplicated trades. Removing exact copies removes no timestamp, so p_ts and the
staleness rule cannot change: the new kept set is the old one minus markets that fall below min_trades.
Q1 on the new kept set, and the Q2 top shares over its deduplicated trades. Descriptive, no verdict.
"""
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from common import connect, md_table, raw_glob, run_stage, write_json, write_manifest
from q2_concentration import top_share
from r3_common import load_kept, load_main_q1, main_net_gap, q1_row, row_line, stage_args

STAGE = "r3_minor4"
TS = "coalesce(to_timestamp(TRY_CAST(block_timestamp AS BIGINT)), TRY_CAST(block_timestamp AS TIMESTAMP))"   # as common.build_market_set
KEPT_SQL = "condition_id IN (SELECT market_id FROM kept)"


def count_duplicates(con) -> dict:
    raw = f"read_parquet('{raw_glob()}', union_by_name=true)"
    n_rows = con.execute(f"SELECT count(*) FROM {raw} WHERE {KEPT_SQL}").fetchone()[0]
    con.execute(f"""CREATE TABLE td AS
        SELECT condition_id, {TS} AS ts, p_event, maker, taker, usdc_amount
        FROM (SELECT DISTINCT * FROM {raw} WHERE {KEPT_SQL})""")
    n_distinct = con.execute("SELECT count(*) FROM td").fetchone()[0]
    n_pilot = con.execute(f"""SELECT count(*) FROM (SELECT DISTINCT asset_id, block_timestamp, maker, taker, price, usdc_amount,
        outcome_seq FROM {raw} WHERE {KEPT_SQL})""").fetchone()[0]
    return {"n_rows": int(n_rows), "n_distinct_all_columns": int(n_distinct), "n_dup_all_columns": int(n_rows - n_distinct),
            "share_dup_all_columns": float((n_rows - n_distinct) / n_rows), "n_distinct_pilot_key": int(n_pilot),
            "n_dup_pilot_key": int(n_rows - n_pilot), "share_dup_pilot_key": float((n_rows - n_pilot) / n_rows)}


def rebuild_p1d(con) -> pd.DataFrame:
    """p_1d and the count before T - 1 day on the deduplicated trades (same rule as build_tables.py)."""
    return con.execute("""
        WITH w AS (SELECT t.condition_id, t.ts, t.p_event FROM td t JOIN kept k ON t.condition_id = k.market_id
                   WHERE t.ts <= k."T" - INTERVAL 1 DAY),
        l AS (SELECT condition_id, max(ts) AS p_ts, count(*) AS n_before FROM w GROUP BY 1)
        SELECT l.condition_id AS market_id, avg(w.p_event) AS p_1d_dedup, l.n_before AS n_before_dedup
        FROM l JOIN w ON w.condition_id = l.condition_id AND w.ts = l.p_ts GROUP BY l.condition_id, l.n_before""").df()


def wallet_shares(con, new_ids: pd.DataFrame) -> dict:
    con.register("newkept", new_ids)
    wallets = con.execute("""
        SELECT role, wallet, sum(usdc_amount) AS volume_usdc FROM (
          SELECT 'maker' AS role, t.maker AS wallet, t.usdc_amount FROM td t SEMI JOIN newkept n ON n.market_id = t.condition_id
          UNION ALL
          SELECT 'taker', t.taker, t.usdc_amount FROM td t SEMI JOIN newkept n ON n.market_id = t.condition_id)
        GROUP BY role, wallet""").df()
    wallets = wallets[wallets["volume_usdc"] > 0]   # as q2_concentration.py
    return {role: {"top1_share": top_share(g["volume_usdc"].to_numpy(float), 0.01),
                   "top20_share": top_share(g["volume_usdc"].to_numpy(float), 0.20), "n_wallets": len(g)}
            for role, g in wallets.groupby("role")}


def draw(q2: dict, out) -> None:
    fig, ax = plt.subplots(figsize=(7, 4), layout="constrained")
    labels = [f"{r} {k}" for r in q2 for k in ("top1_share", "top20_share")]
    x = range(len(labels))
    ax.bar([i - 0.2 for i in x], [q2[r][k]["saved"] for r in q2 for k in ("top1_share", "top20_share")], 0.4, color="#555555",
           label="Saved (duplicates kept)")
    ax.bar([i + 0.2 for i in x], [q2[r][k]["dedup"] for r in q2 for k in ("top1_share", "top20_share")], 0.4, color="#aa5500",
           label="Exact duplicates removed")
    ax.set(xticks=list(x), xticklabels=labels, ylabel="Share of volume", ylim=(0, 1))
    ax.tick_params(axis="x", rotation=20)
    ax.grid(axis="y", alpha=0.3)
    fig.legend(loc="outside upper center", ncol=2)
    fig.savefig(out / "fig_r3_minor4_q2_shares.png", dpi=150)
    plt.close(fig)


def main() -> None:
    _, out, src, params = stage_args()
    alpha, n_bins, min_trades = float(params["alpha"]), int(params["n_bins"]), int(params["min_trades"])

    def work() -> dict[str, str]:
        kept = load_kept(out)
        main_res = load_main_q1(src)
        con = connect()
        con.register("kept", kept[["market_id", "T"]])
        dup = count_duplicates(con)
        rb = rebuild_p1d(con)
        df = kept.merge(rb, on="market_id", how="left")
        df["p_1d_saved"] = df["p_1d"]
        new = df[df["n_before_dedup"].fillna(0) >= min_trades].copy()
        new["p_1d"] = new["p_1d_dedup"]
        row, _ = q1_row(new, "p_1d", alpha, n_bins, main_res, main_net_gap(kept))
        shares = wallet_shares(con, new[["market_id"]])
        saved_q2 = json.loads((src / "q2_results.json").read_text())["concentration"]
        q2 = {role: {k: {"saved": saved_q2[role][k], "dedup": shares[role][k], "delta_pp": 100 * (shares[role][k] - saved_q2[role][k])}
                     for k in ("top1_share", "top20_share")} for role in shares}
        kept_change = {"n_in": len(kept), "n_out": len(new), "n_removed": len(kept) - len(new),
                       "p1d_changed_in_new_kept": int(((new["p_1d_dedup"] - new["p_1d_saved"]).abs() > 1e-12).sum())}
        results = {"duplicates": dup, "kept_set": kept_change, "q1": row, "q2": q2}
        flat_res = dup | {f"kept_{k}": v for k, v in kept_change.items()} | {f"q1_{k}": v for k, v in row.items()}
        for role, d in q2.items():
            for k, v in d.items():
                flat_res |= {f"q2_{role}_{k}_{f}": x for f, x in v.items()}
        write_json(out / "minor4_dedup.json", results | {"flat": flat_res})
        write_json(out / "minor4_results.json", flat_res)
        draw(q2, out)
        write_manifest(out, params, flat_res, __file__, STAGE)
        q2_tab = pd.DataFrame([{"role": r, "share": k, **v} for r, d in q2.items() for k, v in d.items()])
        return {
            "Why": "Minor 4: the pilot found 5% exact duplicate rows. MVP1 keeps them. Do the Q1 and Q2 results survive removing them?",
            "Input data": f"Raw trades of the {len(kept)} kept markets ({raw_glob()}), all 24 columns for the exact-duplicate key. Real data.",
            "Output data": "minor4_dedup.json, minor4_results.json, fig_r3_minor4_q2_shares.png",
            "Result": f"Duplicates: {dup}. Kept set: {kept_change}.\n\n" + md_table(pd.DataFrame([row_line("deduplicated kept set", row)]))
                      + "\n\nQ2 top shares (descriptive, delta in percentage points, no verdict):\n\n" + md_table(q2_tab),
            "Figure": "![minor4](fig_r3_minor4_q2_shares.png)  Caption: top 1% and top 20% volume shares with and without exact duplicates. "
                      "Why: equal bars mean duplicates do not drive the concentration result. Source: this run folder.",
        }

    run_stage(out, STAGE, "Minor 4: exact duplicate rows.", work)


if __name__ == "__main__":
    main()
