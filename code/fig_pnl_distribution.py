"""Redraw the wallet PnL histogram from a saved pnl_summary.json (figure only, no data pass).

Why a separate script: the job figure put the -1e0 and 1e0 tick labels on the two edges
of the narrow centre bin, so they overlapped. Here the centre bin gets one "0" label.
Usage: uv run python code/fig_pnl_distribution.py <pnl_summary.json> <out_dir>
"""
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

SCOPE_TITLE = {"all": "All resolved markets", "non_updown": "Non-Up/Down resolved markets", "kept": "Kept set"}


def tick_positions(edges: np.ndarray) -> tuple[list[float], list[str]]:
    # Bar i spans edges[i]..edges[i+1]; edge k sits at x = k - 0.5. Skip |e| = 1 (centre bin edges).
    pos, lab = [], []
    for k, e in enumerate(edges):
        if not (1 < abs(e) <= 1e8):
            continue
        p = np.log10(abs(e))
        if p.is_integer() and int(p) % 2 == 0:
            pos.append(k - 0.5)
            lab.append(("-" if e < 0 else "") + f"1e{int(p)}")
    centre = int(np.where(edges == -1.0)[0][0])  # bar index of the (-1, 1) bin
    pos.append(centre)
    lab.append("0")
    return pos, lab


def main() -> None:
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    summary = json.loads(src.read_text())
    edges = np.array(summary["hist_edges"])
    names = list(SCOPE_TITLE)
    fig, axes = plt.subplots(len(names), 1, figsize=(7, 8), sharex=True, layout="constrained")
    for ax, name in zip(axes, names):
        s = summary["scopes"][name]
        ax.bar(np.arange(len(s["hist_counts"])), s["hist_counts"], width=0.9, color="#555555")
        ax.set_yscale("log")
        ax.set_ylabel("Wallets (count, log scale)")
        ax.set_title(f"{SCOPE_TITLE[name]}: {s['n_wallets']:,} wallets", fontsize=10)
        ax.grid(axis="y", alpha=0.3)
    pos, lab = tick_positions(edges)
    axes[-1].set_xticks(pos, lab)
    axes[-1].set_xlabel("Net profit per wallet (USDC, symmetric-log bins, centre bin -1 to 1)")
    out.mkdir(parents=True, exist_ok=True)
    fig.savefig(out / "fig_pnl_distribution.png", dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    main()
