# az-dev-130-resiliency

Demonstrate EF Core's `EnableRetryOnFailure` handling of transient Azure SQL faults by injecting them from inside the process.

## Env

- `ANCHORLINE_SQL_SERVER`
- `ANCHORLINE_SQL_DATABASE` = `AnchorlineOrders`

## Modes

```
dotnet run --project . -- setup    # create Pings and Counters tables + seed counter
dotnet run --project . -- noretry  # WITHOUT EnableRetryOnFailure; 2 transient injections -> app-visible failure
dotnet run --project . -- retry    # WITH EnableRetryOnFailure; 3 transient injections -> transparent recovery
dotnet run --project . -- tx       # WITH EnableRetryOnFailure inside CreateExecutionStrategy; multi-command tx
```

## What `TransientInjector` does

It is an EF Core `IDbCommandInterceptor` that throws a synthesized `SqlException` with error number 40613 (Database currently unavailable) the first N times a command executes. `SqlAzureRetryingExecutionStrategy` recognizes 40613 as transient and retries on the next attempt — which succeeds because the injector has already burned its N failures.
