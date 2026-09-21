# az-dev-110-plan-compare

Same Function code deployed to Flex Consumption AND Premium plans for cold-start
comparison. `HelloFunction` (function name `Hello`, catch-all route
`hello/{*probe}`) reports process start time, hostname, and the `PLAN_LABEL`
env var so you can tell warm from cold and which plan answered.

`scripts/coldstart.sh` fires requests to `/api/hello/probeN` with idle windows
between samples to force cold starts. Compare `elapsedMs`, `processAgeSeconds`,
and `planLabel` across the two plans.
