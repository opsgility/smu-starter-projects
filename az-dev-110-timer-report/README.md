# az-dev-110-timer-report

Anchorline's nightly inventory reconciliation report — TimerTrigger writing to Blob Storage.

## Schedule

The cron expression is read from the `NightlyReportSchedule` app setting via `%NightlyReportSchedule%` template.

- Local dev: `*/30 * * * * *` (every 30 seconds) for rapid iteration.
- Production: `0 0 2 * * *` (02:00 UTC daily).

Exercise 2 adds the singleton blob-lease pattern to guarantee once-per-slot execution when scaled out.
