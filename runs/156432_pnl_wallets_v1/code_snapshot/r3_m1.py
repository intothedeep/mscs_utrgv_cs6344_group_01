"""Robustness v3, M1: price definition (prereg_review_fixes.md section 1).

Does the Q1 gap survive when p_1d (mean trade price at the last timestamp) is replaced by a volume-weighted price (p_vwap,
primary) or a trade-based midpoint (p_mid = mean of the last taker-buy and the last taker-sell price)? Descriptive, no verdict.
Reads r3_markets.parquet and r3_trades_window.parquet from r3_build.py.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from common import md_table, run_stage, write_json, write_manifest
from r3_common import bin_of, flat, load_kept, load_main_q1, main_net_gap, q1_row, row_line, stage_args, t_interval

STAGE = "r3_m1"
SIDE_PLUS = {(1, "BUY"), (2, "SELL")}
SIDE_MINUS = {(1, "SELL"), (2, "BUY")}


def side_of(win: pd.DataFrame) -> pd.Series:
    """+1 / -1 aggressor side on the outcome 1 scale, 0 for any other value (counted)."""
    key = list(zip(win["outcome_seq"], win["taker_direction"]))
    return pd.Series([1 if k in SIDE_PLUS else -1 if k in SIDE_MINUS else 0 for k in key], index=win.index)


def last_ts_mean(win: pd.DataFrame, mask: pd.Series) -> pd.Series:
    """Mean p_event at the last timestamp of the masked trades, per market (same tie rule as p_1d)."""
    sub = win[mask]
    last = sub.groupby("market_id")["ts"].transform("max")
    return sub[sub["ts"] == last].groupby("market_id")["p_event"].mean()


def build_prices(win: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    win = win.copy()
    win["s"] = side_of(win)
    ok = win["price"] > 0
    counts = {"n_window_trades": len(win), "n_price_le_0": int((~ok).sum()), "n_side_0": int((win["s"] == 0).sum())}
    pos = win[ok].assign(shares=lambda d: d["usdc_amount"] / d["price"])
    pos["pe_shares"] = pos["p_event"] * pos["shares"]
    g = pos.groupby("market_id")
    prices = pd.DataFrame({"p_vwap": g["pe_shares"].sum() / g["shares"].sum(), "n_trades_W": win.groupby("market_id").size()})
    prices["p_ask"] = last_ts_mean(win, win["s"] == 1)
    prices["p_bid"] = last_ts_mean(win, win["s"] == -1)
    return prices.reset_index(), counts


def paired(p_1d: pd.Series, p_alt: pd.Series, alpha: float) -> dict:
    """Mean of per-market (p_1d - p_alt) = net gap(alt) - net gap(p_1d), with t interval and d_z."""
    r = t_interval((p_1d - p_alt).to_numpy(), alpha)
    return {"mean_diff": r["mean"], "ci_low": r["ci_low"], "ci_high": r["ci_high"], "d_z": r["d_z"], "n": r["n"]}


def read_outcome(vwap: dict, mid: dict | None, same_set: dict | None) -> str:
    """Section 1.5 reading rule. `mid` is None when the sign gate skipped p_mid."""
    if mid is None:
        return "VWAP only: A" if vwap["net_gap_ci_high"] < 0 else "VWAP only: B"
    if vwap["net_gap_ci_high"] < 0 and mid["net_gap_ci_high"] < 0:
        return "A"
    if mid["net_gap_ci_high"] >= 0 and same_set["net_gap_ci_high"] < 0:
        return "B"
    return "C"


def draw(rows: dict[str, dict], out) -> None:
    fig, ax = plt.subplots(figsize=(7, 4), layout="constrained")
    names = list(rows)
    for i, nm in enumerate(names):
        r = rows[nm]
        ax.errorbar(r["net_gap"], i, xerr=[[r["net_gap"] - r["net_gap_ci_low"]], [r["net_gap_ci_high"] - r["net_gap"]]],
                    fmt="o", color="#222222", capsize=3, label="Net gap with 95% t interval" if i == 0 else None)
    ax.axvline(0, color="#888888", ls="--", label="No gap")
    ax.set(yticks=range(len(names)), yticklabels=[f"{n} (n={rows[n]['n']})" for n in names],
           xlabel="Net gap mean(y - price) (USDC per share)")
    ax.invert_yaxis()
    ax.grid(alpha=0.3)
    fig.legend(loc="outside upper center", ncol=2)
    fig.savefig(out / "fig_r3_m1_price_definition.png", dpi=150)
    plt.close(fig)


def main() -> None:
    _, out, src, params = stage_args()
    alpha, n_bins = float(params["alpha"]), int(params["n_bins"])

    def work() -> dict[str, str]:
        kept = load_kept(out)
        main_res = load_main_q1(src)
        gap0 = main_net_gap(kept)
        prices, counts = build_prices(pd.read_parquet(out / "r3_trades_window.parquet"))
        df = kept.merge(prices, on="market_id", how="left")
        df["n_trades_W"] = df["n_trades_W"].fillna(0).astype(int)

        med_raw = float((df["p_ask"] - df["p_bid"]).median())   # NaN rows are skipped: median over S_both
        n_both = int(df[["p_ask", "p_bid"]].notna().all(axis=1).sum())
        if n_both == 0 or med_raw == 0 or np.isnan(med_raw):
            gate, flipped = "skipped", False
        elif med_raw < 0:
            gate, flipped = "flipped", True
            df[["p_ask", "p_bid"]] = df[["p_bid", "p_ask"]].to_numpy()   # side sign reversed: the two sets swap
        else:
            gate, flipped = "validated", False
        has_mid = gate != "skipped"
        if has_mid:
            df["p_mid"] = (df["p_ask"] + df["p_bid"]) / 2
            df["h"] = (df["p_ask"] - df["p_bid"]) / 2
        else:
            df["p_mid"], df["h"] = np.nan, np.nan
        if not has_mid:
            df["p_ask"], df["p_bid"] = np.nan, np.nan   # side not validated: these rows are skipped

        rows: dict[str, dict] = {}
        bins: dict[str, pd.DataFrame] = {}

        def add(name: str, sub: pd.DataFrame, price: str) -> None:
            rows[name], bins[name] = q1_row(sub, price, alpha, n_bins, main_res, gap0)

        add("p_1d (main)", df, "p_1d")
        vw = df[df["p_vwap"].notna()]
        add("p_vwap", vw, "p_vwap")
        both = df[df["p_mid"].notna()]
        if has_mid:
            add("p_1d on S_both", both, "p_1d")
            add("p_mid", both, "p_mid")
            add("p_ask", df[df["p_ask"].notna()], "p_ask")
            add("p_bid", df[df["p_bid"].notna()], "p_bid")
        for col in ["p_1d", "p_vwap", "p_mid"]:
            df[f"bin_{col}"] = np.where(df[col].notna(), bin_of(df[col].fillna(0).to_numpy(), n_bins), -1)
        df[["market_id", "p_1d", "p_vwap", "p_ask", "p_bid", "p_mid", "h", "n_trades_W", "y",
            "bin_p_1d", "bin_p_vwap", "bin_p_mid"]].to_csv(out / "m1_prices_by_market.csv", index=False)

        diffs = {"vwap_minus_1d": paired(vw["p_1d"], vw["p_vwap"], alpha)}
        h_stats = None
        if has_mid:
            diffs["mid_minus_1d_on_S_both"] = paired(both["p_1d"], both["p_mid"], alpha)
            h_stats = t_interval(both["h"].to_numpy(), alpha) | {"median": float(both["h"].median())}
        outcome = read_outcome(rows["p_vwap"], rows.get("p_mid"), rows.get("p_1d on S_both"))
        n_total = len(kept)
        coverage = {"n_vwap": len(vw), "n_S_both": len(both), "share_S_both": len(both) / n_total,
                    "n_ask_only": int((df["p_ask"].notna() & df["p_bid"].isna()).sum()),
                    "n_bid_only": int((df["p_bid"].notna() & df["p_ask"].isna()).sum()),
                    "n_vwap_missing": n_total - len(vw)}
        caveat = has_mid and coverage["share_S_both"] < float(params["m1_subset_caveat_share"])
        side_line = None
        if h_stats:
            side_line = {"abs_net_gap_p1d": abs(rows["p_1d (main)"]["net_gap"]), "mean_h": h_stats["mean"],
                         "gap_within_half_spread": abs(rows["p_1d (main)"]["net_gap"]) <= h_stats["mean"]}
        results = {"sign_gate": gate, "sign_flipped": flipped, "median_ask_minus_bid_raw": med_raw, "outcome": outcome,
                   "subset_caveat": bool(caveat), "mean_h": h_stats["mean"] if h_stats else None,
                   "h": h_stats, "side_line": side_line, "coverage": coverage, "counts": counts, "paired": diffs,
                   "rows": rows} | flat("cov", coverage)
        for nm, r in rows.items():
            results |= flat(nm.split(" ")[0] + ("_same" if "S_both" in nm else ""), r)
        write_json(out / "m1_results.json", results)
        draw(rows, out)
        write_manifest(out, params, {k: v for k, v in results.items() if k != "rows"}, __file__, STAGE)
        tab = pd.DataFrame([row_line(n, r) for n, r in rows.items()])
        pair_tab = pd.DataFrame([{"pair": k, **v} for k, v in diffs.items()])
        return {
            "Why": "M1: the reviewer says half the bid-ask spread could explain the net gap. p_vwap and a trade-based p_mid test that.",
            "Input data": f"{n_total} kept markets (r3_markets.parquet) and {counts['n_window_trades']} kept-market trades in "
                          f"T - 2 days <= ts <= T - 1 day. Real data. p_mid is a trade-based proxy, not a quote midpoint.",
            "Output data": "m1_prices_by_market.csv, m1_results.json, fig_r3_m1_price_definition.png",
            "Result": f"Sign gate: {gate} (median p_ask - p_bid on S_both {med_raw:.6f}). Reading: {outcome}"
                      + (" (on the subset with trades on both sides)" if caveat else "") + ".\n\n" + md_table(tab)
                      + "\n\nPaired difference mean(p_1d - p_alt):\n\n" + md_table(pair_tab)
                      + f"\n\nCoverage: {coverage}. Counts: {counts}. Half-spread proxy h: {h_stats}. Side line: {side_line}.",
            "Figure": "![m1](fig_r3_m1_price_definition.png)  Caption: net gap under each price definition with its 95% t interval. "
                      "Why: an interval left of 0 under p_vwap and p_mid means the gap is not a price-rule artifact. Source: this run folder.",
        }

    run_stage(out, STAGE, "M1: price definition (VWAP and trade-based midpoint).", work)


if __name__ == "__main__":
    main()
