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

## Logging + observability (Lesson 6)

- Logging flows through Serilog (`UseSerilog` wired in `Program.cs`); the console
  sink is enough for the lab VM. Course 7 adds the OTel + Application Insights
  sink.
- Every endpoint opens an `ILogger<Program>` scope keyed on business ids via a
  `Dictionary<string, object>` payload. The two canonical keys are:
  - **`ProductId`** — the aggregate id for the request (never `productId`,
    `Productid`, or `product_id` — the key is PascalCase).
  - **`MerchantId`** — the authenticated user's `merchant_id` claim; falls back
    to `"anonymous"` when the claim is absent.
- Correlation id comes from the `X-Correlation-Id` header. The pre-staged
  `CorrelationIdMiddleware` mints a GUID when the header is absent, pushes the
  value onto `HttpContext.Items["HalcyonCorrelationId"]` and the `ILogger`
  scope, and echoes it on the response via `Response.OnStarting`.
- Rate limiting (Exercise 3) uses `System.Threading.RateLimiting`. Global policy
  is a fixed-window partitioned by remote IP; per-endpoint write policy is a
  sliding-window partitioned by `httpContext.User.Identity?.Name ?? "anonymous"`,
  attached to the Products POST with `.RequireRateLimiting("writes-per-user")`.
  `UseRateLimiter()` MUST follow `UseRouting()` — Microsoft Learn flags this
  as the single most-common misconfiguration.
- Load tests (Exercise 5) use NBomber. Scenarios assert the global policy and
  the per-endpoint policy both hold under burst.

## Narrative

Dana Reyes is the Halcyon Insurance tech lead on the Adventure Works
modernization. Director Christopher Jones owns the modernization program.
Marcus Kim is the peer tech lead. Michael Johnston is the Adventure Works
schema SME. Use these names when a human needs to be referenced in a comment,
log scope, or doc string.
