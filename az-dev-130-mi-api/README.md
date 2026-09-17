# az-dev-130-mi-api

ASP.NET Core minimal API that connects to Azure SQL Database via Managed Identity — no username, no password.

## Config

- `Anchorline:SqlServer` — SQL server FQDN.
- `Anchorline:SqlDatabase` — default `AnchorlineOrders`.
- `Anchorline:MiClientId` — for a User-Assigned MI; leave empty for System-Assigned.

## Endpoints

- `GET /` — health probe.
- `GET /whoami` — opens a SQL connection using an MI-issued token, then prints:
  - `entraIdentity` (from `SUSER_SNAME()`)
  - `databaseUser`  (from `USER_NAME()`)
  - `isDbReader` / `isDbWriter`
  - server time

## Local run

Sign in with `az login`, export the two env vars, then:

```
dotnet run --project .
```
