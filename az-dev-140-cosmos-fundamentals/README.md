# az-dev-140-cosmos-fundamentals

Point-CRUD + query starter for the Anchorline `products` container. Measures RU cost per operation.

## Env

- `ANCHORLINE_COSMOS_ENDPOINT` — e.g. `https://anchorline-cosmos-abc.documents.azure.com:443/`
- `ANCHORLINE_COSMOS_DB` — default `AnchorlineCatalog`
- `ANCHORLINE_COSMOS_CONTAINER` — default `products`

## Modes

```
dotnet run --project . -- seed    # upsert 6 products; print RU per doc
dotnet run --project . -- read    # ReadItemAsync (point read); ~1 RU
dotnet run --project . -- query   # SQL query within one partition; several RU
dotnet run --project . -- upsert  # Overwrite an existing doc
dotnet run --project . -- delete  # Delete a doc
```

Every operation prints the exact `RequestCharge` from the SDK response.
