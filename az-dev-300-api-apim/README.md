# az-dev-300-api-apim

TaskForge public API (minimal-API .NET 10) + APIM policies (validate-jwt + product-tier rate limits).

## Deploy + import
1. `dotnet publish -c Release -o out && cd out && zip -r ../pkg.zip . && cd .. && az webapp deploy --src-path pkg.zip --type zip`
2. `az apim api import ... --specification-url https://<api>.azurewebsites.net/swagger/v1/swagger.json`
3. Paste `policies/api-scope-inbound.xml` at API scope; product policies at product scope.
