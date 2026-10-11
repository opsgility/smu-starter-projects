# Halcyon Adventure API — Copilot grounding

You are helping Dana Reyes on `Halcyon.Adventure.Api`. Keep every response
grounded in these team conventions.

## Platform

- .NET 10, minimal APIs only. Controllers are out of scope on this repo.
- `TypedResults` returns from every endpoint. Never `Results.Ok(...)`; always
  `TypedResults.Ok(...)`.
- URL + header versioning via `Asp.Versioning.Http`. New endpoints go on a
  versioned route group (`/v{version:apiVersion}/...`), never at the root.
- OpenAPI 3.1 is on by default. Do not add Swashbuckle.

## Validation

- Primary path is .NET 10 built-in `AddValidation()` plus `[DataAnnotations]`
  attributes and `IValidatableObject` for cross-field rules.
- FluentValidation is kept only on the comparison endpoint. Do not propose new
  FluentValidation rules anywhere else without first justifying why
  built-in validation does not fit.
- Error responses must flow through `IProblemDetailsService`. Never write a
  `return Results.BadRequest("string")`.

## Logging + observability (introduced in Lesson 6)

- Every endpoint opens an `ILogger<T>` scope keyed on business ids:
  `productId`, `correlationId`, and `operation`.
- Correlation id comes from the `X-Correlation-Id` header (middleware mints a
  GUID when the header is absent) and is echoed on every response.
- Rate limiting uses `System.Threading.RateLimiting`. Global policy is a fixed
  window; per-endpoint write policies are sliding window partitioned on the
  authenticated user id.

## Narrative

Dana Reyes is the Halcyon Insurance tech lead on the Adventure Works
modernization. Director Christopher Jones owns the modernization program.
Marcus Kim is the peer tech lead. Michael Johnston is the Adventure Works
schema SME. Use these names when a human needs to be referenced in a comment,
log scope, or doc string.
