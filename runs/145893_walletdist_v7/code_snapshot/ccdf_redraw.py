"""Redraw of the wallet-volume CCDF with ranks sampled from the TOP (finding A1), plus the cluster x category crosstab.

Why a new script: `q2_concentration.py` `draw_ccdf` samples log-spaced ranks from the smallest wallet, so the top ~0.46% of
wallets has no points and the last segment is one straight chord. That function is stage code of run 142082 and stays as it is.
This script reads the saved `wallets.parquet` of that run and adds a run. It fits nothing: the cluster labels come from the
saved `q2_kmeans_sample.csv`. A wallet is one address, never a person.

Usage on a compute node (job `jobs/ccdf_redraw.slurm`):
  python code/ccdf_redraw.py --source runs/142082_mvp1_full_v1r3 --out runs/<JOB>_ccdf_v6
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
from scipy import stats

CODE_VERSION = "ccdf-v1"      # own label, like lecture_numbers.py; bumped by hand
SEED = 42                     # same as q2_concentration.py SEED
KMEANS_SAMPLE = 200_000       # same as q2_concentration.py KMEANS_SAMPLE
ROLE_COLOR = {"maker": "#222222", "taker": "#aa5500"}   # same as q2_concentration.py, so the figures match
N_LOG = 3000                  # log-spaced ranks per direction (the old figure used 3000 from the bottom)
TOP_ALL = 1000                # every wallet in the top 1,000 by rank is plotted


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def ccdf_points(volume: np.ndarray) -> pd.DataFrame:
    """Volume and CCDF (share of wallets at or above this rank) at log-spaced ranks from the top and from the bottom, plus the top 1,000."""
    xs = np.sort(volume)
    n = len(xs)
    log_pos = np.unique(np.logspace(0, np.log10(n), N_LOG).astype(int))   # 1 .. n
    idx = np.unique(np.concatenate([log_pos - 1,                           # from the smallest wallet (old rule)
                                    n - log_pos,                           # from the largest wallet (new)
                                    np.arange(max(0, n - TOP_ALL), n)]))   # the whole top 1,000
    return pd.DataFrame({"volume_usdc": xs[idx], "ccdf": 1 - idx / n})


def draw_ccdf(points: pd.DataFrame, png: Path) -> None:
    fig, ax = plt.subplots(figsize=(6, 4), layout="constrained")
    for role in ("maker", "taker"):
        g = points[points["role"] == role]
        ax.loglog(g["volume_usdc"], g["ccdf"], label=role, color=ROLE_COLOR[role])
    ax.set(xlabel="Wallet volume (USDC)", ylabel="CCDF (share of wallets above)")
    ax.grid(alpha=0.3)
    fig.legend(loc="outside upper center", ncol=2)
    fig.savefig(png, dpi=150)
    plt.close(fig)


def cluster_tables(wallets: pd.DataFrame, labels: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, dict, int]:
    """Crosstab of the saved cluster (z-score k-means) x dominant category, on the same fixed-seed sample as q2_concentration.py.

    Returns observed, expected, the chi-square result and the number of sample rows missing from the saved labels.
    """
    wallets = wallets.sort_values(["wallet", "role"]).reset_index(drop=True)
    sample = wallets.sample(min(KMEANS_SAMPLE, len(wallets)), random_state=SEED).sort_values(["wallet", "role"]).reset_index(drop=True)
    merged = sample.merge(labels[["wallet", "role", "cluster_z"]], on=["wallet", "role"], how="left")
    n_missing = int(merged["cluster_z"].isna().sum())
    merged = merged.dropna(subset=["cluster_z"])
    ct = pd.crosstab(merged["cluster_z"].astype(int).rename("cluster"), merged["dominant_category"].fillna("Unknown"))
    chi2, p, dof, expected = stats.chi2_contingency(ct)
    expected = pd.DataFrame(expected, index=ct.index, columns=ct.columns)
    return ct, expected, {"chi2": float(chi2), "df": int(dof), "p": float(p)}, n_missing


def main() -> None:
    t0 = time.perf_counter()
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True, help="run folder with wallets.parquet, q2_kmeans_sample.csv, q2_results.json")
    ap.add_argument("--out", default=".")
    a = ap.parse_args()
    src, out = Path(a.source), Path(a.out)
    out.mkdir(parents=True, exist_ok=True)

    wallets = pd.read_parquet(src / "wallets.parquet")
    wallets = wallets[wallets["volume_usdc"] > 0]          # same filter as q2_concentration.py
    parts = []
    for role, g in wallets.groupby("role"):
        parts.append(ccdf_points(g["volume_usdc"].to_numpy(float)).assign(role=role))
    points = pd.concat(parts, ignore_index=True)[["role", "volume_usdc", "ccdf"]]
    points.to_csv(out / "ccdf_points.csv", index=False)     # no wallet ID: later edits redraw from this file
    draw_ccdf(points, out / "fig6_ccdf_top_sampled.png")

    labels = pd.read_csv(src / "q2_kmeans_sample.csv")
    observed, expected, got, n_missing = cluster_tables(wallets, labels)
    observed.to_csv(out / "cluster_category_crosstab.csv")
    expected.to_csv(out / "cluster_category_expected.csv")
    want = json.loads((src / "q2_results.json").read_text())["kmeans"]["chi2_cluster_x_category"]
    reproduced = (n_missing == 0 and got["df"] == want["df"]
                  and math.isclose(got["chi2"], want["chi2"], rel_tol=1e-9)
                  and math.isclose(got["p"], want["p"], rel_tol=1e-9, abs_tol=1e-300))

    manifest = {
        "code_version": CODE_VERSION,
        "code_sha": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()[:12],
        "params": {"source_run": src.name, "seed": SEED, "kmeans_sample": KMEANS_SAMPLE, "n_log_ranks": N_LOG, "top_all": TOP_ALL},
        "env": {"hostname": socket.gethostname(), "python": platform.python_version(), "pandas": pd.__version__,
                "numpy": np.__version__, "slurm_job_id": os.environ.get("SLURM_JOB_ID", "none"),
                "slurm_cpus_per_task": os.environ.get("SLURM_CPUS_PER_TASK", "none")},
        "metrics": {
            "source_sha256": {f: sha256_file(src / f) for f in ("wallets.parquet", "q2_kmeans_sample.csv", "q2_results.json")},
            "n_wallet_role_rows": {r: int(c) for r, c in wallets["role"].value_counts().sort_index().items()},
            "n_points": {r: int(c) for r, c in points["role"].value_counts().sort_index().items()},
            "n_sample_rows_without_saved_label": n_missing,
            "chi2_reproduced": reproduced,
            "chi2_recomputed": got, "chi2_saved": {k: want[k] for k in ("chi2", "df", "p")},
            "wall_time_s": round(time.perf_counter() - t0, 1),
        },
    }
    (out / "manifest_ccdf_redraw.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print("CHI2 REPRODUCED" if reproduced else "CHI2 MISMATCH: see manifest_ccdf_redraw.json")


if __name__ == "__main__":
    main()
