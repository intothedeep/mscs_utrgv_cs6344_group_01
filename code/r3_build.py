"""Robustness v3, gate and raw pass (prereg_review_fixes.md 0.2).

Rebuilds the market table with the unchanged v3 build code, checks it against the saved markets.parquet of the base run,
and stops ("gate failed: <check>") when a check fails. Then saves the inputs the item stages read:
  r3_markets.parquet      all in-scope markets: drop_reason, kept, p_1d, y, T, slug, label1, label2, volume before T - 1 day
  r3_trades_window.parquet kept-market trades with T - 2 days <= ts <= T - 1 day (M1), duplicates kept
"""
import pandas as pd

from build_tables import build_market_table
from common import build_market_set, connect, md_table, raw_glob, run_stage, write_json, write_manifest
from q1_calibration import analyze
from r3_common import stage_args

STAGE = "r3_build"
TS_EXPR = "coalesce(to_timestamp(TRY_CAST({c} AS BIGINT)), TRY_CAST({c} AS TIMESTAMP))"   # as common.build_market_set


def fail(gate: dict, check: str, out) -> None:
    gate["passed"], gate["failed_check"] = False, check
    write_json(out / "r3_gate.json", gate)
    raise ValueError(f"gate failed: {check}")


def run_gate(rebuilt: pd.DataFrame, saved: pd.DataFrame, params: dict, out) -> dict:
    gate: dict = {"passed": None}
    r_kept = set(rebuilt.loc[rebuilt["kept"], "market_id"])
    s_kept = set(saved.loc[saved["kept"], "market_id"])
    gate |= {"n_in_scope": len(rebuilt), "n_kept_rebuilt": len(r_kept), "n_kept_saved": len(s_kept)}
    if len(rebuilt) != int(params["n_in_scope_expected"]):
        fail(gate, f"n_in_scope {len(rebuilt)} != {params['n_in_scope_expected']}", out)
    if r_kept != s_kept or len(r_kept) != int(params["n_kept_expected"]):
        fail(gate, "kept set differs from markets.parquet of the base run", out)
    both = rebuilt.merge(saved, on="market_id", suffixes=("_r", "_s"))
    null_mismatch = int((both["p_1d_r"].isna() != both["p_1d_s"].isna()).sum())
    diff = (both["p_1d_r"] - both["p_1d_s"]).abs().dropna()
    gate |= {"p_1d_null_mismatch": null_mismatch, "p_1d_max_abs_diff": float(diff.max()) if len(diff) else 0.0}
    if null_mismatch or gate["p_1d_max_abs_diff"] > float(params["gate_p1d_abs_tol"]):
        fail(gate, "rebuilt p_1d differs from the saved p_1d", out)
    kept = rebuilt[rebuilt["kept"]].assign(y=lambda d: d["y"].astype(int))
    chi2 = analyze(kept[["market_id", "p_1d", "y"]], int(params["n_bins"]), float(params["alpha"]))[0]["chi2_gof"]["chi2"]
    gate["chi2_rebuilt"] = chi2
    dec = int(params["gate_chi2_decimals"])
    if round(chi2, dec) != round(float(params["gate_chi2_main"]), dec):
        fail(gate, f"Q1 chi-square {chi2:.6f} != {params['gate_chi2_main']:.6f} to {dec} decimals", out)
    gate["passed"] = True
    return gate


def save_inputs(con, out) -> dict:
    """Materialize the item inputs while `raw`, `tr`, `mkts` and `markets` exist."""
    ts = TS_EXPR.format(c="block_timestamp")
    con.execute("""
        CREATE TABLE r3_markets AS
        SELECT m.market_id, m.drop_reason, m.kept, m.p_1d, m.y, m.category_refined, m.opens_at, m.close_at, m."T",
               m.n_trades, m.n_trades_before_T1d, m.volume_usdc, mk.market_slug, mk.label1, lab.label2,
               vol.volume_before_T1d
        FROM markets m
        JOIN mkts mk ON mk.condition_id = m.market_id
        LEFT JOIN (SELECT condition_id, max(outcome_label) FILTER (WHERE CAST(outcome_seq AS BIGINT) = 2) AS label2
                   FROM raw GROUP BY 1) lab ON lab.condition_id = m.market_id
        LEFT JOIN (SELECT t.condition_id, sum(t.usdc_amount) AS volume_before_T1d
                   FROM tr t JOIN markets m2 ON m2.market_id = t.condition_id
                   WHERE t.ts <= m2."T" - INTERVAL 1 DAY GROUP BY 1) vol ON vol.condition_id = m.market_id""")
    con.execute(f"COPY (SELECT * FROM r3_markets ORDER BY market_id) TO '{out}/r3_markets.parquet' (FORMAT PARQUET)")
    con.execute(f"""
        COPY (SELECT r.condition_id AS market_id, r.ts, r.price, r.p_event, r.taker_direction, r.outcome_seq, r.usdc_amount
              FROM (SELECT condition_id, {ts} AS ts, price, p_event, taker_direction,
                           CAST(outcome_seq AS BIGINT) AS outcome_seq, usdc_amount FROM raw) r
              JOIN (SELECT market_id, "T" FROM markets WHERE kept) k ON k.market_id = r.condition_id
              WHERE r.ts >= k."T" - INTERVAL 2 DAY AND r.ts <= k."T" - INTERVAL 1 DAY
              ORDER BY r.condition_id, r.ts, r.price, r.usdc_amount)
        TO '{out}/r3_trades_window.parquet' (FORMAT PARQUET)""")
    n_win = con.execute(f"SELECT count(*) FROM read_parquet('{out}/r3_trades_window.parquet')").fetchone()[0]
    return {"n_window_trades": int(n_win)}


def main() -> None:
    _, out, src, params = stage_args()

    def work() -> dict[str, str]:
        con = connect()
        build_market_set(con, params)
        build_market_table(con, params)
        rebuilt = con.execute("SELECT market_id, p_1d, y, kept FROM markets").df()
        saved = pd.read_parquet(src / "markets.parquet", columns=["market_id", "p_1d", "kept"])
        gate = run_gate(rebuilt, saved, params, out)
        write_json(out / "r3_gate.json", gate)
        extra = save_inputs(con, out)
        write_manifest(out, params, gate | extra, __file__, STAGE)
        return {
            "Why": "Every v3 item reads the kept set and p_1d of the base run. The gate proves the rebuild equals it before any item runs.",
            "Input data": f"Raw trades ({raw_glob()}), base run markets.parquet ({gate['n_in_scope']} markets). Real data.",
            "Output data": f"r3_markets.parquet ({gate['n_in_scope']} rows), r3_trades_window.parquet ({extra['n_window_trades']} rows), r3_gate.json",
            "Result": md_table(pd.DataFrame([{"check": k, "value": v} for k, v in gate.items()])),
        }

    run_stage(out, STAGE, "Gate and raw pass for the robustness v3 items.", work)


if __name__ == "__main__":
    main()
