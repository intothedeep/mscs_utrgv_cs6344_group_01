#!/bin/bash
### MVP2 job: build tables (v2), MVP1 stages again, then Q1a, Q1b, Q1c, summary (CPU only). Usage on login001:
###   cd ~/cs6344_polymarket && sbatch -p gpul40q jobs/mvp2.slurm mvp2_<scope> analysis/prereg_mvp2.json
### One run folder holds the whole v2 report. Structure follows jobs/mvp1_b.slurm. Only the main session submits.
#SBATCH --job-name=pm_mvp2
#SBATCH --output=logs/%x.out.%j
#SBATCH --error=logs/%x.err.%j
#SBATCH -N 1
#SBATCH -c 8
#SBATCH --mem=64G
#SBATCH --time=02:00:00

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
python "$C/q3_describe.py"        --params prereg.json --out "$RUN_DIR" || echo "STAGE q3_describe FAILED"
python "$C/q1_calibration.py"     --params prereg.json --out "$RUN_DIR" || echo "STAGE q1_calibration FAILED"
python "$C/q2_concentration.py"   --params prereg.json --out "$RUN_DIR" || echo "STAGE q2_concentration FAILED"
python "$C/q1a_category.py"       --params prereg.json --out "$RUN_DIR" || echo "STAGE q1a_category FAILED"
python "$C/q1b_deadline.py"       --params prereg.json --out "$RUN_DIR" || echo "STAGE q1b_deadline FAILED"
python "$C/q1c_volume.py"         --params prereg.json --out "$RUN_DIR" || echo "STAGE q1c_volume FAILED"
python "$C/verdicts.py"           --out "$RUN_DIR"                      || echo "STAGE verdicts FAILED"
python "$C/make_summary.py"       --out "$RUN_DIR"                      || echo "STAGE make_summary FAILED"

ls -la "$RUN_DIR"
echo "=== done $(date -Is) ==="
