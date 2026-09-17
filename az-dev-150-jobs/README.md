# az-dev-150-jobs

Same container image runs two different Container Apps Jobs based on the `JOB_MODE` env var.

- `JOB_MODE=etl`      — 10-second ETL simulation
- `JOB_MODE=process`  — 3-second single-work-unit processor
