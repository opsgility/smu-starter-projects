# az-dev-140-partitioning

Compare a bad partition key (`/eventType`) against a hierarchical partition key (`/tenantId/customerId`).

## Env

- `ANCHORLINE_COSMOS_ENDPOINT`
- `ANCHORLINE_COSMOS_DB` — default `AnchorlinePartition`

## Modes

```
dotnet run --project . -- load-bad     # 50k events - 65% land on /eventType="page_view"; expect throttles at 400 RU/s
dotnet run --project . -- load-good    # same 50k events on hierarchical /tenantId/customerId
dotnet run --project . -- query-bad    # query hot partition, high RU
dotnet run --project . -- query-good   # query hierarchical, low RU
```

Note: containers are provisioned at 400 RU/s manual so the bad-key path throttles quickly. Real production would use autoscale.
