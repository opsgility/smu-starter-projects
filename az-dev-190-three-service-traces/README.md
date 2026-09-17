# az-dev-190-three-service-traces

Three services (`Web` → `Api` → `Worker`) instrumented with OpenTelemetry propagating W3C Trace Context and `TenantId` baggage across the full call chain.

## Run
```
dotnet run --project Web    # http://localhost:5001
dotnet run --project Api    # http://localhost:5002
dotnet run --project Worker # http://localhost:5003
```

Then `curl http://localhost:5001/checkout -H 'X-Tenant-Id: anchor-42'` and inspect the App Insights end-to-end trace view — one traceparent through all three services with `TenantId=anchor-42` on every span.

## Environment
- `APPLICATIONINSIGHTS_CONNECTION_STRING` on all three services.
- `API_BASE_URL` on Web pointing at Api.
- `WORKER_BASE_URL` on Api pointing at Worker.
