"""Course report figures for the right-hand figure column: Figure 1 (two panels stacked), Figure 2 (CCDF), Figure 3 (QQ).

Why: the owner asked for text on the left and figures on the right, in reading order (2026-11-18).
Same drawing code as fig_report2p_half; only the printed width changes, to the right column (0.47 of the text width),
so the 7.5 pt text prints at 7.5 pt. Reads saved outputs only (runs 142082, 145892, 145897).
"""
import json
import shutil
from pathlib import Path

import pandas as pd

import fig_report2p_half as h
from fig_calibration_gap import SRC, load_bins

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "runs" / "local_report_col_v16"
COL_IN = round(0.47 * h.TEXTWIDTH_IN, 3)


def main() -> None:
    h.set_font()
    h.W_CALIB = h.W_CCDF = h.W_QQ = COL_IN
    h.H_CALIB, h.H_CCDF, h.H_QQ = 4.3, 2.3, 2.2
    OUT.mkdir(parents=True, exist_ok=True)
    qq = pd.read_csv(h.QQ_RUN / "qq_points.csv")
    qq = qq[qq["variable"] == "Trade size"]
    saved = json.loads((h.QQ_RUN / "manifest_q3_figs.json").read_text())["metrics"]["qq_line"]["Trade size"]
    jobs = {
        "fig4_calibration_gap_col_report.png": lambda p: h.draw_calibration(load_bins(SRC / "q1_bins.csv"), load_bins(SRC / "q1_bins_no_min.csv"), p, legend_ncol=2),
        "fig6_ccdf_top_sampled_col_report.png": lambda p: h.draw_ccdf(pd.read_csv(h.CCDF_CSV), p),
        "qq_trade_size_raw_log_col_report.png": lambda p: lines.update(h.draw_qq(qq, p)),
    }
    lines: dict = {}
    for name, job in jobs.items():
        job(OUT / name)
        shutil.copy(OUT / name, h.PAPER_FIGS / name)
    for tag, (slope, intercept, r) in lines.items():
        assert abs(r - saved[tag]["r"]) < 1e-9 and abs(slope - saved[tag]["slope"]) < 1e-6, f"QQ line differs from run: {tag}"
    print("column width (in):", COL_IN)


if __name__ == "__main__":
    main()
