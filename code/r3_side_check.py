"""Robustness v3, first step: do the side columns mean what M1 assumes? (prereg_review_fixes.md 1.1, 1.3)

Cross-tabulates taker_direction x outcome_seq x D over the whole raw data, and the share of trades where p_event equals
price (outcome 1) or 1 - price (outcome 2). STOPS (exit 1) when the non-null taker_direction values are not exactly
{BUY, SELL} on the trades of outcome_seq 1 and 2. D has no documented meaning: its crosstab is reported, not tested.
"""

import pandas as pd

from common import connect, md_table, raw_glob, run_stage, write_json, write_manifest
from r3_common import stage_args

STAGE = "r3_side_check"
EXPECTED_SIDES = {"BUY", "SELL"}


def crosstab(con, tol: float) -> pd.DataFrame:
    return con.execute(f"""
        SELECT taker_direction, CAST(outcome_seq AS BIGINT) AS outcome_seq, CAST("D" AS BIGINT) AS "D", count(*) AS n,
               sum(CASE WHEN abs(p_event - CASE WHEN CAST(outcome_seq AS BIGINT) = 1 THEN price ELSE 1 - price END) <= {tol}
                        THEN 1 ELSE 0 END) AS n_p_event_consistent
        FROM read_parquet('{raw_glob()}', union_by_name=true)
        GROUP BY ALL ORDER BY ALL""").df()


def main() -> None:
    _, out, _, params = stage_args()

    def work() -> dict[str, str]:
        ct = crosstab(connect(), float(params["m1_p_event_tol"]))
        ct.to_csv(out / "r3_side_crosstab.csv", index=False)
        seqs = ct[ct["outcome_seq"].isin([1, 2])]
        values = set(seqs["taker_direction"].dropna().unique())
        n12 = int(seqs["n"].sum())
        res = {"taker_direction_values": sorted(map(str, values)), "n_trades_seq12": n12,
               "n_trades_other_seq": int(ct["n"].sum() - n12),
               "n_taker_direction_null": int(seqs.loc[seqs["taker_direction"].isna(), "n"].sum()),
               "share_p_event_consistent": float(seqs["n_p_event_consistent"].sum() / n12),
               "d_values": sorted(int(v) for v in ct["D"].dropna().unique()), "mapping_holds": values == EXPECTED_SIDES}
        write_json(out / "r3_side_check.json", res)
        write_manifest(out, params, res, __file__, STAGE)
        if not res["mapping_holds"]:
            print(f"STOP: side mapping does not hold. taker_direction values {sorted(map(str, values))}, expected {sorted(EXPECTED_SIDES)}.")
            raise ValueError(f"side mapping does not hold: taker_direction values {sorted(map(str, values))}")
        return {
            "Why": "M1 maps (taker_direction, outcome_seq) to the aggressor side on the outcome 1 scale. The mapping needs BUY and SELL.",
            "Input data": f"Raw trades ({raw_glob()}), {n12} trades with outcome_seq 1 or 2. Real data.",
            "Output data": "r3_side_crosstab.csv, r3_side_check.json",
            "Result": f"taker_direction values {res['taker_direction_values']}. D values {res['d_values']} (meaning not documented, "
                      f"not tested). p_event equals price or 1 - price in {res['share_p_event_consistent']:.6f} of trades.\n\n"
                      + md_table(ct.head(40)),
        }

    run_stage(out, STAGE, "Check the side columns before M1.", work)


if __name__ == "__main__":
    main()
