# az-dev-150-first-app

A .NET 10 minimal-API microservice packaged as a chiseled Ubuntu container using the .NET SDK's built-in container support (no Dockerfile).

## Endpoints

- `GET /`        — app + version + hostname
- `GET /health`  — liveness probe target
- `GET /whoami`  — reads Container Apps env vars (revision, replica name)

## Build a container

```bash
dotnet publish /t:PublishContainer -p:ContainerRepository=anchorline-first-app -c Release
```

Or to a specific tag:

```bash
dotnet publish /t:PublishContainer \
    -p:ContainerRepository=anchorline-first-app \
    -p:ContainerImageTag=v1 \
    -c Release
```

Push to ACR:

```bash
docker tag anchorline-first-app:v1 <acr>.azurecr.io/anchorline-first-app:v1
docker push <acr>.azurecr.io/anchorline-first-app:v1
```
