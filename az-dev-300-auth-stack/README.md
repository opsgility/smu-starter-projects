# az-dev-300-auth-stack

TaskForge tenant Blazor Server + External ID sign-in.

Fill `appsettings.json` `AzureAdB2C` section with your External ID tenant + app-registration values.

## Admin app
The admin Razor Pages app is a separate `dotnet run` — see `admin/` (create it after the tenant app works, wired against Workforce Entra ID with `AzureAd` config section instead of `AzureAdB2C`).
