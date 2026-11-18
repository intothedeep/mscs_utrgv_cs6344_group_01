"""Course report Q2 figure: share held by the top 1% and top 10% of wallets, for maker volume, taker volume and winnings.

Why: the owner asked for a Q2 figure on wallet winnings next to the volume figure (2026-11-18).
Reads saved outputs only: q2_concentration.csv (run 142082) and pnl_summary.json (run 156432, kept scope).
Each share uses its own ranking: wallets ranked by volume for volume, by winnings for winnings.
Drawn at its printed width (0.48 of the 7.3 in text width), 7.5 pt text, the same as the report CCDF.
"""
import json
import shutil
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from fig_report2p_half import DPI, H_CCDF, PAPER_FIGS, W_CCDF, set_font

__all__ = ["draw"]

ROOT = Path(__file__).resolve().parent.parent
CONC = ROOT / "runs" / "142082_mvp1_full_v1r3" / "q2_concentration.csv"
PNL = ROOT / "runs" / "156432_pnl_wallets_v1" / "pnl_summary.json"
OUT = ROOT / "runs" / "local_report_q2win_v17"
NAME = "fig_report_q2_winnings.png"


def shares() -> dict[str, list[float]]:
    c = pd.read_csv(CONC, index_col=0)
    won = json.loads(PNL.read_text())["scopes"]["kept"]["top_pct_of_all_wallets_share_of_won"]
    return {"Maker volume": [c.loc["maker", "top1_share"], c.loc["maker", "top10_share"]],
            "Taker volume": [c.loc["taker", "top1_share"], c.loc["taker", "top10_share"]],
            "Winnings": [won["1%"], won["10%"]]}


def draw(data: dict[str, list[float]], png: Path) -> None:
    colors = {"Maker volume": "#222222", "Taker volume": "#aa5500", "Winnings": "#0072B2"}
    fig, ax = plt.subplots(figsize=(W_CCDF, H_CCDF), layout="constrained")
    x, w = np.arange(2), 0.26
    for i, (name, vals) in enumerate(data.items()):
        bars = ax.bar(x + (i - 1) * w, [100 * v for v in vals], w, color=colors[name], label=name)
        ax.bar_label(bars, labels=[f"{100 * v:.1f}" for v in vals], padding=1)
    ax.set(xticks=x, xticklabels=["Top 1% of wallets", "Top 10% of wallets"], ylabel="Share of the total (%)", ylim=(0, 115))
    ax.set_yticks([0, 20, 40, 60, 80, 100])
    ax.grid(axis="y", alpha=0.3)
    fig.legend(loc="outside upper center", ncol=3, columnspacing=1.0, handletextpad=0.4)
    fig.savefig(png, dpi=DPI)
    plt.close(fig)


def main() -> None:
    set_font()
    OUT.mkdir(parents=True, exist_ok=True)
    data = shares()
    draw(data, OUT / NAME)
    shutil.copy(OUT / NAME, PAPER_FIGS / NAME)
    print({k: [round(100 * v, 1) for v in vals] for k, vals in data.items()})


if __name__ == "__main__":
    main()
