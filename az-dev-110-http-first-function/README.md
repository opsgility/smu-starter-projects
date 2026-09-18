# az-dev-110-http-first-function

Anchorline Outdoors' first Azure Function — a friendly HTTP endpoint that greets a caller.

## What's inside

- `Program.cs` — isolated worker bootstrap with App Insights wiring
- `HelloAnchorline.cs` — `HttpTrigger` on `GET|POST /api/hello/{name?}`
- `host.json` — extension bundle v4, App Insights sampling
- `local.settings.json.example` — copy to `local.settings.json` for local dev

## Run locally

```bash
# Terminal 1
azurite --silent --location .azurite &

# Terminal 2
cp local.settings.json.example local.settings.json
func start

# Terminal 3
curl http://localhost:7071/api/hello/Michael
```

## Deploy to Azure

The paired ARM template provisions a Flex Consumption Function App running .NET 10 isolated on Linux with managed identity for storage. Publish with `az functionapp deployment source config-zip` after zipping the `bin/publish` output.
