// AZ-DEV-100 Module 2 — Anchorline Outdoors storefront with KV references + App Configuration.
// Endpoints prove the config-source chain works end-to-end:
//   /health       — process is up (Module 1 baseline)
//   /version      — reports AZ_DEV_100_BUILD_TAG from IConfiguration
//   /stripe-key   — reads Anchorline:StripeApiKey (resolved from KV via App Service KV reference)
//   /discount     — reads Beta.FallDiscount feature flag from App Configuration

using Azure.Identity;
using Microsoft.Extensions.Configuration.AzureAppConfiguration;
using Microsoft.FeatureManagement;

var builder = WebApplication.CreateBuilder(args);

// Wire Azure App Configuration when the endpoint env var is set.
// Locally without the env var, the app runs on file + env-var config only and /discount returns false.
var appConfigEndpoint = Environment.GetEnvironmentVariable("AZ_DEV_100_APPCONFIG_ENDPOINT");

if (!string.IsNullOrWhiteSpace(appConfigEndpoint))
{
    builder.Configuration.AddAzureAppConfiguration(options =>
    {
        options.Connect(new Uri(appConfigEndpoint), new DefaultAzureCredential())
            .Select("Anchorline:*", LabelFilter.Null)
            .ConfigureRefresh(refresh =>
                refresh.Register("Anchorline:Sentinel", refreshAll: true)
                       .SetRefreshInterval(TimeSpan.FromSeconds(30)))
            .UseFeatureFlags(flags =>
                flags.SetRefreshInterval(TimeSpan.FromSeconds(30)));
    });

    builder.Services.AddAzureAppConfiguration();
    builder.Services.AddFeatureManagement();
}
else
{
    // No App Config endpoint — register a minimal feature manager so /discount doesn't 500.
    // Local dev fallback; production always has the env var set by the ARM template.
    builder.Services.AddFeatureManagement();
}

var app = builder.Build();

// Middleware that triggers the sentinel-key refresh check on each request when App Config is wired.
if (!string.IsNullOrWhiteSpace(appConfigEndpoint))
{
    app.UseAzureAppConfiguration();
}

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
    appConfigWired = !string.IsNullOrWhiteSpace(appConfigEndpoint)
}));

// Returns the first 6 chars of the Stripe key — enough to prove the KV reference resolved
// without leaking the full secret in a log or a curl body.
app.MapGet("/stripe-key", (IConfiguration config) =>
{
    var key = config["Anchorline:StripeApiKey"] ?? "unset";
    var kvReferenceLeaked = key.StartsWith("@Microsoft.KeyVault(");
    return Results.Ok(new
    {
        keyPreview = key.Length > 6 ? key[..6] + "..." : key,
        length = key.Length,
        kvReferenceResolved = !kvReferenceLeaked && key != "unset",
        // If this is true, App Service failed to resolve the KV reference (check MI + role + secret + restart).
        kvReferenceLeaked
    });
});

// Feature-flag-gated response. Fall-discount defaults to false when the flag is disabled OR
// when App Config isn't wired (local dev). Marketing flips the flag in App Config; sentinel bump
// makes the change visible within the 30s cache window without a restart.
app.MapGet("/discount", async (IFeatureManager features) =>
{
    var discountOn = await features.IsEnabledAsync("Beta.FallDiscount");
    return Results.Ok(new
    {
        feature = "Beta.FallDiscount",
        enabled = discountOn,
        discountPercentage = discountOn ? 10 : 0
    });
});

app.MapGet("/", () => Results.Content(
    """
    Anchorline Outdoors storefront — AZ-DEV-100 Module 2 (KV + App Configuration).
    Try /health, /version, /stripe-key, /discount.
    """,
    "text/plain"));

app.Run();
