"""Shared helpers for the robustness v3 stages (analysis/prereg_review_fixes.md, owner answers D-039).

Pure functions plus the stage argument parser. Every row printed here is a descriptive sensitivity row next to Q1.
"""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

from common import load_params
from q1_calibration import analyze
from verdicts import q1 as q1_rule

OUTSIDE_LECTURE = "outside the lectures (D-039)"   # label the paper prints for X2_cl, Brier skill score, Wilson, logistic calibration


def load_prereg(path: str) -> dict:
    """The review-fixes prereg overlaid on the base prereg it `extends` (found next to it by file name)."""
    review = json.loads(Path(path).read_text())
    base = Path(path).parent / Path(review["extends"]).name if "extends" in review else None
    params = load_params(str(base) if base else None)
    params.update(review)
    return params


def stage_args() -> tuple[argparse.Namespace, Path, Path, dict]:
    ap = argparse.ArgumentParser()
    ap.add_argument("--params", required=True, help="prereg_review_fixes.json copy (its base sits next to it)")
    ap.add_argument("--source", required=True, help="base run folder (142082): markets.parquet, q1_results.json, q2_results.json")
    ap.add_argument("--out", default=".")
    ap.add_argument("--label-run", default=None, help="run folder of the V-1 label check (150296)")
    args = ap.parse_args()
    return args, Path(args.out), Path(args.source), load_prereg(args.params)


def load_kept(out: Path) -> pd.DataFrame:
    """Kept markets from r3_build.py, sorted by market_id, y as int."""
    m = pd.read_parquet(out / "r3_markets.parquet")
    kept = m[m["kept"]].sort_values("market_id").reset_index(drop=True)
    kept["y"] = kept["y"].astype(int)
    return kept


def load_main_q1(src: Path) -> dict:
    return json.loads((src / "q1_results.json").read_text())["main_with_min_filter"]


def bin_of(p: np.ndarray, n_bins: int) -> np.ndarray:
    return np.minimum((np.asarray(p, float) * n_bins).astype(int), n_bins - 1)   # code/q1_calibration.py rule


def t_interval(x: np.ndarray, alpha: float) -> dict:
    """Mean with a t interval and d_z = mean / sd."""
    x = np.asarray(x, float)
    n = len(x)
    mean, sd = float(x.mean()), float(x.std(ddof=1))
    half = float(stats.t.ppf(1 - alpha / 2, n - 1) * sd / np.sqrt(n)) if sd > 0 else 0.0
    return {"n": n, "mean": mean, "ci_low": mean - half, "ci_high": mean + half, "d_z": mean / sd if sd > 0 else float("nan")}


def rule_text(res: dict, alpha: float) -> str:
    """Q1 rule text (prereg_mvp1.md) for a result dict with chi2_gof.p and bins_reject_bh."""
    return q1_rule({"main_with_min_filter": res}, alpha)["verdict"]


def q1_row(df: pd.DataFrame, price: str, alpha: float, n_bins: int, main_res: dict,
           main_gap: float) -> tuple[dict, pd.DataFrame]:
    """The Q1 analysis on one price column, plus net gap with t CI, d_z, rule text and row agreement against main."""
    d = pd.DataFrame({"market_id": df["market_id"].to_numpy(), "p_1d": df[price].to_numpy(float), "y": df["y"].to_numpy(int)})
    res, bins, _ = analyze(d, n_bins, alpha)
    gap = t_interval(d["y"] - d["p_1d"], alpha)
    c, mc = res["chi2_gof"], main_res["chi2_gof"]
    text, main_text = rule_text(res, alpha), rule_text(main_res, alpha)
    row = {"n": res["n_markets"], "chi2": c["chi2"], "df": c["df"], "p": c["p"], "w": c["effect_w"],
           "bins_off_bh": res["bins_reject_bh"], "net_gap": gap["mean"], "net_gap_ci_low": gap["ci_low"],
           "net_gap_ci_high": gap["ci_high"], "d_z": gap["d_z"], "rule_text": text,
           "row_agreement": "same" if text == main_text else "different",
           "delta_w": c["effect_w"] - mc["effect_w"], "delta_net_gap": gap["mean"] - main_gap,
           "mean_sq_residual": res["brier"]}
    return row, bins


def main_net_gap(kept: pd.DataFrame) -> float:
    """Net gap of the main row: mean(y - p_1d) over the kept markets."""
    return float((kept["y"] - kept["p_1d"]).mean())


def bin_gaps(bins: pd.DataFrame, alpha: float) -> pd.DataFrame:
    """Per-bin gap (observed - mean price) with Wilson and z intervals of the observed rate."""
    z = stats.norm.ppf(1 - alpha / 2)
    out = bins[["bin", "n", "mean_price", "observed_rate"]].copy()
    out["gap"] = bins["observed_rate"] - bins["mean_price"]
    out["wilson_low"] = bins["ci_low"] - bins["mean_price"]
    out["wilson_high"] = bins["ci_high"] - bins["mean_price"]
    se = np.sqrt(bins["observed_rate"] * (1 - bins["observed_rate"]) / bins["n"])
    out["z_low"] = out["gap"] - z * se
    out["z_high"] = out["gap"] + z * se
    return out


def flat(prefix: str, row: dict) -> dict:
    return {f"{prefix}_{k}": v for k, v in row.items()}


def row_line(name: str, row: dict) -> dict:
    """One printed table row of a q1_row result."""
    return {"row": name, "n": row["n"], "chi2": f"{row['chi2']:.2f} ({row['df']})", "p": row["p"], "w": row["w"],
            "bins_off_bh": row["bins_off_bh"],
            "net_gap [95% CI]": f"{row['net_gap']:.4f} [{row['net_gap_ci_low']:.4f}, {row['net_gap_ci_high']:.4f}]",
            "d_z": row["d_z"], "agreement": row["row_agreement"]}
