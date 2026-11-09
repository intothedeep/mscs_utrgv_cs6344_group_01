"""Redraw the three body figures at one column width of the two-column paper (D-045, PL-12a).

Why: papers/paper_mvp1 body goes two columns (3.425 in each). Figures drawn at print size keep text at 7.5 pt.
Reuses the drawing functions of code/fig_report2p_half.py with new widths; reads the same saved outputs, fits nothing.
fig:timeline is TikZ in 04-methods.tex, so it is not redrawn.
Usage: OMP_NUM_THREADS=1 timeout 300 uv run python code/fig_column_widths.py
"""
import shutil

import matplotlib.pyplot as plt
import pandas as pd

import fig_report2p_half as h
from fig_calibration_gap import SRC, load_bins

OUT = h.ROOT / "runs" / "local_column_figs_v13"
COL_IN = 3.425   # (8.5 - 2 x 0.7 - 0.25) / 2
H_RATE, H_GAP = 2.7, 2.1   # the combined figure split in two, to fill blank column space
H_COL = {"calib": 4.6, "ccdf": 2.5, "qq": 2.6}


def _series(main: pd.DataFrame, nomin: pd.DataFrame):
    """Same two series, colours and x shift as draw_calibration in fig_report2p_half.py."""
    return [("With trade filter (main)", main, "#222222", 0.0), ("No filter", nomin, "#aa5500", 0.008)]


def draw_rate(main: pd.DataFrame, nomin: pd.DataFrame, png) -> None:
    fig, ax = plt.subplots(figsize=(COL_IN, H_RATE), layout="constrained")
    ax.plot([0, 1], [0, 1], color="#888888", ls="--", label="Perfect calibration")
    for name, b, color, dx in _series(main, nomin):
        ax.errorbar(b["mean_price"] + dx, b["observed_rate"], yerr=b["z_half"], fmt="o", ms=3, capsize=2, lw=1, color=color, label=name)
    ax.set(xlabel="Mean price 1 day before close (USDC per share)", ylabel="Observed outcome-1 rate", xlim=(0, 1), ylim=(0, 1))
    ax.grid(alpha=0.3)
    fig.legend(*ax.get_legend_handles_labels(), loc="outside upper center", ncol=2, columnspacing=1.0, handletextpad=0.4)
    fig.savefig(png, dpi=h.DPI)
    plt.close(fig)


def draw_gap(main: pd.DataFrame, nomin: pd.DataFrame, png) -> None:
    fig, ax = plt.subplots(figsize=(COL_IN, H_GAP), layout="constrained")
    ax.axhline(0, color="#888888", ls="--", label="Zero gap")
    for name, b, color, dx in _series(main, nomin):
        ax.errorbar(b["mean_price"] + dx, b["gap_pp"], yerr=b["gap_half_pp"], fmt="o", ms=3, capsize=2, lw=1, color=color, label=name)
    ax.set(xlabel="Mean price 1 day before close (USDC per share)", ylabel="Gap: rate minus price\n(percentage points)", xlim=(0, 1))
    ax.grid(alpha=0.3)
    fig.legend(*ax.get_legend_handles_labels(), loc="outside upper center", ncol=2, columnspacing=1.0, handletextpad=0.4)
    fig.savefig(png, dpi=h.DPI)
    plt.close(fig)


def main() -> None:
    h.set_font()
    h.W_CALIB = h.W_CCDF = h.W_QQ = COL_IN
    h.H_CALIB, h.H_CCDF, h.H_QQ = H_COL["calib"], H_COL["ccdf"], H_COL["qq"]
    OUT.mkdir(parents=True, exist_ok=True)
    qq = pd.read_csv(h.QQ_RUN / "qq_points.csv")
    qq = qq[qq["variable"] == "Trade size"]
    jobs = {
        "fig4_calibration_gap_col.png": lambda p: h.draw_calibration(load_bins(SRC / "q1_bins.csv"), load_bins(SRC / "q1_bins_no_min.csv"), p, legend_ncol=2),
        "fig6_ccdf_top_sampled_col.png": lambda p: h.draw_ccdf(pd.read_csv(h.CCDF_CSV), p),
        "qq_trade_size_raw_log_col.png": lambda p: h.draw_qq(qq, p),
    }
    main_b, nomin_b = load_bins(SRC / "q1_bins.csv"), load_bins(SRC / "q1_bins_no_min.csv")
    jobs["fig4_calibration_rate_col.png"] = lambda p: draw_rate(main_b, nomin_b, p)
    jobs["fig4_calibration_gap_panel_col.png"] = lambda p: draw_gap(main_b, nomin_b, p)
    for name, job in jobs.items():
        job(OUT / name)
        shutil.copy(OUT / name, h.PAPER_FIGS / name)


if __name__ == "__main__":
    main()
