# SMU-VSCOP-3 Lesson 4 — Validation + typed errors on the Products API

Checkpoint snapshot of `Halcyon.Adventure.Api` as it looks the morning after the Lesson 2 PR landed. Lesson 4 opens on this folder and uses GitHub Copilot Edits to add validation + RFC 7807 problem-details.

## Scenario

Halcyon Insurance acquired Adventure Works Cycles last quarter. Dana Reyes is the tech lead on the modernization effort and shipped a versioned Products API against `AdventureWorks.Production.Product` in Lesson 2. Christopher Jones (engineering director) reviewed the PR and signed off, with one blocker for the next change:

> Nice ship, but 400s coming back without a problem-details body — fix before external consumers see this. They will not know what field they got wrong.

Lesson 4 is Dana's response to that review comment — register `AddValidation()`, add DataAnnotations + an `IValidatableObject` cross-field rule on the request records, land a custom `IProblemDetailsService` that includes a trace id, and introduce FluentValidation on exactly one endpoint for comparison so the "built-in vs FluentValidation" decision lands in the team's `copilot-instructions.md`.

## Files

```
smu-vscop-3-02-validation/
  README.md
  .gitignore
  Project.csproj                                # Halcyon.Adventure.Api, net10.0
  Program.cs                                    # DI + versioning + OpenAPI wiring
  appsettings.json                              # Local SQL Server AdventureWorks2025 connection string
  appsettings.Development.json
  Properties/
    launchSettings.json                         # http (5080) + https (7080); opens /openapi/v1.yaml
  .github/
    copilot-instructions.md                     # Halcyon team conventions Copilot grounds on
    prompts/
      scaffold-crud.prompt.md                   # /scaffold-crud prompt file from Lesson 2
  docs/
    openapi-contract.md                         # Contract notes + Lesson 4 scope
  Data/
    AdventureWorksContext.cs                    # Narrow DbContext over Production.Product
    Product.cs                                  # EF entity mapped to Production.Product
  Products/
    ProductsApi.cs                              # Minimal-API module, 5 endpoints, TypedResults
    ProductDto.cs                               # Read projection
    CreateProductRequest.cs                     # POST payload — NO validation attributes yet
    UpdateProductRequest.cs                     # PUT payload — NO validation attributes yet
```

## How to run

The lab VM (type 11) ships with SQL Server 2025 Developer Edition + `AdventureWorks2025` restored + the .NET 10 SDK + `dotnet-ef` on PATH. No install step is needed inside the container.

1. Open `Project.csproj` in Visual Studio 2026 (the lab's VS 2026 recent-projects pane picks this up as `Halcyon.Adventure.Api`).
2. Press F5. The browser opens on `/openapi/v1.yaml` and the API listens on `https://localhost:7080`.
3. Exercise the loop:
   - `GET https://localhost:7080/api/v1/products` returns every row in `Production.Product` as JSON.
   - `GET https://localhost:7080/api/v1/products/707` returns one product.
   - `POST https://localhost:7080/api/v1/products` with an empty body `{}` returns a bare `400 Bad Request` — that is the Lesson 4 blocker.

## Authentication

None at this stage. The API is anonymous and talks to the local SQL Server on `(local)` using Windows trusted authentication. Entra integration lands in Course 5 when the Sales Portal starts calling this API.

## Notes

- The `.github/copilot-instructions.md` file is the single most important input to Copilot's suggestions in Lesson 4. Read it first — it is what Copilot grounds the Edit-mode working set against.
- The `/scaffold-crud` prompt file in `.github/prompts/` is kept intentionally so students can see what Lesson 2 produced, and so Lesson 4's Edit-mode exercises can reuse it on sibling tables.
- The absence of validation attributes on `CreateProductRequest` + `UpdateProductRequest` is deliberate. Lesson 4 adds them.
- The connection string assumes the default local SQL Server instance baked into VM type 11. If the lab runs against a non-default instance, update `appsettings.json → ConnectionStrings:AdventureWorks` before pressing F5.
