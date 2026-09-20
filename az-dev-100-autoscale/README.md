# AZ-DEV-100 · Module 5 Lab — Scaling and autoscale

Extends the storefront with a `/burn` CPU-load endpoint and a Service Bus producer script so you can trigger both autoscale rules the M5L9 teaching lesson covered.

## Files

```
az-dev-100-autoscale/
  README.md
  .gitignore
  Project.csproj      # net10.0 + Azure.Messaging.ServiceBus
  Program.cs          # /health, /version, /burn, /consume
  appsettings.json
  scripts/
    produce.sh        # loops sending N messages to the Service Bus queue
```

## /burn endpoint

Spins CPU for N seconds so you can drive up the plan's CpuPercentage metric. Use it with `hey` or a bash loop.

```bash
curl "https://<HOST>/burn?seconds=30"
```

## /consume endpoint

Receives messages from the Service Bus queue via Managed Identity (`DefaultAzureCredential`). The producer script pushes work; the autoscale rule sees the queue depth grow; the plan scales; more instances consume.

## scripts/produce.sh

Reads `SERVICE_BUS_NAMESPACE` + `QUEUE_NAME` env vars and sends N messages via `az servicebus queue send-message` in a loop. Set `MESSAGE_COUNT=500` to trigger the queue-depth autoscale rule (per-instance threshold = 100 with 2 running instances = triggers at 200+ total).
