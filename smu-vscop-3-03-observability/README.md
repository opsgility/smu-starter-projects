# SMU-VSCOP-3 Lesson 6 starter — Halcyon Adventure API (observability snapshot)

A snapshot of `Halcyon.Adventure.Api` at the state Lesson 4 ends on. Opening
this folder in Visual Studio 2026 gives Dana Reyes a working .NET 10 minimal
API with:

- Versioned Products CRUD (`/v1/products`, `/v2/products`) scaffolded against
  the shape of `AdventureWorks.Production.Product`.
- Built-in `AddValidation()` with DataAnnotations on `CreateProductRequest` and
  `UpdateProductRequest`, plus an `IValidatableObject` cross-field rule
  enforcing Halcyon's 15% price-vs-cost margin policy.
- A custom `HalcyonProblemDetailsService` that stamps every 4xx and 5xx with a
  trace id and a Halcyon problem-type URI.
- One comparison endpoint, `POST /v1/products/create-with-fluent-validation`,
  that routes through FluentValidation so the student can diff the two paths.
- A pre-staged `CorrelationIdMiddleware` (reads/mints `X-Correlation-Id`, pushes
  onto `HttpContext.Items["HalcyonCorrelationId"]` + an `ILogger` scope, echoes
  on the response via `Response.OnStarting`) and the `UseCorrelationId()`
  extension — wired first in the pipeline.
- Serilog console sink wired via `UseSerilog`; every log line carries the
  correlation id and (on write endpoints) the business-id scope.
- xUnit integration tests covering the happy path, the problem-details 400,
  and the margin rule — all three pass out-of-the-box.
- One `[Fact(Skip="…")]` test — `PostProduct_LoggerScopeIncludesProductId` —
  that Lesson 6 Exercise 4 unlocks to surface a deliberately-broken scope key
  (the Create handler attaches `"Productid"` instead of `"ProductId"`). The
  @debugger specialized agent walks the student through finding the typo at
  runtime.

Lesson 6 adds rate-limiting policies and an NBomber load-test suite on top of
this baseline.

## Scenario

**Halcyon Insurance** acquired Adventure Works Cycles last quarter. **Dana
Reyes** (senior C# developer, Halcyon) is the tech lead on the modernization
effort to lift Adventure Works onto Halcyon's .NET 10 stack. Director
**Christopher Jones** owns the program; peer tech lead **Marcus Kim** reviews
the API work; Adventure Works' legacy app SME **Michael Johnston** owns the
schema questions.

The `Halcyon.Adventure.Api` project is the backing service every downstream
course in this skill path consumes (Sales Portal, Analytics, ETL, Modernize).

## Files

```
smu-vscop-3-03-observability/
  Halcyon.Adventure.Api.sln              # VS 2026 solution — open this.
  README.md
  .gitignore
  docs/
    openapi-contract.md                  # OpenAPI 3.1 + Halcyon error-envelope notes.
  .github/
    copilot-instructions.md              # Repo grounding file — Copilot reads this.
  src/
    Halcyon.Adventure.Api/
      Halcyon.Adventure.Api.csproj
      Program.cs                         # Validation + ProblemDetails + Serilog + versioning + UseCorrelationId
      appsettings.json                   # Serilog config
      appsettings.Development.json
      Properties/launchSettings.json
      Infrastructure/
        HalcyonProblemDetailsService.cs  # Custom IProblemDetailsService w/ trace id.
      Middleware/
        CorrelationIdMiddleware.cs       # Pre-staged. Exercise 2 reviews with Agent mode.
      Products/
        Product.cs                       # AdventureWorks product shape.
        CreateProductRequest.cs          # DataAnnotations + IValidatableObject margin rule.
        UpdateProductRequest.cs          # Same shape for PUT.
        ProductsEndpoints.cs             # List/Get/Create/Update/Delete on v1 + v2.
                                         # Create handler ships with a deliberately-broken
                                         # scope key ("Productid") that Exercise 4 fixes.
        IProductRepository.cs
        ProductRepository.cs             # In-memory store seeded with 4 AW bikes.
        Comparison/
          FluentCreateProductRequest.cs
          FluentUpdateProductRequestValidator.cs
          FluentValidationComparisonEndpoint.cs
  tests/
    Halcyon.Adventure.Api.Tests/
      Halcyon.Adventure.Api.Tests.csproj
      ProductsEndpointsTests.cs          # 3 passing tests + 1 [Skip] that Exercise 4 unlocks.
```

## How to run

1. Open `Halcyon.Adventure.Api.sln` in Visual Studio 2026.
2. Press `F5` with the `https` profile selected. The API comes up on
   `https://localhost:7080`.
3. In a browser, open `https://localhost:7080/openapi/v1.json` to see the
   OpenAPI 3.1 document (Development only).
4. Hit `GET https://localhost:7080/v1/products` to see the four seeded bikes.
5. Inspect the response headers — every response carries `X-Correlation-Id`
   (either the one you sent, or a GUID the middleware minted).

To run the test suite from the command line:

```
dotnet test
```

All three unskipped tests pass against this baseline. The
`PostProduct_LoggerScopeIncludesProductId` test stays skipped until Exercise 4.

## What Lesson 6 lands on top of this starter

- **Exercise 2** — Review the pre-staged `CorrelationIdMiddleware` with
  Copilot Agent mode; add structured business-id `ILogger` scopes to every
  write handler (the pre-staged scopes serve as the baseline Copilot iterates
  against).
- **Exercise 3** — Add a global fixed-window rate-limit policy and a per-endpoint
  sliding-window policy on `POST /products`, chained via
  `.RequireRateLimiting("writes-per-user")`.
- **Exercise 4** — Unskip `PostProduct_LoggerScopeIncludesProductId`, run under
  @debugger to find the `"Productid"` typo on the Create handler's scope,
  land the one-line fix via Edit mode.
- **Exercise 5** — Scaffold an NBomber load-test project that proves both
  rate-limit policies hold under burst, then run the Git-agent review on the
  staged commit before opening the PR.

## Authentication

Local only. The API trusts the ambient dev-certificate for TLS. No cloud
credentials are needed to drive this starter — Lesson 6 never leaves the VM.

## Notes

- Every endpoint returns `TypedResults.*`. Do not propose `Results.*` elsewhere
  in the codebase; the `.github/copilot-instructions.md` grounds Copilot on
  the Halcyon convention.
- The in-memory `ProductRepository` is intentional. Course 4 (EF Core) is
  where the real `AdventureWorksDbContext` lands behind the same
  `IProductRepository` interface. Keeping it in-memory for Course 3 keeps the
  lab's attention on API shape, not EF plumbing.
- The margin floor (`15%`) lives on `CreateProductRequest.MinimumMarginPercent`
  as a constant. Both the built-in-validation path and the FluentValidation
  comparison path read it, so changing it in one place changes both.
- The `tests/` project uses `WebApplicationFactory<Program>`; the `Program`
  class is `public partial` at the bottom of `Program.cs` for that reason.
- The deliberately-broken scope key on `ProductsEndpoints.Create` is the one
  thing in this starter that is intentionally wrong. Exercise 4 is built
  around finding it; don't fix it ahead of the lab.
