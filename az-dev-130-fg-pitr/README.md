# az-dev-130-fg-pitr

Exercise a failover-group failover and a PITR recovery.

## Env

- `ANCHORLINE_FG_WRITE` — failover group write listener FQDN (e.g. `anchorline-fg-<suffix>.database.windows.net`).
- `ANCHORLINE_SQL_DATABASE` = `AnchorlineOrders`.

## Modes

```
dotnet run --project . -- setup   # create dbo.Heartbeats via the write listener
dotnet run --project . -- burst   # 30 seconds of 2 Hz writes — run this while failing over in another shell
dotnet run --project . -- read    # show last 15 heartbeat rows and the server they landed on
```
