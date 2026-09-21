using System.Diagnostics.Metrics;
using Azure.Identity;
using Azure.Monitor.OpenTelemetry.AspNetCore;
using Microsoft.Azure.Cosmos;
using Microsoft.Azure.Functions.Worker;
using Microsoft.Azure.Functions.Worker.Builder;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using OpenTelemetry.Metrics;
using OpenTelemetry.Trace;

var builder = FunctionsApplication.CreateBuilder(args);
builder.ConfigureFunctionsWebApplication();

builder.Services
    .AddApplicationInsightsTelemetryWorkerService()
    .ConfigureFunctionsApplicationInsights();

builder.Services.AddOpenTelemetry()
    .UseAzureMonitor()
    .WithMetrics(m => m.AddMeter("Anchorline.Capstone"))
    .WithTracing(t => t.AddSource("Anchorline.Capstone"));

builder.Services.AddSingleton(new Meter("Anchorline.Capstone", "1.0.0"));
builder.Services.AddSingleton(new System.Diagnostics.ActivitySource("Anchorline.Capstone"));

// Cosmos client — RBAC-only (COSMOS_ENDPOINT app setting, no key). Uses the Function
// App's system-assigned managed identity via DefaultAzureCredential.
builder.Services.AddSingleton(sp =>
{
    var endpoint = Environment.GetEnvironmentVariable("COSMOS_ENDPOINT")
        ?? throw new InvalidOperationException("COSMOS_ENDPOINT app setting is required");
    return new CosmosClient(endpoint, new DefaultAzureCredential());
});

builder.Build().Run();
