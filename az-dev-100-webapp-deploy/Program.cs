// AZ-DEV-100 Module 1 — Anchorline Outdoors storefront scaffold.
// Minimal API with /health and /version — proves the app is live and reports the deployed build tag.

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

// /health — returns 200 when the process is up. App Service and any downstream monitoring
// (Application Insights availability tests, custom health-check probes) target this endpoint.
app.MapGet("/health", () => Results.Ok(new
{
    status = "healthy",
    timestamp = DateTime.UtcNow
}));

// /version — reports the build tag from configuration.
// AZ_DEV_100_BUILD_TAG is set as an App Setting on the Web App at ARM-deploy time.
// The value flows into IConfiguration via App Service's environment-variable → app-setting binding.
app.MapGet("/version", (IConfiguration config) => Results.Ok(new
{
    buildTag = config["AZ_DEV_100_BUILD_TAG"] ?? "unset",
    dotnetVersion = Environment.Version.ToString(),
    environment = app.Environment.EnvironmentName
}));

// Root — friendly landing page for the browser hitting the default hostname.
app.MapGet("/", () => Results.Content(
    """
    Anchorline Outdoors storefront scaffold — AZ-DEV-100 Module 1.
    Try /health or /version.
    """,
    "text/plain"));

app.Run();
