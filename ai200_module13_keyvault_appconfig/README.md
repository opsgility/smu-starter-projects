# ai200_module13_keyvault_appconfig — Key Vault + App Configuration

Starter project for **AI-200 Module 13**. You wire a FastAPI app to read
secrets from Key Vault (via managed identity) and settings + feature
flags from Azure App Configuration. App Config also resolves a secret
into a Key Vault reference.

## What's already scaffolded

| Path | Purpose |
| --- | --- |
| `lib/secrets.py` | TODOs in `get_secret_client` (4a) and `get_secret` (4b) |
| `lib/config.py` | TODOs in `get_config` (6a) and `feature_enabled` (6b) |
| `app/main.py` | FastAPI app exposing `/config` and `/secret-length` |
| `scripts/smoke_test.py` | Runs after Step 6 |
