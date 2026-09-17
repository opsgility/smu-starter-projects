# az-dev-140-data-modeling

Load the same domain in two Cosmos DB models and measure the RU cost difference.

- **orders_embed** — order doc contains its own line items nested inline.
- **orders_ref** + **lines_ref** — order doc holds only `lineIds`; the physical line records live in a second container.

## Env

- `ANCHORLINE_COSMOS_ENDPOINT`
- `ANCHORLINE_COSMOS_DB` — default `AnchorlineModeling`

## Modes

```
dotnet run --project . -- seed-embed    # 5000 orders, each with embedded lines
dotnet run --project . -- seed-ref      # 5000 orders + all their lines separately
dotnet run --project . -- query-embed   # "last 10 orders for cus-0007" via embed model
dotnet run --project . -- query-ref     # same access pattern via reference model (N+1 reads)
```

Every mode prints the total RequestCharge — that is the number you compare.
