# az-dev-130-sql-connect

Connect to Azure SQL Database from .NET 10 using a Managed Identity access token — no username, no password.

## Environment variables

- `ANCHORLINE_SQL_SERVER` — fully-qualified server (e.g. `anchorline-sql-<suffix>.database.windows.net`)
- `ANCHORLINE_SQL_DATABASE` — default `AnchorlineOrders`

## Run

```
dotnet run --project .
```

The program uses `DefaultAzureCredential` to acquire a token for `https://database.windows.net/.default` and attaches it to `SqlConnection.AccessToken`. It then runs a small metadata query showing the Entra identity, the database name, the SQL server version, and the server time.
