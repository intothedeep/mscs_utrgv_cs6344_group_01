"""Calibration figure with a gap panel: observed outcome-1 rate vs mean price, and the per-bin gap in percentage points.

Reads saved q1_bins.csv and q1_bins_no_min.csv only. The 95% z interval is rate +- 1.96 sqrt(rate (1 - rate) / n),
the same rule as code/lecture_numbers.py. The gap interval is that half-width around the gap (the price is a fixed number).
"""
import re
import shutil
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "runs" / "142082_mvp1_full_v1r3"
OUT = ROOT / "runs" / "local_fig4gap_v9"
PAPER = ROOT / "papers" / "paper_mvp1"
Z95 = 1.96
BIN_MACROS = ["ZeroTen", "TenTwenty", "TwentyThirty", "ThirtyForty", "FortyFifty",
              "FiftySixty", "SixtySeventy", "SeventyEighty", "EightyNinety", "NinetyHundred"]


def load_bins(csv: Path) -> pd.DataFrame:
    b = pd.read_csv(csv)
    half = Z95 * np.sqrt(b["observed_rate"] * (1 - b["observed_rate"]) / b["n"])
    b["z_half"] = half
    b["gap_pp"] = (b["observed_rate"] - b["mean_price"]) * 100
    b["gap_half_pp"] = half * 100
    return b


def check_against_numbers(main: pd.DataFrame, nomin: pd.DataFrame) -> list[str]:
    """Compare plotted gaps with the numbers.tex macros. Returns mismatch lines (empty = all match)."""
    tex = (PAPER / "numbers.tex").read_text()
    val = lambda name: float(re.search(r"\\newcommand\{\\" + name + r"\}\{\\ensuremath\{(-?[\d.]+)\}", tex).group(1))
    checks = [(f"Bin{m}Diff", main["gap_pp"][i]) for i, m in enumerate(BIN_MACROS)]
    checks += [("NoMinBinZeroDiff", nomin["gap_pp"][0]), ("NoMinBinOneDiff", nomin["gap_pp"][1])]
    return [f"{k}: tex {val(k)} vs plotted {g:.2f}" for k, g in checks if abs(val(k) - round(g, 2)) > 1e-9]


def draw(main: pd.DataFrame, nomin: pd.DataFrame, png: Path) -> None:
    plt.rcParams.update({"font.size": 9, "axes.labelsize": 9, "legend.fontsize": 9, "xtick.labelsize": 8, "ytick.labelsize": 8})
    fig, (ax, gx) = plt.subplots(2, 1, figsize=(6, 7.5), sharex=True, layout="constrained",
                                  gridspec_kw={"height_ratios": [1.3, 1]})
    series = [("With minimum-trade filter (main)", main, "#222222", 0.0),
              ("Without filter", nomin, "#aa5500", 0.006)]
    ax.plot([0, 1], [0, 1], color="#888888", ls="--", label="Perfect calibration")
    gx.axhline(0, color="#888888", ls="--")
    for name, b, color, dx in series:
        x = b["mean_price"] + dx
        ax.errorbar(x, b["observed_rate"], yerr=Z95 * np.sqrt(b["observed_rate"] * (1 - b["observed_rate"]) / b["n"]),
                    fmt="o", ms=4, capsize=3, color=color, label=name)
        gx.errorbar(x, b["gap_pp"], yerr=b["gap_half_pp"], fmt="o", ms=4, capsize=3, color=color)
    ax.set(ylabel="Observed outcome-1 rate", xlim=(0, 1), ylim=(0, 1))
    gx.set(xlabel="Mean price 1 day before close in bin (USDC per share)",
           ylabel="Gap: observed rate minus\nmean price (percentage points)")
    ax.grid(alpha=0.3)
    gx.grid(alpha=0.3)
    ax.set_title("Rate against price", fontsize=9)
    gx.set_title("Gap (dashed line: zero gap)", fontsize=9)
    fig.legend(*ax.get_legend_handles_labels(), loc="outside upper center", ncol=3)
    fig.savefig(png, dpi=150)
    plt.close(fig)


def main() -> None:
    main_b, nomin_b = load_bins(SRC / "q1_bins.csv"), load_bins(SRC / "q1_bins_no_min.csv")
    mismatches = check_against_numbers(main_b, nomin_b)
    print("numbers.tex mismatches:", mismatches or "none")
    print("main gaps (pp):", [round(g, 2) for g in main_b["gap_pp"]])
    OUT.mkdir(parents=True, exist_ok=True)
    png = OUT / "fig4_calibration_gap.png"
    draw(main_b, nomin_b, png)
    shutil.copy(png, PAPER / "figures" / "fig4_calibration_gap.png")


if __name__ == "__main__":
    main()
