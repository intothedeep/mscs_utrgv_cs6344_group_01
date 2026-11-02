#!/bin/bash
# Fetch one run folder from the cluster into runs/ (tar over ssh, one connection: rules/ssh.md).
# Why: individual-level CSVs (per market, per wallet) are not in git; they stay on the cluster.
# Usage (from cs6344_group_01/):  bash jobs/fetch_run.sh 142082_mvp1_full_v1r3 [--with-parquet]
# Needs VPN and the ssh alias below (skills/cradle-cluster §4).
set -euo pipefail
RUN="${1:?give a run folder name, e.g. 142082_mvp1_full_v1r3}"
HOST="${HOST:-utrgv_cluster}"
EXCL=(--exclude=data --exclude=duckdb_tmp)
[ "${2:-}" = "--with-parquet" ] || EXCL+=(--exclude='*.parquet')
mkdir -p runs
ssh "$HOST" "cd ~/cs6344_polymarket/runs && tar cf - ${EXCL[*]} $RUN" < /dev/null | tar xf - -C runs
echo "fetched runs/$RUN"; ls runs/"$RUN" | head -50
