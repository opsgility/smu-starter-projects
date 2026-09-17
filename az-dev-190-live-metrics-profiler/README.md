# az-dev-190-live-metrics-profiler

Two endpoints — `/report/full` (deliberately expensive) and `/report/full-fixed` (cached options, no intermediate list). Deploy to the P0v3 App Service, enable Profiler, hit `/report/full` under load, wait ~2 minutes for a Profiler trace, and inspect the hot path. Switch to `/report/full-fixed` to confirm the improvement in Live Metrics.
