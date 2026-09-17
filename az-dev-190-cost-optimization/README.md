# az-dev-190-cost-optimization

Anchorline OTel with 5% head sampling (`TraceIdRatioBasedSampler`). Metrics are never sampled — they aggregate at emit time. Route debug logs to a basic-tier custom table via a Log Analytics data collection rule and confirm the workspace ingestion drops ~60% vs the 100%-sampled baseline.
