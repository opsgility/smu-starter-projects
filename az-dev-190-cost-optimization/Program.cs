// Anchorline cost-optimized OTel — 5% adaptive-style sampling via TraceIdRatioBasedSampler,
// plus verbose logs routed to a basic-tier custom table (via workspace routing on the ARM side).

using Azure.Monitor.OpenTelemetry.AspNetCore;
using OpenTelemetry.Resources;
using OpenTelemetry.Trace;
using OpenTelemetry.Metrics;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddOpenTelemetry()
    .ConfigureResource(r => r.AddService("anchorline-cost-opt", serviceVersion: "1.0.0"))
    .WithTracing(t => t
        .SetSampler(new TraceIdRatioBasedSampler(0.05))    // 5% of traces
        .AddAspNetCoreInstrumentation()
        .AddHttpClientInstrumentation())
    .WithMetrics(m => m.AddAspNetCoreInstrumentation())    // metrics NEVER sampled
    .UseAzureMonitor();

var app = builder.Build();

// Generates enough traffic to matter.
app.MapGet("/health", () => Results.Ok(new { status = "ok" }));
app.MapGet("/orders/{id}", (string id, ILogger<Program> log) =>
{
    log.LogDebug("debug — cheap chatter, want basic-tier only");
    log.LogInformation("Fetched order {OrderId}", id);
    return Results.Ok(new { id, total = 249.5m });
});

app.Run();
