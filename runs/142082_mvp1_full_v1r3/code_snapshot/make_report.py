"""Build an English HTML report from a SAVED run folder (CSV, JSON, PNG only: no parquet, no model, no raw data).

Usage: make_report.py --run <run_dir> --version v1|v2 --out <html> [--compare <v1_run_dir>]
Every number on the page is read from the saved files (rules/answering.md section 3).
Verdicts are read from verdicts.json (code/verdicts.py). This script never recomputes a verdict.
"""
import argparse
import base64
import csv
import hashlib
import html
import json
import math
import re
from pathlib import Path

CODE_VERSION = "v3"   # not imported from common.py: that module needs duckdb, this script reads saved files only

# Theme tokens and page CSS: the <style> block of tips/polymarket_proposal_tips.html, inlined.
CSS = r"""
:root{--radius:0;--background:oklch(1 0 0);--foreground:oklch(0.145 0 0);--card:oklch(1 0 0);--card-foreground:oklch(0.145 0 0);--primary:oklch(0.205 0 0);--primary-foreground:oklch(0.985 0 0);--muted:oklch(0.97 0 0);--muted-foreground:oklch(0.556 0 0);--border:oklch(0.55 0 0);--rule:oklch(0.9 0 0);--ring:oklch(0.45 0 0);--signal-instruction:#d40000;--signal-plan:#0432ff;--signal-flag-fill:#fff3a0;--signal-flag-line:#e6d24a;--signal-dead-fill:#e4e4e2;--signal-dead-ink:oklch(0.53 0.01 260);--font:"IBM Plex Mono","IBM Plex Sans KR",ui-monospace,"SF Mono",Menlo,monospace;
--over:oklch(0.62 0.17 45);--under:oklch(0.5 0.1 210);--busy:oklch(0.62 0.17 45);--quiet:oklch(0.82 0 0)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){color-scheme:dark;--background:oklch(0.145 0 0);--foreground:oklch(0.985 0 0);--card:oklch(0.185 0 0);--card-foreground:oklch(0.985 0 0);--primary:oklch(0.922 0 0);--primary-foreground:oklch(0.205 0 0);--muted:oklch(0.269 0 0);--muted-foreground:oklch(0.708 0 0);--border:oklch(0.5 0 0);--rule:oklch(0.3 0 0);--ring:oklch(0.6 0 0);--signal-instruction:#ff5a52;--signal-plan:#6f8cff;--signal-flag-fill:#4a4312;--signal-flag-line:#c9b53a;--signal-dead-fill:#2b2b2a;--signal-dead-ink:oklch(0.68 0.01 260);--over:oklch(0.72 0.15 50);--under:oklch(0.72 0.1 210);--busy:oklch(0.72 0.15 50);--quiet:oklch(0.42 0 0)}}
:root[data-theme="dark"]{color-scheme:dark;--background:oklch(0.145 0 0);--foreground:oklch(0.985 0 0);--card:oklch(0.185 0 0);--card-foreground:oklch(0.985 0 0);--primary:oklch(0.922 0 0);--primary-foreground:oklch(0.205 0 0);--muted:oklch(0.269 0 0);--muted-foreground:oklch(0.708 0 0);--border:oklch(0.5 0 0);--rule:oklch(0.3 0 0);--ring:oklch(0.6 0 0);--signal-instruction:#ff5a52;--signal-plan:#6f8cff;--signal-flag-fill:#4a4312;--signal-flag-line:#c9b53a;--signal-dead-fill:#2b2b2a;--signal-dead-ink:oklch(0.68 0.01 260);--over:oklch(0.72 0.15 50);--under:oklch(0.72 0.1 210);--busy:oklch(0.72 0.15 50);--quiet:oklch(0.42 0 0)}
*{box-sizing:border-box;border-radius:var(--radius)}
body{background:var(--background);color:var(--foreground);font:15px/1.5 var(--font);padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:24px 40px;margin:0;overflow-wrap:anywhere}
main{max-width:860px;margin:0 auto;display:flex;flex-direction:column;gap:18px}
h1,h2,h3{font-family:var(--font);text-wrap:balance;margin:0;line-height:1.2}
h1{font-size:clamp(26px,4.5vw,34px);font-weight:650;letter-spacing:-.01em}
h2{font-size:21px;font-weight:650;margin-bottom:10px}
h3{font-size:14px;font-weight:600;margin:12px 0 4px}
p{margin:0 0 6px}
.eyebrow{font:500 11px/1 var(--font);letter-spacing:.12em;text-transform:uppercase;color:var(--signal-plan);margin-bottom:8px}
.lede{font-size:15.5px;color:var(--muted-foreground);margin-top:8px}
.steps-nav{display:flex;flex-wrap:wrap;gap:6px;margin:14px 0 0;padding:0;list-style:none;counter-reset:st}
.steps-nav li{counter-increment:st}
.steps-nav a{display:block;padding:4px 10px;border:1px solid var(--rule);color:var(--foreground);text-decoration:none;font-size:12.5px}
.steps-nav a::before{content:counter(st) " ";color:var(--signal-plan);font-weight:600}
main>section{border:1px solid var(--border);border-top:4px solid var(--signal-plan);background:var(--card);padding:16px 18px 18px;margin-top:14px;scroll-margin-top:12px;display:flex;flex-direction:column;gap:8px}
main>section>.eyebrow{font-size:12px;margin-bottom:0}
.flow{display:flex;flex-wrap:wrap;gap:6px}
.stage{flex:1 1 160px;background:var(--card);border:1px solid var(--rule);padding:6px 8px;min-width:0}
.stage.big{border-color:var(--signal-plan)}
.stage .n{font:600 12.5px var(--font)}
.stage .s{font:12px/1.4 var(--font);color:var(--muted-foreground)}
.chart{overflow-x:auto}
.chart svg{display:block;width:100%;height:auto;min-width:520px}
svg text{font-family:var(--font)}
.tablewrap{overflow-x:auto;border:1px solid var(--rule);background:var(--card);overflow-wrap:normal}
table{border-collapse:collapse;width:100%;font-size:13px;font-variant-numeric:tabular-nums}
th,td{text-align:left;padding:5px 8px;border-bottom:1px solid var(--rule);vertical-align:top}
th{font:600 11px/1.3 var(--font);letter-spacing:.06em;text-transform:uppercase;color:var(--muted-foreground);background:var(--background)}
tr:last-child td{border-bottom:0}
td.num{white-space:nowrap;color:var(--signal-plan)}
td ul{margin:0;padding-left:16px}
ul,ol{margin:0;padding-left:18px}
li{margin:2px 0}
.note{font-size:12.5px;color:var(--muted-foreground)}
.callout{border-left:3px solid var(--signal-flag-line);background:var(--signal-flag-fill);padding:6px 12px;font-size:13px}
.callout p:last-child{margin:0}
.add{border:1px solid var(--signal-plan);padding:6px 12px;font-size:13.5px}
.add b{color:var(--signal-plan)}
footer{font-size:12.5px;color:var(--muted-foreground);border-top:1px solid var(--rule);padding-top:8px}
a{color:var(--signal-plan)}
:focus-visible{outline:2px solid var(--ring);outline-offset:2px}
@media (max-width:720px){main>section{padding:12px}}
figure{margin:6px 0;display:flex;flex-direction:column;gap:4px}
figure img{max-width:100%;height:auto;border:1px solid var(--rule);background:#fff}
figcaption{font-size:12.5px;color:var(--muted-foreground)}
.scroll{max-height:360px;overflow-y:auto}
.how{font-size:13.5px}
.verdict td:first-child{white-space:nowrap;font-weight:600}
"""

PAPER = "Qin and Yang 2026, Polymarket-v1, arXiv:2606.04217"
# Dataset paper Table 3, mean return (payout minus price) per token, counted per trade. Quoted from the plan, not computed here.
PAPER_LONGSHOT = {"0.0-0.1": -0.0023, "0.1-0.2": -0.0019}
# Plan figure ids of the saved PNGs (tips/polymarket_plan_detailed.md). The report numbers its figures in page order.
PLAN_FIG = {"drop_reasons.png": "no plan figure", "fig1_fig2_hist.png": "plan Fig. 1 and 2", "ecdf.png": "plan Q3 ECDF, no number",
            "fig3_qq.png": "plan Fig. 3", "fig_violin_p1d_by_category.png": "plan Q3 violin, no number",
            "fig4_calibration.png": "plan Fig. 4", "fig5_ecdf_yes_no.png": "plan Fig. 5", "fig6_ccdf.png": "plan Fig. 6",
            "fig7_lorenz.png": "plan Fig. 7", "fig8_elbow.png": "plan Fig. 8", "fig9_calibration_by_category.png": "plan Fig. 9",
            "fig10_ecdf_7d_vs_1d.png": "plan Fig. 10", "fig11_volume_vs_error.png": "plan Fig. 11"}
DROP_LABEL = {"updown": "Up/Down market", "non_binary": "Not binary", "no_outcome": "No outcome",
              "no_price": "No price at T - 1 day", "stale_price": "Price older than the limit",
              "below_min_trades": "Fewer trades than the minimum", "kept": "Kept"}


# ---------- formatting ----------
def fmt(x, dec: int | None = None) -> str:
    """Thousands separators for counts, 4 significant digits for the rest."""
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "n/a"
    if isinstance(x, bool):
        return "yes" if x else "no"
    if isinstance(x, int):
        return f"{x:,}"
    if isinstance(x, float):
        if dec is not None:
            return f"{x:,.{dec}f}"
        return f"{x:,.0f}" if abs(x) >= 1000 else f"{x:.4g}"
    return str(x)


def fp(p) -> str:
    """p-value as plain text: p < 1e-4 is shown as '< 0.0001'. Page.table escapes it."""
    if p is None:
        return "n/a"
    return "< 0.0001" if p < 1e-4 else f"{p:.4f}"


def ci(lo, hi, dec: int = 4) -> str:
    return f"[{lo:.{dec}g}, {hi:.{dec}g}]"


def g(d, *keys):
    """Nested get that returns None when a key is missing."""
    for k in keys:
        if not isinstance(d, dict) or k not in d:
            return None
        d = d[k]
    return d


# ---------- loading ----------
def jload(run: Path, name: str):
    f = run / name
    return json.loads(f.read_text()) if f.exists() else None


def cload(run: Path, name: str) -> list[dict] | None:
    f = run / name
    if not f.exists():
        return None
    with f.open(newline="") as fh:
        rows = list(csv.reader(fh))
    head = [h or "name" for h in rows[0]]
    return [dict(zip(head, r)) for r in rows[1:]]


def num(s: str):
    try:
        v = float(s)
    except ValueError:
        return s
    return int(v) if v.is_integer() and "." not in s and "e" not in s.lower() else v


# ---------- html pieces ----------
class Raw(str):
    """A cell that is already HTML. Every other text cell is escaped (review F13)."""


def cell(c) -> str:
    if isinstance(c, Raw):
        return str(c)
    return html.escape(c) if isinstance(c, str) else html.escape(fmt(c))


class Page:
    def __init__(self, run: Path):
        self.run, self.fig_n, self.tab_n = run, 0, 0

    def table(self, caption: str, head: list[str], rows: list[list], scroll: bool = False) -> str:
        self.tab_n += 1
        th = "".join(f"<th>{html.escape(h)}</th>" for h in head)
        body = "".join("<tr>" + "".join(f"<td>{cell(c)}</td>" for c in r) + "</tr>" for r in rows)
        cls = "tablewrap scroll" if scroll else "tablewrap"
        return (f'<div class="{cls}"><table><tr>{th}</tr>{body}</table></div>'
                f'<p class="note">Table {self.tab_n}. {html.escape(caption)}</p>')

    def figure(self, png: str, what: str, why: str) -> str:
        f = self.run / png
        if not f.exists():
            return skipped(png)
        self.fig_n += 1
        b64 = base64.b64encode(f.read_bytes()).decode()
        return (f'<figure><img alt="{html.escape(what)}" src="data:image/png;base64,{b64}">'
                f'<figcaption>Figure {self.fig_n} ({html.escape(PLAN_FIG.get(png, "no plan figure"))}). {html.escape(what)} Why: {html.escape(why)} '
                f'Source: {html.escape(str(self.run))}/{html.escape(png)}</figcaption></figure>')


def bullets(items: list[str]) -> str:
    return '<h3>How to read</h3><ul class="how">' + "".join(f"<li>{html.escape(i)}</li>" for i in items) + "</ul>"


def ask(text: str) -> str:
    return f'<p><b>Asks:</b> {text}</p>'


def skipped(what: str) -> str:
    return f'<div class="callout"><p>Skipped: {html.escape(what)} not found in the run folder.</p></div>'


# ---------- verdicts: read from verdicts.json, never recomputed here ----------
def numbers(e: dict) -> str:
    """The numbers of one verdicts.json entry, in one line."""
    st, ef = e["statistic"], e["effect_size"]
    out = f"{st['name']} {fmt(st['value'])}" + (f" (df {st['df']})" if st.get("df") else "")
    out += f", p {fp(e['p'])}, {ef['name']} {fmt(ef['value'])}"
    if ef.get("mean_diff") is not None:
        out += f", mean difference {fmt(ef['mean_diff'])}"
    if ef.get("ci"):
        out += f", 95% CI {ci(*ef['ci'])}"
    out += f", n {fmt(e['n'])}."
    extra = ", ".join(f"{k.replace('_', ' ')} {fmt(v)}" for k, v in (e.get("extra") or {}).items())
    return out + (f" {extra}." if extra else "")


def verdict_row(V: dict | None, key: str) -> str:
    if V is None:
        return "Skipped: verdicts.json not found in the run folder."
    e = V["comparisons"].get(key)
    if e is None:
        return f"Skipped: no {key} entry in verdicts.json (its results file was missing when the verdicts were written)."
    return f"{e['verdict']} {numbers(e)}"


def summary_rows(D: dict, v2: bool) -> list[tuple[str, str]]:
    rows = []
    q3 = D["q3"]
    if q3:
        s, f = q3["summary"], q3["fits"]
        best = min(f["trade_size_usdc"], key=lambda k: f["trade_size_usdc"][k]["D"])
        rows.append(("Q3: how are price, trade size and wallet volume distributed?",
                     f"Descriptive, no pre-registered criterion. Median trade size {fmt(s['trade_size_usdc']['median'])} USDC, "
                     f"mean {fmt(s['trade_size_usdc']['mean'])} USDC. Closest of the three fits for trade size: {best.replace('_', ' ')} "
                     f"(KS D {fmt(f['trade_size_usdc'][best]['D'])}). Mean price p_1d {fmt(s['p_1d']['mean'])}."))
    V = D["verdicts"]
    rows.append(("Q1: do prices match how often events happen?", verdict_row(V, "Q1")))
    q2 = g(D["q2"], "concentration")
    if q2:
        m, t = q2["maker"], q2["taker"]
        rows.append(("Q2: is wallet volume concentrated?",
                     f"Descriptive, no pre-registered criterion. Gini maker {fmt(m['gini'])}, taker {fmt(t['gini'])}. "
                     f"The top 1% of maker wallets hold {m['top1_share']:.1%} of maker volume. "
                     f"A wallet is an address, not a person."))
    if v2:
        rows += [("Q1a: does accuracy depend on the topic?", verdict_row(V, "Q1a")),
                 ("Q1b: is the price better near the deadline?", verdict_row(V, "Q1b")),
                 ("Q1c: are busier markets more accurate?", verdict_row(V, "Q1c"))]
    return rows


# ---------- sections ----------
def sec_summary(P: Page, D: dict, full: bool, v2: bool) -> str:
    scope = g(D["prereg"], "scope")
    note = ("Pre-registered verdict: this is the full-data run, judged by the criteria in "
            "<code>analysis/prereg_mvp1.md</code>" + (" and <code>analysis/prereg_mvp2.md</code>." if v2 else ".")
            if full else
            f"Scope is <b>{html.escape(str(scope))}</b>. This is a first cycle, so there is no verdict. Numbers only.")
    rows = [[Raw(f"<b>{html.escape(q)}</b>"), a] for q, a in summary_rows(D, v2)]
    return (f'<div class="callout"><p>{note}</p></div>'
            + ask("the question each analysis answers, in one line each.")
            + P.table("Questions and answers. Verdicts come from verdicts.json, numbers from the saved results.", ["Question", "Answer"], rows)
            + bullets(["Each answer repeats numbers from the sections below. Check the p-value together with the effect size.",
                       "With tens of thousands of markets, a small effect can give a tiny p. Read the effect size first.",
                       "Tests assume independent markets. Markets on one event are not independent."]))


def sec_data(P: Page, D: dict) -> str:
    t, pr = D["tables"], D["prereg"]
    drops = t["drop_reasons"]
    scope_n = t["n_markets_in_scope"]
    order = [r for r in t["reason_order"] if r in drops] + ["kept"]
    rows = [[DROP_LABEL.get(r, r), drops[r], f"{drops[r] / scope_n:.1%}"] for r in order]
    sizes = [["Markets in scope", t["n_markets_in_scope"]], ["Markets kept (min trades filter)", t["n_kept"]],
             ["Markets kept without the min trades filter", t["n_kept_no_min_filter"]],
             ["Trades in kept markets", t["n_trades_in_kept_markets"]],
             ["Wallet x role rows", t["n_wallet_role_rows"]],
             [f"Trade-size sample rows ({'hash-order rule' if t.get('trade_size_sample_rule') else 'seed ' + fmt(t.get('trade_size_sample_seed'))})",
              t["trade_size_sample_rows"]]]
    prow = [[k, str(v)] for k, v in pr.items()]
    return (ask("which markets enter the analysis, and why the others are dropped.")
            + P.table("Size of each set, counted from tables_summary.json.", ["Set", "Count"], sizes)
            + P.table("Markets by the first rule that drops them (rules run in this order).",
                      ["First failing rule", "Markets", "Share of scope"], rows)
            + P.figure("drop_reasons.png", "Markets by first failing rule.",
                       "it shows which rule removes the most markets.")
            + P.table("Pre-registered parameters (prereg.json of this run).", ["Parameter", "Value"], prow)
            + '<div class="callout"><ul>'
              "<li>Duplicate rows are kept. No row id tells a repeat fill from a copy.</li>"
              "<li><code>no_outcome</code> includes markets whose outcome_seq=1 label never traded.</li>"
              "<li>Volume and trade counts include trades after T - 1 day (used in Q1c).</li></ul></div>"
            + bullets(["Only the kept markets enter Q1 and the price part of Q3.",
                       "A market is counted once, at the first rule it fails."]))


def dist_rows(s: dict) -> list[list]:
    names = {"p_1d": "Price p_1d", "trade_size_usdc": "Trade size (USDC)", "wallet_volume_usdc": "Wallet volume (USDC)"}
    return [[names.get(k, k), v["n"], v["mean"], v["median"], v["q25"], v["q75"], v["q95"], v["q99"], v["max"]]
            for k, v in s.items()]


def sec_q3(P: Page, D: dict) -> str:
    q = D["q3"]
    if not q:
        return skipped("q3_results.json")
    fits = []
    for var, models in q["fits"].items():
        for m, v in models.items():
            par = {"normal": f"mu {fmt(v.get('mu'))}, sigma {fmt(v.get('sigma'))}",
                   "exponential": f"scale {fmt(v.get('scale'))}",
                   "power_law": f"alpha {fmt(v.get('alpha'))}, xmin {fmt(v.get('xmin'))}, n_tail {fmt(v.get('n_tail'))}"}[m]
            fits.append([var, m.replace("_", " "), par, v["D"], fp(v["p"])])
    return (ask("what the price, trade-size and wallet-volume distributions look like.")
            + P.table("Summary statistics from q3_results.json.",
                      ["Variable", "n", "Mean", "Median", "Q25", "Q75", "Q95", "Q99", "Max"], dist_rows(q["summary"]))
            + P.table("Fitted models with KS distance D (the effect size) next to p. "
                      "Power law is fitted to the top 10% (xmin quantile 0.9).",
                      ["Variable", "Model", "Parameters", "KS D", "KS p"], fits)
            + P.figure("fig1_fig2_hist.png", "Histograms of price and trade size.",
                       "the shape shows whether a normal model could fit.")
            + P.figure("ecdf.png", "ECDFs of price and trade size.", "the curve shows where most values sit.")
            + P.figure("fig3_qq.png", "QQ plots before and after a log transform.",
                       "a straight line after log means the log values are close to normal.")
            + P.figure("fig_violin_p1d_by_category.png", "Violin of p_1d by category_refined over the kept markets (bar = median).",
                       "a wide body at both ends means the price is near 0 or 1 in that topic.")
            + bullets(["A smaller KS D means a closer fit. D is the size of the gap, p only says if the gap is zero.",
                       "KS p-values are optimistic for fitted parameters. The fit used the same data as the test.",
                       "Mean far above median means a long right tail: a few large trades and wallets.",
                       "Wallet volume pools maker and taker rows, so one address can appear twice."]))


def bins_table(P: Page, rows: list[dict] | None, caption: str, nb: int | None) -> str:
    if rows is None:
        return skipped("a bin table")
    out = []
    for r in rows:
        b = r["bin"]
        label = f"{int(b) / nb:.1f} to {(int(b) + 1) / nb:.1f}" if nb and b.isdigit() else b
        diff = float(r["diff_obs_minus_price"])
        row = [label, int(float(r["n"])), float(r["mean_price"]), float(r["observed_rate"]), f"{diff:+.4f}",
               ci(float(r["ci_low"]), float(r["ci_high"]))]
        if "p_bh" in r:
            row += [fp(float(r["p_bh"])), "off" if r["reject_bh"] == "True" else "ok"]
        out.append(row)
    head = ["Bin", "n", "Mean price", "Observed Yes rate", "Observed minus price", "95% Wilson CI"]
    if rows and "p_bh" in rows[0]:
        head += ["BH p", "Call"]
    return P.table(caption, head, out)


def confusion_block(P: Page, m: dict) -> str:
    cf = m["confusion_at_0.5"]
    tab = P.table("Confusion matrix of the main set. Predicted Yes means p_1d > 0.5.",
                  ["", "Actual Yes", "Actual No", "Total"],
                  [["Predicted Yes", cf["tp"], cf["fp"], cf["tp"] + cf["fp"]],
                   ["Predicted No", cf["fn"], cf["tn"], cf["fn"] + cf["tn"]]])
    return (tab + f"<p>Precision {fmt(cf['precision'])}, recall {fmt(cf['recall'])}, accuracy {fmt(cf['accuracy'])}, "
                  f"class balance (Yes share) {fmt(m['class_balance_yes'])}.</p>")


def paper_longshot_block(P: Page, long_main: dict) -> str:
    rows = [[b, f"{PAPER_LONGSHOT[b]:+.4f}", f"{v['obs_minus_expected']:+.4f}" if v else "n/a", ci(v["ci_low_diff"], v["ci_high_diff"]) if v else "n/a",
             v["n"] if v else None] for b in PAPER_LONGSHOT for v in [long_main.get(b)]]
    return (P.table("Longshot bins against the dataset paper, Table 3 (main set).",
                    ["Bin", "Paper: mean return per token (per trade)", "Ours: observed minus mean price (per market)",
                     "95% CI of ours", "Our n"], rows)
            + '<p class="note">The units differ. The paper counts every trade and takes payout minus price per token. '
              "We count every market once and take the observed Yes rate minus the mean price. Compare the sign and the size, not the digits.</p>")


def sec_q1(P: Page, D: dict) -> str:
    q = D["q1"]
    if not q:
        return skipped("q1_results.json")
    nb = g(D["prereg"], "n_bins") or 10
    rows = []
    for key, label in [("main_with_min_filter", "Main (min trades filter)"), ("no_min_filter", "Without min trades filter")]:
        r = q[key]
        c, k = r["chi2_gof"], r["ks_yes_vs_no"]
        rows.append([label, r["n_markets"], r["class_balance_yes"], r["brier"], r["log_loss"], r["mean_entropy_bits"],
                     f"{fmt(c['chi2'])} (df {c['df']})", fp(c["p"]), c["effect_w"],
                     f"{r['bins_reject_bh']} / {r['bins_reject_bonferroni']}", r["confusion_at_0.5"]["accuracy"],
                     k["D"], fp(k["p"])])
    long = []
    for key, label in [("main_with_min_filter", "Main"), ("no_min_filter", "No min filter")]:
        for bin_, v in q[key]["longshot"].items():
            long.append([label, bin_, v["n"], v["mean_price"], v["observed_rate"], f"{v['obs_minus_expected']:+.4f}",
                         ci(v["ci_low_diff"], v["ci_high_diff"])])
    main = q["main_with_min_filter"]
    return (ask("when the price is p, does the event happen about p of the time? (price at T - 1 day, 10 equal-width bins)")
            + "<p><b>Model:</b> each market's outcome is Bernoulli(p), where p is its price. If prices are calibrated, "
              "the Yes count in a bin is binomial(n, mean p).</p>"
            + P.table("Calibration metrics. Chi-square p sits next to effect size w. Bins off: BH / Bonferroni.",
                      ["Set", "Markets", "Yes share", "Brier", "Log loss", "Mean H(p) bits", "Chi-square", "p", "Effect w",
                       "Bins off (BH / Bonf.)", "Accuracy at 0.5", "KS D Yes vs No", "KS p"], rows)
            + bins_table(P, D["q1_bins"], "Per bin, main set. BH p is the corrected binomial p. Observed minus price is the effect.", nb)
            + P.figure("fig4_calibration.png", "Observed Yes rate against mean price per bin, with 95% Wilson CI.",
                       "points on the diagonal mean the price matches the outcome rate.")
            + P.figure("fig5_ecdf_yes_no.png", "ECDFs of p_1d for Yes-resolved and No-resolved markets.",
                       "the further apart the curves, the better the price separates the outcomes.")
            + confusion_block(P, main)
            + P.table("Longshot bins (price below 0.2): observed rate against mean price.",
                      ["Set", "Bin", "n", "Mean price", "Observed rate", "Observed minus price", "95% CI of the difference"], long)
            + paper_longshot_block(P, main["longshot"])
            + bins_table(P, D["q1_bins_no_min"], "Robustness: the same bins without the min trades filter.", nb)
            + bins_table(P, D["q1_bins_eqfreq"], "Robustness: equal-frequency bins, main set.", None)
            + bullets(["Pre-registered line: chi-square p < 0.05 means prices are not calibrated as a whole.",
                       "A bin is off when its BH-corrected p < 0.05. A negative difference means the event happened less often than priced.",
                       "Effect w is Cohen's w. About 0.1 is small. A tiny p with a small w is a real but small gap.",
                       "Brier is the mean squared error of the price. 0.25 is a coin flip at 0.5, 0 is perfect."]))


def sec_q2(P: Page, D: dict) -> str:
    q = D["q2"]
    if not q:
        return skipped("q2_results.json")
    ref = q.get("paper_gini_full_data_reference", {})
    conc = [[role.title(), v["n_wallets"], v["mean"], v["median"], v["mean_over_median"], f"{v['top1_share']:.1%}",
             f"{v['top5_share']:.1%}", f"{v['top10_share']:.1%}", f"{v['top20_share']:.1%}", v["gini"], ref.get(role)]
            for role, v in q["concentration"].items()]
    w, ks, sp, km = q["role_tests"]["welch_t"], q["role_tests"]["ks"], q["spearman_n_trades_vs_volume"], q["kmeans"]
    tests = [["Welch t, log10 volume maker vs taker", f"t {fmt(w['t'])}", fp(w["p"]), f"Cohen's d {fmt(w['cohens_d'])}"],
             ["KS, volume maker vs taker", f"D {fmt(ks['D'])}", fp(ks["p"]), f"D {fmt(ks['D'])}"],
             ["Spearman, n_trades vs volume (n " + fmt(sp["n"]) + ")", f"rho {fmt(sp['rho'])}", fp(sp["p"]), f"rho {fmt(sp['rho'])}"]]
    cl = [[c["cluster"], c["n"], c["median_volume"], c["median_n_trades"], c["median_n_markets"], c["mean_trade_price"]]
          for c in km["cluster_summary"]]
    ch, an_new, an_old = km["chi2_cluster_x_category"], km.get("anova_mean_trade_price"), km["anova_log_median_trade_size"]
    mx = ch.get("min_expected_count")
    ctest = [[f"Chi-square, cluster x category ({ch['n_categories']} categories" + (f", min expected count {fmt(mx)})" if mx is not None else ")"),
              f"{fmt(ch['chi2'])} (df {ch['df']})", fp(ch["p"]), f"Cramer's V {fmt(ch['cramers_v'])}"]]
    for label, an in ([("ANOVA of mean trade price", an_new), ("Secondary: ANOVA of log median trade size", an_old)] if an_new
                      else [("ANOVA of log median trade size", an_old)]):
        ctest.append([f"{label} ({fmt(an['n_perm'])} permutations)", f"F {fmt(an['F'])}", fp(an["perm_p"]),
                      f"eta squared {fmt(an['eta_squared'])}"])
    rb, scal = km.get("robust_scaling_check"), D["q2_scaling"]
    robust = (P.table("k-means feature scaling: z-score (mean, sd) and robust (median, IQR). A zero IQR falls back to the sd.",
                      ["Feature", "Mean", "SD", "Median", "IQR", "Scale used (robust)", "IQR was zero"],
                      [[r["feature"], float(r["mean"]), float(r["sd"]), float(r["median"]), float(r["iqr"]),
                        float(r["robust_scale_used"]), r["iqr_was_zero"]] for r in scal])
              + f"<p>Stability check: k-means on the robust-scaled features (same K {rb['k']}, seed {rb['seed']}) against the z-score clusters, "
                f"adjusted Rand index {fmt(rb['adjusted_rand_index_vs_zscore'])}. 1 means the same clusters.</p>"
              if scal and rb else skipped("q2_kmeans_scaling.csv"))
    return (ask("do a few wallets hold most of the volume, and do makers differ from takers?")
            + P.table("Volume concentration per role. The last column is the paper's Gini on the full data, for reference.",
                      ["Role", "Wallets", "Mean (USDC)", "Median (USDC)", "Mean / median", "Top 1%", "Top 5%", "Top 10%",
                       "Top 20%", "Gini", "Paper Gini"], conc)
            + P.table("Role and activity tests, each with p and an effect size.", ["Test", "Statistic", "p", "Effect size"], tests)
            + P.figure("fig6_ccdf.png", "Wallet volume CCDF on log-log axes.",
                       "a long straight tail means a few wallets trade very large volumes.")
            + P.figure("fig7_lorenz.png", "Lorenz curves of wallet volume against the equality line.",
                       "a curve far below the line means few wallets hold most of the volume.")
            + P.table(f"Side analysis: k-means clusters (K = {km['k_chosen']}, {fmt(km['n_sample'])} sampled wallets, "
                      f"seed {km['sample_seed']}). K rule: {km['k_rule']}.",
                      ["Cluster", "Wallets", "Median volume", "Median trades", "Median markets", "Mean trade price"], cl)
            + P.figure("fig8_elbow.png", "K-means inertia against K, with the chosen K dashed.",
                       "the bend in the curve is the rule used to pick K.")
            + P.table("Cluster tests with effect sizes.", ["Test", "Statistic", "p", "Effect size"], ctest)
            + robust
            + bullets(["Gini 0 means equal volume. Gini 1 means one wallet holds everything.",
                       "Top 1% share is the share of total volume held by the top 1% of wallets.",
                       "A wallet is an address. One person may use many addresses.",
                       "K-means is a side analysis. The clusters describe the sample and are not groups of people."]))


def sec_q1a(P: Page, D: dict) -> str:
    q = D["q1a"]
    if not q:
        return skipped("q1a_results.json")
    c, bt, br = q["chi_square_independence"], q["bin_tests"], q.get("brier_tests", {})
    tab = D["q1a_tab"] or []
    rows = [[r["category_group"], int(float(r["won"])), int(float(r["lost"])), int(float(r["n"])),
             float(r["favorite_win_rate"]), float(r["mean_brier"])] for r in tab]
    stat = ([["Chi-square of independence", f"{fmt(c['chi2'])} (df {c['df']})", fp(c["p"]), f"Cramer's V {fmt(c['cramers_v'])}"]]
            if c.get("p") is not None else [["Chi-square of independence", "not defined", "n/a", c.get("note", "")]])
    if "anova_F" in br:
        stat += [["ANOVA of Brier across categories", f"F {fmt(br['anova_F'])}", fp(br["anova_p"]), f"eta squared {fmt(br['eta_squared'])}"],
                 [f"Permutation test ({fmt(br['n_perm'])} permutations)", f"eta squared {fmt(br['eta_squared'])}", fp(br["perm_p"]), f"eta squared {fmt(br['eta_squared'])}"]]
    sports = q.get("sports_n")
    sports_txt = (", ".join(f"{html.escape(k)}: {fmt(v)}" for k, v in sports.items()) if isinstance(sports, dict)
                  else html.escape(str(sports)))
    return (ask("does the favorite win equally often in every topic? (favorite = the side with p_1d at least 0.5)")
            + P.table("Tests across categories, each with p and an effect size. The chi-square line is the primary test.",
                      ["Test", "Statistic", "p", "Effect size"], stat)
            + P.table("Per category: favorite won, favorite lost, n and mean Brier.",
                      ["Category", "Favorite won", "Favorite lost", "n", "Favorite win rate", "Mean Brier"], rows, scroll=True)
            + f"<p>Sports n: {sports_txt}. Categories under {q['min_category_n']} markets merged into one small-category group: "
              f"{len(q.get('merged_into_other', {}))}. Category x bin tests: {bt['n_tested']} tested of {bt['bins_total']}, "
              f"{bt['reject_bonferroni']} off after Bonferroni, {bt['reject_bh']} off after BH.</p>"
            + P.figure("fig9_calibration_by_category.png", "Observed Yes rate against mean price per bin, one line per category.",
                       "lines far from the diagonal mark topics where the price is off.")
            + bullets(["Pre-registered line: chi-square p < 0.05 means accuracy depends on the topic.",
                       "Cramer's V is the effect size. About 0.1 is small.",
                       "Small categories give noisy rates. Read the n column first.",
                       "Missing categories are called Unknown."]))


def sec_q1b(P: Page, D: dict) -> str:
    q = D["q1b"]
    if not q:
        return skipped("q1b_results.json")
    rows = []
    for key, label in [("brier_diff_7d_minus_1d", "Brier difference (7 d minus 1 d), primary"),
                       ("abs_error_diff_7d_minus_1d", "Absolute error difference (7 d minus 1 d)")]:
        t = q[key]
        rows.append([label, t["n"], t["mean_diff"], ci(t["ci_low"], t["ci_high"]), f"{fmt(t['t'])} (df {t['df']})", fp(t["p"]), t["cohens_d"]])
    ks, ent, br, sel = q["ks_yes_vs_no"], q["mean_entropy_bits"], q["brier"], q["selection"]
    sec = [["Brier", br["7d"], br["1d"], ""],
           ["Mean H(p) bits", ent["7d"], ent["1d"], f"change {fmt(ent['diff_7d_minus_1d'])}"],
           ["KS D Yes vs No", ks["7d"]["D"], ks["1d"]["D"], f"p {fp(ks['7d']['p'])} / {fp(ks['1d']['p'])}"]]
    return (ask("is the price closer to the outcome 1 day before T than 7 days before T? (same markets, paired)")
            + f"<p>Markets used: {fmt(sel['n_used'])} of {fmt(sel['n_kept'])} kept ({fmt(sel['n_kept_open_ge_7d'])} opened at least 7 days before T). "
              f"Both prices at most {fmt(sel['max_staleness_h'])} h old.</p>"
            + P.table("Paired one-sample t-tests. Positive mean means the error at 7 d is larger, so better near the deadline.",
                      ["Test", "n", "Mean difference", "95% CI", "t", "p", "Cohen's d"], rows)
            + P.table("Secondary results. They do not change the verdict.", ["Quantity", "7 d", "1 d", "Note"], sec)
            + P.figure("fig10_ecdf_7d_vs_1d.png", "ECDFs of the price for Yes-resolved and No-resolved markets at 7 d and at 1 d.",
                       "the further apart the two curves, the better the price separates the outcomes.")
            + bullets(["Pre-registered line: p < 0.05 and mean difference above 0 means better near the deadline.",
                       "Cohen's d is the effect size. About 0.2 is small.",
                       "The entropy drop is expected by construction. Prices move toward 0 or 1 near the deadline.",
                       "The error change is the real test."]))


def raw_edges(label: str) -> str:
    """A log1p decile interval '(a, b]' shown as raw x edges, so the column shares the scale of the median x (review F14)."""
    m = re.fullmatch(r"[(\[]\s*(-?[\d.eE+-]+),\s*(-?[\d.eE+-]+)\s*[)\]]", label)
    if not m:
        return label
    lo, hi = (math.expm1(float(v)) for v in m.groups())
    return f"({fmt(lo)}, {fmt(hi)}]"


def sec_q1c(P: Page, D: dict) -> str:
    q = D["q1c"]
    if not q:
        return skipped("q1c_results.json")
    rows = [[lab, q[k]["n"], q[k]["rho"], ci(q[k]["ci_low"], q[k]["ci_high"]), fp(q[k]["p"])]
            for k, lab in [("spearman_log_volume_vs_error", "log1p(volume_usdc), primary"),
                           ("spearman_log_trades_vs_error", "log1p(n_trades), secondary")]]
    bn = D["q1c_binned"] or []
    brow = [[r["predictor"], raw_edges(r["bin"]), float(r["x_median"]), float(r["mean_error"]), int(float(r["n"]))]
            for r in bn]
    rho = q["spearman_log_volume_vs_error"]["rho"]
    direction = ("positive: busier markets have larger errors, the opposite of the pre-registered direction" if rho > 0
                 else "negative or zero: busier markets have equal or smaller errors")
    return (ask("do markets with more volume or more trades have a price closer to the outcome?")
            + P.table("Spearman rho (the effect size) of log volume and log trades against per-market Brier error.",
                      ["x", "n", "rho", "95% CI", "p"], rows)
            + f"<p>Primary rho is {fmt(rho)}: {direction}.</p>"
            + P.table("Mean Brier error per decile of x. Decile edges are raw x (converted back from log1p).",
                      ["Predictor", "Decile (raw x edges)", "Median x", "Mean error", "n"], brow, scroll=True)
            + P.figure("fig11_volume_vs_error.png", "Per-market Brier error against volume and trade count, with mean error per decile.",
                       "the line shows how mean error changes with activity. A rising line means busier markets have larger errors.")
            + bullets(["Pre-registered line: p < 0.05 and rho below 0 means busier is more accurate.",
                       "rho near 0 means no monotone link, even when p is small.",
                       "Volume and trade count cover the whole life of the market, also after T - 1 day.",
                       "So they are not known at evaluation time."]))


def same(a, b) -> str:
    """'same' = equal to 6 significant digits (counts must be equal)."""
    if a is None or b is None:
        return "n/a"
    if isinstance(a, int) and isinstance(b, int):
        return "same" if a == b else "differs"
    return "same" if f"{a:.6g}" == f"{b:.6g}" else "differs"


def fmt6(x) -> str:
    if x is None:
        return "n/a"
    return f"{x:,}" if isinstance(x, int) else f"{x:.6g}"


def key_numbers(D: dict) -> dict[str, object]:
    """Every MVP1 headline number of a run, by label, read from its saved files."""
    out: dict[str, object] = {}
    t = D["tables"] or {}
    out["Markets in scope"], out["Markets kept"] = t.get("n_markets_in_scope"), t.get("n_kept")
    for k, v in (t.get("drop_reasons") or {}).items():
        out[f"Drop: {DROP_LABEL.get(k, k)}"] = v
    m = g(D["q1"], "main_with_min_filter") or {}
    for label, val in [("Q1 n markets", m.get("n_markets")), ("Q1 Brier", m.get("brier")), ("Q1 log loss", m.get("log_loss")),
                       ("Q1 chi-square", g(m, "chi2_gof", "chi2")), ("Q1 chi-square p", g(m, "chi2_gof", "p")),
                       ("Q1 effect w", g(m, "chi2_gof", "effect_w")), ("Q1 bins off (BH)", m.get("bins_reject_bh")),
                       ("Q1 bins off (Bonferroni)", m.get("bins_reject_bonferroni"))]:
        out[label] = val
    for r in D["q1_bins"] or []:
        out[f"Q1 bin {r['bin']} mean price"], out[f"Q1 bin {r['bin']} observed rate"] = float(r["mean_price"]), float(r["observed_rate"])
    q3 = D["q3"] or {}
    for var, st in (q3.get("summary") or {}).items():
        out[f"Q3 {var} mean"], out[f"Q3 {var} median"], out[f"Q3 {var} max"] = st["mean"], st["median"], st["max"]
    for var, models in (q3.get("fits") or {}).items():
        for mod, f in models.items():
            out[f"Q3 {var} {mod} KS D"] = f["D"]
        out[f"Q3 {var} power law n_tail"] = g(models, "power_law", "n_tail")
    q2 = D["q2"] or {}
    for role, c in (q2.get("concentration") or {}).items():
        out[f"Q2 {role} wallets"], out[f"Q2 {role} top 1% share"], out[f"Q2 {role} Gini"] = c["n_wallets"], c["top1_share"], c["gini"]
    rt, sp, km = q2.get("role_tests") or {}, q2.get("spearman_n_trades_vs_volume") or {}, q2.get("kmeans") or {}
    out["Q2 Welch t"], out["Q2 role KS D"], out["Q2 Spearman rho"] = g(rt, "welch_t", "t"), g(rt, "ks", "D"), sp.get("rho")
    out["Q2 k-means K"] = km.get("k_chosen")
    for k, v in (km.get("inertia") or {}).items():
        out[f"Q2 inertia K={k}"] = v
    # Cluster labels are arbitrary, so sizes are compared largest first.
    for i, n in enumerate(sorted((c["n"] for c in km.get("cluster_summary") or []), reverse=True), 1):
        out[f"Q2 cluster size, rank {i}"] = n
    out["Q2 cluster x category chi-square"] = g(km, "chi2_cluster_x_category", "chi2")
    out["Q2 cluster x category df"] = g(km, "chi2_cluster_x_category", "df")
    out["Q2 ANOVA F (primary)"] = g(km, "anova_mean_trade_price", "F") if "anova_mean_trade_price" in km else g(km, "anova_log_median_trade_size", "F")
    return out


def sec_compare(P: Page, D: dict, D1: dict) -> str:
    a, b = key_numbers(D1), key_numbers(D)
    rows = []
    for label in list(a) + [k for k in b if k not in a]:
        x, y = a.get(label), b.get(label)
        diff = fmt6(abs(x - y)) if isinstance(x, (int, float)) and isinstance(y, (int, float)) else "n/a"
        rows.append([label, fmt6(x), fmt6(y), same(x, y), diff])
    n_diff = sum(r[3] == "differs" for r in rows)
    return (ask("do the MVP1 numbers stay the same when the MVP2 run recomputes them?")
            + f'<div class="callout"><p>{n_diff} of {len(rows)} rows differ. "Same" means equal to 6 significant digits. '
              "Runs of code before v3 differ for known reasons: a tie in the last price (F1), the category rule (F2), "
              "a thread-dependent sample (F3) and parquet row order (F4). See <code>analysis/review_mvp1_mvp2.md</code>.</p></div>"
            + P.table("All MVP1 headline numbers: the v1 run next to this run.", ["Quantity", "v1 run", "This run", "Same?", "Absolute difference"], rows, scroll=True)
            + bullets(["The two runs may differ in scope (for example a pilot month against the full data).",
                       "Then every row differs and the table only shows the size of the gap.",
                       "With the same scope, parameters and code version, every row must say same. A row that differs is a bug to find."]))


def limit_bullets(D: dict) -> list[str]:
    """The data-dependent limits, with their numbers read from the saved files."""
    out = []
    t = D["tables"] or {}
    scope_n, drops = t.get("n_markets_in_scope"), t.get("drop_reasons") or {}
    sel = g(D["q1b"], "selection")
    if sel:
        out.append(f"Q1b uses {fmt(sel['n_used'])} of {fmt(sel['n_kept'])} kept markets ({sel['n_used'] / sel['n_kept']:.1%}). "
                   "These are long, active markets, so the Q1b answer is about them.")
    if D["q1c"]:
        out.append(f"Q1c: Brier error is larger for contested markets (price near 0.5) by construction. So rho "
                   f"({fmt(g(D['q1c'], 'spearman_log_volume_vs_error', 'rho'))}) mixes activity with how contested the market is.")
    if drops.get("no_price") is not None and scope_n:
        out.append(f"Q1 covers only markets with a trade at least 1 day before T. {fmt(drops['no_price'])} markets "
                   f"({drops['no_price'] / scope_n:.1%} of scope) have none and are dropped (no_price).")
    if drops.get("no_outcome") is not None:
        out.append(f"no_outcome ({fmt(drops['no_outcome'])} markets) includes markets whose outcome_seq=1 label never traded.")
    return out


def sec_method(P: Page, D: dict, run: Path) -> str:
    mf = []
    for f in sorted(run.glob("manifest_*.json")):
        m = json.loads(f.read_text())
        mf.append([f.stem.replace("manifest_", ""), str(m.get("code_version")), str(m.get("code_sha")),
                   str(g(m, "env", "slurm_job_id")), str(g(m, "env", "hostname")),
                   f"{g(m, 'env', 'slurm_cpus_per_task') or 'n/a'} / {g(m, 'env', 'duckdb_threads') or 'n/a'}"])
    sports = g(D["q1a"], "sports_n")
    s_txt = (f" Sports n in Q1a: {', '.join(f'{html.escape(k)} {fmt(v)}' for k, v in sports.items())}."
             if isinstance(sports, dict) else "")
    limits = "".join(f"<li>{html.escape(b)}</li>" for b in limit_bullets(D))
    V = D["verdicts"]
    vtxt = (f"verdicts.json: code {html.escape(str(V.get('code_version')))}, verdicts.py sha {html.escape(str(V.get('verdicts_py_sha256_12')))}"
            if V else "verdicts.json: Skipped, not found in the run folder")
    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()[:12]
    return ("<h3>Method notes and limits</h3><ul>"
            "<li>KS p-values are optimistic when parameters are fitted to the same data.</li>"
            "<li>K-means is a side analysis. The clusters describe the sample.</li>"
            "<li>A wallet is an address, not a person.</li>"
            "<li>Tests assume independent markets. Markets on one event are not independent.</li>"
            "<li>Duplicate rows are kept. Volume includes trades after T - 1 day.</li>"
            + limits +
            f"<li>Pre-registered verdicts exist only for scope = full runs.{s_txt}</li></ul>"
            "<h3>Reproduce</h3>"
            f"<p>Run id: <code>{html.escape(run.name)}</code>. Pre-registration: <code>analysis/prereg_mvp1.md</code>"
            + (", <code>analysis/prereg_mvp2.md</code>" if D.get("q1a") or D.get("q1b") or D.get("q1c") else "")
            + ". Parameters: <code>prereg.json</code> in the run folder. "
            f"Report code: <code>make_report.py</code> {CODE_VERSION}, sha <code>{sha}</code>. {vtxt}.</p>"
            + P.table("Code version, code SHA, SLURM job id, host and CPUs of every stage (from the manifests). CPUs: SLURM / DuckDB threads.",
                      ["Stage", "code_version", "code_sha", "SLURM job id", "Host", "CPUs"], mf))


# ---------- main ----------
def load_run(run: Path) -> dict:
    return {"prereg": jload(run, "prereg.json") or {}, "tables": jload(run, "tables_summary.json"),
            "q3": jload(run, "q3_results.json"), "q1": jload(run, "q1_results.json"), "q2": jload(run, "q2_results.json"),
            "q1_bins": cload(run, "q1_bins.csv"), "q1_bins_no_min": cload(run, "q1_bins_no_min.csv"),
            "q1_bins_eqfreq": cload(run, "q1_bins_eqfreq.csv"),
            "q1a": jload(run, "q1a_results.json"), "q1a_tab": cload(run, "q1a_contingency.csv"),
            "q1b": jload(run, "q1b_results.json"), "q1c": jload(run, "q1c_results.json"),
            "q1c_binned": cload(run, "q1c_binned.csv"), "verdicts": jload(run, "verdicts.json"),
            "q2_scaling": cload(run, "q2_kmeans_scaling.csv")}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--version", required=True, choices=["v1", "v2"])
    ap.add_argument("--out", required=True)
    ap.add_argument("--compare", help="v1 run folder for the consistency table (v2 only)")
    a = ap.parse_args()
    run, v2 = Path(a.run), a.version == "v2"
    D = load_run(run)
    if not D["tables"]:
        raise SystemExit(f"{run}/tables_summary.json not found: not a run folder")
    full = D["prereg"].get("scope") == "full"
    P = Page(run)
    steps = [("summary", "Summary", sec_summary(P, D, full, v2)), ("data", "Data and filters", sec_data(P, D)),
             ("q3", "Q3: distributions", sec_q3(P, D)), ("q1", "Q1: calibration", sec_q1(P, D)),
             ("q2", "Q2: wallet concentration", sec_q2(P, D))]
    if v2:
        steps += [("q1a", "Q1a: topic", sec_q1a(P, D)), ("q1b", "Q1b: deadline", sec_q1b(P, D)),
                  ("q1c", "Q1c: volume", sec_q1c(P, D))]
        if a.compare:
            steps.append(("compare", "Consistency with v1", sec_compare(P, D, load_run(Path(a.compare)))))
    steps.append(("method", "Method notes and reproduce", sec_method(P, D, run)))
    n = len(steps)
    nav = "".join(f'<li><a href="#{i}">{html.escape(t)}</a></li>' for i, t, _ in steps)
    boxes = "".join(f'<section id="{i}"><div class="eyebrow">Step {k} of {n}</div><h2>{html.escape(t)}</h2>{b}</section>'
                    for k, (i, t, b) in enumerate(steps, 1))
    scope = html.escape(str(D["prereg"].get("scope")))
    page = (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>Polymarket calibration report {a.version}</title>'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;700&amp;family=IBM+Plex+Sans+KR:wght@400;500&amp;display=swap">'
            f"<style>{CSS}</style></head><body><main><header>"
            f'<div class="eyebrow">CS 6344 Intro to Data Science · Group 1 project · {"MVP1 and MVP2" if v2 else "MVP1"} · scope {scope}</div>'
            "<h1>When Polymarket says 70%, does it happen 70% of the time?</h1>"
            f'<p class="lede">Report {a.version} from the saved run <code>{html.escape(run.name)}</code>. {n} steps.</p>'
            f'<ol class="steps-nav">{nav}</ol></header>{boxes}'
            f"<footer>Data source: {PAPER}. Run folder: {html.escape(str(run))}</footer></main></body></html>")
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page)
    print(f"wrote {out} ({out.stat().st_size / 1e6:.2f} MB), {n} steps: " + ", ".join(t for _, t, _ in steps))


if __name__ == "__main__":
    main()
