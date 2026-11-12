"""Redraw the r3 paper figures with plain-word labels from the saved files of run 150310 (no model fit).

Usage (local, one core, saved JSON/CSV only):
    OMP_NUM_THREADS=1 timeout 300 uv run python code/fig_r3_paper.py \
        --r3 runs/150310_r3_review_fixes_v6 --macros papers/paper_mvp1/numbers.tex \
        --out runs/local_r3figs_v10

Why: the cluster figures show code names and bare n. The paper needs plain words (figures.md).
After drawing, the script compares every plotted gap, interval end and n with the RThree macros.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FuncFormatter, MultipleLocator
from scipy.special import expit, logit

from make_paper_numbers import count, pct2

__all__ = ["main"]

DARK, GREY, BAND = "#222222", "#888888", "#bbbbbb"
GAP_LABEL = "Net gap: mean of (outcome - price), USDC per share"
# Print widths: article 11pt, letter paper, 0.9 in margins -> linewidth 6.7 in (main.tex \\figorbox 0.8 / 0.55).
# Figures are drawn at print size so a font size in pt is the printed size (figures.md section 4: 7 pt or more).
W_WIDE, W_NARROW, FONT_PT, DPI = 0.8 * 6.7, 0.55 * 6.7, 7.5, 300
plt.rcParams.update({"font.size": FONT_PT, "figure.dpi": DPI})
FINE_GRID = np.linspace(0.02, 0.98, 49)  # same grid as code/r3_m5.py


def fmt_n(n: int) -> str:
    return f"{n:,}"


def save(fig: plt.Figure, out: Path, name: str) -> None:
    fig.savefig(out / name, dpi=DPI)
    plt.close(fig)


def forest(rows: list[tuple[str, dict[str, float]]], xlabel: str, out: Path, name: str,
           ylabel: str | None = None, tick_step: float | None = None, size=(W_WIDE, 3.1)) -> None:
    """One dot and one interval per row. Row label is already wrapped plain words."""
    fig, ax = plt.subplots(figsize=size, layout="constrained")
    for i, (_, r) in enumerate(rows):
        ax.errorbar(r["net_gap"], i, xerr=[[r["net_gap"] - r["ci_low"]], [r["ci_high"] - r["net_gap"]]],
                    fmt="o", color=DARK, capsize=3, label=r["legend"] if i == 0 else None)
    ax.axvline(0, color=GREY, ls="--", label="No gap")
    ax.set(yticks=range(len(rows)), yticklabels=[label for label, _ in rows], xlabel=xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    if tick_step:
        ax.xaxis.set_major_locator(MultipleLocator(tick_step))
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v + 0.0:.3f}".replace("-0.000", "0.000").replace("-", "\u2212")))
    ax.invert_yaxis()
    ax.grid(alpha=0.3)
    fig.legend(loc="outside upper center", ncol=2)
    save(fig, out, name)


def row(d: dict[str, Any], key: str = "") -> dict[str, float]:
    return {"net_gap": d[key + "net_gap"], "ci_low": d[key + "net_gap_ci_low"],
            "ci_high": d[key + "net_gap_ci_high"],
            "legend": "Net gap with 95% t interval"}


def draw_m1(r3: Path, out: Path, checks: list) -> None:
    rows = json.loads((r3 / "m1_results.json").read_text())["rows"]
    names = [("p_1d (main)", "Price 1 day before close\n(main)"),
             ("p_vwap", "VWAP, last 24 h"),
             ("p_1d on S_both", "Price 1 day before close,\nmarkets with both sides"),
             ("p_mid", "Trade-based midpoint"),
             ("p_ask", "Buyer-initiated trades"),
             ("p_bid", "Seller-initiated trades")]
    data = [(f"{label}\n(n={fmt_n(rows[k]['n'])})", row(rows[k])) for k, label in names]
    forest(data, GAP_LABEL, out, "fig_r3_m1_price_definition.png", tick_step=0.005, size=(W_WIDE, 3.7))
    for k, name in (("p_vwap", "MOneVwap"), ("p_mid", "MOneMid")):
        checks += [(f"{name}NetGap", pct2(rows[k]["net_gap"])), (f"{name}NetGapCiLow", pct2(rows[k]["net_gap_ci_low"])),
                   (f"{name}NetGapCiHigh", pct2(rows[k]["net_gap_ci_high"])), (f"{name}N", count(rows[k]["n"]))]


def draw_m2(r3: Path, out: Path, checks: list) -> None:
    res = json.loads((r3 / "m2_results.json").read_text())
    bins = pd.read_csv(r3 / "m2_bins_yes_no.csv")
    lo, hi = bins["mean_price"] + bins["z_low"], bins["mean_price"] + bins["z_high"]  # saved as gap-scale ends (D-047)
    fig, ax = plt.subplots(figsize=(W_NARROW, W_NARROW), layout="constrained")
    ax.plot([0, 1], [0, 1], color=GREY, ls="--", label="Perfect calibration")
    err = np.clip(np.vstack([bins["observed_rate"] - lo, hi - bins["observed_rate"]]), 0, None)
    ax.errorbar(bins["mean_price"], bins["observed_rate"], yerr=err, fmt="o", ms=4, capsize=3, color=DARK,
                label=f"Markets labelled Yes/No (n={fmt_n(res['yes_no_n'])}), 95% z interval")
    ax.set(xlabel="Mean Yes price in bin (USDC per share)", ylabel="Observed Yes rate", xlim=(0, 1), ylim=(0, 1))
    ax.grid(alpha=0.3)
    fig.legend(loc="outside upper center", ncol=1)
    save(fig, out, "fig_r3_m2_yes_reliability.png")
    checks.append(("MTwoYesNoN", count(int(bins["n"].sum()))))


def draw_m3(r3: Path, out: Path, checks: list) -> None:
    prox = json.loads((r3 / "m3_bootstrap.json").read_text())["proxies"]
    names = [("k0_market", "Each market alone"), ("k1_slug_stem", "Slug stem (3 words)"),
             ("k2_category_close_hour", "Topic x close hour")]
    data = [(f"{label}\n({fmt_n(prox[k]['n_clusters'])} clusters)", row(prox[k])) for k, label in names]
    for d in data:
        d[1]["legend"] = "Net gap with bootstrap 95% interval"
    forest(data, "Net gap: mean of (outcome - price 1 day before close), USDC per share", out,
           "fig_r3_m3_cluster_bootstrap.png", tick_step=0.004)
    for k, name in (("k1_slug_stem", "MThreeKOne"), ("k2_category_close_hour", "MThreeKTwo")):
        checks += [(f"{name}NClusters", count(prox[k]["n_clusters"])), (f"{name}NetGapCiLow", pct2(prox[k]["net_gap_ci_low"])),
                   (f"{name}NetGapCiHigh", pct2(prox[k]["net_gap_ci_high"]))]


def draw_m5(r3: Path, out: Path, checks: list) -> None:
    fit = json.loads((r3 / "m5_calibration_fit.json").read_text())
    gap = lambda p: expit(fit["a"] + fit["b"] * logit(p)) - p  # same formula as code/r3_m5.py implied_gap
    grid = fit["delta_table"]
    px = np.array([g["price"] for g in grid])
    lo, hi, mid = (np.array([g[k] for g in grid]) for k in ("ci_low", "ci_high", "delta"))
    fig, ax = plt.subplots(figsize=(W_WIDE, 3.2), layout="constrained")
    ax.errorbar(px, mid, yerr=[mid - lo, hi - mid], fmt="none", ecolor=BAND, elinewidth=6, capsize=0,
                label="Cluster bootstrap 95% interval (7 prices)")
    ax.plot(FINE_GRID, gap(FINE_GRID), color=DARK, label="Implied gap from the fit")
    ax.axhline(0, color=GREY, ls="--", label="Calibrated")
    half = json.loads((r3 / "m1_results.json").read_text())["mean_h"]  # practical line: mean half spread
    ax.axhline(half, color=DARK, ls=":", label="Practical line: \u00b1 mean half spread")
    ax.axhline(-half, color=DARK, ls=":")
    ax.set(xlabel="Price 1 day before close (USDC per share)", ylabel="Implied gap: fitted probability - price")
    ax.grid(alpha=0.3)
    fig.legend(loc="outside upper center", ncol=2)
    save(fig, out, "fig_r3_m5_implied_gap.png")
    checks.append(("MFiveMaxAbsDelta", pct2(float(np.max(np.abs(mid))))))
    if not np.allclose(gap(px), mid, atol=1e-9):
        raise ValueError("fit curve differs from saved delta_table")


def draw_peer(r3: Path, out: Path, checks: list) -> None:
    a = json.loads((r3 / "peer_a_results.json").read_text())
    names = [("low", "low"), ("mid", "middle"), ("high", "high")]
    data = [(f"{label}\n(n={fmt_n(a[f'tercile_{t}_n'])})", row(a, f"tercile_{t}_")) for t, label in names]
    forest(data, GAP_LABEL, out, "fig_r3_peer_a_volume.png", ylabel="Volume tercile, until 1 day before close",
           tick_step=0.005)
    for t, label in names:
        checks += [(f"PeerA{t.capitalize()}NetGap", pct2(a[f"tercile_{t}_net_gap"])), (f"PeerA{t.capitalize()}N", count(a[f"tercile_{t}_n"])),
                   (f"PeerA{t.capitalize()}NetGapCiLow", pct2(a[f"tercile_{t}_net_gap_ci_low"])),
                   (f"PeerA{t.capitalize()}NetGapCiHigh", pct2(a[f"tercile_{t}_net_gap_ci_high"]))]
    b = json.loads((r3 / "peer_b_results.json").read_text())
    periods = list(dict.fromkeys(b["year_to_period"].values()))
    data = [(f"{p}\n(n={fmt_n(b[f'period_{p}_n'])})", row(b, f"period_{p}_")) for p in periods]
    forest(data, GAP_LABEL, out, "fig_r3_peer_b_period.png", ylabel="Close year", tick_step=0.005)
    for i, p in enumerate(periods):
        w = ["One", "Two", "Three"][i]
        checks += [(f"PeerBPeriod{w}NetGap", pct2(b[f"period_{p}_net_gap"])), (f"PeerBPeriod{w}N", count(b[f"period_{p}_n"])),
                   (f"PeerBPeriod{w}NetGapCiLow", pct2(b[f"period_{p}_net_gap_ci_low"])),
                   (f"PeerBPeriod{w}NetGapCiHigh", pct2(b[f"period_{p}_net_gap_ci_high"]))]


def draw_m4(r3: Path, out: Path, checks: list) -> None:
    t = pd.read_csv(r3 / "m4_kept_vs_dropped.csv", usecols=["group", "n", "share_of_total"])
    total = int(json.loads((r3 / "m4_results.json").read_text())["n_in_scope"])
    label = {"kept": "Kept", "updown": "Up/Down", "no_outcome": "No winner\nlabel", "no_price": "No price",
             "stale_price": "Stale price", "below_min_trades": "Under\n10 trades",
             "eligible_dropped_pooled": "All eligible\ndropped"}
    fig, ax = plt.subplots(figsize=(W_WIDE, 3.0), layout="constrained")
    ax.bar([label[g] for g in t["group"]], t["share_of_total"], color="#555555",
           label=f"Share of {fmt_n(total)} in-scope markets")
    ax.set(xlabel="Group (kept or first failing rule)", ylabel="Share of markets")
    ax.grid(alpha=0.3, axis="y")
    fig.legend(loc="outside upper center", ncol=1)
    save(fig, out, "fig_r3_m4_kept_vs_dropped.png")
    if not np.allclose(t["n"] / total, t["share_of_total"]):
        raise ValueError("saved share_of_total differs from n / n_in_scope")


def verify(macros: Path, checks: list[tuple[str, str]]) -> None:
    """Every plotted gap, interval end and n must equal its RThree macro, text for text."""
    tex = macros.read_text()
    bad = []
    for name, shown in checks:
        m = re.search(r"\\newcommand\{\\RThree" + name + r"\}\{(.*)\}\n", tex)
        if m is None or m.group(1) != shown:
            bad.append((name, shown, m.group(1) if m else None))
    print(f"macro check: {len(checks) - len(bad)} of {len(checks)} plotted numbers equal their RThree macro")
    if bad:
        raise ValueError(f"mismatch: {bad}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--r3", required=True, type=Path)
    ap.add_argument("--macros", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    checks: list[tuple[str, str]] = []
    for fn in (draw_m1, draw_m2, draw_m3, draw_m5, draw_peer, draw_m4):
        fn(a.r3, a.out, checks)
    verify(a.macros, checks)


if __name__ == "__main__":
    main()
