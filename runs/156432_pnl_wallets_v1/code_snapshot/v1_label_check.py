"""V-1 label check (D-036): what is the label of the outcome coded 1 (`outcome_seq = 1`) in the 47,948 kept markets?

Follows `analysis/prereg_v1_label_check.md` (written before the run). `label1` is not saved in `markets.parquet`, so this
script reads the kept list, `y`, `p_1d` and `category_refined` from the saved `markets.parquet` of the source run, and reads
three raw columns plus `winning_outcome_label` of the kept markets. `label1` uses the same expression as
`common.build_market_set`. Counts and shares only. No model, no fit, no new test.

Usage on a compute node (job `jobs/v1_label_check.slurm`):
  python code/v1_label_check.py --source runs/142082_mvp1_full_v1r3 --out runs/<JOB>_v1label
"""
import argparse
import hashlib
import json
import time
from pathlib import Path

import numpy as np
import pandas as pd

from common import code_sha, connect, env_info, raw_glob
from q1_calibration import analyze

CODE_VERSION = "v1label-v2"   # own label, like ccdf_redraw.py; bumped by hand
BASE_RUN = "142082_mvp1_full_v1r3"
NORMALIZATION = "label_norm = lower(trim(label1)), runs of inner whitespace collapsed to one space; no other change"
EXPECTED_KEPT = 47_948        # prereg: the joined row count must be this, else Stop
ALPHA = 0.05                  # only passed to analyze(); chi2 does not use it
TOP_ALL, TOP_CAT = 20, 5
SHARE_LINE = 0.95             # prereg section 4
OFF_BINS = (0, 1, 6, 7, 8)    # prereg section 3 (off after BH)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def normalize(label: pd.Series) -> pd.Series:
    """lower(trim()) and inner whitespace runs collapsed to one space. NULL stays NULL."""
    return label.str.strip().str.lower().str.replace(r"\s+", " ", regex=True)


def load_raw_labels(kept_ids: pd.DataFrame) -> pd.DataFrame:
    """label1 and winning_outcome_label per kept market (market-level pass over four raw columns)."""
    con = connect()
    con.register("kept", kept_ids)
    return con.execute(f"""
        SELECT r.condition_id AS market_id,
               max(r.outcome_label) FILTER (WHERE CAST(r.outcome_seq AS BIGINT) = 1) AS label1,
               count(DISTINCT r.outcome_label) FILTER (WHERE CAST(r.outcome_seq AS BIGINT) = 1) AS n_distinct_label1,
               max(r.winning_outcome_label) AS winning_outcome_label
        FROM read_parquet('{raw_glob()}', union_by_name=true) r
        SEMI JOIN kept k ON k.market_id = r.condition_id
        GROUP BY r.condition_id""").df()


def top_labels(s: pd.Series, k: int) -> list[dict]:
    vc = s.value_counts(dropna=False).head(k)
    return [{"label_norm": None if pd.isna(v) else str(v), "n": int(n), "share": float(n / len(s))}
            for v, n in vc.items()]


def group_stats(g: pd.DataFrame) -> dict:
    return {"n": int(len(g)), "n_yes_like": int(g["is_yes_like"].sum()),
            "share_yes_like": float(g["is_yes_like"].mean()) if len(g) else None}


def yes_only_stats(g: pd.DataFrame) -> dict:
    y = g[g["is_yes_like"]]
    n = len(y)
    mean_price = float(y["p_1d"].mean()) if n else None
    rate = float(y["y"].sum() / n) if n else None
    return {"n": int(n), "n_y1": int(y["y"].sum()), "mean_price": mean_price, "observed_rate": rate,
            "diff_obs_minus_price": rate - mean_price if n else None}


def decide(result: dict, q1_n: dict[int, int]) -> str:
    """Prereg section 4: Stop, else A when the overall share and the five off bins are all >= 0.95, else B."""
    if result["n_markets"] != EXPECTED_KEPT or any(result["by_bin"][str(b)]["n"] != q1_n.get(b) for b in range(10)):
        return "STOP"
    shares = [result["overall"]["share_yes_like"]] + [result["by_bin"][str(b)]["share_yes_like"] for b in OFF_BINS]
    return "A" if all(s is not None and s >= SHARE_LINE for s in shares) else "B"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True, help="run folder with markets.parquet, prereg.json, q1_bins.csv")
    ap.add_argument("--out", default=".")
    args = ap.parse_args()
    src, out = Path(args.source), Path(args.out)
    t0 = time.time()

    n_bins = int(json.loads((src / "prereg.json").read_text())["n_bins"])
    q1_n = {int(r.bin): int(r.n) for r in pd.read_csv(src / "q1_bins.csv").itertuples()}
    m = pd.read_parquet(src / "markets.parquet", columns=["market_id", "category_refined", "p_1d", "y", "kept"])
    kept = m[m["kept"]].drop(columns="kept")
    df = kept.merge(load_raw_labels(kept[["market_id"]]), on="market_id", how="left")
    df["category_refined"] = df["category_refined"].fillna("Unknown")
    df["label_norm"] = normalize(df["label1"])
    df["is_yes_like"] = df["label_norm"].eq("yes")
    df["is_no_like"] = df["label_norm"].eq("no")
    df["bin"] = np.minimum((df["p_1d"] * n_bins).astype(int), n_bins - 1)   # same rule as q1_calibration.analyze
    df[["market_id", "label1", "label_norm", "is_yes_like", "category_refined", "p_1d", "y", "bin"]] \
        .sort_values("market_id").to_csv(out / "label1_by_market.csv", index=False)

    # Mirror check: p -> 1 - p and y -> 1 - y, same bin rule and chi-square code as Q1 (prereg section 5.1).
    mirrored = df[["market_id", "p_1d", "y"]].assign(p_1d=1 - df["p_1d"], y=1 - df["y"])
    chi2_mirrored = analyze(mirrored, n_bins, ALPHA)[0]["chi2_gof"]
    chi2_q1 = analyze(df[["market_id", "p_1d", "y"]], n_bins, ALPHA)[0]["chi2_gof"]
    scaled = df["p_1d"] * n_bins
    win_norm = normalize(df["winning_outcome_label"])

    result = {
        "n_markets": int(len(df)),
        "base_run": BASE_RUN,
        "normalization": NORMALIZATION,
        "overall": {
            "top_labels": top_labels(df["label_norm"], TOP_ALL),
            "n_distinct_label_norm": int(df["label_norm"].nunique()),
            "n_yes_like": int(df["is_yes_like"].sum()), "share_yes_like": float(df["is_yes_like"].mean()),
            "n_no_like": int(df["is_no_like"].sum()), "share_no_like": float(df["is_no_like"].mean()),
        },
        "by_category": {str(c): {**group_stats(g), "top_labels": top_labels(g["label_norm"], TOP_CAT)}
                        for c, g in df.groupby("category_refined")},
        "by_bin": {str(b): group_stats(df[df["bin"] == b]) for b in range(n_bins)},
        "by_bin_yes_only": {str(b): yes_only_stats(df[df["bin"] == b]) for b in range(n_bins)},
        "checks": {
            "n_multi_label1": int((df["n_distinct_label1"] > 1).sum()),
            "n_y_case_mismatch": int(((win_norm == df["label_norm"]) & (df["winning_outcome_label"] != df["label1"])).sum()),
            "n_p1d_on_inner_edge": int(((scaled == scaled.round()) & (scaled.round() >= 1) & (scaled.round() <= n_bins - 1)).sum()),
            "chi2_mirrored": {**chi2_mirrored, "chi2_q1_recomputed": chi2_q1["chi2"]},
        },
    }
    result["decision"] = decide(result, q1_n)
    (out / "label1_counts.json").write_text(json.dumps(result, indent=2, default=str))

    pd.DataFrame([{"category_refined": c, **{k: v[k] for k in ("n", "n_yes_like", "share_yes_like")}}
                  for c, v in result["by_category"].items()]).to_csv(out / "label_check_by_category.csv", index=False)

    script = str(Path(__file__).resolve())
    manifest = {"code_version": CODE_VERSION, "code_sha": code_sha(script),
                "params": {"source": str(src), "n_bins": n_bins, "expected_kept": EXPECTED_KEPT,
                           "share_line": SHARE_LINE, "off_bins": list(OFF_BINS), "normalization": NORMALIZATION,
                           "prereg": "analysis/prereg_v1_label_check.md"},
                "env": env_info(),
                "metrics": {"n_markets": result["n_markets"], "decision": result["decision"],
                            "share_yes_like": result["overall"]["share_yes_like"],
                            "wall_s": round(time.time() - t0, 1),
                            "source_markets_parquet_sha256": sha256_file(src / "markets.parquet")}}
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, default=str))
    print(f"decision {result['decision']} n {result['n_markets']} yes_like {result['overall']['n_yes_like']} "
          f"share {result['overall']['share_yes_like']:.4f}")


if __name__ == "__main__":
    main()
