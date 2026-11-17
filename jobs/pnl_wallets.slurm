#!/bin/bash
### Wallet profit and loss (analysis/prereg_pnl.md, owner request 2026-11-16). CPU only. Usage on login001:
###   cd ~/cs6344_polymarket && sbatch -p kimq -c 8 --mem=64G --time=04:00:00 --export=ALL,DUCKDB_MEM=44GB jobs/pnl_wallets.slurm pnl_wallets_v1 142123_robust_full_v4
### Arg 1 = new run name. Arg 2 = source run folder under runs/ that holds markets.parquet (the kept set and Up/Down flags).
### Four passes over the raw trades (market table, wallet table, market check, short check on the kept markets). No model, no fit.
### DuckDB spills to $RUN_DIR/duckdb_tmp: delete that folder by hand after the fetch. Only the main session submits.
#SBATCH --job-name=pm_pnl
#SBATCH --output=logs/%x.out.%j
#SBATCH --error=logs/%x.err.%j
#SBATCH -N 1
#SBATCH -c 8
#SBATCH --mem=64G
#SBATCH --time=04:00:00

set -euo pipefail
RUN="${1:?give the new run name}"; SRC="${2:?give the source run folder name under runs/}"

PROJ=~/cs6344_polymarket
ENV=~/myEnvs/cs6344

SRC_DIR="$PROJ/runs/$SRC"
[ -f "$SRC_DIR/markets.parquet" ] || { echo "no markets.parquet in $SRC_DIR"; exit 1; }
RUN_DIR="$PROJ/runs/${SLURM_JOB_ID}_${RUN}"
mkdir -p "$RUN_DIR" "$PROJ/logs"
ln -sfn "$PROJ/data" "$RUN_DIR/data"        # read-only by convention
cp "$PROJ/analysis/prereg_pnl.md" "$RUN_DIR/prereg_pnl.md"   # the criteria fixed before the run, kept with its results
cd "$RUN_DIR"

source "$ENV/bin/activate"
export DUCKDB_THREADS=${SLURM_CPUS_PER_TASK:-8} DUCKDB_MEM=${DUCKDB_MEM:-44GB} OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK:-8}
echo "=== run $RUN job $SLURM_JOB_ID source $SRC host $(hostname) dir $RUN_DIR start $(date -Is) ==="
python - <<'PY'
import platform, duckdb, pandas, numpy
print("python", platform.python_version(), "duckdb", duckdb.__version__, "pandas", pandas.__version__, "numpy", numpy.__version__)
PY

mkdir -p code_snapshot && cp "$PROJ"/code/*.py code_snapshot/   # code snapshot (measurement.md §2)
sha256sum code_snapshot/*.py > code.sha256

python "$PROJ/code/pnl_wallets.py" --markets-src "$SRC_DIR" --out "$RUN_DIR" || echo "STAGE pnl_wallets FAILED"

ls -la "$RUN_DIR"
echo "=== done $(date -Is) ==="
