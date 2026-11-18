"""Per-bin calibration gap at p_1d and at p_T, one panel, for paper Appendix F (D-053).

Reads the saved bins of run local_r2close_v14 only. The 95% z interval is rate +- 1.96 sqrt(rate (1 - rate) / n),
the same rule as code/fig_calibration_gap.py. Drawn at its print width (5.5 in) so text stays at or above 7 pt in print.
"""
import shutil
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

__all__ = ["draw"]

ROOT = Path(__file__).resolve().parent.parent
RUN = ROOT / "runs" / "local_r2close_v14"
PAPER = ROOT / "papers" / "paper_mvp1"
Z95 = 1.96


def draw(png: Path) -> None:
    plt.rcParams.update({"font.size": 8, "axes.labelsize": 8, "legend.fontsize": 7.5,
                         "xtick.labelsize": 7.5, "ytick.labelsize": 7.5})
    fig, ax = plt.subplots(figsize=(5.5, 2.0), layout="constrained")
    ax.axhline(0, color="#888888", ls="--", lw=0.8)
    series = [("1 day before close", "bins_p_1d.csv", "#222222", -0.006),
              ("last price before close", "bins_p_T.csv", "#1f5fbf", 0.006)]
    for name, csv, color, dx in series:
        b = pd.read_csv(RUN / csv)
        half = Z95 * np.sqrt(b["observed_rate"] * (1 - b["observed_rate"]) / b["n"]) * 100
        ax.errorbar(b["mean_price"] + dx, b["gap_pp"], yerr=half, fmt="o", ms=3, capsize=2, lw=0.9,
                    color=color, label=name)
    ax.set(xlabel="Mean price in bin (USDC per share)", ylabel="Gap: observed rate minus\nmean price (pp)", xlim=(0, 1))
    ax.grid(alpha=0.3)
    fig.legend(*ax.get_legend_handles_labels(), loc="outside upper center", ncol=2, frameon=False)
    fig.savefig(png, dpi=300)
    plt.close(fig)


def main() -> None:
    png = RUN / "fig_r2_close_gap.png"
    draw(png)
    shutil.copy(png, PAPER / "figures" / "fig_r2_close_gap.png")
    print(png)


if __name__ == "__main__":
    main()
