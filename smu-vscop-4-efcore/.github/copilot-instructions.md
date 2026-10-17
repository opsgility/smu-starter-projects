# Halcyon.Adventure.Data — Copilot instructions

Halcyon Insurance acquired Adventure Works Cycles last quarter. This project is `Halcyon.Adventure.Data` — the data-access class library that owns the EF Core 10 context + entities for the Sales schema. Every downstream Halcyon-Adventure Works app (Sales Portal, Analytics Dashboard, ETL Worker, Modernization pivot) consumes this library.

Follow these conventions when Copilot proposes code in this repo.

## Framework and surface

- Target framework is **.NET 10**. EF Core pinned to **10.0.0** (Nov 2025 LTS).
- Data-access only — this is a class library (no `WebApplication.CreateBuilder`). The web APIs that consume it live in sibling projects.
- `AsNoTracking()` on every read-only query. Opt into tracking only when a method is about to mutate.
- Async everywhere; no `.Result` / `.Wait()` / `GetAwaiter().GetResult()`.
- `CancellationToken` plumbed through every method signature; passed into every `ToListAsync`, `FirstOrDefaultAsync`, `SaveChangesAsync` call.

## Scaffolding + partial classes (Lesson 1, 2)

- Reverse-engineered DbContexts live under `src/Halcyon.Adventure.Data/Generated/` and are produced by `dotnet ef dbcontext scaffold` with these flags:

  ```
  --use-database-names --no-pluralize --no-onconfiguring --force
  ```

- Do not edit anything under `Generated/` directly. The next `--force` re-scaffold will overwrite your edits silently. All customizations go in sibling `src/Halcyon.Adventure.Data/Conventions/*.Partial.cs` files.
- Partial-class files MUST share the exact namespace of the generated class they extend (`Halcyon.Adventure.Data.Generated`).
- DbSet property names match the table name — AdventureWorks tables are singular (`Customer`, not `Customers`), so DbSets are singular.
- Fluent API is the configuration mode for scaffolded entities. Data Annotations only on hand-authored request records consumed by the ASP.NET Core minimal-API validation layer.
- Money columns always carry an explicit `.HasPrecision(19, 4)`.
- Enum-backed columns always carry explicit `HasConversion<byte>()` + `HasColumnType("tinyint")` + `HasCheckConstraint("CK_<Table>_<Column>", "...")`.
- Global query filters on `ModifiedDate != null` for every acquired-system entity (soft-delete convention).

## Querying (Lesson 3, 4)

- **N+1 patterns are forbidden.** Any `foreach` over an `IQueryable<T>` with a nested `await ...Async()` is an N+1 by construction — rewrite with `Include().ThenInclude()` + projection.
- **`AsSplitQuery()`** on any `Include().ThenInclude()` chain where parent-to-child cardinality is high enough to risk Cartesian explosion (>50 total rows is the Halcyon threshold).
- **Projection** — read-only queries that produce a view project to a DTO in the SELECT: `.Select(c => new CustomerDto(c.CustomerID, ...))`. Never materialize the full entity and then map in memory.
- **See the SQL first.** Design-time context factories call `.LogTo(Console.WriteLine, new[] { DbLoggerCategory.Database.Command.Name }, LogLevel.Information).EnableSensitiveDataLogging()` so the generated SQL is visible under integration tests. `EnableSensitiveDataLogging` is dev + test only — forbidden in `Program.cs` under any non-Development environment.

## Migrations (Lesson 5, 6)

- All migrations live in `src/Halcyon.Adventure.Data/Migrations/` and ship via source control. Never run `ALTER TABLE` by hand against any environment.
- Dev + lab: `dotnet ef database update`. Staging + production: `dotnet ef migrations script --idempotent --output artifacts/migrations.sql` + DBA review.
- Every migration PR walks the Halcyon review checklist in `.github/pull_request_template.md`:
  1. Up method's operation order (DROPs after dependents; ADDs before consumers).
  2. Down method is a true semantic reverse of Up (`AddColumn` ↔ `DropColumn`, `AddCheckConstraint` ↔ `DropCheckConstraint`).
  3. No DROP + ADD on same-name-similar-type pairs — scan for this + swap for `RenameColumn`.
  4. No `type: "datetime2"` where the fluent config said `datetime2(3)` — EF Core 10 generator quirk, hand-fix after generation.
  5. No `defaultValue: "<enum-name-as-string>"` — must be the underlying numeric value.
  6. No data operations (`InsertData` / `UpdateData` / `.Sql(...)`) without an explicit "safe to re-run" note.
  7. Rollback plan in the PR body (`dotnet ef database update <PriorMigrationName>`).

## Connection strings

- Never in source. The design-time context factory supplies the connection for scaffolding + migrations; runtime DI supplies the connection for the app.
- Design-time connection: `Server=.;Database=AdventureWorks2025;Trusted_Connection=True;TrustServerCertificate=True` (local SQL Server 2025 default instance; Windows integrated auth).

## Data-access patterns: use the simplest shape that works (Lesson 7)

| Pattern | Default? | Introduce when |
| --- | --- | --- |
| DbContext directly in endpoint handlers | **YES** | — |
| IUnitOfWork wrapper over DbContext | NO | Multi-DbContext coordination OR database-plus-outbox transaction |
| IRepository abstraction over DbContext | NO | Multi-source lookup (SQL + legacy + cache) OR strict Clean/Hex architectural layering |
| ISpecification pattern | NO | Same complex filter spans 5+ endpoints AND is likely to change together |
| Static IQueryable extension methods | YES, when applicable | Filter spans 2-3 endpoints — lighter than Specification |

Every PR introducing one of the NO-by-default patterns must link the specific scenario it earns its place in. "Testability" alone is not sufficient — Halcyon tests via `WebApplicationFactory<Program>` + the EF Core in-memory provider.

## Testing

- xUnit is the house framework. Integration tests use `WebApplicationFactory<Program>` for API projects + direct DbContext construction (via the design-time factory) for data-only tests.
- One test class per entity (reads) + per migration (writes).
- Perf regression tests on any report that has a performance budget (see `CustomerSalesReportTests.Report_For_Top_10_Platinum_Customers_Completes_Under_500ms`).

## What NOT to propose

- No AutoMapper. Hand-written `ToDto(...)` is the house style; projection in SELECT is preferred.
- No MediatR. The team evaluated it in Q3 and rejected the dependency.
- No lazy loading (`UseLazyLoadingProxies` or virtual navigation properties). Lazy loading hides N+1s.
- No `async void`.
- No connection strings in source. Design-time factory + runtime DI.
- No edits inside `Generated/`. Convention overrides live in `Conventions/`.
