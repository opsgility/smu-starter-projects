# az-dev-140-vector-search

Enable Cosmos DB integrated vector search + run semantic-search queries.

Note: for lab simplicity the "embeddings" are deterministic 8-dim keyword vectors, not real Azure OpenAI embeddings. The API surface is identical; only the embedder function changes.

## Env

- `ANCHORLINE_COSMOS_ENDPOINT`
- `ANCHORLINE_COSMOS_DB` — default `AnchorlineVector`

## Modes

```
dotnet run --project . -- seed              # 8 Anchorline products with mock embeddings
dotnet run --project . -- search warm       # find products semantically close to "warm"
dotnet run --project . -- search shelter    # etc.
dotnet run --project . -- search "warm winter"
```
