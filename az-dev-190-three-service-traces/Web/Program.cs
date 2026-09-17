using System.Diagnostics;
using Azure.Monitor.OpenTelemetry.AspNetCore;
using OpenTelemetry.Resources;
using OpenTelemetry.Trace;
using OpenTelemetry.Metrics;

var builder = WebApplication.CreateBuilder(args);
var apiBase = Environment.GetEnvironmentVariable("API_BASE_URL") ?? "http://localhost:5002";

builder.Services.AddOpenTelemetry()
    .ConfigureResource(r => r.AddService("anchorline-web", serviceVersion: "1.0.0"))
    .WithTracing(t => t.AddAspNetCoreInstrumentation().AddHttpClientInstrumentation())
    .WithMetrics(m => m.AddAspNetCoreInstrumentation().AddHttpClientInstrumentation())
    .UseAzureMonitor();

builder.Services.AddHttpClient("api", c => c.BaseAddress = new Uri(apiBase));

var app = builder.Build();
var source = new ActivitySource("Anchorline.Web", "1.0.0");

app.MapPost("/checkout", async (HttpRequest req, IHttpClientFactory hcf) =>
{
    var tenantId = req.Headers["X-Tenant-Id"].FirstOrDefault() ?? "anchor-default";
    // Propagate baggage — appears on every downstream span.
    Baggage.SetBaggage("TenantId", tenantId);
    using var activity = source.StartActivity("Web.Checkout");
    activity?.SetTag("tenant.id", tenantId);
    var client = hcf.CreateClient("api");
    var response = await client.PostAsync("/orders", null);
    return await response.Content.ReadAsStringAsync();
});

app.Run("http://0.0.0.0:5001");
