"""Last analysis stage: write verdicts.json into the run folder (measurement.md section 4.1).

Reads only saved JSON of the run folder. Applies the pre-registered decision criteria, encoded below, to the numbers.
Criteria files: analysis/prereg_mvp1.md (Q1) and analysis/prereg_mvp2.md (Q1a, Q1b, Q1c). Each entry records the
criteria file, so a verdict can be issued again from the same criteria and the same code (sha of this file).
Scope other than "full" is the first cycle: no verdict (the entry says so and keeps the numbers).
"""
import argparse
import hashlib
import json
from pathlib import Path

CODE_VERSION = "v3"   # no import from common.py: that module needs duckdb, this stage needs only the JSON files
CRITERIA = {"Q1": "analysis/prereg_mvp1.md", "Q1a": "analysis/prereg_mvp2.md",
            "Q1b": "analysis/prereg_mvp2.md", "Q1c": "analysis/prereg_mvp2.md"}


def sha12(path: Path) -> str | None:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:12] if path.exists() else None


def load(run: Path, name: str) -> dict | None:
    f = run / name
    return json.loads(f.read_text()) if f.exists() else None


def q1(res: dict, alpha: float) -> dict:
    """prereg_mvp1.md: chi-square p < alpha means not calibrated as a whole. Else no bin off after BH means no evidence."""
    m = res["main_with_min_filter"]
    c = m["chi2_gof"]
    if c["p"] < alpha:
        verdict = "Prices are not calibrated as a whole at this n."
    elif m["bins_reject_bh"] == 0:
        verdict = "No evidence of miscalibration at this n."
    else:
        verdict = "Chi-square does not reject, but some bins are off after BH."
    return {"statistic": {"name": "chi-square", "value": c["chi2"], "df": c["df"]}, "p": c["p"],
            "effect_size": {"name": "Cohen's w", "value": c["effect_w"]}, "n": m["n_markets"], "verdict": verdict,
            "extra": {"bins_off_bh": m["bins_reject_bh"], "bins_off_bonferroni": m["bins_reject_bonferroni"],
                      "brier": m["brier"]}}


def q1a(res: dict, alpha: float) -> dict:
    """prereg_mvp2.md Q1a: chi-square of independence p < alpha means accuracy depends on the topic."""
    c = res["chi_square_independence"]
    if c.get("p") is None:
        return {"statistic": {"name": "chi-square", "value": None, "df": None}, "p": None,
                "effect_size": {"name": "Cramer's V", "value": None}, "n": c.get("n"),
                "verdict": "Test not defined. " + str(c.get("note", ""))}
    verdict = ("Accuracy depends on the topic at this n." if c["p"] < alpha
               else "No evidence that accuracy depends on the topic at this n.")
    return {"statistic": {"name": "chi-square", "value": c["chi2"], "df": c["df"]}, "p": c["p"],
            "effect_size": {"name": "Cramer's V", "value": c["cramers_v"]}, "n": c["n"], "verdict": verdict,
            "extra": {"n_categories": c["n_categories"]}}


def q1b(res: dict, alpha: float) -> dict:
    """prereg_mvp2.md Q1b: p < alpha and mean Brier difference (7 d minus 1 d) > 0 means better near the deadline."""
    t = res["brier_diff_7d_minus_1d"]
    verdict = ("Better near the deadline." if t["p"] < alpha and t["mean_diff"] > 0
               else "No evidence of a gain near the deadline at this n.")
    return {"statistic": {"name": "t", "value": t["t"], "df": t["df"]}, "p": t["p"],
            "effect_size": {"name": "Cohen's d", "value": t["cohens_d"], "mean_diff": t["mean_diff"],
                            "ci": [t["ci_low"], t["ci_high"]]},
            "n": t["n"], "verdict": verdict}


def q1c(res: dict, alpha: float) -> dict:
    """prereg_mvp2.md Q1c: p < alpha and Spearman rho < 0 means busier markets are more accurate."""
    t = res["spearman_log_volume_vs_error"]
    verdict = ("Busier markets are more accurate." if t["p"] < alpha and t["rho"] < 0
               else "No evidence that busier markets are more accurate at this n.")
    return {"statistic": {"name": "Spearman rho", "value": t["rho"], "df": None}, "p": t["p"],
            "effect_size": {"name": "rho", "value": t["rho"], "ci": [t["ci_low"], t["ci_high"]]},
            "n": t["n"], "verdict": verdict}


COMPARISONS = {"Q1": ("q1_results.json", q1), "Q1a": ("q1a_results.json", q1a),
               "Q1b": ("q1b_results.json", q1b), "Q1c": ("q1c_results.json", q1c)}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=".", help="the run folder")
    run = Path(ap.parse_args().out)
    prereg = load(run, "prereg.json") or {}
    alpha, judged = float(prereg.get("alpha", 0.05)), prereg.get("scope") == "full"
    project = Path(__file__).resolve().parent.parent   # criteria files live in <project>/analysis
    entries = {}
    for name, (file, rule) in COMPARISONS.items():
        res = load(run, file)
        if res is None:
            continue   # Q1a to Q1c exist only in MVP2 runs
        entry = rule(res, alpha)
        entry["judged"] = judged
        entry["rule_result"] = entry["verdict"]   # what the criteria say; kept even when the scope gives no verdict
        if not judged:
            entry["verdict"] = "First cycle, no verdict."
        entry["criteria_file"] = CRITERIA[name]
        entry["criteria_sha256_12"] = sha12(project / CRITERIA[name])
        entries[name] = entry
    out = {"code_version": CODE_VERSION, "verdicts_py_sha256_12": sha12(Path(__file__)), "alpha": alpha,
           "scope": prereg.get("scope"), "prereg_json_sha256_12": sha12(run / "prereg.json"), "comparisons": entries}
    (run / "verdicts.json").write_text(json.dumps(out, indent=2, default=str))
    print(f"wrote {run / 'verdicts.json'}: " + ", ".join(f"{k}: {v['verdict']}" for k, v in entries.items()))


if __name__ == "__main__":
    main()
