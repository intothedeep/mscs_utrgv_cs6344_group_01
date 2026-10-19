# CHANGELOG (code versions, `rules/measurement.md` §2.2)

| Version | Date | Changed | Affected runs |
| --- | --- | --- | --- |
| v1 | 2026-10-19 | First MVP1 pipeline: `pilot_inspect.py` (Job A), `build_tables.py`, `q3_describe.py`, `q1_calibration.py`, `q2_concentration.py`, `make_summary.py` (Job B) | none yet |
| v2 | 2026-10-19 | `build_tables.py`: appended columns `p_7d`, `p_age_7d_h`, `open_ge_7d` to `markets` (existing columns and drop logic unchanged). `common.py`: `CODE_VERSION` v2, default params `horizon_long_days`, `min_category_n`, `n_perm`, `seed`. `make_summary.py`: lists MVP2 stages when their reports exist. New: `q1a_category.py`, `q1b_deadline.py`, `q1c_volume.py`, `jobs/mvp2.slurm` | none yet |

Invariance evidence: none needed for v1 (first version).

Invariance evidence for v2: by construction, the new columns are added after `kept_no_min` with `ALTER TABLE ... ADD COLUMN` and `UPDATE`. No SQL that builds an existing column or `drop_reason` changed. Not yet measured. To confirm in the first v2 run: the v1 columns of `markets.parquet` and `n_kept`, `drop_reasons` in `tables_summary.json` match the MVP1 pilot run.
