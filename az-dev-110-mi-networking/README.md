# az-dev-110-mi-networking

Anchorline Functions wired to Blob Storage and Key Vault via `DefaultAzureCredential` — no connection strings, no secrets. `/whoami` reports the token payload, `/blobs` lists the container, `/secret/{name}` reads a KV secret.
