#!/bin/bash
### Robustness job (D-013, code v4): build tables, Q1 (base for the sensitivity row), R1 split payouts, R2 price path, summary. CPU only. Usage on login001:
###   cd ~/cs6344_polymarket && sbatch -p gpul40q -c 16 --mem=200G --time=04:00:00 --export=ALL,DUCKDB_MEM=160GB jobs/robustness.slurm robust_full_v4 analysis/prereg_robustness.json
### Self-contained: it rebuilds markets.parquet with the unchanged v4 build_tables.py (no reuse of an older run).
### R2 reads the raw trades of the kept markets once more (build_tables.py does not keep the trade table), so this job makes two passes over the raw data.
### Structure follows jobs/mvp2.slurm. Only the main session submits.
#SBATCH --job-name=pm_robust
#SBATCH --output=logs/%x.out.%j
#SBATCH --error=logs/%x.err.%j
#SBATCH -N 1
#SBATCH -c 16
#SBATCH --mem=200G
#SBATCH --time=04:00:00

set -euo pipefail
RUN="${1:?give the run name}"; PREREG="${2:?give the prereg JSON path relative to ~/cs6344_polymarket}"

PROJ=~/cs6344_polymarket
ENV=~/myEnvs/cs6344

RUN_DIR="$PROJ/runs/${SLURM_JOB_ID}_${RUN}"
mkdir -p "$RUN_DIR" "$PROJ/logs"
ln -sfn "$PROJ/data" "$RUN_DIR/data"     # read-only by convention
cp "$PROJ/$PREREG" "$RUN_DIR/prereg.json"  # the criteria fixed before the run, kept with its results
cd "$RUN_DIR"

source "$ENV/bin/activate"
# Sized from the request so a bigger sbatch -c/--mem needs no edit here.
export DUCKDB_THREADS=${SLURM_CPUS_PER_TASK:-8} DUCKDB_MEM=${DUCKDB_MEM:-48GB} OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK:-8}
echo "=== run $RUN job $SLURM_JOB_ID host $(hostname) dir $RUN_DIR start $(date -Is) ==="
python - <<'PY'
import platform, duckdb, pandas, scipy, statsmodels
print("python", platform.python_version(), "duckdb", duckdb.__version__, "pandas", pandas.__version__,
      "scipy", scipy.__version__, "statsmodels", statsmodels.__version__)
PY

mkdir -p code_snapshot && cp "$PROJ"/code/*.py code_snapshot/   # code snapshot (measurement.md §2)
sha256sum code_snapshot/*.py > code.sha256

# A failing stage must not stop the later stages: each one is guarded.
C="$PROJ/code"
python "$C/build_tables.py"       --params prereg.json --out "$RUN_DIR" || echo "STAGE build_tables FAILED"
python "$C/q1_calibration.py"     --params prereg.json --out "$RUN_DIR" || echo "STAGE q1_calibration FAILED"
python "$C/r1_split_payout.py"    --params prereg.json --out "$RUN_DIR" || echo "STAGE r1_split_payout FAILED"
python "$C/r2_price_path.py"      --params prereg.json --out "$RUN_DIR" || echo "STAGE r2_price_path FAILED"
python "$C/make_summary.py"       --out "$RUN_DIR" --robust             || echo "STAGE make_summary FAILED"

ls -la "$RUN_DIR"
echo "=== done $(date -Is) ==="
