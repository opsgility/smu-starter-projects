# ai200_module14_otel_kql — OpenTelemetry + Azure Monitor + KQL

Starter project for **AI-200 Module 14**. Instrument a FastAPI app with
Python OTel + the Azure Monitor exporter, deploy to Container Apps,
generate traffic, and query traces from Log Analytics with KQL.

## What's already scaffolded

| Path | Purpose |
| --- | --- |
| `lib/telemetry.py` | `configure` TODO (Step 4) |
| `app/main.py` | FastAPI app with two manual spans; one more span TODO (Step 6) |
| `scripts/loadgen.py` | Drives 200 requests through the deployed app |
| `kql/01_recent_traces.kql` | Most recent 50 spans |
| `kql/02_classify_p95.kql` | P50/P95/P99 latency over the last hour |
| `kql/03_top_labels.kql` | Most-frequent classifier labels by tenant |
| `kql/04_slowest_traces.kql` | 20 slowest classify operations |
| `Dockerfile` | Container image used for ACA deploy |
