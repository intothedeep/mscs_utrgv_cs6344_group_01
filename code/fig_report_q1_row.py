"""Course report Figure 1 as one full-width row: rate against price (left) and per-bin gap (right).

Why: the owner asked for Figure 1 in one row with the Q1 text below it (2026-11-18).
Same data, intervals and colours as fig_report2p_half.draw_calibration; only the layout changes.
Drawn at its printed width (text width 7.3 in) so the 7.5 pt text prints at 7.5 pt.
Reads saved outputs only: q1_bins.csv, q1_bins_no_min.csv of run 142082.
"""
import shutil
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from fig_calibration_gap import SRC, load_bins
from fig_report2p_half import DPI, PAPER_FIGS, TEXTWIDTH_IN, set_font

__all__ = ["draw_row"]

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "runs" / "local_report_q1row_v15"
H_ROW = 2.5
NAME = "fig4_calibration_gap_row.png"


def draw_row(main: pd.DataFrame, nomin: pd.DataFrame, png: Path) -> None:
    fig, (ax, gx) = plt.subplots(1, 2, figsize=(TEXTWIDTH_IN, H_ROW), layout="constrained")
    series = [("With trade filter (main)", main, "#222222", 0.0), ("No filter", nomin, "#aa5500", 0.008)]
    ax.plot([0, 1], [0, 1], color="#888888", ls="--", label="Perfect calibration")
    gx.axhline(0, color="#888888", ls="--")
    for name, b, color, dx in series:
        x = b["mean_price"] + dx
        ax.errorbar(x, b["observed_rate"], yerr=b["z_half"], fmt="o", ms=3, capsize=2, lw=1, color=color, label=name)
        gx.errorbar(x, b["gap_pp"], yerr=b["gap_half_pp"], fmt="o", ms=3, capsize=2, lw=1, color=color)
    xl = "Mean price 1 day before close (USDC per share)"
    ax.set(xlabel=xl, ylabel="Observed outcome-1 rate", xlim=(0, 1), ylim=(0, 1), title="Rate against price")
    gx.set(xlabel=xl, ylabel="Gap: rate minus price\n(percentage points)", xlim=(0, 1),
           title="Gap (dashed line: zero gap)")
    ax.grid(alpha=0.3)
    gx.grid(alpha=0.3)
    fig.legend(*ax.get_legend_handles_labels(), loc="outside upper center", ncol=3, columnspacing=1.0, handletextpad=0.4)
    fig.savefig(png, dpi=DPI)
    plt.close(fig)


def main() -> None:
    set_font()
    OUT.mkdir(parents=True, exist_ok=True)
    draw_row(load_bins(SRC / "q1_bins.csv"), load_bins(SRC / "q1_bins_no_min.csv"), OUT / NAME)
    shutil.copy(OUT / NAME, PAPER_FIGS / NAME)
    print(OUT / NAME, "width", TEXTWIDTH_IN, "in")


if __name__ == "__main__":
    main()
