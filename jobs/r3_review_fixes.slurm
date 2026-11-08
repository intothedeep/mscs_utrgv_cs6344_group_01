#!/bin/bash
### Robustness v3 (review fixes M1 to M5, minor 4, peer asks), code v6, prereg analysis/prereg_review_fixes.{md,json} (commit aef0808). CPU only. Usage on login001:
###   cd ~/cs6344_polymarket && sbatch jobs/r3_review_fixes.slurm r3_review_fixes_v6 142082_mvp1_full_v1r3 150296_v1label
### Arg 1 = new run name. Arg 2 = base run folder under runs/ (markets.parquet, q1_results.json, q2_results.json). Arg 3 = V-1 label run folder under runs/.
### The prereg JSON `extends` analysis/prereg_robustness.json: both files are copied into the run folder (prereg.json and prereg_robustness.json).
### Memory note: the gate rebuilds the full market table (all raw trades in DuckDB), which ran with 16 CPU / 200G in 142082. If it is killed for memory, resubmit with:
###   sbatch -p gpul40q -c 16 --mem=200G --time=04:00:00 --export=ALL,DUCKDB_MEM=160GB jobs/r3_review_fixes.slurm <same args>
### Order: side check (stops the job on failure), gate and raw pass (stops the job on failure), then each item guarded. Only the main session submits.
#SBATCH --job-name=pm_r3_fixes
#SBATCH --output=logs/%x.out.%j
#SBATCH --error=logs/%x.err.%j
#SBATCH -N 1
#SBATCH -p kimq
#SBATCH -c 8
#SBATCH --mem=64G
#SBATCH --time=03:00:00

set -euo pipefail
RUN="${1:?give the new run name}"; SRC="${2:?give the base run folder name under runs/}"; LABEL="${3:?give the label run folder name under runs/}"

PROJ=~/cs6344_polymarket
ENV=~/myEnvs/cs6344

SRC_DIR="$PROJ/runs/$SRC"; LABEL_DIR="$PROJ/runs/$LABEL"
RUN_DIR="$PROJ/runs/${SLURM_JOB_ID}_${RUN}"
mkdir -p "$RUN_DIR" "$PROJ/logs"
ln -sfn "$PROJ/data" "$RUN_DIR/data"     # read-only by convention; common.DATA_ROOT is relative to the run dir
cp "$PROJ/analysis/prereg_review_fixes.json" "$RUN_DIR/prereg.json"      # criteria fixed before the run, kept with its results
cp "$PROJ/analysis/prereg_robustness.json" "$RUN_DIR/prereg_robustness.json"   # the base the prereg extends
cd "$RUN_DIR"

source "$ENV/bin/activate"
export DUCKDB_THREADS=${SLURM_CPUS_PER_TASK:-8} DUCKDB_MEM=${DUCKDB_MEM:-48GB} OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK:-8}
echo "=== run $RUN job $SLURM_JOB_ID base $SRC label $LABEL host $(hostname) dir $RUN_DIR start $(date -Is) ==="
python - <<'PY'
import platform, duckdb, pandas, scipy, statsmodels
print("python", platform.python_version(), "duckdb", duckdb.__version__, "pandas", pandas.__version__,
      "scipy", scipy.__version__, "statsmodels", statsmodels.__version__)
PY

mkdir -p code_snapshot && cp "$PROJ"/code/*.py code_snapshot/   # code snapshot (measurement.md §2)
sha256sum code_snapshot/*.py > code.sha256

C="$PROJ/code"
A="--params prereg.json --source $SRC_DIR --out $RUN_DIR"

# Step 1: side columns. A failure stops the job before anything else runs.
python "$C/r3_side_check.py" $A || { echo "STOP: side mapping check failed (see report_r3_side_check.md). No item computed."; exit 1; }
# Step 2: gate and raw pass. A failure stops the job: "gate failed", no item computed.
python "$C/r3_build.py" $A || { echo "STOP: gate failed (see r3_gate.json). No item computed."; exit 1; }

# Items: a failing item must not stop the others. M5 needs M1 (h) and M3 (read proxy).
python "$C/r3_m1.py" $A                      || echo "STAGE r3_m1 FAILED"
python "$C/r3_m3.py" $A                      || echo "STAGE r3_m3 FAILED"
python "$C/r3_m5.py" $A                      || echo "STAGE r3_m5 FAILED"
python "$C/r3_m2.py" $A --label-run "$LABEL_DIR" || echo "STAGE r3_m2 FAILED"
python "$C/r3_m4.py" $A                      || echo "STAGE r3_m4 FAILED"
python "$C/r3_peer.py" $A                    || echo "STAGE r3_peer FAILED"
python "$C/r3_minor4.py" $A                  || echo "STAGE r3_minor4 FAILED"

ls -la "$RUN_DIR"
echo "=== done $(date -Is) ==="
