# SMU-VSCOP-3 Lesson 2 — Scaffold the Products API with Copilot

Minimal `Halcyon.Adventure.Api` skeleton for the first hands-on lab in SMU-VSCOP-3 ("ASP.NET Core APIs with Copilot"). The starter opens Visual Studio 2026 on an empty .NET 10 ASP.NET Core Web API with the Halcyon team's grounding files already in place — Copilot has `.github/copilot-instructions.md` to read on first chat turn, Dana has Christopher's one-page API contract in `docs/openapi-contract.md` to review, and the AdventureWorks connection string placeholder is already in `appsettings.json`. The exercises build the Products API from here.

## Scenario

Halcyon Insurance (SOC 2 Type II P&C carrier, Hartford CT) acquired Adventure Works Cycles last quarter. Dana Reyes — senior C# developer, tech lead on the Adventure Works modernization — just got a one-pager from engineering director Christopher Jones asking for a Products API against the acquired AdventureWorks2025 database by end of quarter. The service name is `Halcyon.Adventure.Api`; the first endpoint set is Products, backed by the `AdventureWorks.Production.Product` table. Tech-lead peer Marcus Kim already seeded the repo with the team's `.github/copilot-instructions.md` and dropped Christopher's contract draft at `docs/openapi-contract.md`. Dana's job in this lab is to turn that skeleton into a running, versioned Products API using Copilot ghost text and a reusable `/scaffold-crud` prompt file.

## Files

```
smu-vscop-3-01-scaffold/
  README.md                           # This file.
  .gitignore                          # .NET + VS 2026 + .vs/ patterns.
  HalcyonAdventureApi.sln             # Single-project solution, VS 2026 format.
  Halcyon.Adventure.Api/
    Halcyon.Adventure.Api.csproj      # .NET 10 ASP.NET Core Web API project file.
    Program.cs                        # Minimal WebApplication builder — intentionally bare.
    appsettings.json                  # AdventureWorks SQL Server connection-string placeholder.
    appsettings.Development.json      # Dev-only logging overrides.
    Properties/
      launchSettings.json             # Launch profile for `dotnet run` + VS 2026 F5.
  docs/
    openapi-contract.md               # Christopher's draft Products API contract.
  .github/
    copilot-instructions.md           # Halcyon team conventions — Copilot reads this first.
```

## How to run

VS 2026 opens the solution automatically on lab launch; the student does not run `dotnet restore` — the lab container variant has the .NET 10 SDK + ASP.NET Core shared framework preinstalled.

1. Open `HalcyonAdventureApi.sln` in Visual Studio 2026.
2. Press F5 to launch `Halcyon.Adventure.Api` under IIS Express; the browser opens on `https://localhost:7229`.
3. The default route returns `404` — the first exercise adds the Products controller skeleton.

## Authentication

No authentication at this stage. The API will be fronted by Halcyon's Entra ID gateway in Course 5 (Sales Portal); Course 3 focuses on the API shape, not the auth story.

The AdventureWorks SQL Server runs locally on the lab VM at the default instance (`Server=.;Database=AdventureWorks2025;Trusted_Connection=True;TrustServerCertificate=True`). The student connects via Windows integrated auth, so no credentials are stored in the project.

## Notes

- The `Program.cs` is intentionally two lines — a `WebApplication.CreateBuilder(args)` + `app.Run()`. Exercise 2 adds the first endpoint using Copilot ghost text; exercise 3 adds URL versioning via `Asp.Versioning.Http`; exercise 4 lands a `/scaffold-crud` prompt file; exercise 5 adds header versioning + verifies the OpenAPI 3.1 document at `/openapi/v1.yaml`.
- `.github/copilot-instructions.md` is the grounding file Copilot Chat reads on every turn. Halcyon's conventions are already in there (thin controllers, service layer, async end-to-end, `TypedResults` returns) — the first lab exercise relies on Copilot picking those up without any extra prompting from the student.
- `docs/openapi-contract.md` is draft shape, not final. Lesson 1 teaches the Ask-mode review loop against this document; Lesson 2 builds against the version Dana and Christopher land on.
- `HalcyonAdventureApi.sln` is the renamed solution file — the earlier internal name (`HalcyonClaimsApi.sln`) was dropped when Christopher moved the sprint goal from Claims to Products.
