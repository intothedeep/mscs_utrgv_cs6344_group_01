"""Shared helpers for the Polymarket MVP1 pipeline (paths, DuckDB, manifest, reports, market set)."""
import hashlib
import json
import os
import platform
import socket
import sys
import traceback
from pathlib import Path
from typing import Callable

import duckdb

CODE_VERSION = "v4"

# Pilot = Standard Binary markets whose close_at falls in this month (UTC), with ALL their trades.
# Why: one month of trade partitions would cut markets mid-life and break the close-time check.
PILOT_MONTH = "2025-06"

DATA_ROOT = Path(os.environ.get("PM_DATA", "data/polymarket_v1"))  # relative to the run dir (data symlink)

DEFAULT_PARAMS = {
    "t_rule": "close_at",       # "last_trade" or "close_at"
    "min_trades": 10,
    "max_staleness_h": 24,
    "n_bins": 10,
    "alpha": 0.05,
    "pilot_month": PILOT_MONTH,
    "scope": "pilot",           # "pilot" or "full"
    "updown_rule": "default",   # "default" or "none"
    # v2 (MVP2) additions. Defaults only, so the MVP1 prereg still loads; prereg_mvp2.json sets them.
    "horizon_long_days": 7,
    "min_category_n": 30,
    "n_perm": 1000,
    "seed": 42,
    # v4 (robustness) additions. Defaults only, so older preregs still load; prereg_robustness.json sets them.
    "robust_agree_min": 0.95,
    "robust_delta_thresholds": [0.10, 0.25, 0.50],
    "robust_quantiles": [0.5, 0.75, 0.9, 0.95, 0.99],
    "robust_yes_payout_index": 0,
}

# Up/Down markets: slug pattern or category_refined pattern. Job A confirms which one marks them.
# Why a parameter: the marking is unknown until Job A has looked at value_counts.csv.
UPDOWN_SQL = {
    "default": (
        "(coalesce(market_slug,'') ILIKE '%up-or-down%' OR coalesce(market_slug,'') ILIKE '%updown%'"
        " OR coalesce(category_refined,'') ILIKE '%up%down%' OR coalesce(category_refined,'') ILIKE '%updown%')"
    ),
    "none": "FALSE",
}


def load_params(path: str | None) -> dict:
    """Defaults, overridden by the prereg JSON when a path is given."""
    params = dict(DEFAULT_PARAMS)
    if path:
        params.update(json.loads(Path(path).read_text()))
    return params


def connect() -> duckdb.DuckDBPyConnection:
    """DuckDB connection sized from env (job sets DUCKDB_THREADS / DUCKDB_MEM)."""
    con = duckdb.connect()
    con.execute(f"SET threads={int(os.environ.get('DUCKDB_THREADS', 8))}")
    con.execute(f"SET memory_limit='{os.environ.get('DUCKDB_MEM', '48GB')}'")
    con.execute("SET temp_directory='duckdb_tmp'")
    con.execute("SET TimeZone='UTC'")  # tz-aware timestamps cast to UTC wall time
    return con


def code_sha(script: str) -> str:
    return hashlib.sha256(Path(script).read_bytes()).hexdigest()[:12]


def env_info() -> dict:
    import numpy
    import pandas
    return {
        "hostname": socket.gethostname(), "python": platform.python_version(),
        "duckdb": duckdb.__version__, "pandas": pandas.__version__, "numpy": numpy.__version__,
        "slurm_job_id": os.environ.get("SLURM_JOB_ID", "none"),
        # Thread count caused the v1/v2 non-determinism (review F3, F4): the run folder must show it.
        "slurm_cpus_per_task": os.environ.get("SLURM_CPUS_PER_TASK", "none"),
        "slurm_mem_per_node": os.environ.get("SLURM_MEM_PER_NODE", "none"),
        "duckdb_threads": os.environ.get("DUCKDB_THREADS", "none"),
        "duckdb_mem": os.environ.get("DUCKDB_MEM", "none"),
    }


def write_manifest(out_dir: Path, params: dict, metrics: dict, script: str, stage: str | None = None) -> None:
    """measurement.md §2.1 fields. Job A: manifest.json. Job B: manifest_<stage>.json (one per stage)."""
    name = "manifest.json" if stage is None else f"manifest_{stage}.json"
    manifest = {"code_version": CODE_VERSION, "code_sha": code_sha(script), "params": params,
                "env": env_info(), "metrics": metrics}
    (out_dir / name).write_text(json.dumps(manifest, indent=2, default=str))


def write_json(path: Path, obj: object) -> None:
    path.write_text(json.dumps(obj, indent=2, default=str))


def write_report(out_dir: Path, stage: str, fields: dict[str, str]) -> None:
    """Stage report: What / Why / Input data / Output data / Result / Status (+ optional Figure/Table)."""
    lines = [f"# Stage report: {stage}", ""]
    lines += [f"**{key}:** {value}\n" for key, value in fields.items()]
    (out_dir / f"report_{stage}.md").write_text("\n".join(lines))


def run_stage(out_dir: Path, stage: str, what: str, fn: Callable[[], dict[str, str]]) -> None:
    """Run a stage; on failure write a 'failed' report and exit 1 so the job script prints STAGE FAILED.

    fn returns the report fields. Status is added here.
    """
    try:
        fields = fn()
        fields.setdefault("Status", "ran")
        write_report(out_dir, stage, {"What": what, **fields})
    except Exception:
        write_report(out_dir, stage, {"What": what, "Status": "failed: " + traceback.format_exc()[-1500:]})
        raise


def raw_glob() -> str:
    return str(DATA_ROOT / "daily_aligned" / "*.parquet")


def build_market_set(con: duckdb.DuckDBPyConnection, params: dict) -> None:
    """Create tables `mkts` (one row per market in scope, with flags) and `tr` (their trades).

    Pilot scope: close_at in pilot_month. Flags (not filters) mark Up/Down and non-binary markets,
    so Job A can inspect them and Job B can drop them with counted reasons.
    Assumptions Job A must confirm: close_at is constant per market; binary = at most 2 distinct
    outcome_seq values and neg_risk != 'true'.
    """
    updown = UPDOWN_SQL[params["updown_rule"]]
    con.execute(f"""
        CREATE VIEW raw AS SELECT * FROM read_parquet('{raw_glob()}', union_by_name=true)""")
    scope_sql = ""
    if params["scope"] == "pilot":
        month = params["pilot_month"]
        scope_sql = (f"HAVING max(TRY_CAST(close_at AS TIMESTAMP)) >= TIMESTAMP '{month}-01' "
                     f"AND max(TRY_CAST(close_at AS TIMESTAMP)) < TIMESTAMP '{month}-01' + INTERVAL 1 MONTH")
    # Market-level columns only: parquet reads just these columns, so this pass is cheap.
    con.execute(f"""
        CREATE TABLE mkts_raw AS
        SELECT condition_id,
               max(TRY_CAST(close_at AS TIMESTAMP)) AS close_at,
               max(TRY_CAST(opens_at AS TIMESTAMP)) AS opens_at,
               max(TRY_CAST(resolved_at AS TIMESTAMP)) AS resolved_at,
               max(category) AS category, max(category_refined) AS category_refined,
               max(resolution_status) AS resolution_status,
               max(CAST(neg_risk AS VARCHAR)) AS neg_risk, max(market_slug) AS market_slug,
               max(winning_outcome_label) AS winning_outcome_label,
               max(outcome_label) FILTER (WHERE CAST(outcome_seq AS BIGINT) = 1) AS label1,
               count(DISTINCT CAST(outcome_seq AS BIGINT)) AS n_outcome_seq
        FROM raw GROUP BY condition_id {scope_sql}""")
    con.execute(f"""
        CREATE TABLE mkts AS
        SELECT *, {updown} AS is_updown,
               (n_outcome_seq <= 2 AND coalesce(neg_risk,'false') <> 'true') AS is_binary
        FROM mkts_raw""")
    con.execute("""
        CREATE TABLE tr AS
        SELECT r.condition_id, r.asset_id,
               -- int64 seconds in the card; fall back to a timestamp cast if the type differs
               coalesce(to_timestamp(TRY_CAST(r.block_timestamp AS BIGINT)),
                        TRY_CAST(r.block_timestamp AS TIMESTAMP)) AS ts,
               r.price, r.p_event, r.maker, r.taker, r.usdc_amount,
               CAST(r.outcome_seq AS BIGINT) AS outcome_seq
        FROM raw r SEMI JOIN mkts m USING (condition_id)""")


def md_table(df) -> str:
    """Markdown table without the optional `tabulate` dependency (cluster env may lack it)."""
    head = "| " + " | ".join(map(str, df.columns)) + " |"
    sep = "| " + " | ".join("---" for _ in df.columns) + " |"
    rows = ["| " + " | ".join(f"{v:.4g}" if isinstance(v, float) else str(v) for v in r) + " |"
            for r in df.itertuples(index=False)]
    return "\n".join([head, sep, *rows])
