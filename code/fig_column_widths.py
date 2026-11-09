"""Redraw the three body figures at one column width of the two-column paper (D-045, PL-12a).

Why: papers/paper_mvp1 body goes two columns (3.425 in each). Figures drawn at print size keep text at 7.5 pt.
Reuses the drawing functions of code/fig_report2p_half.py with new widths; reads the same saved outputs, fits nothing.
fig:timeline is TikZ in 04-methods.tex, so it is not redrawn.
Usage: OMP_NUM_THREADS=1 timeout 300 uv run python code/fig_column_widths.py
"""
import shutil

import pandas as pd

import fig_report2p_half as h
from fig_calibration_gap import SRC, load_bins

OUT = h.ROOT / "runs" / "local_column_figs_v13"
COL_IN = 3.425   # (8.5 - 2 x 0.7 - 0.25) / 2
H_COL = {"calib": 4.6, "ccdf": 2.5, "qq": 2.6}


def main() -> None:
    h.set_font()
    h.W_CALIB = h.W_CCDF = h.W_QQ = COL_IN
    h.H_CALIB, h.H_CCDF, h.H_QQ = H_COL["calib"], H_COL["ccdf"], H_COL["qq"]
    OUT.mkdir(parents=True, exist_ok=True)
    qq = pd.read_csv(h.QQ_RUN / "qq_points.csv")
    qq = qq[qq["variable"] == "Trade size"]
    jobs = {
        "fig4_calibration_gap_col.png": lambda p: h.draw_calibration(load_bins(SRC / "q1_bins.csv"), load_bins(SRC / "q1_bins_no_min.csv"), p, legend_ncol=2),
        "fig6_ccdf_top_sampled_col.png": lambda p: h.draw_ccdf(pd.read_csv(h.CCDF_CSV), p),
        "qq_trade_size_raw_log_col.png": lambda p: h.draw_qq(qq, p),
    }
    for name, job in jobs.items():
        job(OUT / name)
        shutil.copy(OUT / name, h.PAPER_FIGS / name)


if __name__ == "__main__":
    main()
