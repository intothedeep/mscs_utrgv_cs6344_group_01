#!/bin/bash
### Job A: inspect the pilot set (CPU only). Usage on login001:
###   cd ~/cs6344_polymarket && sbatch jobs/pilot_a.slurm pilotA_2025_06
### Structure follows skills/cradle-cluster/templates/job.slurm. Only the main session submits.
#SBATCH --job-name=pm_pilot_a
#SBATCH --output=logs/%x.out.%j
#SBATCH --error=logs/%x.err.%j
#SBATCH -N 1
#SBATCH -p kimq
#SBATCH -c 8
#SBATCH --mem=64G
#SBATCH --time=02:00:00

set -euo pipefail
RUN="${1:?give the run name, e.g. sbatch jobs/pilot_a.slurm pilotA_2025_06}"; shift || true

PROJ=~/cs6344_polymarket
ENV=~/myEnvs/cs6344

RUN_DIR="$PROJ/runs/${SLURM_JOB_ID}_${RUN}"
mkdir -p "$RUN_DIR" "$PROJ/logs"
ln -sfn "$PROJ/data" "$RUN_DIR/data"     # read-only by convention
cd "$RUN_DIR"

source "$ENV/bin/activate"
export DUCKDB_THREADS=8 DUCKDB_MEM=48GB OMP_NUM_THREADS=8
echo "=== run $RUN job $SLURM_JOB_ID host $(hostname) dir $RUN_DIR start $(date -Is) ==="
python - <<'PY'
import platform, duckdb
print("python", platform.python_version(), "duckdb", duckdb.__version__)
PY

cp "$PROJ/code/pilot_inspect.py" "$PROJ/code/common.py" "$RUN_DIR/"   # code snapshot (measurement.md §2)
sha256sum pilot_inspect.py common.py > code.sha256
python "$PROJ/code/pilot_inspect.py" --run "$RUN" --job "$SLURM_JOB_ID" --out "$RUN_DIR" "$@" \
  || echo "STAGE pilot_inspect FAILED"

ls -la "$RUN_DIR"
echo "=== done $(date -Is) ==="
