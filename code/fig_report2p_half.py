"""Redraw three report figures at their exact printed size in the 2-page course report, so no scaling shrinks the text.

Why: the full-width originals print at 4.5 to 5 pt in papers/course_report_mvp1/main.tex (rule: .claude/rules/figures.md section 4, 7 pt).
Reads saved outputs only: q1_bins.csv, q1_bins_no_min.csv (run 142082), ccdf_points.csv (run 145892), qq_points.csv (run 145897).
Fits nothing new: the QQ line is the same least-squares line the run drew, checked against its manifest.
"""
import json
import shutil
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D

from fig_calibration_gap import SRC, Z95, load_bins

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "runs" / "local_report2p_figs_v11"
PAPER_FIGS = ROOT / "papers" / "paper_mvp1" / "figures"
CCDF_CSV = ROOT / "runs" / "145892_ccdf_v6" / "ccdf_points.csv"
QQ_RUN = ROOT / "runs" / "145897_q3figs_v8"
TEXTWIDTH_IN = 8.5 - 2 * 0.6          # letter paper, geometry margin=0.6in in main.tex
FONT = 7.5                            # printed size, since each figure is drawn at its printed size
DPI = 300
# (minipage fraction in main.tex) x TEXTWIDTH_IN = printed width; heights are chosen to keep the report at 2 pages
W_CALIB, W_CCDF, W_QQ = (round(f * TEXTWIDTH_IN, 3) for f in (0.56, 0.48, 0.50))
H_CALIB, H_CCDF, H_QQ = 4.7, 2.3, 2.3
ROLE_COLOR = {"maker": "#222222", "taker": "#aa5500"}   # same as the original CCDF
GRAY, LINE_COLOR = "#555555", "#aa5500"                 # same as the original QQ plot


def set_font() -> None:
    plt.rcParams.update({"font.size": FONT, "axes.labelsize": FONT, "axes.titlesize": FONT, "legend.fontsize": FONT,
                         "xtick.labelsize": FONT, "ytick.labelsize": FONT})


def draw_calibration(main: pd.DataFrame, nomin: pd.DataFrame, png: Path) -> None:
    fig, (ax, gx) = plt.subplots(2, 1, figsize=(W_CALIB, H_CALIB), sharex=True, layout="constrained",
                                 gridspec_kw={"height_ratios": [1.3, 1]})
    series = [("With trade filter (main)", main, "#222222", 0.0), ("No filter", nomin, "#aa5500", 0.008)]
    ax.plot([0, 1], [0, 1], color="#888888", ls="--", label="Perfect calibration")
    gx.axhline(0, color="#888888", ls="--")
    for name, b, color, dx in series:
        x = b["mean_price"] + dx
        ax.errorbar(x, b["observed_rate"], yerr=b["z_half"], fmt="o", ms=3, capsize=2, lw=1, color=color, label=name)
        gx.errorbar(x, b["gap_pp"], yerr=b["gap_half_pp"], fmt="o", ms=3, capsize=2, lw=1, color=color)
    ax.set(ylabel="Observed outcome-1 rate", xlim=(0, 1), ylim=(0, 1), title="Rate against price")
    gx.set(xlabel="Mean price 1 day before close (USDC per share)", ylabel="Gap: rate minus price\n(percentage points)",
           title="Gap (dashed line: zero gap)")
    ax.grid(alpha=0.3)
    gx.grid(alpha=0.3)
    fig.legend(*ax.get_legend_handles_labels(), loc="outside upper center", ncol=3, columnspacing=1.0, handletextpad=0.4)
    fig.savefig(png, dpi=DPI)
    plt.close(fig)


def draw_ccdf(points: pd.DataFrame, png: Path) -> None:
    fig, ax = plt.subplots(figsize=(W_CCDF, H_CCDF), layout="constrained")
    for role, label in (("maker", "Makers (post orders)"), ("taker", "Takers (accept orders)")):
        g = points[points["role"] == role]
        ax.loglog(g["volume_usdc"], g["ccdf"], color=ROLE_COLOR[role], label=label)
    ax.set(xlabel="Wallet volume (USDC)", ylabel="Share of wallets above that volume")
    ax.grid(alpha=0.3)
    fig.legend(loc="outside upper center", ncol=2, columnspacing=1.0, handletextpad=0.4)
    fig.savefig(png, dpi=DPI)
    plt.close(fig)


def qq_line(p: pd.DataFrame) -> tuple[float, float, float]:
    """Least-squares slope, intercept and r of value on z (the line scipy.stats.linregress gives on the same points)."""
    slope, intercept = np.polyfit(p["z"], p["value"], 1)
    return float(slope), float(intercept), float(np.corrcoef(p["z"], p["value"])[0, 1])


def draw_qq(points: pd.DataFrame, png: Path) -> dict:
    lines = {}
    fig, axes = plt.subplots(1, 2, figsize=(W_QQ, H_QQ), layout="constrained")
    for ax, tag, title, ylabel in zip(axes, ("raw", "log"), ("Raw", "Log"),
                                      ("Trade size (USDC)", "Log trade size (log USDC)")):
        p = points[points["scale"] == tag]
        slope, intercept, r = lines[tag] = qq_line(p)
        ax.plot(p["z"], p["value"], ".", color=GRAY, ms=2)
        z = np.array([p["z"].min(), p["z"].max()])
        ax.plot(z, slope * z + intercept, color=LINE_COLOR, lw=1.2)
        ax.set(title=f"{title} (r = {r:.3f})", xlabel="Normal quantile (z)", ylabel=ylabel)
        ax.grid(alpha=0.3)
    handles = [Line2D([], [], marker=".", color=GRAY, ls="", label=f"{len(points) // 2:,} sampled trades"),
               Line2D([], [], color=LINE_COLOR, label="Straight line = normal")]
    fig.legend(handles=handles, loc="outside upper center", ncol=2, columnspacing=1.0, handletextpad=0.4)
    fig.savefig(png, dpi=DPI)
    plt.close(fig)
    return lines


def main() -> None:
    set_font()
    OUT.mkdir(parents=True, exist_ok=True)
    main_b, nomin_b = load_bins(SRC / "q1_bins.csv"), load_bins(SRC / "q1_bins_no_min.csv")
    qq = pd.read_csv(QQ_RUN / "qq_points.csv")
    qq = qq[qq["variable"] == "Trade size"]
    saved = json.loads((QQ_RUN / "manifest_q3_figs.json").read_text())["metrics"]["qq_line"]["Trade size"]
    jobs = {
        "fig4_calibration_gap_half.png": lambda p: draw_calibration(main_b, nomin_b, p),
        "fig6_ccdf_top_sampled_half.png": lambda p: draw_ccdf(pd.read_csv(CCDF_CSV), p),
        "qq_trade_size_raw_log_half.png": lambda p: lines.update(draw_qq(qq, p)),
    }
    lines: dict = {}
    for name, job in jobs.items():
        job(OUT / name)
        shutil.copy(OUT / name, PAPER_FIGS / name)
    for tag, (slope, intercept, r) in lines.items():
        assert abs(r - saved[tag]["r"]) < 1e-9 and abs(slope - saved[tag]["slope"]) < 1e-6, f"QQ line differs from run: {tag}"
    print("printed widths (in):", W_CALIB, W_CCDF, W_QQ)
    print("QQ lines match the run manifest:", {k: round(v[2], 4) for k, v in lines.items()})


if __name__ == "__main__":
    main()
