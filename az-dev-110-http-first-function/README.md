# az-dev-110-http-first-function

Anchorline Outdoors' first Azure Function — a friendly HTTP endpoint that greets a caller by name.

## What's inside

- `Program.cs` — isolated worker bootstrap with App Insights wiring
- `HelloAnchorline.cs` — `HttpTrigger` on `GET|POST /api/hello/{name?}` returning `Hello, {name}. Anchorline Outdoors welcomes you.`
- `host.json` — extension bundle v4, App Insights sampling
- `local.settings.json.example` — copy to `local.settings.json` for local dev

## Run locally

```bash
# Terminal 1 — start Azurite (Storage emulator)
azurite --silent --location .azurite &

# Terminal 2 — build and run the Function host
cp local.settings.json.example local.settings.json
dotnet build
func start

# Terminal 3 — invoke
curl http://localhost:7071/api/hello/Michael
# → Hello, Michael. Anchorline Outdoors welcomes you.
```

## Deploy to Azure

The AZ-DEV-110 M1L2 lab exercises create the target Flex Consumption Function App with `az functionapp create` (no ARM template — see the exercise pane for the exact CLI). The Function App is provisioned with an MI-authenticated `app-package` blob container as its deployment source, so `az functionapp deployment source config-zip` uploads the zip through the app's managed identity — no storage keys and no `WEBSITE_RUN_FROM_PACKAGE` app setting are needed.

```bash
dotnet publish -c Release -o out
cd out && zip -r ../pkg.zip . && cd ..
az functionapp deployment source config-zip -g $RG -n $APP --src pkg.zip
```
