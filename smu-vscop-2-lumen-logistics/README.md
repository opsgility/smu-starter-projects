# Lumen Logistics API

A minimal ASP.NET Core Web API that tracks parcels for **Lumen Logistics**, a fictional parcel-delivery SaaS startup. This repository is the starter codebase for the SkillMeUp course **Using Visual Studio 2026 with GitHub** (`SMU-VS2026-GH`).

## Prerequisites

- Visual Studio 2026 (18.0 or higher)
- .NET 10 SDK

Both are pre-installed on the lab VM — nothing to install.

## Project layout

```
lumen-logistics/
├─ LumenLogistics.sln
├─ LumenLogistics.Api/
│  ├─ LumenLogistics.Api.csproj      # ASP.NET Core Web API, net10.0
│  ├─ Program.cs                     # Minimal-API endpoints
│  ├─ Models/Package.cs              # Package domain type
│  ├─ Data/PackageStore.cs           # In-memory store (seeded)
│  ├─ Properties/launchSettings.json
│  ├─ appsettings.json
│  └─ appsettings.Development.json
├─ LumenLogistics.Api.http           # VS 2026 .http file for request testing
├─ .gitignore
└─ README.md
```

## What it does

Three endpoints:

| Verb | Route            | Returns                                     |
|-----:|------------------|---------------------------------------------|
| GET  | `/packages`      | All packages in the in-memory store         |
| GET  | `/packages/{id}` | A single package by id, or 404              |
| POST | `/packages`      | Creates a new package, returns 201 + object |

Packages are kept in memory and seeded at startup — this is a teaching project, not a production system.

## Running from Visual Studio 2026

1. Open `LumenLogistics.sln`.
2. Press **F5** (or click the green run button).
3. The default profile launches on `https://localhost:7042`.
4. Open `LumenLogistics.Api.http` and click **Send request** on any of the pre-written calls.

## About this starter

Every exercise in the course works against this same codebase. The narrative follows **Alex Rivera**, a new .NET developer at Lumen Logistics onboarding under engineering lead **Michael Peters**. Both characters are fictional.
