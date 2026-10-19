#!/bin/bash
### Job B: build tables, Q3, Q1, Q2, summary (CPU only). Usage on login001:
###   cd ~/cs6330_polymarket && sbatch jobs/mvp1_b.slurm mvp1b_pilot_2025_06 analysis/prereg_mvp1.json
### Structure follows skills/cradle-cluster/templates/job.slurm. Only the main session submits.
#SBATCH --job-name=pm_mvp1_b
#SBATCH --output=logs/%x.out.%j
#SBATCH --error=logs/%x.err.%j
#SBATCH -N 1
#SBATCH -p kimq
#SBATCH -c 8
#SBATCH --mem=64G
#SBATCH --time=02:00:00

set -euo pipefail
RUN="${1:?give the run name}"; PREREG="${2:?give the prereg JSON path relative to ~/cs6330_polymarket}"

PROJ=~/cs6330_polymarket
ENV=~/myEnvs/cs6330

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
import platform, duckdb, pandas
print("python", platform.python_version(), "duckdb", duckdb.__version__, "pandas", pandas.__version__)
PY

mkdir -p code_snapshot && cp "$PROJ"/code/*.py code_snapshot/   # code snapshot (measurement.md §2)
sha256sum code_snapshot/*.py > code.sha256

# A failing stage must not stop the later stages: each one is guarded.
C="$PROJ/code"
python "$C/build_tables.py"       --params prereg.json --out "$RUN_DIR" || echo "STAGE build_tables FAILED"
python "$C/q3_describe.py"        --params prereg.json --out "$RUN_DIR" || echo "STAGE q3_describe FAILED"
python "$C/q1_calibration.py"     --params prereg.json --out "$RUN_DIR" || echo "STAGE q1_calibration FAILED"
python "$C/q2_concentration.py"   --params prereg.json --out "$RUN_DIR" || echo "STAGE q2_concentration FAILED"
python "$C/make_summary.py"       --out "$RUN_DIR"                      || echo "STAGE make_summary FAILED"

ls -la "$RUN_DIR"
echo "=== done $(date -Is) ==="
