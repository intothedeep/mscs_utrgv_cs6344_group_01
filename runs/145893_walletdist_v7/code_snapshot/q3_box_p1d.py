"""Box plot of p_1d by topic group (G1, plan Q3 row "box plot").

Reads ONLY runs/142123_robust_full_v4/r2_markets.csv (columns category_group, p_1d).
This is not a Q3 stage output of run 142082: it is drawn after the run from a saved file.
The input comes from `bash jobs/fetch_run.sh 142123_robust_full_v4` (fetch_run).
Usage (from the project folder): uv run python code/q3_box_p1d.py
"""
import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

KEPT_ROWS = 47_948  # n_kept of runs 142082 and 142123 (tables_summary.json)


def load_groups(csv: Path) -> pd.Series:
    """p_1d per market, indexed by category_group. Stops if the file is not the kept set."""
    df = pd.read_csv(csv, usecols=["category_group", "p_1d"])
    if len(df) != KEPT_ROWS:
        raise SystemExit(f"{csv} has {len(df)} rows, expected {KEPT_ROWS}: not the kept set")
    if df["p_1d"].isna().any() or df["category_group"].isna().any():
        raise SystemExit("missing category_group or p_1d")
    return df.set_index("category_group")["p_1d"]


def draw_box(p: pd.Series, png: Path) -> None:
    counts = p.groupby(level=0).size()
    order = counts.sort_index().sort_values(ascending=False, kind="stable")  # n desc, name asc
    data = [p.loc[c].to_numpy(float) for c in order.index]
    fig, ax = plt.subplots(figsize=(max(6, 1.2 * len(order) + 2), 4.5), layout="constrained")
    ax.boxplot(data, flierprops={"marker": ".", "markersize": 2, "alpha": 0.3})  # one series: no legend
    ax.set_xticks(range(1, len(order) + 1), [f"{c}\n(n={n:,})" for c, n in order.items()])
    ax.set(xlabel="Topic group (category_group)", ylabel="Price p_1d (USDC per share)", ylim=(0, 1))
    ax.grid(axis="y", alpha=0.3)
    fig.savefig(png, dpi=150)
    plt.close(fig)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default="runs/142123_robust_full_v4/r2_markets.csv")
    ap.add_argument("--out", default="reports/figures/box_p1d_by_category_group.png")
    a = ap.parse_args()
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    p = load_groups(Path(a.csv))
    draw_box(p, out)
    print(f"rows {len(p)}, groups {p.index.nunique()}, wrote {out}")


if __name__ == "__main__":
    main()
