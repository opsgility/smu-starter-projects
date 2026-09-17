# az-dev-190-otel-foundations

Anchorline Outdoors' first OpenTelemetry-to-Azure-Monitor instrumentation for a .NET 10 minimal API.

## Environment
- `APPLICATIONINSIGHTS_CONNECTION_STRING` — copied from the pre-provisioned Application Insights component.

## Run
```
dotnet run
```

Then hit `/orders`, `/orders/ord-001`, and `/simulate/error` to generate traces, metrics, and log entries. All three signals appear in Application Insights within about 60 seconds.

## What to look for in App Insights
- **Transaction search** — the request telemetry with a correlated trace and any dependencies.
- **Live Metrics** — real-time RPS, failure rate, and duration.
- **Logs** — KQL over `requests`, `dependencies`, `traces`, `customMetrics`, `exceptions`.
- **Metrics explorer** — the custom `anchorline.foundations.requests.total` counter under `customMetrics`.
