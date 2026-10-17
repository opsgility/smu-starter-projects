# SMU-VSCOP-4 — Halcyon.Adventure.Data starter

This starter is the pre-staged project for Course 4 ("EF Core + Data Access with Copilot") in the Modern Enterprise App Development with VS 2026 + Copilot skill path (smu-vscop). Three LT1 hands-on labs consume this starter — reverse-engineering the AdventureWorks Sales schema (Lesson 2), fixing an N+1 query under the @debugger agent (Lesson 4), and shipping a Customer-Tier migration (Lesson 6).

## Solution layout

```
smu-vscop-4-efcore/
  Halcyon.Adventure.Data.sln              # 3-project solution
  README.md                               # this file
  .gitignore                              # .NET + VS 2026 + .vs/ patterns
  .config/
    dotnet-tools.json                     # dotnet-ef 10.0.0 pinned
  .github/
    copilot-instructions.md               # Halcyon EF Core conventions — Copilot grounds here
    prompts/
      add-ef-feature.prompt.md            # (student authors in Lesson 6 Exercise 5)
  docs/
    data-decisions/
      README.md                           # ADR-lite folder; students add per-feature design docs
    scratch/                              # SQL logs, benchmark reports — exercises reference
  src/
    Halcyon.Adventure.Data/               # The data-access class library
      Halcyon.Adventure.Data.csproj       # .NET 10, EF Core packages are added by students in Lesson 2 Exercise 2
      Design/                                   # Lesson 2 Exercise 2 adds AdventureWorksSalesContextFactory.cs here
      Generated/                                # Empty — scaffold command fills in Lesson 2 Exercise 3
      Conventions/                              # Empty — partial-class additions land in Lesson 2 Exercise 5 + Lesson 6
      Reporting/                                # Lesson 4 Exercise 2 adds CustomerSalesReportService.cs here
      Migrations/                               # Empty — created in Lesson 6 Exercise 4
    Halcyon.Adventure.Data.Benchmarks/
      Halcyon.Adventure.Data.Benchmarks.csproj  # BenchmarkDotNet harness project (empty — populated in Lesson 4 Exercise 5)
      Program.cs                                # One-liner — exists for the project to compile
  tests/
    Halcyon.Adventure.Data.Tests/
      Halcyon.Adventure.Data.Tests.csproj
      Smoke/
        AdventureWorksSmokeTest.cs              # Proves local SQL Server + AdventureWorks2025 is reachable
      Sales/
        SalesSmokeTest.cs                       # [Fact(Skip = "Lesson 2 Exercise 3 unlocks ...")]
        SalesConventionsTest.cs                 # [Fact(Skip = "Lesson 2 Exercise 5 unlocks ...")] — 3 tests
      Reporting/
        CustomerSalesReportTests.cs             # 1 passing + 1 [Fact(Skip = "Lesson 4 Ex 5 unlocks ...")] perf test
        CustomerTierMigrationTests.cs           # 4 [Fact(Skip = "Lesson 6 Exercise N unlocks ...")] tests
```

## How to run

The lab VM ships with .NET 10 SDK, SQL Server 2025 Developer Edition with `AdventureWorks2025` restored, SQL Server Management Studio 20, and the `dotnet-ef` + `sqlcmd` CLIs on PATH.

1. Open `Halcyon.Adventure.Data.sln` in Visual Studio 2026.
2. Restore the local `dotnet-ef` tool (first lab lease only):

   ```powershell
   dotnet tool restore
   ```

3. Build the solution:

   ```powershell
   dotnet build Halcyon.Adventure.Data.sln
   ```

4. Run the baseline smoke test to confirm SQL Server is reachable:

   ```powershell
   dotnet test tests\Halcyon.Adventure.Data.Tests --filter "FullyQualifiedName~AdventureWorksSmokeTest"
   ```

   Expected: 1 test passes.

## Narrative

**Halcyon Insurance** acquired Adventure Works Cycles last quarter. **Dana Reyes** (senior C# developer, Halcyon) is the tech lead on the modernization effort to lift Adventure Works onto Halcyon's .NET 10 stack. Director **Christopher Jones** owns the program. **Michael Johnston** (AW legacy app lead) is the SME on the AdventureWorks schema. **Marcus Kim** reviews the data-layer PRs.

Course 3 (SMU-VSCOP-3) shipped the Products API against `AdventureWorks.Production.Product`. Course 4 scaffolds the Sales schema (`Sales.Customer`, `Sales.SalesOrderHeader`, `Sales.SalesOrderDetail`), teaches the LINQ-to-SQL patterns Copilot gets wrong without grounding, ships a Customer-Tier migration, and lands the decision table that keeps Copilot's proposals on-pattern for the rest of the modernization program.

## Lesson progression + what each exercise lands here

### Lesson 2 (Lab 3205) — Reverse-engineer the AdventureWorks Sales schema

- **Exercise 2** adds EF Core 10 packages (`Microsoft.EntityFrameworkCore` + `.SqlServer` + `.Design`) to `Halcyon.Adventure.Data.csproj`.
- **Exercise 3** runs `dotnet ef dbcontext scaffold` and populates `Generated/`.
- **Exercise 4** reviews the generated DbContext with Copilot Ask mode.
- **Exercise 5** adds `Conventions/AdventureWorksSalesContext.Partial.cs` and `Conventions/Customer.Partial.cs` with the Halcyon convention overrides.

### Lesson 4 (Lab 3207) — Fix N+1 queries with Copilot and @debugger

- **Exercise 2** wires `LogTo` + `EnableSensitiveDataLogging` on `AdventureWorksSalesContextFactory.cs` so the N+1 trace is visible.
- **Exercise 3** uses the `@debugger` agent to walk the slow method and surface the N+1 call site.
- **Exercise 4** rewrites `CustomerSalesReportService.GetTopPlatinumWithOrdersAsync` via Copilot Edits with `Include().ThenInclude().AsSplitQuery().AsNoTracking().Select(DTO)`.
- **Exercise 5** scaffolds the BenchmarkDotNet harness in `src/Halcyon.Adventure.Data.Benchmarks/`.

### Lesson 6 (Lab 3209) — Add a Customer-Tier feature via migration

- **Exercise 2** writes `docs/data-decisions/add-customer-tier.md`.
- **Exercise 3** adds `Conventions/CustomerTier.cs` + extends `Customer.Partial.cs` and `AdventureWorksSalesContext.Partial.cs`.
- **Exercise 4** runs `dotnet ef migrations add AddCustomerTier`, reviews with the `@git` agent, applies with `dotnet ef database update`.
- **Exercise 5** authors `.github/prompts/add-ef-feature.prompt.md` and opens the PR with Copilot drafting the summary.

## Authentication

Local only. The design-time context factory uses `Server=.;Trusted_Connection=True;TrustServerCertificate=True` — Windows integrated auth against the VM's default SQL Server instance. No credentials ever enter source control.

## Notes

- The `Generated/` folder is deliberately empty in the starter. Lesson 2 Exercise 3 populates it with the scaffold command's output. Students should never edit anything in `Generated/` directly — the convention is partial-class additions in `Conventions/`.
- The `Migrations/` folder is empty. Lesson 6 Exercise 4 creates it via `dotnet ef migrations add`.
- `CustomerSalesReportService.cs` ships with the N+1 anti-pattern intentionally. Lesson 4 Exercise 4 fixes it; the exercise is built around seeing the pattern in the SQL log first.
- The three EF Core NuGet packages are NOT in `Halcyon.Adventure.Data.csproj` at starter time — Lesson 2 Exercise 2 adds them. This is deliberate: students learn the package names + versions by running the commands.
- `AdventureWorks2025` must be restored on the local SQL Server 2025 Developer Edition instance. The VM image bakes this; a fresh VM lease without AW2025 restored is an image bug — report it.
