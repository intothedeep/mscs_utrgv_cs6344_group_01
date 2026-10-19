"""Job B last stage: summary.md linking every stage report with its status."""
import argparse
import re
from pathlib import Path

STAGES = ["build_tables", "q3_describe", "q1_calibration", "q2_concentration"]


def stage_status(report: Path) -> str:
    if not report.exists():
        return "failed or not run: no report written"
    match = re.search(r"\*\*Status:\*\* (.*)", report.read_text())
    return match.group(1).splitlines()[0][:120] if match else "unknown (no Status field)"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=".")
    out = Path(ap.parse_args().out)
    lines = ["# MVP1 first end-to-end cycle: summary", "", "| Stage | Status | Report |", "| --- | --- | --- |"]
    for stage in STAGES:
        report = out / f"report_{stage}.md"
        lines.append(f"| {stage} | {stage_status(report)} | [report_{stage}.md](report_{stage}.md) |")
    (out / "summary.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
