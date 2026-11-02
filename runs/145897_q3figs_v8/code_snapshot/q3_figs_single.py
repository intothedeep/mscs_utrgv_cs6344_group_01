"""Four single Q3 figures from the saved tables of a run (D-032, owner 2026-11-02).

Why: `fig1_fig2_hist.png` holds two histograms in one image, and `fig3_qq.png` holds four QQ panels. At page width each panel is small.
This script redraws them one figure per image. Raw and log QQ stay side by side because that pair is a real comparison.
It reads markets.parquet, trade_sizes_sample.parquet, wallets.parquet (saved outputs, no raw-data pass), q3_results.json and
tables_summary.json. It fits nothing new: the QQ reference line is the same least-squares line scipy.stats.probplot draws in q3_describe.py.

Same inputs, filters, sample, bins and transforms as q3_describe.py: kept p_1d (50 bins on 0..1), trade size > 0 (60 log bins),
wallet volume > 0, QQ sample = rng(SEED) over sorted values, trade size first and wallet volume second, QQ_POINTS each.

Usage on a compute node (job `jobs/q3_figs.slurm`):
  python code/q3_figs_single.py --source runs/142082_mvp1_full_v1r3 --out runs/<JOB>_q3figs_v8
"""
import argparse
import hashlib
import json
import os
import platform
import socket
import time
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from scipy import stats

from q3_describe import QQ_POINTS, SEED   # one source for the sample rule

CODE_VERSION = "q3figs-v1"   # own label, like wallet_dist_figs.py; bumped by hand
COLOR = "#555555"            # same gray as the histograms in q3_describe.py
LINE_COLOR = "#aa5500"       # QQ reference line
FONT = 9                     # drawn at 7 in wide, printed at full text width, so 9 pt stays above the 7 pt floor (rules/figures.md §4)
SIZE = (7.0, 3.6)
SIZE_QQ = (7.0, 3.9)
DPI = 300


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def hist_table(x: np.ndarray, bins) -> pd.DataFrame:
    counts, edges = np.histogram(x, bins=bins)
    return pd.DataFrame({"bin_lo": edges[:-1], "bin_hi": edges[1:], "count": counts})


def draw_hist(tab: pd.DataFrame, log_x: bool, xlabel: str, ylabel: str, title: str, png: Path) -> None:
    fig, ax = plt.subplots(figsize=SIZE, layout="constrained")
    ax.bar(tab["bin_lo"], tab["count"], width=tab["bin_hi"] - tab["bin_lo"], align="edge", color=COLOR)   # exact edges, so log bins stay true
    if log_x:
        ax.set_xscale("log")
    ax.set(xlabel=xlabel, ylabel=ylabel, title=title)
    ax.grid(alpha=0.3)
    fig.savefig(png, dpi=DPI)
    plt.close(fig)


def qq_points(name: str, s: np.ndarray) -> tuple[pd.DataFrame, dict]:
    """Raw and log QQ points of one sample. probplot is the call q3_describe.py plots with."""
    rows, lines = [], {}
    for tag, v in (("raw", s), ("log", np.log(s))):
        (z, ordered), (slope, intercept, r) = stats.probplot(v, dist="norm")
        rows.append(pd.DataFrame({"variable": name, "scale": tag, "z": z, "value": ordered}))
        lines[tag] = {"slope": float(slope), "intercept": float(intercept), "r": float(r)}
    return pd.concat(rows, ignore_index=True), lines


def draw_qq(points: pd.DataFrame, lines: dict, name: str, unit: str, png: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=SIZE_QQ, layout="constrained")
    for ax, tag in zip(axes, ("raw", "log")):
        p = points[points["scale"] == tag]
        ln = lines[tag]
        ax.plot(p["z"], p["value"], ".", color=COLOR, ms=3)
        z = np.array([p["z"].min(), p["z"].max()])
        ax.plot(z, ln["slope"] * z + ln["intercept"], color=LINE_COLOR, lw=1.5)
        ax.set_title(f"{tag.title()} (r = {ln['r']:.3f})")
        ax.set_xlabel("Normal theoretical quantile (z)")
        ax.set_ylabel(f"Ordered values ({unit})" if tag == "raw" else f"Ordered log values (log {unit})")
        ax.grid(alpha=0.3)
    handles = [Line2D([], [], marker=".", color=COLOR, ls="", label=f"{QQ_POINTS:,} sampled values"),
               Line2D([], [], color=LINE_COLOR, label="Least-squares line (straight = normal)")]
    fig.suptitle(f"{name}: raw beside log")
    fig.legend(handles=handles, loc="outside upper center", ncol=2)
    fig.savefig(png, dpi=DPI)
    plt.close(fig)


def check_counts(got: dict, js: dict, tabs: dict) -> list[str]:
    """Each count from the saved tables against the counts the Q3 and build stages saved."""
    want = {"n_price": [("q3_results summary p_1d n", js["summary"]["p_1d"]["n"]), ("tables_summary n_kept", tabs["n_kept"])],
            "n_size": [("q3_results summary trade_size_usdc n", js["summary"]["trade_size_usdc"]["n"]),
                       ("q3_results notes trade_size_sample_rows", js["notes"]["trade_size_sample_rows"]),
                       ("tables_summary trade_size_sample_rows", tabs["trade_size_sample_rows"])],
            "n_wallet_rows": [("q3_results summary wallet_volume_usdc n", js["summary"]["wallet_volume_usdc"]["n"]),
                              ("tables_summary n_wallet_role_rows", tabs["n_wallet_role_rows"])]}
    bad = []
    for key, refs in want.items():
        for label, n in refs:
            if got[key] != n:
                bad.append(f"{key} {got[key]} vs {label} {n}")
    for key in ("hist_price_total", "hist_size_total"):
        base = got["n_price"] if key == "hist_price_total" else got["n_size"]
        if got[key] != base:
            bad.append(f"{key} {got[key]} vs {base}")
    for key in ("qq_size_rows", "qq_wallet_rows"):
        if got[key] != 2 * min(QQ_POINTS, got["n_size"] if "size" in key else got["n_wallet_rows"]):
            bad.append(f"{key} {got[key]} not 2 x sample size")
    return bad


def main() -> None:
    t0 = time.perf_counter()
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True, help="run folder with markets.parquet, trade_sizes_sample.parquet, wallets.parquet, q3_results.json, tables_summary.json")
    ap.add_argument("--out", default=".")
    a = ap.parse_args()
    src, out = Path(a.source), Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.size": FONT, "axes.titlesize": FONT, "axes.labelsize": FONT,
                         "xtick.labelsize": FONT, "ytick.labelsize": FONT})

    markets = pd.read_parquet(src / "markets.parquet")
    price = markets.loc[markets["kept"], "p_1d"].dropna().to_numpy(float)
    size = pd.read_parquet(src / "trade_sizes_sample.parquet")["usdc_amount"].to_numpy(float)
    size = size[size > 0]
    vol = pd.read_parquet(src / "wallets.parquet")["volume_usdc"].to_numpy(float)
    vol = vol[vol > 0]

    h_price = hist_table(price, np.linspace(0, 1, 51))   # bins=50, range=(0, 1) in q3_describe.py
    h_size = hist_table(size, np.logspace(np.log10(max(size.min(), 1e-6)), np.log10(size.max()), 60))
    h_price.to_csv(out / "hist_price_p1d.csv", index=False)
    h_size.to_csv(out / "hist_trade_size.csv", index=False)
    draw_hist(h_price, False, "p_1d (price, USDC per share)", "Markets (count)",
              f"Price 1 day before T ({len(price):,} kept markets)", out / "hist_price_p1d.png")
    draw_hist(h_size, True, "Trade size (USDC)", "Trades (count)",
              f"Trade size ({len(size):,} sampled trades)", out / "hist_trade_size.png")

    rng = np.random.default_rng(SEED)   # same order as q3_describe.py draw_qq: trade size, then wallet volume
    qq, lines = [], {}
    for name, x, unit, stem in (("Trade size", size, "USDC", "qq_trade_size_raw_log.png"),
                                ("Wallet volume", vol, "USDC", "qq_wallet_volume_raw_log.png")):
        s = rng.choice(np.sort(x), min(QQ_POINTS, len(x)), replace=False)   # sorted first: row order must not pick the points
        pts, lines[name] = qq_points(name, s)
        draw_qq(pts, lines[name], name, unit, out / stem)
        qq.append(pts)
    qq_all = pd.concat(qq, ignore_index=True)
    qq_all.to_csv(out / "qq_points.csv", index=False)   # values only, no wallet ID

    js = json.loads((src / "q3_results.json").read_text())
    tabs = json.loads((src / "tables_summary.json").read_text())
    got = {"n_price": len(price), "n_size": len(size), "n_wallet_rows": len(vol),
           "hist_price_total": int(h_price["count"].sum()), "hist_size_total": int(h_size["count"].sum()),
           "qq_size_rows": int((qq_all["variable"] == "Trade size").sum()), "qq_wallet_rows": int((qq_all["variable"] == "Wallet volume").sum())}
    mismatches = check_counts(got, js, tabs)

    manifest = {
        "code_version": CODE_VERSION,
        "code_sha": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()[:12],
        "params": {"source_run": src.name, "qq_points": QQ_POINTS, "seed": SEED, "price_bins": 50, "size_bins": 59,
                   "dpi": DPI, "font": FONT},
        "env": {"hostname": socket.gethostname(), "python": platform.python_version(), "pandas": pd.__version__,
                "numpy": np.__version__, "slurm_job_id": os.environ.get("SLURM_JOB_ID", "none"),
                "slurm_cpus_per_task": os.environ.get("SLURM_CPUS_PER_TASK", "none")},
        "metrics": {
            "source_sha256": {f: sha256_file(src / f) for f in ("markets.parquet", "trade_sizes_sample.parquet", "wallets.parquet",
                                                                  "q3_results.json", "tables_summary.json")},
            "counts": got, "qq_line": lines,
            "counts_match": not mismatches, "mismatches": mismatches,
            "wall_time_s": round(time.perf_counter() - t0, 1),
        },
    }
    (out / "manifest_q3_figs.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print("COUNTS MATCH" if not mismatches else "COUNT MISMATCH: " + "; ".join(mismatches))


if __name__ == "__main__":
    main()
