using System.Diagnostics;
using Azure.Monitor.OpenTelemetry.AspNetCore;
using OpenTelemetry.Resources;
using OpenTelemetry.Trace;
using OpenTelemetry.Metrics;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddOpenTelemetry()
    .ConfigureResource(r => r.AddService("anchorline-worker", serviceVersion: "1.0.0"))
    .WithTracing(t => t.AddAspNetCoreInstrumentation())
    .WithMetrics(m => m.AddAspNetCoreInstrumentation())
    .UseAzureMonitor();

var app = builder.Build();
var source = new ActivitySource("Anchorline.Worker", "1.0.0");

app.MapPost("/fulfill", async () =>
{
    var tenantId = Baggage.GetBaggage("TenantId") ?? "unknown";
    using var activity = source.StartActivity("Worker.Fulfill");
    activity?.SetTag("tenant.id", tenantId);
    await Task.Delay(75); // simulate fulfillment work
    return Results.Ok();
});

app.Run("http://0.0.0.0:5003");
