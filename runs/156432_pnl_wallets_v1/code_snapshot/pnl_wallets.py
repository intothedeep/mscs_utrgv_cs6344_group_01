"""Wallet profit and loss (owner request 2026-11-16, descriptive, tips page only). Criteria: analysis/prereg_pnl.md.

Per wallet: cash flow of every fill plus the payout of the shares at resolution, minus the fees the wallet paid.
A wallet is one address, never a person. The scope flags (is_updown, kept) come from the saved markets.parquet
of a finished run, so the kept set is exactly the build_tables one. No model, no fit.
"""
import argparse
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from common import connect, md_table, raw_glob, run_stage, write_json, write_manifest

STAGE = "pnl_wallets"
EPS = 1e-6                    # USDC. |pnl_net| below this counts as zero.
CHECK_REL_TOL = 1e-6          # market identity: |sum gross| <= tol x market fill volume
SHORT_TOL = 1e-6              # shares. A net position below -SHORT_TOL is a short (needs a mint to exist).
QUANTILES = [0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99]
TOP_PCTS = [1, 10]
SCOPES = {"all": "TRUE", "non_updown": "NOT is_updown", "kept": "kept"}
SCOPE_TITLE = {"all": "All resolved markets", "non_updown": "Non-Up/Down resolved markets", "kept": "Kept set"}
# Symmetric-log grid: one centre bin (-1, 1) USDC, then half-decade bins out to 1e8, then one open tail each side.
POS_EDGES = 10.0 ** np.arange(0, 8.5, 0.5)
HIST_EDGES = np.concatenate([[-1e12], -POS_EDGES[::-1], POS_EDGES, [1e12]])

OK_SQL = ("coalesce(price > 0 AND usdc_amount IS NOT NULL AND taker_direction IN ('BUY','SELL') "
          "AND maker IS NOT NULL AND taker IS NOT NULL, FALSE)")
# Leg sign: taker BUY = +1 share leg, taker SELL = -1. The maker takes the opposite leg of the same fill.
SGN_SQL = "(CASE WHEN x.taker_direction = 'BUY' THEN 1 ELSE -1 END) * (CASE WHEN r.is_taker = 1 THEN 1 ELSE -1 END)"
# Gross profit of one leg = cash + payout = sgn * u * (won / price - 1).
GROSS_SQL = f"{SGN_SQL} * x.usdc_amount * (CASE WHEN x.outcome_label = m.win THEN 1.0 / x.price ELSE 0.0 END - 1.0)"
LEGS_SQL = ("FROM raw x JOIN mk m ON m.condition_id = x.condition_id AND m.usable "
            "CROSS JOIN (VALUES (1), (0)) AS r(is_taker) WHERE x.ok")


def build_market_table(con, markets_src: Path) -> None:
    """mk: one row per market in the saved markets.parquet, with its winner, usable flag and scope flags."""
    con.execute(f"""
        CREATE VIEW raw AS
        SELECT condition_id, outcome_label, winning_outcome_label, CAST(outcome_seq AS BIGINT) AS outcome_seq,
               maker, taker, taker_direction, usdc_amount, price, fee_usdc, {OK_SQL} AS ok
        FROM read_parquet('{raw_glob()}', union_by_name=true)""")
    con.execute(f"""
        CREATE TABLE mk AS
        WITH w AS (
          SELECT condition_id, max(winning_outcome_label) AS win,
                 count(DISTINCT winning_outcome_label) AS n_win_labels,
                 coalesce(bool_or(outcome_label = winning_outcome_label), FALSE) AS has_winner_row,
                 count(*) AS n_rows, sum(usdc_amount) AS vol_rows,
                 count(*) FILTER (WHERE NOT ok) AS n_excluded,
                 count(*) FILTER (WHERE price IS NULL OR price <= 0) AS n_bad_price,
                 count(*) FILTER (WHERE coalesce(taker_direction NOT IN ('BUY','SELL'), TRUE)) AS n_bad_direction,
                 count(*) FILTER (WHERE fee_usdc IS NULL) AS n_fee_null,
                 count(*) FILTER (WHERE maker = taker) AS n_self_trade,
                 sum(fee_usdc) AS fee_rows
          FROM raw GROUP BY condition_id)
        SELECT w.*, (w.n_win_labels = 1 AND w.has_winner_row) AS usable,
               coalesce(s.is_updown, FALSE) AS is_updown, coalesce(s.kept, FALSE) AS kept,
               s.n_trades AS saved_n_trades, s.volume_usdc AS saved_volume
        FROM w JOIN read_parquet('{markets_src}/markets.parquet') s ON s.market_id = w.condition_id""")


def build_wallet_table(con) -> None:
    """wp: one row per wallet x scope. Gross profit is linear in the fills, so no per-market netting is needed.

    Groups (wallet, is_updown, kept) split the markets into disjoint sets, so n_markets adds up across groups.
    """
    con.execute(f"""
        CREATE TABLE g AS
        SELECT CASE WHEN r.is_taker = 1 THEN x.taker ELSE x.maker END AS wallet, m.is_updown, m.kept,
               count(DISTINCT x.condition_id) AS n_markets, count(*) AS n_trades,
               sum(x.usdc_amount) AS volume_usdc, sum({GROSS_SQL}) AS pnl_gross,
               sum(r.is_taker * coalesce(x.fee_usdc, 0)) AS fees
        {LEGS_SQL}
        GROUP BY 1, 2, 3""")
    parts = [f"""
        SELECT wallet, '{name}' AS scope, CAST(sum(n_markets) AS BIGINT) AS n_markets,
               CAST(sum(n_trades) AS BIGINT) AS n_trades, sum(volume_usdc) AS volume_usdc,
               sum(pnl_gross) AS pnl_gross, sum(fees) AS fees, sum(pnl_gross) - sum(fees) AS pnl_net
        FROM g WHERE {cond} GROUP BY wallet""" for name, cond in SCOPES.items()]
    con.execute("CREATE TABLE wp AS " + " UNION ALL ".join(parts))


def build_market_check(con, out: Path) -> dict:
    """market_check.csv: one row per usable market. Identity and row-count checks, see prereg 'Sanity checks'."""
    con.execute(f"""
        CREATE TABLE mchk AS
        SELECT x.condition_id, sum({GROSS_SQL}) AS gross_sum, sum(x.usdc_amount * r.is_taker) AS fill_volume
        {LEGS_SQL} GROUP BY 1""")
    con.execute(f"""
        CREATE TABLE mc AS
        SELECT m.condition_id, m.is_updown, m.kept, m.n_rows, m.saved_n_trades, m.vol_rows, m.saved_volume,
               m.n_excluded, coalesce(c.fill_volume, 0) AS fill_volume, coalesce(c.gross_sum, 0) AS gross_sum,
               abs(coalesce(c.gross_sum, 0)) <= {CHECK_REL_TOL} * coalesce(c.fill_volume, 0) AS identity_ok,
               coalesce(m.n_rows = m.saved_n_trades, FALSE) AS rows_match_saved,
               coalesce(abs(m.vol_rows - m.saved_volume) <= {CHECK_REL_TOL} * greatest(abs(m.saved_volume), 1), FALSE)
                 AS volume_match_saved
        FROM mk m LEFT JOIN mchk c USING (condition_id) WHERE m.usable""")
    con.execute(f"COPY (SELECT * FROM mc ORDER BY condition_id) TO '{out}/market_check.csv' (HEADER, DELIMITER ',')")
    row = con.execute("""
        SELECT count(*), count(*) FILTER (WHERE NOT identity_ok), count(*) FILTER (WHERE NOT rows_match_saved),
               count(*) FILTER (WHERE NOT volume_match_saved) FROM mc""").fetchone()
    return dict(zip(["n_markets_checked", "n_identity_failures", "n_rows_mismatch_saved", "n_volume_mismatch_saved"], row))


def build_data_checks(con) -> dict:
    """Counts that show how far the accounting rule fits the data (not pass or fail by construction)."""
    row = con.execute("""
        SELECT count(*), count(*) FILTER (WHERE usable), count(*) FILTER (WHERE kept AND NOT usable),
               count(*) FILTER (WHERE n_win_labels > 1), count(*) FILTER (WHERE is_updown AND usable),
               sum(n_rows), sum(n_rows) FILTER (WHERE usable), sum(n_excluded) FILTER (WHERE usable),
               sum(n_bad_price) FILTER (WHERE usable), sum(n_bad_direction) FILTER (WHERE usable),
               sum(n_fee_null) FILTER (WHERE usable), sum(n_self_trade) FILTER (WHERE usable),
               sum(vol_rows) FILTER (WHERE usable), sum(vol_rows), sum(fee_rows) FILTER (WHERE usable)
        FROM mk""").fetchone()
    keys = ["n_markets_in_scope", "n_usable", "n_kept_not_usable", "n_markets_conflicting_winner_label",
            "n_updown_usable", "n_rows_in_scope", "n_rows_usable", "n_rows_excluded_usable", "n_bad_price_usable",
            "n_bad_direction_usable", "n_fee_null_usable", "n_self_trade_usable", "volume_usable", "volume_in_scope",
            "fee_sum_usable_rows"]
    res = {k: (float(v) if isinstance(v, float) else v) for k, v in zip(keys, row)}
    res["share_rows_excluded_usable"] = (res["n_rows_excluded_usable"] or 0) / max(res["n_rows_usable"] or 1, 1)
    res["share_volume_in_unusable_markets"] = 1 - (res["volume_usable"] or 0) / max(res["volume_in_scope"] or 1, 1)
    return res


def build_short_check(con) -> dict:
    """Kept markets only: share of (wallet, market, outcome) positions with negative net shares.

    A fill pair never creates a short on its own. Shorts mean the counter-leg came from a mint or merge (or a
    maker simplification error), which this accounting does not model.
    """
    pos = con.execute(f"""
        WITH p AS (
          SELECT CASE WHEN r.is_taker = 1 THEN x.taker ELSE x.maker END AS wallet, x.condition_id, x.outcome_seq,
                 sum({SGN_SQL} * x.usdc_amount / x.price) AS shares, sum(x.usdc_amount) AS vol
          FROM raw x JOIN mk m ON m.condition_id = x.condition_id AND m.usable AND m.kept
          CROSS JOIN (VALUES (1), (0)) AS r(is_taker) WHERE x.ok GROUP BY 1, 2, 3)
        SELECT count(*), count(*) FILTER (WHERE shares < -{SHORT_TOL}), sum(vol), sum(vol) FILTER (WHERE shares < -{SHORT_TOL})
        FROM p""").fetchone()
    n, n_short, vol, vol_short = pos
    return {"n_positions_kept": n, "n_short_positions_kept": n_short, "share_short_positions_kept": n_short / n if n else None,
            "share_volume_in_short_positions_kept": float(vol_short or 0) / float(vol) if vol else None}


def top_share(sorted_desc: np.ndarray, pct: int, total: float) -> float | None:
    if len(sorted_desc) == 0 or total <= 0:
        return None
    k = math.ceil(len(sorted_desc) * pct / 100)
    return float(sorted_desc[:k].sum() / total)


def summarize_scope(x: np.ndarray, volume: float, fees: float) -> dict:
    """x = pnl_net per wallet. Winner = pnl_net > EPS, loser = pnl_net < -EPS, else zero."""
    win, lose = np.sort(x[x > EPS])[::-1], np.sort(-x[x < -EPS])[::-1]   # both descending, loss as a positive number
    total_won, total_lost = float(win.sum()), float(lose.sum())
    all_desc = np.sort(x)[::-1]
    counts, _ = np.histogram(x, bins=HIST_EDGES)
    return {
        "n_wallets": len(x), "n_winners": len(win), "n_losers": len(lose),
        "n_zero": int(len(x) - len(win) - len(lose)),
        "total_won": total_won, "total_lost": total_lost, "sum_pnl_net": float(x.sum()), "total_fees": fees,
        "sum_pnl_net_plus_fees": float(x.sum() + fees), "total_volume_usdc": volume,
        "sum_identity_ok": abs(float(x.sum()) + fees) <= CHECK_REL_TOL * max(volume, 1.0),
        "median_pnl_net": float(np.median(x)) if len(x) else None,
        "quantiles_pnl_net": {f"{int(q * 100)}%": float(np.quantile(x, q)) for q in QUANTILES} if len(x) else {},
        "top_pct_of_all_wallets_share_of_won": {f"{p}%": top_share(all_desc.clip(min=0), p, total_won) for p in TOP_PCTS},
        "top_pct_of_winners_share_of_won": {f"{p}%": top_share(win, p, total_won) for p in TOP_PCTS},
        "top_pct_of_losers_share_of_lost": {f"{p}%": top_share(lose, p, total_lost) for p in TOP_PCTS},
        "hist_counts": counts.tolist(), "hist_n_outside": int(len(x) - counts.sum()),
    }


def draw_distribution(summary: dict, out: Path) -> None:
    names = list(SCOPES)
    fig, axes = plt.subplots(len(names), 1, figsize=(7, 8), sharex=True, layout="constrained")
    ticks = [i for i, e in enumerate(HIST_EDGES) if abs(e) <= 1e8 and np.log10(abs(e)).is_integer() and int(np.log10(abs(e))) % 2 == 0]
    labels = [("-" if HIST_EDGES[i] < 0 else "") + f"1e{int(np.log10(abs(HIST_EDGES[i])))}" for i in ticks]
    for ax, name in zip(axes, names):
        s = summary["scopes"][name]
        ax.bar(np.arange(len(s["hist_counts"])), s["hist_counts"], width=0.9, color="#555555")
        ax.set_yscale("log")
        ax.set_ylabel("Wallets (count, log scale)")
        ax.set_title(f"{SCOPE_TITLE[name]}: {s['n_wallets']:,} wallets", fontsize=10)
        ax.grid(axis="y", alpha=0.3)
    axes[-1].set_xticks([i - 0.5 for i in ticks], labels)
    axes[-1].set_xlabel("Net profit per wallet (USDC, symmetric-log bins, centre bin -1 to 1)")
    fig.savefig(out / "fig_pnl_distribution.png", dpi=150)
    plt.close(fig)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--markets-src", required=True, help="run folder that holds markets.parquet (build_tables output)")
    ap.add_argument("--out", default=".")
    args = ap.parse_args()
    out, src = Path(args.out), Path(args.markets_src)
    params = {"markets_src": str(src), "eps_usdc": EPS, "check_rel_tol": CHECK_REL_TOL, "short_tol_shares": SHORT_TOL,
              "scopes": SCOPES, "hist_edges": HIST_EDGES.tolist(), "prereg": "analysis/prereg_pnl.md"}

    def work() -> dict[str, str]:
        con = connect()
        con.execute(f"SET temp_directory='{out}/duckdb_tmp'")   # spill inside the run folder
        con.execute("SET preserve_insertion_order=false")       # lower memory for the big group-bys
        build_market_table(con, src)
        build_wallet_table(con)
        con.execute(f"COPY (SELECT * FROM wp ORDER BY scope, wallet) TO '{out}/wallet_pnl.parquet' (FORMAT PARQUET)")
        checks = {**build_data_checks(con), **build_market_check(con, out), **build_short_check(con)}
        summary = {"scopes": {}, "checks": checks, "hist_edges": HIST_EDGES.tolist(), "eps_usdc": EPS}
        for name in SCOPES:
            d = con.execute("SELECT pnl_net, volume_usdc, fees FROM wp WHERE scope = ?", [name]).fetchnumpy()
            summary["scopes"][name] = summarize_scope(d["pnl_net"], float(d["volume_usdc"].sum()), float(d["fees"].sum()))
        write_json(out / "pnl_summary.json", summary)
        draw_distribution(summary, out)
        write_manifest(out, params, {"checks": checks, "scopes": {k: {kk: vv for kk, vv in v.items() if kk != "hist_counts"}
                                                                   for k, v in summary["scopes"].items()}}, __file__, STAGE)
        rows = [{"scope": n, "wallets": s["n_wallets"], "winners": s["n_winners"], "losers": s["n_losers"], "zero": s["n_zero"],
                 "total_won_usdc": s["total_won"], "total_lost_usdc": s["total_lost"], "sum_pnl_net_usdc": s["sum_pnl_net"],
                 "median_pnl_net_usdc": s["median_pnl_net"]} for n, s in summary["scopes"].items()]
        problems = [f"{k}={checks[k]}" for k in ("n_identity_failures", "n_rows_mismatch_saved", "n_volume_mismatch_saved",
                                                 "n_kept_not_usable") if checks[k]]
        problems += [f"sum identity fails in {n}" for n, s in summary["scopes"].items() if not s["sum_identity_ok"]]
        k = summary["scopes"]["kept"]
        return {
            "Why": "Owner request 2026-11-16: how much money each wallet won or lost. Descriptive, for a later tips page. "
                   "Not in the report or the paper.",
            "Input data": f"Real data, raw trades ({raw_glob()}) and the scope flags of {src}/markets.parquet. "
                          f"{checks['n_markets_in_scope']} markets in scope, {checks['n_usable']} with a usable winner, "
                          f"{checks['n_rows_usable']} fills in them.",
            "Output data": f"wallet_pnl.parquet ({con.execute('SELECT count(*) FROM wp').fetchone()[0]} rows, one per wallet x scope), "
                           f"pnl_summary.json, market_check.csv ({checks['n_markets_checked']} markets), fig_pnl_distribution.png.",
            "Result": f"Kept set: {k['n_wallets']} wallets, {k['n_winners']} winners, {k['n_losers']} losers. "
                      f"Short positions in kept markets: {checks['share_short_positions_kept']} of positions "
                      f"(mint or merge counter-legs are not modelled). "
                      + ("Checks: all passed.\n\n" if not problems else f"Checks failed: {', '.join(problems)}.\n\n")
                      + md_table(pd.DataFrame(rows)),
            "Figure": "![pnl distribution](fig_pnl_distribution.png)  Caption: wallets by net profit, symmetric-log bins. "
                      "Why: it shows how many wallets sit near zero and how long the tails are. Source: this run folder.",
            "Status": "ran" if not problems else "ran, check failures: " + ", ".join(problems),
        }

    run_stage(out, STAGE, "Net profit and loss per wallet from resolved markets.", work)


if __name__ == "__main__":
    main()
