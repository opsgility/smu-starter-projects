// AZ-DEV-100 Module 4 — Anchorline storefront with deployment-slot visibility.
// /version reports slotName so a swap is provable via curl.

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/health", () => Results.Ok(new { status = "healthy", timestamp = DateTime.UtcNow }));

app.MapGet("/version", (IConfiguration config) => Results.Ok(new
{
    buildTag = config["AZ_DEV_100_BUILD_TAG"] ?? "unset",
    slotName = Environment.GetEnvironmentVariable("WEBSITE_SLOT_NAME") ?? "not-app-service",
    dotnetVersion = Environment.Version.ToString(3),
    environment = app.Environment.EnvironmentName
}));

// Warmup endpoint the platform pings before completing a swap.
// Do the same work the hot path does so the process is fully JIT'd + cache-warm.
app.MapGet("/warmup", () => Results.Ok(new { warmed = true, timestamp = DateTime.UtcNow }));

app.MapGet("/", () => Results.Content(
    """
    Anchorline storefront — AZ-DEV-100 Module 4 (slots + swap).
    Try /health, /version, /warmup.
    """,
    "text/plain"));

app.Run();
