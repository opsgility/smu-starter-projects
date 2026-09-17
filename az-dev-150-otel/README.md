# az-dev-150-otel

Two-service OpenTelemetry demo. OrderApi calls OrderProcessor via HTTP; both export to Application Insights.

## Env

Both services need:
- `APPLICATIONINSIGHTS_CONNECTION_STRING` — App Insights connection string

OrderApi also needs:
- `PROCESSOR_URL` — internal DNS of OrderProcessor
