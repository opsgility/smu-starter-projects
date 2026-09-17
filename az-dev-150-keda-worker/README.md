# az-dev-150-keda-worker

.NET 10 Service Bus queue consumer for the KEDA autoscale demo.

## Env

- `SB_NAMESPACE` — Service Bus FQDN (e.g. `anchorline-sb-xxx.servicebus.windows.net`)
- `SB_QUEUE`     — default `orders`

## Build

```
dotnet publish /t:PublishContainer -c Release
```

Uses `DefaultAzureCredential` so it works with:
- Local: `az login`
- Container Apps: user-assigned MI attached to the app
