// Anchorline SLO demo — Orders API with a toggleable latency injection endpoint so
// students can drive their SLO error budget below threshold and fire the burn-rate alert.

using Azure.Monitor.OpenTelemetry.AspNetCore;
using OpenTelemetry.Resources;
using OpenTelemetry.Trace;
using OpenTelemetry.Metrics;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddOpenTelemetry()
    .ConfigureResource(r => r.AddService("anchorline-orders-slo", serviceVersion: "1.0.0"))
    .WithTracing(t => t.AddAspNetCoreInstrumentation())
    .WithMetrics(m => m.AddAspNetCoreInstrumentation())
    .UseAzureMonitor();

var app = builder.Build();
int induced = 0; // ms of injected latency (0 = healthy)

// SLO endpoint — meant to complete in < 500ms as our 99.5% SLO promise.
app.MapGet("/orders", async () =>
{
    await Task.Delay(induced + Random.Shared.Next(20, 80));
    return Results.Ok();
});
app.MapPost("/simulate/latency/{ms:int}", (int ms) => { induced = ms; return Results.Ok(new { induced }); });
app.MapPost("/simulate/heal",             ()       => { induced = 0;  return Results.Ok(new { induced }); });

app.Run();
