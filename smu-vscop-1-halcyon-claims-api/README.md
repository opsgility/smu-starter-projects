# Halcyon Claims API

A sample ASP.NET Core Web API for the fictional Halcyon Insurance claims-processing system. Used as the starter project in the "Modern Enterprise App Development with VS 2026 + Copilot" course.

## Run locally

```bash
dotnet build
dotnet run --project HalcyonClaimsApi
```

The API listens on `http://localhost:5000` by default and exposes:

- `GET /api/claims` — list all claims
- `GET /api/claims/{id}` — fetch a claim
- `POST /api/claims` — submit a new claim
- `GET /api/policies` — list all policies
- `GET /api/policies/{id}` — fetch a policy
- `POST /api/policies` — register a new policy

## Project layout

- `HalcyonClaimsApi/` — Web API project
- `HalcyonClaimsApi.Tests/` — xUnit test project
- `docs/` — architecture + API contract reference material
