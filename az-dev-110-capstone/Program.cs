using System.Diagnostics.Metrics;
using Microsoft.Azure.Functions.Worker;
using Microsoft.Azure.Functions.Worker.Builder;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

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

builder.Build().Run();
