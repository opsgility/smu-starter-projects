# Halcyon.Adventure.Api — Copilot instructions

Halcyon Insurance acquired Adventure Works Cycles last quarter. The modernization program is lifting the Adventure Works apps onto Halcyon's .NET 10 stack. This project is `Halcyon.Adventure.Api`, the single Products API that every downstream Halcyon-Adventure Works app will consume.

Follow these conventions when Copilot proposes code in this repo.

## Solution layout

- `src/Halcyon.Adventure.Api` — ASP.NET Core 10 minimal-API host.
- `src/Halcyon.Adventure.Shared` — contract records (request / response DTOs). Both the API and any future client project reference these.
- `tests/Halcyon.Adventure.Api.Tests` — xUnit integration tests driven by `WebApplicationFactory<Program>`.

Keep request / response records in `Halcyon.Adventure.Shared`. Infrastructure (middleware, repositories, EF entities) stays in `Halcyon.Adventure.Api`. Never duplicate a record across the two projects.

## Framework and surface

- Target framework is **.NET 10**. Do not propose .NET 8 or .NET 9 patterns.
- API surface is **ASP.NET Core minimal APIs**. Controllers are reserved for the two edge cases Marcus signed off on (SignalR hubs; a legacy webhook adapter).
- Every endpoint returns `TypedResults.*` wrapped in `Results<T1, T2, ...>` where more than one status code is possible. Do not use `Results.*` — the OpenAPI 3.1 document relies on `TypedResults` for the response shape.
- OpenAPI document shape is **OpenAPI 3.1**, served from `/openapi/v1.yaml` and `/openapi/v1.json` via `Microsoft.AspNetCore.OpenApi`. Do not re-introduce Swashbuckle.

## Data access

- The starter uses an in-memory `IProductRepository` for lab scope. Course 4 swaps the repository for an EF Core 10 scaffold against `AdventureWorks.Production.Product`.
- Keep the repository interface narrow — `GetAll / Get / Add / Update / Delete` only.

## Request / response records

- Payloads live in `src/Halcyon.Adventure.Shared/Products/`. Use `record` types so .NET 10 minimal-API validation (added in Exercise 2) picks them up automatically.
- Keep DTO records separate from the EF-ready `Product` entity in the Api project. Never return `Product` directly; always project to `ProductDto`.
- Validation attributes are deliberately absent in the starter. Exercise 2 wires `AddValidation()` + DataAnnotations, Exercise 3 lands the `IValidatableObject` margin rule.

## Error responses

- The starter calls `builder.Services.AddProblemDetails()` with no customization. Exercise 4 replaces that with the delegate overload that threads `halcyonTraceId` (from `CorrelationIdMiddleware`) onto every problem-details body.
- When Copilot sees `return Results.BadRequest(...)` in a proposal, prefer suggesting `TypedResults.ValidationProblem(...)` instead so the response routes through `IProblemDetailsService`.

## Correlation + middleware

- `CorrelationIdMiddleware` is already present at `src/Halcyon.Adventure.Api/Middleware/CorrelationIdMiddleware.cs`. It reads `X-Correlation-Id`, mints a GUID if the header is absent, stores it in `HttpContext.Items["HalcyonCorrelationId"]`, pushes it onto the `ILogger` scope, and echoes it on the response via `Response.OnStarting`.
- The middleware is wired first in the pipeline (`app.UseMiddleware<CorrelationIdMiddleware>()` before any endpoint map). Do not move it later.

## Testing

- xUnit is the house framework. Integration tests use `WebApplicationFactory<Program>` and the baseline suite in `tests/Halcyon.Adventure.Api.Tests/Products/ProductsEndpointsTests.cs`.
- One test class per endpoint group — `ProductsEndpointsTests`, `BatchImportValidationTests` (added in Exercise 5), `ProblemDetailsTraceIdTests` (added in Exercise 4).
- Reuse the existing fixture via `IClassFixture<WebApplicationFactory<Program>>`. Do not spin up a second host.

## Naming

- Namespaces mirror the folder path (`Halcyon.Adventure.Api.Products`, `Halcyon.Adventure.Shared.Products`).
- Minimal-API modules are `public static class <Area>Endpoints` with a `Map<Area>Endpoints` extension method on `IEndpointRouteBuilder`.
- Endpoint names use `WithName("<VerbNoun>")` — `ListProducts`, `GetProduct`, `CreateProduct`, `UpdateProduct`, `DeleteProduct`, `BatchImportProducts`.

## What NOT to propose

- No AutoMapper. Hand-written `ToDto(...)` is the house style.
- No MediatR. The team evaluated it in Q3 and rejected the dependency.
- No `async void`.
- No validation attributes on the batch-import record — Exercise 5 switches the batch-import endpoint to FluentValidation specifically because its rules (duplicate-SKU detection, batch-size limits) fit chaining better than attributes.
