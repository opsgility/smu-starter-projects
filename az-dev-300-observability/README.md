# az-dev-300-observability

OTel + Azure Monitor exporter starter + SLO KQL queries.

Set `ApplicationInsights:ConnectionString` in appsettings or as env var.

## SLO queries
- `kql/slo-availability.kql` — fast burn 14.4× for 5 min → page
- `kql/slo-latency.kql` — p95 latency > 500 ms → alert

Wire each as a Log Analytics alert rule; route to a `taskforge-oncall` Action Group.
