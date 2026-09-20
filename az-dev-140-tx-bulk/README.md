# az-dev-140-tx-bulk

Bulk ingest + TransactionalBatch atomicity demo.

## Env

- `ANCHORLINE_COSMOS_ENDPOINT`
- `ANCHORLINE_COSMOS_DB` — default `AnchorlineTxBulk`

## Modes

```
dotnet run --project . -- bulk        # 100k events at 10000 RU/s target throughput
dotnet run --project . -- batch       # atomic order + 4 lines via TransactionalBatch
dotnet run --project . -- batch-fail  # force one line id to conflict; observe atomic rollback
```
