#!/bin/bash
### Q1-only rerun (code v5): writes p_bh and reject_bh into q1_bins_eqfreq.csv. Reuses markets.parquet of an earlier run. CPU only. Usage on login001:
###   cd ~/cs6330_polymarket && sbatch -p kimq -c 4 --mem=32G --time=00:30:00 jobs/q1_only.slurm q1eqfreq_v5 142083_mvp2_full_v2r3
### Arg 1 = new run name. Arg 2 = source run folder name under runs/ that holds markets.parquet and prereg.json.
### No raw-data pass: q1_calibration.py reads only markets.parquet. Only the main session submits.
#SBATCH --job-name=pm_q1only
#SBATCH --output=logs/%x.out.%j
#SBATCH --error=logs/%x.err.%j
#SBATCH -N 1
#SBATCH -c 4
#SBATCH --mem=32G
#SBATCH --time=00:30:00

set -euo pipefail
RUN="${1:?give the new run name}"; SRC="${2:?give the source run folder name under runs/}"

PROJ=~/cs6330_polymarket
ENV=~/myEnvs/cs6330

SRC_DIR="$PROJ/runs/$SRC"
RUN_DIR="$PROJ/runs/${SLURM_JOB_ID}_${RUN}"
mkdir -p "$RUN_DIR" "$PROJ/logs"
cp "$SRC_DIR/markets.parquet" "$RUN_DIR/markets.parquet"   # q1_calibration.py reads $RUN_DIR/markets.parquet
cp "$SRC_DIR/prereg.json" "$RUN_DIR/prereg.json"           # same criteria as the source run
cd "$RUN_DIR"
sha256sum markets.parquet > input.sha256                   # which input this run used

source "$ENV/bin/activate"
export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK:-4}
echo "=== run $RUN job $SLURM_JOB_ID source $SRC host $(hostname) dir $RUN_DIR start $(date -Is) ==="

mkdir -p code_snapshot && cp "$PROJ"/code/*.py code_snapshot/   # code snapshot (measurement.md §2)
sha256sum code_snapshot/*.py > code.sha256

python "$PROJ/code/q1_calibration.py" --params prereg.json --out "$RUN_DIR" || echo "STAGE q1_calibration FAILED"

ls -la "$RUN_DIR"
echo "=== done $(date -Is) ==="
