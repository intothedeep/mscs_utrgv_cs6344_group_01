#!/bin/bash
### V-1 label check (D-036): label of the outcome coded 1 over the 47,948 kept markets. CPU only. Usage on login001:
###   cd ~/cs6344_polymarket && sbatch jobs/v1_label_check.slurm v1label 142082_mvp1_full_v1r3
### Arg 1 = new run name. Arg 2 = source run folder name under runs/ that holds markets.parquet and prereg.json.
### Reads markets.parquet (saved) and three raw columns (condition_id, outcome_seq, outcome_label) of the kept markets. No fit.
### The source run stays untouched. Only the main session submits.
#SBATCH --job-name=pm_v1label
#SBATCH --output=logs/%x.out.%j
#SBATCH --error=logs/%x.err.%j
#SBATCH -N 1
#SBATCH -p gpul40q
#SBATCH -w gpu011
#SBATCH -c 8
#SBATCH --mem=64G
#SBATCH --time=01:00:00

set -euo pipefail
RUN="${1:?give the new run name}"; SRC="${2:?give the source run folder name under runs/}"

PROJ=~/cs6344_polymarket
ENV=~/myEnvs/cs6344

SRC_DIR="$PROJ/runs/$SRC"
RUN_DIR="$PROJ/runs/${SLURM_JOB_ID}_${RUN}"
mkdir -p "$RUN_DIR" "$PROJ/logs"
ln -sfn "$PROJ/data" "$RUN_DIR/data"     # read-only by convention; common.DATA_ROOT is relative to the run dir
cd "$RUN_DIR"

source "$ENV/bin/activate"
export DUCKDB_THREADS=${SLURM_CPUS_PER_TASK:-8} DUCKDB_MEM=${DUCKDB_MEM:-48GB} OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK:-8}
echo "=== run $RUN job $SLURM_JOB_ID source $SRC host $(hostname) dir $RUN_DIR start $(date -Is) ==="

mkdir -p code_snapshot && cp "$PROJ"/code/*.py code_snapshot/   # code snapshot (measurement.md §2)
sha256sum code_snapshot/*.py > code.sha256

python "$PROJ/code/v1_label_check.py" --source "$SRC_DIR" --out "$RUN_DIR" || echo "STAGE v1_label_check FAILED"

ls -la "$RUN_DIR"
echo "=== done $(date -Is) ==="
