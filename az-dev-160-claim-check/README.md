# az-dev-160-claim-check

Claim-check pattern for large payloads over Service Bus.

## Env
- `SB_NAMESPACE`, `SB_QUEUE`
- `STORAGE_ACCOUNT`, `STORAGE_CONTAINER`

## Modes
```
dotnet run -- upload 100    # upload 100 MB blob + SB claim-check
dotnet run -- process       # consume + fetch blob
```
