# SMU Starter Projects

Starter project templates for SkillMeUp VS Code Server labs. Each subfolder contains a ready-to-run .NET 8.0 project with VS Code debug configurations.

## Projects

| Subfolder | Description | Run |
|-----------|-------------|-----|
| `console` | .NET Console App | `dotnet run` |
| `webapi` | ASP.NET Core Web API (controllers) | `dotnet run` then browse `/swagger` |
| `webapp` | ASP.NET Core Razor Pages | `dotnet run` then browse `/` |
| `mvc` | ASP.NET Core MVC | `dotnet run` then browse `/` |
| `blazor-server` | Blazor Server App | `dotnet run` then browse `/` |
| `api-and-webapp` | Multi-project: API + Razor Pages | `dotnet run --project Project.Api` and `dotnet run --project Project.Web` |

## Usage

Set the **Starter Project Git URL** on a lab to:

    https://github.com/opsgility/smu-starter-projects.git

Set the **Subfolder** to the desired template (e.g., `webapi`).

When a student launches VS Code for the first time, the subfolder contents are copied into their workspace with `.vscode/` debug configs ready to go.

## Debugging

All projects include `.vscode/launch.json` and `tasks.json`. Press **F5** to build and launch with the debugger attached.

The `api-and-webapp` project includes a **compound launch** configuration ("API + Web App") that starts both services simultaneously.
