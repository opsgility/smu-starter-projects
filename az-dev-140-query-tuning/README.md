# az-dev-140-query-tuning

Diagnose a slow query with `IndexMetrics`, add a composite index, verify cost drops.

## Env

- `ANCHORLINE_COSMOS_ENDPOINT`
- `ANCHORLINE_COSMOS_DB` — default `AnchorlineQueryTune`

## Modes

```
dotnet run --project . -- seed        # 20k products; ~3-5 min
dotnet run --project . -- query       # measured query with index metrics
dotnet run --project . -- avg100      # avg RU over 100 executions
dotnet run --project . -- add-index   # add /category ASC + /rating DESC composite index
```
