# Halcyon.Adventure.Api — Copilot instructions

Halcyon Insurance acquired Adventure Works Cycles last quarter. The modernization program is lifting the Adventure Works apps onto Halcyon's .NET 10 stack. This project is `Halcyon.Adventure.Api`, the single Products API that every downstream Halcyon-Adventure Works app will consume.

Follow these conventions when Copilot proposes code in this repo.

## Framework and surface

- Target framework is **.NET 10**. Do not propose .NET 8 or .NET 9 patterns.
- API surface is **ASP.NET Core minimal APIs**. Controllers are reserved for the two edge cases Marcus signed off on (SignalR hubs; a legacy webhook adapter). Do not introduce new controllers without a Christopher-level approval.
- Every endpoint returns `TypedResults.*` wrapped in `Results<T1, T2, ...>` where more than one status code is possible. Do not use `Results.*` — the OpenAPI document relies on `TypedResults` for the response shape.
- OpenAPI document shape is **OpenAPI 3.1**. It is served from `/openapi/v1.yaml` and `/openapi/v1.json`. Do not re-introduce Swashbuckle; the project uses the built-in `Microsoft.AspNetCore.OpenApi` package.

## Versioning

- URL + header versioning via `Asp.Versioning.Http`. Routes live under `/api/v{apiVersion:apiVersion}` and `Api-Version: 1.0` is accepted as a header alternative.
- Default version is `1.0`. Unversioned requests fall through to `v1`.
- When Copilot proposes a new endpoint, place it inside the versioned `MapGroup` and call `.HasApiVersion(new ApiVersion(major, minor))` on the sub-group.

## Data access

- `AdventureWorksContext` is a narrow DbContext that only projects the slice of `AdventureWorks.Production` that this API serves. Do not add `DbSet<T>` entries for unrelated schemas; EF Core 10 scaffolding for the broader schema lives in Course 4's `Halcyon.Adventure.Data` project.
- Reads use `.AsNoTracking()`. Writes go through the tracked path.
- SQL Server 2025 Developer Edition is baked into VM type 11; the local connection string is in `appsettings.json`.

## Request / response records

- Request payloads are `record` types in `Products/`. Use records (not classes) for request + response DTOs so .NET 10 minimal-API validation (added in Lesson 4) picks them up automatically.
- Keep DTO records separate from EF entities. Never return `Product` directly; always project to `ProductDto`.
- Do not add validation attributes yet. The next pull request (Lesson 4) wires `AddValidation()` + DataAnnotations + an `IValidatableObject` cross-field rule + a custom `IProblemDetailsService`. Copilot should flag the absence of validation as a known follow-up rather than adding it ad-hoc.

## Error responses (follow-up)

- Today the API returns `400 Bad Request` with no body on bind failures. Christopher flagged this at the Lesson 2 PR review — the next change wires RFC 7807 problem-details with a Halcyon correlation / trace id in every error response.
- When Copilot sees `return Results.BadRequest(...)` in a proposal, prefer suggesting `TypedResults.ValidationProblem(...)` instead.

## Testing

- xUnit is the house test framework. Tests live under a sibling `tests/Halcyon.Adventure.Api.Tests` project that lands in Lesson 4 — do not scaffold a separate test framework (NUnit, MSTest) when asked for tests.

## Naming

- Namespaces mirror the folder path under `Halcyon.Adventure.Api`.
- Minimal-API modules are `public static class <Area>Api` with a `Map<Area>Api` extension method on `RouteGroupBuilder`.
- Endpoint names use `WithName("<VerbNoun>")` — `ListProducts`, `GetProduct`, `CreateProduct`, `UpdateProduct`, `DeleteProduct`.

## What NOT to propose

- No AutoMapper. Hand-written `ToDto(...)` is the house style.
- No MediatR. The team evaluated it in Q3 and rejected the dependency.
- No in-memory `List<T>` fakes outside tests. The API talks to SQL Server.
- No `async void`.
