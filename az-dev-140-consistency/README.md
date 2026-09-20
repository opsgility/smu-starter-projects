# az-dev-140-consistency

Benchmark all five consistency levels against the same read/write pattern.

## Env

- `ANCHORLINE_COSMOS_ENDPOINT`
- `ANCHORLINE_COSMOS_DB` — default `AnchorlineConsistency`

## Modes

```
dotnet run --project . -- bench       # measure all five levels
dotnet run --project . -- override    # per-request override demo (Session default -> Eventual on one read)
```

Note: the account default consistency must be at or above the level being tested. Strong is not testable on multi-region-write accounts. Bounded Staleness needs the account provisioned for it.
