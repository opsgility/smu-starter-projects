# az-dev-150-mi-app

Single ACA microservice that calls Key Vault, Cosmos, and Storage using ONE User-Assigned MI.

## Config

- `MI_CLIENT_ID` — user-assigned MI client id (from ARM output)
- `KV_NAME` — Key Vault name
- `STORAGE_ACCOUNT` — storage account name
- `COSMOS_ENDPOINT` — Cosmos endpoint URL

## Endpoints

- `GET /kv/{name}` — read a secret via MI
- `GET /storage/list` — list containers via MI
- `GET /cosmos/dbs` — list databases via MI
