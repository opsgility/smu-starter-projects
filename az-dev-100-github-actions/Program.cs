// AZ-DEV-100 Module 3 — Anchorline storefront (GH Actions OIDC deploy target).
// Same endpoint shape as Module 1's baseline. Focus of this module is the workflow, not the app.

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/health", () => Results.Ok(new
{
    status = "healthy",
    timestamp = DateTime.UtcNow
}));

app.MapGet("/version", (IConfiguration config) => Results.Ok(new
{
    buildTag = config["AZ_DEV_100_BUILD_TAG"] ?? "unset",
    dotnetVersion = Environment.Version.ToString(),
    environment = app.Environment.EnvironmentName,
    commitSha = config["GITHUB_SHA"] ?? "not-set-by-workflow"
}));

app.MapGet("/", () => Results.Content(
    """
    Anchorline Outdoors storefront — AZ-DEV-100 Module 3 (GitHub Actions OIDC deploy target).
    Try /health or /version.
    """,
    "text/plain"));

app.Run();
