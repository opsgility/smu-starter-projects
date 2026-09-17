# az-dev-130-hyperscale

Prove Hyperscale named-replica routing by writing to primary and reading from the replica.

## Env

- `ANCHORLINE_SQL_PRIMARY` — primary Hyperscale server FQDN.
- `ANCHORLINE_SQL_REPLICA` — named-replica server FQDN.
- `ANCHORLINE_SQL_DATABASE` = `AnchorlineOrders`.

## Modes

```
dotnet run --project . -- setup     # create dbo.Signals on primary
dotnet run --project . -- write     # write from the app (goes to primary)
dotnet run --project . -- read      # read from the named replica
dotnet run --project . -- readonly  # try to write to replica — expect failure
```
