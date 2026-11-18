"""Q1 calibration repeated with the last price before the close (p_T), next to the main price (p_1d).

Reads the saved per-market file of check R2 only (runs/142123_robust_full_v4/r2_markets.csv).
Same rules as code/q1_calibration.py: 10 equal-width bins, chi-square goodness of fit with
df = 10, exact two-sided binomial test per bin, Benjamini-Hochberg and Bonferroni at 0.05.
The p_1d rows must reproduce the main run (chi-square 67.99, 5 BH bins); the script stops if not.
Descriptive check for the tips page. It is not in the paper.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

__all__ = ["calibrate"]

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "runs" / "142123_robust_full_v4" / "r2_markets.csv"
OUT = ROOT / "runs" / "local_r2close_v14"
N_BINS = 10
ALPHA = 0.05


def bh_reject(p: np.ndarray, alpha: float) -> np.ndarray:
    """Benjamini-Hochberg step-up: reject ranks up to the largest i with p_(i) <= i * alpha / m."""
    m = len(p)
    order = np.argsort(p)
    ok = p[order] <= alpha * np.arange(1, m + 1) / m
    k = np.max(np.nonzero(ok)[0]) + 1 if ok.any() else 0
    rej = np.zeros(m, dtype=bool)
    rej[order[:k]] = True
    return rej


def calibrate(df: pd.DataFrame, col: str) -> tuple[pd.DataFrame, dict]:
    b = np.minimum((df[col] * N_BINS).astype(int), N_BINS - 1)
    g = df.groupby(b).agg(n=("y", "size"), n_yes=("y", "sum"), mean_price=(col, "mean")).reset_index(names="bin")
    e = g["n"] * g["mean_price"]
    d = g["n_yes"] - e
    g["expected"] = e
    g["observed_rate"] = g["n_yes"] / g["n"]
    g["gap_pp"] = (g["observed_rate"] - g["mean_price"]) * 100
    g["chi_part"] = d**2 / e + d**2 / (g["n"] - e)
    g["binom_p"] = [stats.binomtest(int(k), int(n), float(np.clip(p, 0, 1))).pvalue
                    for k, n, p in zip(g["n_yes"], g["n"], g["mean_price"])]
    g["reject_bh"] = bh_reject(g["binom_p"].to_numpy(), ALPHA)
    g["reject_bonferroni"] = g["binom_p"] * N_BINS <= ALPHA
    chi = float(g["chi_part"].sum())
    summary = {
        "price": col, "n": int(len(df)), "chi_square": chi, "df": N_BINS,
        "p": float(stats.chi2.sf(chi, N_BINS)),
        "bins_bh": int(g["reject_bh"].sum()), "bins_bonferroni": int(g["reject_bonferroni"].sum()),
        "bins_negative": int((g["gap_pp"] < 0).sum()),
        "net_gap_pp": float((df["y"].mean() - df[col].mean()) * 100),
    }
    return g, summary


def main() -> None:
    df = pd.read_csv(SRC)
    OUT.mkdir(parents=True, exist_ok=True)
    out = {}
    for col in ("p_1d", "p_T"):
        g, s = calibrate(df, col)
        g.to_csv(OUT / f"bins_{col}.csv", index=False)
        out[col] = s
    # Gate: p_1d must match the main run 142082 before p_T is trusted.
    main_run = out["p_1d"]
    assert abs(main_run["chi_square"] - 67.99) < 0.01 and main_run["bins_bh"] == 5, main_run
    (OUT / "results.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
