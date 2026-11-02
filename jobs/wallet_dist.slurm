#!/bin/bash
### Wallet and volume distributions + full Lorenz curve (D-031, visualization.md §7). CPU only. Usage on login001:
###   cd ~/cs6344_polymarket && sbatch -p kimq -c 4 --mem=32G --time=00:30:00 jobs/wallet_dist.slurm walletdist_v7 142082_mvp1_full_v1r3
### Arg 1 = new run name. Arg 2 = source run folder name under runs/ that holds wallets.parquet and q2_results.json.
### One read of wallets.parquet (a saved output, 2.1 million rows), no raw-data pass, no model fit. The source run stays untouched.
### Only the main session submits.
#SBATCH --job-name=pm_walletdist
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

python "$PROJ/code/wallet_dist_figs.py" --source "$SRC_DIR" --out "$RUN_DIR" || echo "STAGE wallet_dist_figs FAILED"

ls -la "$RUN_DIR"
echo "=== done $(date -Is) ==="
