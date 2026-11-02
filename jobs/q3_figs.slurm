#!/bin/bash
### Four single Q3 figures: price histogram, trade-size histogram, raw-beside-log QQ of trade size and of wallet volume (D-032). CPU only. Usage on login001:
###   cd ~/cs6344_polymarket && sbatch -p kimq -c 4 --mem=32G --time=00:30:00 jobs/q3_figs.slurm q3figs_v8 142082_mvp1_full_v1r3
### Arg 1 = new run name. Arg 2 = source run folder name under runs/ that holds markets.parquet, trade_sizes_sample.parquet, wallets.parquet,
### q3_results.json and tables_summary.json. One read of each saved table, no raw-data pass, no model fit. The source run stays untouched.
### Only the main session submits.
#SBATCH --job-name=pm_q3figs
#SBATCH --output=logs/%x.out.%j
#SBATCH --error=logs/%x.err.%j
#SBATCH -N 1
#SBATCH -c 4
#SBATCH --mem=32G
#SBATCH --time=00:30:00

set -euo pipefail
RUN="${1:?give the new run name}"; SRC="${2:?give the source run folder name under runs/}"

PROJ=~/cs6344_polymarket
ENV=~/myEnvs/cs6344

SRC_DIR="$PROJ/runs/$SRC"
RUN_DIR="$PROJ/runs/${SLURM_JOB_ID}_${RUN}"
mkdir -p "$RUN_DIR" "$PROJ/logs"
cd "$RUN_DIR"

source "$ENV/bin/activate"
export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK:-4}
echo "=== run $RUN job $SLURM_JOB_ID source $SRC host $(hostname) dir $RUN_DIR start $(date -Is) ==="

mkdir -p code_snapshot && cp "$PROJ"/code/*.py code_snapshot/   # code snapshot (measurement.md §2)
sha256sum code_snapshot/*.py > code.sha256

python "$PROJ/code/q3_figs_single.py" --source "$SRC_DIR" --out "$RUN_DIR" || echo "STAGE q3_figs_single FAILED"

ls -la "$RUN_DIR"
echo "=== done $(date -Is) ==="
