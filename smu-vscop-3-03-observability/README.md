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
- xUnit integration tests covering the happy path, the problem-details 400,
  and the margin rule.

Lesson 6 adds correlation-ID middleware, `ILogger<T>` business-id scopes, two
`System.Threading.RateLimiting` policies, and an NBomber load-test suite on top
of this baseline.

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
      Program.cs                         # Validation + ProblemDetails + versioning wiring.
      appsettings.json
      appsettings.Development.json
      Properties/launchSettings.json
      Infrastructure/
        HalcyonProblemDetailsService.cs  # Custom IProblemDetailsService w/ trace id.
      Products/
        Product.cs                       # AdventureWorks product shape.
        CreateProductRequest.cs          # DataAnnotations + IValidatableObject margin rule.
        UpdateProductRequest.cs          # Same shape for PUT.
        ProductsEndpoints.cs             # List/Get/Create/Update/Delete on v1 + v2.
        IProductRepository.cs
        ProductRepository.cs             # In-memory store seeded with 4 AW bikes.
        Comparison/
          FluentCreateProductRequest.cs
          FluentUpdateProductRequestValidator.cs
          FluentValidationComparisonEndpoint.cs
  tests/
    Halcyon.Adventure.Api.Tests/
      Halcyon.Adventure.Api.Tests.csproj
      ProductsEndpointsTests.cs          # Happy path + 400 problem-details + margin rule.
```

## How to run

1. Open `Halcyon.Adventure.Api.sln` in Visual Studio 2026.
2. Press `F5` with the `https` profile selected. The API comes up on
   `https://localhost:7080`.
3. In a browser, open `https://localhost:7080/openapi/v1.json` to see the
   OpenAPI 3.1 document (Development only).
4. Hit `GET https://localhost:7080/v1/products` to see the four seeded bikes.

To run the test suite from the command line:

```
dotnet test
```

All three tests should pass against this baseline. Lesson 6 Exercise 4
deliberately breaks a logger scope so one test fails until the student fixes
it with `@debugger`.

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
