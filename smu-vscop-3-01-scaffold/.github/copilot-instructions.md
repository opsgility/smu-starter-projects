# Halcyon Insurance — ASP.NET Core API team conventions

GitHub Copilot reads this file on every chat turn in this repository. Keep every answer, scaffold, and ghost-text suggestion aligned with the conventions below. If a request conflicts with a convention, flag the conflict first and propose a convention-compliant alternative before writing code.

## Project context

- **Service:** `Halcyon.Adventure.Api` — the Products API for the Halcyon Insurance / Adventure Works Cycles acquisition. Backs the Sales Portal (downstream course 5) and the Analytics Dashboard (downstream course 6).
- **Runtime:** .NET 10 ASP.NET Core on Windows + Kestrel. SQL Server 2025 Developer Edition local on the lab VM, Windows integrated auth, database `AdventureWorks2025`.
- **Team:** Dana Reyes (tech lead), Marcus Kim (tech-lead peer), Christopher Jones (engineering director), Michael Johnston (Adventure Works legacy SME).

## Architecture rules

1. **Thin controllers.** A controller action never contains business logic — only parameter binding, a single service call, and the response shape. If an action grows past ten lines, that is a signal to extract a service.
2. **Service layer handles the work.** Inject an `IProductService` (or equivalent per aggregate) into controllers. Services own the EF Core calls, business rules, mapping, and error outcomes.
3. **Async end-to-end.** Every I/O-touching method is `async Task<T>` with `CancellationToken` plumbed through from the controller signature down to `DbContext` calls. Never `.Result`, `.Wait()`, `.GetAwaiter().GetResult()`, or sync EF Core methods.
4. **`TypedResults` returns.** Controllers and minimal-API endpoints return `Results<Ok<T>, NotFound, ProblemHttpResult>` (or similar discriminated unions) so OpenAPI 3.1 can describe the shape without `[ProducesResponseType]` annotations. Never return the untyped `IResult` from `Results.Ok(...)`.
5. **Minimal APIs by default; controllers when earned.** Reach for minimal APIs unless the endpoint set needs model binding attributes, filters, or OpenAPI operation metadata that controllers express more cleanly. Lesson 1 walks the decision table.
6. **Problem-details for every error.** 4xx and 5xx responses use RFC 7807 problem-details via `TypedResults.Problem(...)` or `IProblemDetailsService`. Never return a bare `string` error body.

## Code style

- **Nullable reference types on.** Non-nullable by default; use `?` deliberately.
- **File-scoped namespaces, top-level statements for `Program.cs`.** No `Startup.cs` — everything in `Program.cs`.
- **Primary constructors on services and controllers** (`public class ProductService(AdventureWorksContext db, ILogger<ProductService> logger) : IProductService`).
- **`sealed`** on service and controller classes unless a derivation is explicitly needed.
- **Records for DTOs** (`public sealed record ProductResponse(int ProductId, string Name, ...)`). Classes for aggregates with behaviour.
- **No `AutoMapper`.** Hand-rolled mapping methods (`static ProductResponse ToResponse(Product p) => new(p.ProductID, p.Name, ...)`). Marcus's team found the convention-magic bugs more expensive than the mapping lines.
- **Naming:** `PascalCase` types, `camelCase` locals, `_camelCase` private fields, async methods end in `Async`.

## API shape

- **URL + header versioning via `Asp.Versioning.Http`.** URL segment is primary (`/api/v{version:apiVersion}/products`); header (`X-Api-Version: 1.0`) is a secondary opt-in.
- **OpenAPI 3.1 document at `/openapi/v1.yaml`.** YAML, not JSON — Christopher's architecture review tooling reads YAML.
- **Route lowercase, kebab-case for multi-word segments** (`/api/v1/product-categories`, not `/api/v1/ProductCategories`).
- **Pagination:** `page` + `pageSize` query parameters, defaults `page=1`, `pageSize=25`, max `pageSize=100`.

## Data access

- **EF Core 10** against `AdventureWorks2025`. Scaffold the `DbContext` from the existing schema — do not hand-author entity types.
- **`AsNoTracking()` on read-only queries.** Default to no-tracking; opt into tracking only when the method is about to mutate.
- **`CancellationToken` on every EF method call.** `await db.Products.FirstOrDefaultAsync(p => p.ProductID == id, cancellationToken)`.
- **`rowversion` for concurrency** on every mutable aggregate. PUT returns `409 Conflict` on mismatch — Lesson 2 covers the pattern.
- **Soft-delete, never physical delete** on acquired-system tables. Set `DiscontinuedDate` to today; subsequent GET returns `410 Gone`.

## Testing

- **xUnit** with `Microsoft.AspNetCore.Mvc.Testing`. One test class per controller or endpoint group.
- **Arrange-Act-Assert** with blank lines separating the three. No helper methods that hide the Arrange step.
- Tests use `WebApplicationFactory<Program>` and a scoped in-memory `AdventureWorksContext` where feasible; the Lesson 4 validation lab adds the first test suite.

## Pull-request etiquette

- **Feature branches off `main`, squash-merge via GitHub UI.** Delete the branch after merge.
- **Copilot-generated PR title + description** via the Visual Studio 2026 Git Changes window — Lesson 2 exercise 5 walks the flow.
- **Every PR passes the Git-agent review** before the reviewer is tagged.

## Things to flag back instead of writing

- A controller action with inline SQL or raw ADO.NET — route through EF Core + the service layer.
- A physical `DELETE` on `Production.Product` or any other acquired-system table — soft-delete is the rule.
- Hard-coded connection strings — read from `IConfiguration` keyed on `"ConnectionStrings:AdventureWorks"`.
- `Results.Ok(x)` without a `TypedResults` wrapper — rewrite as `TypedResults.Ok(x)` so the OpenAPI shape stays accurate.
- Synchronous EF Core calls (`db.Products.ToList()`) — flag and rewrite async.
- `AutoMapper`, `FluentValidation` in lesson-2 scope — FluentValidation is a comparison tool in Lesson 4, not the default; AutoMapper is forbidden.
