"""Robustness R2 (D-013): the price path in the last day. How far does the price move from p_1d (T - 1 day) to p_T?

p_T = mean p_event of the trades at the last timestamp strictly before T (same tie rule as p_1d).
Window = T - 1 day < ts < T. No trade in the window: p_T = p_1d. Descriptive, no verdict. Criteria: analysis/prereg_robustness.md.
build_tables.py does not keep the trade table, so this stage reads the raw trades of the kept markets once more.
"""
import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

from common import connect, load_params, md_table, raw_glob, run_stage, write_json, write_manifest
from q1a_category import group_categories

STAGE = "r2_price_path"


def load_window(con, kept: pd.DataFrame) -> pd.DataFrame:
    """Per kept market: p_T and the trade count in the window T - 1 day < ts < T (markets without a trade are absent)."""
    con.register("kept", kept[["market_id", "T"]])
    con.execute(f"""
        CREATE VIEW raw AS SELECT * FROM read_parquet('{raw_glob()}', union_by_name=true)""")
    return con.execute("""
        WITH win AS (
          SELECT k.market_id, w.ts, w.p_event
          FROM (SELECT condition_id,
                       -- same timestamp parse as common.build_market_set
                       coalesce(to_timestamp(TRY_CAST(block_timestamp AS BIGINT)),
                                TRY_CAST(block_timestamp AS TIMESTAMP)) AS ts, p_event FROM raw) w
          JOIN kept k ON w.condition_id = k.market_id
          WHERE w.ts > k."T" - INTERVAL 1 DAY AND w.ts < k."T"),
        last AS (SELECT market_id, max(ts) AS p_ts, count(*) AS n_window FROM win GROUP BY 1)
        SELECT l.market_id, avg(w.p_event) AS p_T, l.n_window
        FROM last l JOIN win w ON w.market_id = l.market_id AND w.ts = l.p_ts
        GROUP BY l.market_id, l.n_window""").fetchdf()


def paired_diff(brier_1d: pd.Series, brier_t: pd.Series, alpha: float, with_test: bool) -> dict:
    """Mean of (Brier at p_T minus Brier at p_1d) with a t interval. p and Cohen's d_z only when with_test."""
    d = (brier_t - brier_1d).to_numpy()
    n = len(d)
    if n < 2:
        return {"n": n, "mean_diff": float(d.mean()) if n else None}
    mean, sd = float(d.mean()), float(d.std(ddof=1))
    half = float(stats.t.ppf(1 - alpha / 2, n - 1) * sd / np.sqrt(n)) if sd > 0 else 0.0
    res = {"n": n, "brier_1d": float(brier_1d.mean()), "brier_T": float(brier_t.mean()), "mean_diff": mean,
           "ci_low": mean - half, "ci_high": mean + half}
    if with_test and sd > 0:
        t = mean / (sd / np.sqrt(n))
        res |= {"t": float(t), "df": n - 1, "p": float(2 * stats.t.sf(abs(t), n - 1)), "cohens_dz": mean / sd}
    return res


def summarize_group(g: pd.DataFrame, thresholds: list[float], alpha: float) -> dict:
    a = g["abs_delta"]
    row = {"n": len(g), "median_abs_delta": float(a.median()), "share_no_trade": float((g["n_window"] == 0).mean()),
           "share_crossing": float(g["crosses_half"].mean())}
    row |= {f"share_abs_delta_ge_{t:.2f}": float((a >= t).mean()) for t in thresholds}
    return row | {"brier": paired_diff(g["brier_1d"], g["brier_T"], alpha, with_test=False)}


def draw_ecdf(df: pd.DataFrame, out: Path) -> None:
    fig, ax = plt.subplots(figsize=(6, 4), layout="constrained")
    x = np.sort(df["abs_delta"].to_numpy())
    ax.step(x, np.arange(1, len(x) + 1) / len(x), where="post", color="#222222", label=f"All kept markets (n={len(x)})")
    ax.set(xlabel="Absolute price change |p_T - p_1d| (USDC per share)", ylabel="ECDF (share of markets)", xlim=(0, 1))
    ax.grid(alpha=0.3)
    fig.legend(loc="outside upper center", ncol=1)
    fig.savefig(out / "fig_r2_price_path.png", dpi=150)
    plt.close(fig)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--params", required=True)
    ap.add_argument("--out", default=".")
    args = ap.parse_args()
    out, params = Path(args.out), load_params(args.params)
    alpha, thresholds = float(params["alpha"]), [float(t) for t in params["robust_delta_thresholds"]]
    quantiles = [float(q) for q in params["robust_quantiles"]]

    def work() -> dict[str, str]:
        m = pd.read_parquet(out / "markets.parquet")
        kept = m[m["kept"]][["market_id", "T", "p_1d", "y", "category_refined"]].sort_values("market_id").reset_index(drop=True)
        win = load_window(connect(), kept)
        df = kept.merge(win, on="market_id", how="left")
        df["n_window"] = df["n_window"].fillna(0).astype(int)
        df["p_T"] = df["p_T"].fillna(df["p_1d"])   # no trade in the window: the last price before T is p_1d
        df["delta"] = df["p_T"] - df["p_1d"]
        df["abs_delta"] = df["delta"].abs()
        df["crosses_half"] = (df["p_1d"] >= 0.5) != (df["p_T"] >= 0.5)
        df["brier_1d"] = (df["p_1d"] - df["y"]) ** 2
        df["brier_T"] = (df["p_T"] - df["y"]) ** 2
        df, cat_counts = group_categories(df, int(params["min_category_n"]))
        df[["market_id", "category_group", "p_1d", "p_T", "delta", "n_window", "crosses_half", "y"]].to_csv(
            out / "r2_markets.csv", index=False)   # one row per kept market, sorted by market_id

        a = df["abs_delta"]
        overall = summarize_group(df, thresholds, alpha)
        overall["quantiles_abs_delta"] = {f"q{q:g}": float(a.quantile(q)) for q in quantiles} | {"max": float(a.max())}
        overall["n_window_trades"] = {"median": float(df["n_window"].median()),
                                      "q0.9": float(df["n_window"].quantile(0.9)), "max": int(df["n_window"].max())}
        overall["brier"] = paired_diff(df["brier_1d"], df["brier_T"], alpha, with_test=True)
        traded = df[df["n_window"] > 0]
        overall["brier_traded_only"] = paired_diff(traded["brier_1d"], traded["brier_T"], alpha, with_test=True)
        by_cat = {c: summarize_group(g, thresholds, alpha) for c, g in df.groupby("category_group")}
        write_json(out / "r2_results.json", {"overall": overall, "by_category": by_cat,
                                              "category_counts_before_merge": cat_counts.to_dict()})
        draw_ecdf(df, out)
        write_manifest(out, params, {"overall": overall, "n_categories": len(by_cat)}, __file__, STAGE)

        b, bt = overall["brier"], overall["brier_traded_only"]
        keys = [f"share_abs_delta_ge_{t:.2f}" for t in thresholds]
        tab = pd.DataFrame({"metric": ["n markets", "median abs delta", *keys, "share crossing 0.5", "share no trade in window",
                                       "Brier at p_1d", "Brier at p_T", "mean diff (p_T minus p_1d)", "95% CI", "p", "Cohen's d_z"],
                            "all kept": [overall["n"], overall["median_abs_delta"], *[overall[k] for k in keys],
                                         overall["share_crossing"], overall["share_no_trade"], b["brier_1d"], b["brier_T"],
                                         b["mean_diff"], f"{b['ci_low']:.4g} to {b['ci_high']:.4g}", b.get("p"), b.get("cohens_dz")],
                            "with a trade in window": [bt["n"], float(traded["abs_delta"].median()),
                                                       *[float((traded["abs_delta"] >= t).mean()) for t in thresholds],
                                                       float(traded["crosses_half"].mean()), 0.0, bt["brier_1d"], bt["brier_T"],
                                                       bt["mean_diff"], f"{bt['ci_low']:.4g} to {bt['ci_high']:.4g}",
                                                       bt.get("p"), bt.get("cohens_dz")]})
        cat_tab = pd.DataFrame([{"category": c, "n": r["n"], "median_abs_delta": r["median_abs_delta"], **{k: r[k] for k in keys},
                                 "crossing": r["share_crossing"], "no_trade": r["share_no_trade"],
                                 "brier_1d": r["brier"].get("brier_1d"), "brier_T": r["brier"].get("brier_T"),
                                 "mean_diff": r["brier"]["mean_diff"]} for c, r in by_cat.items()]).sort_values("category")
        qs = ", ".join(f"{k} {v:.3f}" for k, v in overall["quantiles_abs_delta"].items())
        return {
            "Why": "D-013: how far does the price move between p_1d and the last trade before T?",
            "Input data": f"markets.parquet: {len(df)} kept markets. Raw trades in the window T - 1 day < ts < T "
                          f"({raw_glob()}). Real data.",
            "Output data": "r2_markets.csv (one row per kept market), r2_results.json, fig_r2_price_path.png",
            "Result": md_table(tab) + f"\n\nQuantiles of abs(delta): {qs}.\n\nBy category (descriptive, no p-values):\n\n"
                      + md_table(cat_tab),
            "Figure": "![r2](fig_r2_price_path.png)  Caption: ECDF of the absolute price change from p_1d to p_T. "
                      "Why: a curve near 1 at small values means p_1d is close to the last price. Source: this run folder.",
        }

    run_stage(out, STAGE, "R2: price path from T - 1 day to the last trade before T.", work)


if __name__ == "__main__":
    main()
