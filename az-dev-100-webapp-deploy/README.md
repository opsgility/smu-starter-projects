# AZ-DEV-100 · Module 1 Lab — Provision an App Service Plan and deploy your first ASP.NET Core app

Minimal ASP.NET Core 10 Web API for Anchorline Outdoors' storefront-scaffold work.
Two endpoints out of the box (`/health` and `/version`) so you can prove the app is live and running the version you just deployed.

## Scenario

Anchorline Outdoors is migrating their monolithic storefront off a colocated VM onto Azure App Service. This starter is the first slice — the empty storefront skeleton — that Module 1's hands-on lab deploys to the Standard S1 App Service Plan pre-provisioned for you by the lab's ARM template.

## Files

```
az-dev-100-webapp-deploy/
  README.md
  .gitignore
  Project.csproj                # net10.0 Minimal API — restore already baked into container variant CSharp
  Program.cs                    # Minimal API with /health and /version
  appsettings.json              # Base settings — reads AZ_DEV_100_BUILD_TAG from env for /version response
  appsettings.Development.json  # Dev override — Information log level
  Properties/
    launchSettings.json         # Local dev profile (port 5000)
```

## How to run (locally in the lab VS Code container)

The .NET 10 (LTS) SDK is already installed in the container — no `dotnet restore` needed for this scaffold, but if you want to verify:

```bash
dotnet --list-sdks
```

Run the app on the default local dev port:

```bash
dotnet run --project Project.csproj
```

Then in a second terminal:

```bash
curl http://localhost:5000/health
curl http://localhost:5000/version
```

## How to deploy to Azure App Service

The lab's ARM template has already pre-provisioned a resource group, an S1 App Service Plan (Linux), and an empty Web App with the .NET 10 stack configured. Grab the web app name from the Environment tab and:

```bash
dotnet publish --configuration Release --output ./publish
```

```bash
cd publish && zip -r ../app.zip . && cd ..
```

```bash
az webapp deploy --resource-group $RG --name $WEBAPP --src-path ./app.zip --type zip
```

Then hit the default hostname:

```text
https://<web-app-name>.azurewebsites.net/health
```

## Authentication

None from the app to Azure — this scaffold does not call any Azure data plane. The lab's `az login --use-device-code` flow is for the CLI (deploy + scale) only. Later modules add Managed Identity, Key Vault, SQL, and Cosmos.

## Notes

- **`AZ_DEV_100_BUILD_TAG`** app setting drives what `/version` returns. The ARM template sets it to `v1.0.0-anchorline-storefront-baseline`; override it locally with `export AZ_DEV_100_BUILD_TAG=local-dev` before `dotnet run`.
- **`ASPNETCORE_ENVIRONMENT`** is set to `Production` in App Service by default. Locally, `dotnet run` uses `Development` via `launchSettings.json`.
- **Minimal API vs Controllers** — this scaffold uses the Minimal API style (single `Program.cs`), which is the modern default for new ASP.NET Core 10 web APIs. If your team prefers Controllers, swap in a `Controllers/` folder in a later lesson.
- **.NET 10 target** — the container ships both .NET 9 (STS) and .NET 10 (LTS) SDKs side-by-side, so `TargetFramework=net10.0` restores and builds without extra work. If you pin to `net9.0` for compatibility with a downstream library, the container supports that too.
