# az-dev-110-plan-compare

Same Function code deployed to Flex Consumption AND Premium plans for cold-start comparison. `PingFunction` reports process start time so you can tell warm from cold.

`scripts/coldstart.sh` fires periodic requests with idle windows to force cold starts. Compare `elapsedMs` and `processAge` across plans.
