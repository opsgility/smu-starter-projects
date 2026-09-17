# az-dev-170-mi-fanout

One .NET service reaches Storage, Key Vault, Azure SQL, Cosmos, and Service Bus via a single User-Assigned MI.

## Env
- `UAMI_CLIENT_ID` (optional: pin to this UAMI's client id)
- `STORAGE_ACCOUNT`, `KV_NAME`, `SQL_SERVER`, `SQL_DB`, `COSMOS_ENDPOINT`, `SB_NAMESPACE`
