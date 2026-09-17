# az-dev-130-perf

Slow-query diagnostic starter for AZ-DEV-130 M5L10.

## Env

- `ANCHORLINE_SQL_SERVER`
- `ANCHORLINE_SQL_DATABASE` — default `AnchorlineOrders`

## Modes

```
dotnet run --project . -- seed   # load 1M rows into dbo.LoadOrders (~2-3 min at GP_Gen5_2)
dotnet run --project . -- slow   # run the target query — expect ~1-5s at first
dotnet run --project . -- fast   # same query, but after you added the covering index
dotnet run --project . -- top    # read Query Store for the query's runtime stats
```

## The target query

Marked with a `/*QLABEL:perf-search*/` comment so you can filter Query Store to it.
