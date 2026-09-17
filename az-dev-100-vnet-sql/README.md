# AZ-DEV-100 · Module 6 Lab — VNet integration + private endpoints on SQL

Extends the storefront with a `/products` endpoint that queries Azure SQL over a **private endpoint** — the app reads via the public hostname, DNS resolves to a private IP inside the customer VNet, TCP goes over the Azure backbone. Public SQL access is disabled entirely.

## Endpoints

- `/health` — process health.
- `/version` — build tag + slot name.
- `/products` — SELECTs from the SQL Products table using the connection string in `Anchorline:SqlConnection`. Returns the first 10 rows.
- `/dns` — reports what DNS resolves for the SQL hostname. On the deployed app you should see a private IP (10.x.x.x); locally you'll see the public IP.

## Connection

The `Anchorline:SqlConnection` app setting is populated via a Key Vault reference on the deployed Web App. The KV holds the connection string (SQL Auth for lab simplicity; Module 7 replaces this with Managed Identity + contained DB users).

## Notes

- **Private DNS zone** must be linked to the Web App's VNet. The ARM template does this.
- **Public network access** on SQL is set to `Disabled` — direct-to-SQL from your laptop returns "Cannot connect".
- **Regional VNet integration** is set on the plan, delegated to `Microsoft.Web/serverFarms`.
