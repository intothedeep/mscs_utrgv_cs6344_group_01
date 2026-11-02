"""Six single figures from the saved outputs of run 145893_walletdist_v7: one image per figure (owner, 2026-11-02).

Why: `wallet_dist_panels.png` holds six panels in one image, so one figure number covers six pictures.
This script redraws each panel alone, same look, same split at the top 20% cutoff, same x axis in the count
and volume figures. It reads only wallet_dist_bins.csv, lorenz_points.csv and manifest_wallet_dist.json. No parquet, no fit, no Gini.

Usage (one core, under "Allowed locally" of ~/.claude/CLAUDE.md):
  OMP_NUM_THREADS=1 timeout 300 uv run python code/wallet_figs_single.py \
      --run runs/145893_walletdist_v7 --out reports/figures
"""
import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

from wallet_dist_figs import REST_COLOR, ROLE_COLOR, TOP_FRAC, draw_split

FONT = 8            # half page width (D-033): drawn 3.4 in, printed near that, so 8 pt stays above the 7 pt floor (rules/figures.md §4)
SIZE = (3.4, 3.0)   # inches, count and volume figures: one pair per row, so both have this size and the same x axis
SIZE_LORENZ = (3.4, 3.4)   # the Lorenz pair: equal size, the axes are square
DPI = 300


def pct(x: float) -> str:
    """Percent with one decimal; a value that would print 0.0% is shown as '<0.01%'."""
    return "<0.01%" if x < 1e-4 else f"{x:.1%}" if x >= 1e-3 else f"{x:.2%}"


def dist_figure(bins: pd.DataFrame, info: dict, role: str, kind: str, x_lo: float, png: Path) -> None:
    i, color = info[role], ROLE_COLOR[role]
    b = bins[(bins["role"] == role) & (bins["bin_hi_usdc"] > x_lo)]
    edges = np.append(b["bin_lo_usdc"].to_numpy(), b["bin_hi_usdc"].to_numpy()[-1])
    col = "wallet_share" if kind == "count" else "volume_share"
    fig, ax = plt.subplots(figsize=SIZE, layout="constrained")
    draw_split(ax, edges, b[col].to_numpy() / np.diff(np.log10(edges)), i["cutoff_usdc"], color)
    ax.set_xscale("log")
    ax.set_xlim(edges[0], edges[-1])
    lo, hi = int(round(np.log10(edges[0]))), int(round(np.log10(edges[-1])))
    ax.set_xticks([10.0 ** e for e in range(lo, hi + 1, 2)])   # every second decade: eleven labels do not fit in 3.4 in
    ax.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
    ax.set_ylim(bottom=0)
    ax.grid(alpha=0.3)
    if kind == "count":
        ax.set_title(f"{role.title()}: wallet distribution f(x)")
        ax.set_ylabel("Share of wallets per decade")
        clipped, what = i["clipped_wallet_share"], "wallets"
    else:
        ax.set_title(f"{role.title()}: top 20% hold {i['top20_share']:.1%} of volume")
        ax.set_ylabel("Share of volume per decade")
        clipped, what = i["clipped_volume_share"], "volume"
    xl = "Wallet volume (USDC)"
    if clipped > 0:
        xl += f"\nnot shown: {pct(clipped)} of {what}"
    ax.set_xlabel(xl)
    handles = [Patch(color=REST_COLOR, label="Bottom 80%"), Patch(color=color, label="Top 20%")]
    fig.legend(handles=handles, loc="outside upper center", ncol=2)
    fig.savefig(png, dpi=DPI)
    plt.close(fig)


def lorenz_figure(lor: pd.DataFrame, info: dict, role: str, png: Path) -> None:
    i = info[role]
    g = lor[lor["role"] == role]
    fig, ax = plt.subplots(figsize=SIZE_LORENZ, layout="constrained")
    ax.plot([0, 1], [0, 1], color="#888888", ls="--", lw=1)
    ax.plot(g["x"], g["y"], color=ROLE_COLOR[role], lw=1.8)
    ax.plot([1 - TOP_FRAC], [TOP_FRAC], marker="o", mfc="white", mec="#aa0000", ls="", ms=6)
    ax.plot([i["lorenz_x_at_80"]], [i["lorenz_y_at_80"]], marker="o", color="#aa0000", ls="", ms=5)
    ax.set(xlim=(0, 1), ylim=(0, 1), xlabel="Share of wallets (lowest volume first)", ylabel="Share of volume")
    ax.set_title(f"{role.title()}: bottom 80% hold {i['lorenz_y_at_80']:.1%} of volume")
    ax.set_aspect("equal", adjustable="box")
    ax.grid(alpha=0.3)
    handles = [Line2D([], [], color=ROLE_COLOR[role], lw=1.8, label="Lorenz curve"),
               Line2D([], [], color="#888888", ls="--", label="Equality y = x"),
               Line2D([], [], marker="o", mfc="white", mec="#aa0000", ls="", label="80/20 reference"),
               Line2D([], [], marker="o", color="#aa0000", ls="", label="Measured at 80%")]
    fig.legend(handles=handles, loc="outside upper center", ncol=2)
    fig.savefig(png, dpi=DPI)
    plt.close(fig)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True, help="run folder with wallet_dist_bins.csv, lorenz_points.csv, manifest_wallet_dist.json")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    run, out = Path(a.run), Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    bins, lor = pd.read_csv(run / "wallet_dist_bins.csv"), pd.read_csv(run / "lorenz_points.csv")
    man = json.loads((run / "manifest_wallet_dist.json").read_text())
    info, x_lo = man["metrics"]["per_role"], man["params"]["x_axis_start_usdc"]
    plt.rcParams.update({"font.size": FONT, "axes.titlesize": FONT, "axes.labelsize": FONT,
                         "xtick.labelsize": FONT, "ytick.labelsize": FONT, "legend.fontsize": FONT})
    for role in ("maker", "taker"):
        dist_figure(bins, info, role, "count", x_lo, out / f"wallet_dist_{role}_count.png")
        dist_figure(bins, info, role, "volume", x_lo, out / f"wallet_dist_{role}_volume.png")
        lorenz_figure(lor, info, role, out / f"wallet_lorenz_{role}.png")
    print("wrote 6 PNGs to", out)


if __name__ == "__main__":
    main()
