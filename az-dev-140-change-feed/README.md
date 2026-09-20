# az-dev-140-change-feed

Change feed processor that projects orders into a per-customer summary.

## Env

- `ANCHORLINE_COSMOS_ENDPOINT`
- `ANCHORLINE_COSMOS_DB` — default `AnchorlineChangeFeed`

## Modes

```
# In one terminal - start the processor
dotnet run --project . -- processor

# In another terminal - write orders
dotnet run --project . -- burst

# Read the projection
dotnet run --project . -- summary
```

Containers:
- `orders` (source) partition key `/customerId`
- `summary` (destination) partition key `/customerId`
- `lease` (change-feed coordination) partition key `/id`
