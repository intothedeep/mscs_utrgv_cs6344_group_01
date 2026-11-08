"""Robustness v3, M5: practical size of the miscalibration (prereg_review_fixes.md section 5).

Logistic calibration fit logit(P(y = 1)) = a + b logit(p_1d) (outside the lectures: calibration use is ours), implied gap
at fixed prices with a cluster bootstrap interval (read proxy and draws of M3), Brier skill score against the in-sample
climatology (outside the lectures), majority baseline. Needs m3_bootstrap.json and m3_clusters.csv (M3); uses the mean
half-spread proxy h from m1_results.json when it exists. Descriptive, no verdict.
"""
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.special import expit, logit
from statsmodels.tools.sm_exceptions import PerfectSeparationError

from common import md_table, run_stage, write_json, write_manifest
from r3_common import OUTSIDE_LECTURE, load_kept, stage_args

STAGE = "r3_m5"
FINE_GRID = np.linspace(0.02, 0.98, 49)


def fit_logit(x: np.ndarray, y: np.ndarray, start: np.ndarray | None = None) -> np.ndarray:
    return np.asarray(sm.Logit(y, sm.add_constant(x)).fit(disp=0, start_params=start, maxiter=100).params)


def implied_gap(params: np.ndarray, grid: np.ndarray) -> np.ndarray:
    return expit(params[0] + params[1] * logit(grid)) - grid


def bootstrap_fits(codes: np.ndarray, n_clusters: int, x: np.ndarray, y: np.ndarray, start: np.ndarray, reps: int, seed: int) -> np.ndarray:
    """Refit on cluster resamples, same generator and draw pattern as r3_m3.bootstrap. Failed fits give NaN rows."""
    rng = np.random.default_rng(seed)
    out = np.full((reps, 2), np.nan)
    for i in range(reps):
        w = np.bincount(rng.integers(0, n_clusters, n_clusters), minlength=n_clusters)
        idx = np.repeat(np.arange(len(x)), w[codes])
        try:
            out[i] = fit_logit(x[idx], y[idx], start)
        except (ValueError, np.linalg.LinAlgError, PerfectSeparationError):   # counted as failed refits, not hidden
            continue
    return out


def draw(boot: np.ndarray, base: np.ndarray, out) -> None:
    fig, ax = plt.subplots(figsize=(7, 4), layout="constrained")
    gaps = np.array([implied_gap(b, FINE_GRID) for b in boot if np.isfinite(b).all()])
    lo, hi = np.percentile(gaps, [2.5, 97.5], axis=0)
    ax.fill_between(FINE_GRID, lo, hi, color="#bbbbbb", label="Cluster bootstrap 95% interval")
    ax.plot(FINE_GRID, implied_gap(base, FINE_GRID), color="#222222", label="Implied gap from the fit")
    ax.axhline(0, color="#888888", ls="--", label="Calibrated")
    ax.set(xlabel="Price p_1d (USDC per share)", ylabel="Implied gap: expit(a + b logit p) - p")
    ax.grid(alpha=0.3)
    fig.legend(loc="outside upper center", ncol=3)
    fig.savefig(out / "fig_r3_m5_implied_gap.png", dpi=150)
    plt.close(fig)


def main() -> None:
    _, out, _, params = stage_args()
    eps = float(params["m5_clip_eps"])
    grid = np.array(params["m5_delta_grid"], float)

    def work() -> dict[str, str]:
        kept = load_kept(out)
        p, y = kept["p_1d"].to_numpy(float), kept["y"].to_numpy(float)
        x = logit(np.clip(p, eps, 1 - eps))
        n_clipped = int(((p < eps) | (p > 1 - eps)).sum())
        res = sm.Logit(y, sm.add_constant(x)).fit(disp=0)
        base = np.asarray(res.params)
        wald = np.asarray(res.conf_int(alpha=float(params["alpha"])))

        m3 = json.loads((out / "m3_bootstrap.json").read_text())
        read = m3["read_proxy"]
        col = "k1" if read.startswith("k1") else "k2"
        clusters = pd.read_csv(out / "m3_clusters.csv", dtype=str, keep_default_na=False)
        if not clusters["market_id"].equals(kept["market_id"]):
            raise ValueError("m3_clusters.csv rows differ from the kept markets")
        codes, uniques = pd.factorize(clusters[col], sort=True)
        boot = bootstrap_fits(codes, len(uniques), x, y, base, int(params["m3_bootstrap_B"]), int(params["m3_seed"]))
        ok = np.isfinite(boot).all(axis=1)
        bci = np.percentile(boot[ok], [2.5, 97.5], axis=0)

        h = None
        m1_path = out / "m1_results.json"
        if m1_path.exists():
            h = json.loads(m1_path.read_text()).get("mean_h")
        delta_boot = np.array([implied_gap(b, grid) for b in boot[ok]])
        d_lo, d_hi = np.percentile(delta_boot, [2.5, 97.5], axis=0)
        d_hat = implied_gap(base, grid)
        table = []
        for i, g in enumerate(grid):
            min_abs = d_lo[i] if d_lo[i] > 0 else (-d_hi[i] if d_hi[i] < 0 else 0.0)   # smallest |gap| inside the interval
            practical = None if h is None else bool(min_abs > h)
            table.append({"price": float(g), "delta": float(d_hat[i]), "ci_low": float(d_lo[i]), "ci_high": float(d_hi[i]),
                          "practically_sized": practical})

        brier = float(np.mean((p - y) ** 2))
        ybar = float(y.mean())
        clim = ybar * (1 - ybar)
        acc = float(((p > 0.5) == (y == 1)).mean())
        results = {"a": float(base[0]), "b": float(base[1]), "a_wald_ci": wald[0].tolist(), "b_wald_ci": wald[1].tolist(),
                   "a_boot_ci": bci[:, 0].tolist(), "b_boot_ci": bci[:, 1].tolist(), "read_proxy": read, "n_boot_ok": int(ok.sum()),
                   "n_boot_failed": int((~ok).sum()), "n_clipped": n_clipped, "n": len(kept), "delta_table": table,
                   "practical_line_mean_h": h, "brier": brier, "climatology": clim, "brier_skill_score": 1 - brier / clim,
                   "bss_note": "in-sample climatology", "class_balance_yes": ybar, "majority_accuracy": max(ybar, 1 - ybar),
                   "accuracy_at_0.5": acc, "labels": {"logistic_calibration": OUTSIDE_LECTURE, "brier_skill_score": OUTSIDE_LECTURE}}
        write_json(out / "m5_calibration_fit.json", results)
        write_json(out / "m5_results.json", {k: v for k, v in results.items() if k != "delta_table"}
                   | {f"delta_{t['price']:.2f}": t["delta"] for t in table})
        draw(boot[ok], base, out)
        write_manifest(out, params, {k: v for k, v in results.items() if k != "delta_table"}, __file__, STAGE)
        return {
            "Why": "M5: the chi-square p is tiny but w is 0.0377. How large is the miscalibration in usable terms?",
            "Input data": f"{len(kept)} kept markets (p_1d, y). Bootstrap draws of the read proxy {read} (M3). Real data.",
            "Output data": "m5_calibration_fit.json, m5_results.json, fig_r3_m5_implied_gap.png",
            "Result": f"a {base[0]:.4f} (Wald {wald[0][0]:.4f} to {wald[0][1]:.4f}), b {base[1]:.4f} (Wald {wald[1][0]:.4f} to "
                      f"{wald[1][1]:.4f}). b < 1: prices too extreme. Clipped {n_clipped}. Failed refits {int((~ok).sum())}.\n\n"
                      + md_table(pd.DataFrame(table)) + f"\n\nPractical line (mean h from M1): {h}. Brier {brier:.4f}, climatology "
                      f"{clim:.4f}, skill score {1 - brier / clim:.4f} (in-sample climatology). Majority accuracy "
                      f"{max(ybar, 1 - ybar):.4f}, accuracy at 0.5 {acc:.4f}. Logistic calibration and the skill score are {OUTSIDE_LECTURE}.",
            "Figure": "![m5](fig_r3_m5_implied_gap.png)  Caption: implied gap between the fitted probability and the price. "
                      "Why: a band that excludes 0 at a price shows the gap there is not noise. Source: this run folder.",
        }

    run_stage(out, STAGE, "M5: practical size of the miscalibration.", work)


if __name__ == "__main__":
    main()
