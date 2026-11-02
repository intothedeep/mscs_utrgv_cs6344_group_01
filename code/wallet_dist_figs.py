"""Three linked panels per role: wallet distribution, volume distribution, full Lorenz curve (`.claude/rules/visualization.md` §7, D-031).

Why a new script: the report shows a coarse Lorenz drawn from four saved top shares (`lecture_numbers.py`). Section 7 asks for three
linked panels whenever a report says "top x% holds y%". This script reads the saved `wallets.parquet` of the source run and fits nothing.
A wallet is one address, never a person.

Panel 1: wallet distribution f(x). Area = share of wallets. Panel 2: volume distribution x f(x). Area = share of volume.
Both use a log x axis. The height is multiplied by ln 10 * x, so on the log10 axis the area under a bar is the share itself.
In each bin that is share / (bin width in log10 units). Panel 3: Lorenz curve, read by height.

Usage on a compute node (job `jobs/wallet_dist.slurm`):
  python code/wallet_dist_figs.py --source runs/142082_mvp1_full_v1r3 --out runs/<JOB>_walletdist_v7
"""
import argparse
import hashlib
import json
import math
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
from matplotlib.patches import Patch

CODE_VERSION = "walletdist-v1"   # own label, like ccdf_redraw.py; bumped by hand
ROLE_COLOR = {"maker": "#222222", "taker": "#aa5500"}   # same as q2_concentration.py, so the figures match
REST_COLOR = "#cccccc"           # the bottom 80% of wallets, both roles
TOP_FRAC = 0.20                  # the 80/20 split
SHARE_TOLS = 1e-9                # saved vs recomputed top shares, and bin sums
BINS_PER_DECADE = 20
LEFT_QUANTILE = 0.001            # the x axis starts at the decade below this volume quantile of all wallet-role rows
N_LORENZ_LINEAR = 1500           # Lorenz points spaced evenly in wallet rank
N_LORENZ_TOP = 500               # plus log-spaced ranks from the top, where the curve turns steeply
TOP_SHARE_KEYS = {"top1_share": 0.01, "top5_share": 0.05, "top10_share": 0.10, "top20_share": 0.20}
FONT = 11                        # the PNG is 11 in wide and prints at about 7 in, so 11 pt prints at 7 pt


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def top_share(volume: np.ndarray, frac: float) -> float:
    """Same rule as q2_concentration.py: the top ceil(frac * n) wallets, at least one."""
    xs = np.sort(volume)[::-1]
    return float(xs[: max(1, math.ceil(frac * len(xs)))].sum() / xs.sum())


def bin_shares(volume: np.ndarray, log_edges: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Share of wallets and share of volume per log10 bin. The largest value goes into the last bin."""
    nb = len(log_edges) - 1
    idx = np.clip(np.searchsorted(log_edges, np.log10(volume), side="right") - 1, 0, nb - 1)
    wallet = np.bincount(idx, minlength=nb) / len(volume)
    vol = np.bincount(idx, weights=volume, minlength=nb) / volume.sum()
    return wallet, vol


def lorenz_points(volume: np.ndarray) -> pd.DataFrame:
    """Lorenz curve (wallets lowest volume first): evenly spaced ranks, log-spaced ranks from the top, and both ends."""
    xs = np.sort(volume)
    n = len(xs)
    cum = np.concatenate([[0.0], np.cumsum(xs) / xs.sum()])
    k_top = max(1, math.ceil(TOP_FRAC * n))
    from_top = n - np.unique(np.logspace(0, np.log10(n), N_LORENZ_TOP).astype(int))
    idx = np.unique(np.concatenate([np.linspace(0, n, N_LORENZ_LINEAR).astype(int), from_top, [0, n, n - k_top]]))
    return pd.DataFrame({"x": idx / n, "y": cum[idx]})


def draw_split(ax, edges: np.ndarray, heights: np.ndarray, cutoff: float, top_color: str) -> None:
    """Step plot of one distribution. The part at or above the cutoff gets the role color, the rest gray."""
    full = np.unique(np.append(edges, cutoff)) if edges[0] < cutoff < edges[-1] else edges
    h = heights[np.clip(np.searchsorted(edges, np.sqrt(full[:-1] * full[1:]), side="right") - 1, 0, len(heights) - 1)]
    j = int(np.searchsorted(full, cutoff))
    if j >= 1:
        ax.stairs(h[:j], full[: j + 1], fill=True, color=REST_COLOR)
    if j < len(h):
        ax.stairs(h[j:], full[j:], fill=True, color=top_color)
    ax.axvline(cutoff, color="#888888", lw=0.8, ls=":")


def draw_figure(bins: pd.DataFrame, lor: pd.DataFrame, info: dict, x_lo: float, png: Path) -> None:
    plt.rcParams.update({"font.size": FONT, "axes.titlesize": FONT, "axes.labelsize": FONT,
                         "xtick.labelsize": FONT, "ytick.labelsize": FONT})
    roles = list(info)
    fig, axes = plt.subplots(len(roles), 3, figsize=(11, 3.6 * len(roles)), layout="constrained")
    for r, role in enumerate(roles):
        i, color = info[role], ROLE_COLOR[role]
        b = bins[(bins["role"] == role) & (bins["bin_hi_usdc"] > x_lo)]
        edges = np.append(b["bin_lo_usdc"].to_numpy(), b["bin_hi_usdc"].to_numpy()[-1])
        width = np.diff(np.log10(edges))
        for c, (col, kind) in enumerate((("wallet_share", "wallet"), ("volume_share", "volume"))):
            ax = axes[r, c]
            draw_split(ax, edges, b[col].to_numpy() / width, i["cutoff_usdc"], color)
            ax.set_xscale("log")
            ax.set_xlim(edges[0], edges[-1])
            ax.set_ylim(bottom=0)
            ax.grid(alpha=0.3)
            label = ("top 20% of wallets" if kind == "wallet" else f"top 20% hold {i['top20_share']:.1%} of volume")
            ax.set_title(f"{role}: {'wallet distribution f(x)' if kind == 'wallet' else 'volume distribution x f(x)'}\n{label}")
            ax.set_ylabel("Share of wallets per decade" if kind == "wallet" else "Share of volume per decade")
            xl = "Wallet volume (USDC)"
            clipped = i["clipped_wallet_share"] if kind == "wallet" else i["clipped_volume_share"]
            if clipped > 0:
                xl += f"\nnot shown: {clipped:.2%} of {'wallets' if kind == 'wallet' else 'volume'}"
            ax.set_xlabel(xl)
        ax = axes[r, 2]
        g = lor[lor["role"] == role]
        ax.plot([0, 1], [0, 1], color="#888888", ls="--", lw=1)
        ax.plot(g["x"], g["y"], color=color, lw=1.8)
        ax.plot([1 - TOP_FRAC], [TOP_FRAC], marker="o", mfc="white", mec="#aa0000", ls="", ms=7)
        ax.plot([i["lorenz_x_at_80"]], [i["lorenz_y_at_80"]], marker="o", color="#aa0000", ls="", ms=6)
        ax.set(xlim=(0, 1), ylim=(0, 1), xlabel="Share of wallets (lowest volume first)", ylabel="Share of volume")
        ax.set_title(f"{role}: Lorenz curve\nbottom 80% hold {i['lorenz_y_at_80']:.1%}")
        ax.set_aspect("equal", adjustable="box")
        ax.grid(alpha=0.3)
    handles = [Patch(color=REST_COLOR, label="Bottom 80% of wallets"),
               Patch(color=ROLE_COLOR["maker"], label="Top 20%: maker"), Patch(color=ROLE_COLOR["taker"], label="Top 20%: taker"),
               Line2D([], [], color="#888888", ls="--", label="Equality (y = x)"),
               Line2D([], [], marker="o", mfc="white", mec="#aa0000", ls="", label="80/20 reference (0.8, 0.2)"),
               Line2D([], [], marker="o", color="#aa0000", ls="", label="Measured at 80% of wallets")]
    fig.legend(handles=handles, loc="outside upper center", ncol=3)
    fig.savefig(png, dpi=200)
    plt.close(fig)


def main() -> None:
    t0 = time.perf_counter()
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True, help="run folder with wallets.parquet and q2_results.json")
    ap.add_argument("--out", default=".")
    a = ap.parse_args()
    src, out = Path(a.source), Path(a.out)
    out.mkdir(parents=True, exist_ok=True)

    wallets = pd.read_parquet(src / "wallets.parquet")
    wallets = wallets[wallets["volume_usdc"] > 0]          # same filter as q2_concentration.py
    vols = {role: g["volume_usdc"].to_numpy(float) for role, g in wallets.groupby("role")}
    saved = json.loads((src / "q2_results.json").read_text())["concentration"]

    all_log = np.log10(np.concatenate(list(vols.values())))
    grid_lo, grid_hi = math.floor(all_log.min()), math.ceil(all_log.max())
    log_edges = np.linspace(grid_lo, grid_hi, (grid_hi - grid_lo) * BINS_PER_DECADE + 1)
    x_lo_dec = math.floor(np.quantile(all_log, LEFT_QUANTILE))
    x_lo = 10.0 ** x_lo_dec

    bin_parts, lor_parts, info, mismatches = [], [], {}, []
    for role in ("maker", "taker"):
        v = vols[role]
        wallet_sh, vol_sh = bin_shares(v, log_edges)
        bin_parts.append(pd.DataFrame({"role": role, "bin_lo_usdc": 10.0 ** log_edges[:-1], "bin_hi_usdc": 10.0 ** log_edges[1:],
                                       "wallet_share": wallet_sh, "volume_share": vol_sh}))
        lor = lorenz_points(v).assign(role=role)
        lor_parts.append(lor)

        n, k = len(v), max(1, math.ceil(TOP_FRAC * len(v)))
        cutoff = float(np.sort(v)[::-1][k - 1])             # smallest volume inside the top 20% of wallets
        s = (x_lo_dec - grid_lo) * BINS_PER_DECADE           # first plotted bin
        at80 = lor.iloc[int(np.argmin(np.abs(lor["x"].to_numpy() - (n - k) / n)))]
        got = {key: top_share(v, f) for key, f in TOP_SHARE_KEYS.items()}
        for key, val in got.items():
            if abs(val - saved[role][key]) > SHARE_TOLS:
                mismatches.append(f"{role} {key}: recomputed {val!r} saved {saved[role][key]!r}")
        if n != saved[role]["n_wallets"]:
            mismatches.append(f"{role} n_wallets: {n} saved {saved[role]['n_wallets']}")
        for name, sh in (("wallet_share", wallet_sh), ("volume_share", vol_sh)):
            if abs(sh.sum() - 1.0) > SHARE_TOLS:
                mismatches.append(f"{role} {name} sums to {sh.sum()!r}")
        if abs(at80["y"] - (1 - got["top20_share"])) > SHARE_TOLS:
            mismatches.append(f"{role} Lorenz at 80% {at80['y']!r} vs 1 - top20_share {1 - got['top20_share']!r}")
        info[role] = {"n_wallets": n, "top_k": k, "cutoff_usdc": cutoff, **got,
                      "lorenz_x_at_80": float(at80["x"]), "lorenz_y_at_80": float(at80["y"]),
                      "clipped_wallet_share": float(wallet_sh[:s].sum()), "clipped_volume_share": float(vol_sh[:s].sum()),
                      "bin_wallet_share_sum": float(wallet_sh.sum()), "bin_volume_share_sum": float(vol_sh.sum()),
                      "n_lorenz_points": int(len(lor))}

    bins = pd.concat(bin_parts, ignore_index=True)
    lor_all = pd.concat(lor_parts, ignore_index=True)[["role", "x", "y"]]
    bins.to_csv(out / "wallet_dist_bins.csv", index=False)     # no wallet ID: later edits redraw from these two files
    lor_all.to_csv(out / "lorenz_points.csv", index=False)
    draw_figure(bins, lor_all, info, x_lo, out / "wallet_dist_panels.png")

    manifest = {
        "code_version": CODE_VERSION,
        "code_sha": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()[:12],
        "params": {"source_run": src.name, "top_frac": TOP_FRAC, "bins_per_decade": BINS_PER_DECADE, "x_axis_start_usdc": x_lo,
                   "left_quantile": LEFT_QUANTILE, "n_lorenz_linear": N_LORENZ_LINEAR, "n_lorenz_top": N_LORENZ_TOP,
                   "share_tolerance": SHARE_TOLS},
        "env": {"hostname": socket.gethostname(), "python": platform.python_version(), "pandas": pd.__version__,
                "numpy": np.__version__, "slurm_job_id": os.environ.get("SLURM_JOB_ID", "none"),
                "slurm_cpus_per_task": os.environ.get("SLURM_CPUS_PER_TASK", "none")},
        "metrics": {
            "source_sha256": {f: sha256_file(src / f) for f in ("wallets.parquet", "q2_results.json")},
            "n_wallet_role_rows": {r: i["n_wallets"] for r, i in info.items()},
            "per_role": info,
            "shares_match_q2_results": not mismatches,
            "mismatches": mismatches,
            "wall_time_s": round(time.perf_counter() - t0, 1),
        },
    }
    (out / "manifest_wallet_dist.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print("SHARES MATCH" if not mismatches else "SHARE MISMATCH: " + "; ".join(mismatches))


if __name__ == "__main__":
    main()
