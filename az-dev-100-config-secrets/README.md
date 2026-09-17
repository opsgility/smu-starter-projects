# AZ-DEV-100 · Module 2 Lab — Wire Key Vault and App Configuration into an ASP.NET Core app

Extends the Module 1 Anchorline Outdoors storefront scaffold with the two configuration mechanisms every real Anchorline workload needs: a Stripe-lookalike API key resolved from Key Vault via a KV reference, and a `Beta.FallDiscount` feature flag centralized in Azure App Configuration with sentinel-key live refresh.

## Scenario

Anchorline's security team flagged the hardcoded Stripe API key that shipped in Module 1's baseline. Marketing separately asked for a fall-discount toggle they can flip without waiting for a deploy. This starter is the extended storefront that reads the Stripe key from Key Vault (via `IConfiguration` — no code change from a plain app setting) and the fall-discount flag from Azure App Configuration (via `Microsoft.FeatureManagement`).

## Files

```
az-dev-100-config-secrets/
  README.md
  .gitignore
  Project.csproj                # net10.0 + AzureAppConfiguration + FeatureManagement + Azure.Identity
  Program.cs                    # Minimal API — /health, /version, /stripe-key, /discount, /
  appsettings.json              # Base + Anchorline:StripeApiKey fallback
  appsettings.Development.json  # Dev override — Information log level
  Properties/
    launchSettings.json         # Local dev profile
```

## How to run (locally in the lab VS Code container)

The container ships both .NET 9 (STS) and .NET 10 (LTS) SDKs — the .csproj targets `net10.0`. First-time `dotnet run` will restore the NuGet packages listed in `Project.csproj` (Microsoft.Extensions.Configuration.AzureAppConfiguration, Microsoft.FeatureManagement, Microsoft.FeatureManagement.AspNetCore, Azure.Identity); this takes ~30–60 seconds the first time and is cached thereafter. Do not run `dotnet restore` explicitly — the restore is implicit in `dotnet run` / `dotnet build`.

Run the app:

```bash
dotnet run --project Project.csproj
```

Then in a second terminal:

```bash
curl http://localhost:5000/health
curl http://localhost:5000/version
curl http://localhost:5000/stripe-key
curl http://localhost:5000/discount
```

Locally (no App Config endpoint set), `/discount` returns `enabled: false` — the feature flag defaults to disabled when the App Configuration provider isn't wired.

## How to deploy to Azure App Service

The lab's ARM template has already pre-provisioned:

- A resource group + Standard S1 App Service Plan (Linux) + Web App with system-assigned managed identity.
- A Key Vault (RBAC mode) with a seeded `StripeApiKey` secret. The Web App's MI has `Key Vault Secrets User` on the vault.
- An Azure App Configuration store (Free tier) with a seeded `Anchorline:Sentinel` key and a `Beta.FallDiscount` feature flag (disabled by default). The Web App's MI has `App Configuration Data Reader` on the store.
- Two App Settings on the Web App: `Anchorline__StripeApiKey` with a Key Vault reference to the seeded secret, and `AZ_DEV_100_APPCONFIG_ENDPOINT` with the App Config store's endpoint.

Deploy the code:

```bash
dotnet publish --configuration Release --output ./publish
```

```bash
cd publish && zip -r ../app.zip . && cd ..
```

```bash
az webapp deploy --resource-group $RG --name $WEBAPP --src-path ./app.zip --type zip
```

## Authentication

- **Key Vault reference resolution** — happens at App Service platform layer using the Web App's system-assigned managed identity (no code path in this starter).
- **App Configuration + Feature Management** — happens in `Program.cs` using `DefaultAzureCredential()`. On App Service the credential chain resolves to the Web App's system-assigned MI. Locally it resolves to your `az login` account.

No connection strings, no API keys in the code or config. If you see `Anchorline__StripeApiKey` show up as the literal `@Microsoft.KeyVault(...)` string in the `/stripe-key` response, the KV reference didn't resolve — check the four requirements in Module 2's teaching lesson (MI assigned, MI has KV role, secret exists, Web App restarted after setting added).

## Notes

- **`AZ_DEV_100_APPCONFIG_ENDPOINT`** is what wires the App Configuration provider. When it's set (App Service), Program.cs adds `AzureAppConfiguration` to the IConfiguration chain and enables `Microsoft.FeatureManagement`. When it's not set (local dev without the env var), Program.cs skips App Config entirely and the feature flag returns `false`.
- **Sentinel refresh** — the App Config provider is configured with `refresh.Register("Anchorline:Sentinel", refreshAll: true)` and a 30-second cache expiration. Bumping the sentinel value in App Config triggers all connected app instances to re-read their selected keys and flags within the cache window — no restart needed.
- **`Beta.FallDiscount`** — read via `IFeatureManager.IsEnabledAsync("Beta.FallDiscount")` in the `/discount` endpoint. Wire it up as a `[FeatureGate]` attribute on a controller in a later module if the app grows into MVC.
- **KV reference vs KV provider** — this starter uses the App Service **KV reference** mechanism (App Setting value = `@Microsoft.KeyVault(SecretUri=...)`), NOT the ASP.NET Core Key Vault configuration provider (`builder.Configuration.AddAzureKeyVault(...)`). Both work; KV reference is simpler and doesn't require a code change to add/remove secrets.
