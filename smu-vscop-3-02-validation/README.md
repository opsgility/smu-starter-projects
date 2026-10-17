# SMU-VSCOP-3 Lesson 4 — Validation + typed errors on the Products API

Checkpoint snapshot of `Halcyon.Adventure.Api` the morning after the Lesson 2 PR landed. Lesson 4 opens on this folder and uses GitHub Copilot Edits to add `.NET 10 AddValidation()`, DataAnnotations, an `IValidatableObject` cross-field rule, a custom problem-details delegate that threads a correlation trace id, and FluentValidation on exactly one endpoint.

## Scenario

Halcyon Insurance acquired Adventure Works Cycles last quarter. Dana Reyes is the tech lead on the modernization effort and shipped a versioned Products API in Lesson 2. Christopher Jones (engineering director) reviewed the PR and signed off, with one blocker for the next change:

> Nice ship, but 400s coming back without a problem-details body — fix before external consumers see this. They will not know what field they got wrong.

Lesson 4 is Dana's response to that review comment.

## Solution layout

```
smu-vscop-3-02-validation/
  README.md
  .gitignore
  Halcyon.Adventure.Api.sln              # 3-project solution
  .github/
    copilot-instructions.md              # Halcyon team conventions
    prompts/
      scaffold-crud.prompt.md            # /scaffold-crud prompt file from Lesson 2
  docs/
    openapi-contract.md                  # Contract notes + Lesson 4 scope
  src/
    Halcyon.Adventure.Api/               # ASP.NET Core 10 minimal-API host
      Halcyon.Adventure.Api.csproj
      Program.cs                         # DI + CorrelationIdMiddleware + endpoint maps
      appsettings.json
      appsettings.Development.json
      Properties/launchSettings.json     # http://localhost:5117 + https://localhost:7117
      Middleware/
        CorrelationIdMiddleware.cs       # Reads/mints X-Correlation-Id; HttpContext.Items["HalcyonCorrelationId"]
      Products/
        Product.cs                       # Domain entity
        IProductRepository.cs
        InMemoryProductRepository.cs
        ProductsEndpoints.cs             # GET, POST, PUT, DELETE — no validation yet
      Endpoints/
        BatchImportEndpoint.cs           # POST /products/batch-import — no validation yet
    Halcyon.Adventure.Shared/            # Contract records consumed by Api + future clients
      Halcyon.Adventure.Shared.csproj
      Products/
        CreateProductRequest.cs          # record { Sku, Name, Price, Cost } — NO attributes
        UpdateProductRequest.cs          # record { Name, Price, Cost } — NO attributes
        BatchImportRequest.cs            # record { Items } — Exercise 5 adds FluentValidation
        ProductDto.cs                    # Read projection
  tests/
    Halcyon.Adventure.Api.Tests/
      Halcyon.Adventure.Api.Tests.csproj
      Products/
        ProductsEndpointsTests.cs        # Baseline xUnit suite using WebApplicationFactory<Program>
```

## How to run

The lab VM ships with the .NET 10 SDK pre-installed.

1. Open `Halcyon.Adventure.Api.sln` in Visual Studio 2026 (the lab's VS 2026 recent-projects pane picks this up as `Halcyon.Adventure.Api`).
2. Set `src/Halcyon.Adventure.Api` as the startup project.
3. Press F5. The browser opens on `/openapi/v1.yaml` and the API listens on `https://localhost:7117`.
4. Exercise the loop:
   - `GET https://localhost:7117/products` returns the two seeded rows.
   - `GET https://localhost:7117/products/1` returns one product.
   - `POST https://localhost:7117/products` with `{}` returns a bare `400 Bad Request` with no body — that is the Lesson 4 blocker.
5. Run the baseline tests from the VS Test Explorer or:

   ```
   dotnet test Halcyon.Adventure.Api.sln
   ```

   All three baseline tests in `ProductsEndpointsTests` pass.

## What Lesson 4 lands on top of this starter

- **Exercise 2** — `builder.Services.AddValidation()` in `Program.cs`, `[Required]` + `[Range]` + `[StringLength]` attributes on `CreateProductRequest` + `UpdateProductRequest`, three new `ValidationTests` cases.
- **Exercise 3** — `IValidatableObject` margin rule (`Price >= 1.2 × Cost`) on both request records, three new boundary tests.
- **Exercise 4** — `AddProblemDetails(options => options.CustomizeProblemDetails = ...)` delegate that reads `HttpContext.Items["HalcyonCorrelationId"]` and copies it onto every problem-details response as the `halcyonTraceId` extension, plus two tests under a new `ProblemDetailsTraceIdTests` class.
- **Exercise 5** — FluentValidation on the one `POST /products/batch-import` endpoint only, paired with `.DisableValidation()` on that map call, routed through `IProblemDetailsService` so `halcyonTraceId` still appears on FV-generated errors, decision table landed in `.github/copilot-instructions.md`.

## Authentication

None at this stage. The API is anonymous. Entra integration lands in Course 5 when the Sales Portal starts calling it.

## Notes

- The in-memory repository is deliberate for lab scope — Lesson 4 is about validation, not data access. Course 4 swaps the repository for an EF Core 10 scaffold against `AdventureWorks.Production.Product`.
- `CorrelationIdMiddleware` is already wired in `Program.cs` so Exercise 4's delegate has a populated `HttpContext.Items["HalcyonCorrelationId"]` to read from the moment the student lands the delegate.
- The three baseline tests in `ProductsEndpointsTests` MUST pass as-is before Exercise 2. If they fail on a fresh clone, something in the VM image drifted — do not start Exercise 2 before the baseline is green.
