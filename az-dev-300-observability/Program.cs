using System.Diagnostics;
using Azure.Monitor.OpenTelemetry.AspNetCore;
using OpenTelemetry.Trace;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddOpenTelemetry()
    .UseAzureMonitor(o =>
    {
        o.ConnectionString = builder.Configuration["ApplicationInsights:ConnectionString"];
        o.SamplingRatio = 0.2f;
    })
    .WithTracing(t => t.AddSource("TaskForge.Custom"));

var app = builder.Build();
var activitySource = new ActivitySource("TaskForge.Custom");

app.MapGet("/", () =>
{
    using var activity = activitySource.StartActivity("HomePage.Render");
    activity?.SetTag("taskforge.demo", true);
    return "TaskForge observability demo — trace visible in App Insights";
});

app.MapGet("/error", () =>
{
    throw new InvalidOperationException("Simulated failure for burn-rate testing");
});

app.Run();
