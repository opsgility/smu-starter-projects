// Anchorline Outdoors — first OpenTelemetry-to-Azure-Monitor instrumentation.
// This minimal API emits traces, metrics and logs; the Azure Monitor Distro exports them to
// the App Insights connection string in APPLICATIONINSIGHTS_CONNECTION_STRING.

using System.Diagnostics;
using System.Diagnostics.Metrics;
using Azure.Monitor.OpenTelemetry.AspNetCore;
using OpenTelemetry.Resources;
using OpenTelemetry.Trace;
using OpenTelemetry.Metrics;

var builder = WebApplication.CreateBuilder(args);

// Named ActivitySource + Meter to prove BOTH auto and manual signals land in App Insights.
var activitySource = new ActivitySource("Anchorline.Otel.Foundations", "1.0.0");
var meter = new Meter("Anchorline.Otel.Foundations", "1.0.0");
var requestsCounter = meter.CreateCounter<long>("anchorline.foundations.requests.total",
    unit: "{request}", description: "Total requests handled by the foundations demo.");

builder.Services.AddOpenTelemetry()
    .ConfigureResource(r => r
        .AddService("anchorline-otel-foundations", serviceVersion: "1.0.0")
        .AddAttributes(new Dictionary<string, object>
        {
            ["deployment.environment"] = builder.Environment.EnvironmentName,
            ["anchorline.team"]        = "platform"
        }))
    .WithTracing(t => t
        .AddSource("Anchorline.Otel.Foundations")
        .AddAspNetCoreInstrumentation()
        .AddHttpClientInstrumentation()
        .AddSqlClientInstrumentation())
    .WithMetrics(m => m
        .AddMeter("Anchorline.Otel.Foundations")
        .AddAspNetCoreInstrumentation()
        .AddHttpClientInstrumentation())
    .UseAzureMonitor();  // reads APPLICATIONINSIGHTS_CONNECTION_STRING from env

var app = builder.Build();

app.MapGet("/", () => "Anchorline OTel foundations — try /orders and /orders/{id}");

app.MapGet("/orders", (ILogger<Program> log) =>
{
    using var activity = activitySource.StartActivity("Orders.List");
    activity?.SetTag("orders.count", 3);
    requestsCounter.Add(1, new KeyValuePair<string, object?>("route", "/orders"));
    log.LogInformation("Listing {Count} orders for anonymous browse", 3);
    return new[]
    {
        new { id = "ord-001", customer = "cust-42", total = 249.50m },
        new { id = "ord-002", customer = "cust-42", total =  59.00m },
        new { id = "ord-003", customer = "cust-77", total = 122.10m }
    };
});

app.MapGet("/orders/{id}", (string id, ILogger<Program> log) =>
{
    using var activity = activitySource.StartActivity("Orders.GetById");
    activity?.SetTag("order.id", id);
    requestsCounter.Add(1, new KeyValuePair<string, object?>("route", "/orders/{id}"));
    log.LogInformation("Fetching order {OrderId}", id);
    return Results.Ok(new { id, customer = "cust-42", total = 249.50m });
});

app.MapGet("/simulate/error", () =>
{
    using var activity = activitySource.StartActivity("Simulate.Error");
    activity?.SetStatus(ActivityStatusCode.Error, "Simulated failure for OTel demo");
    throw new InvalidOperationException("Simulated Anchorline error — traces should show this.");
});

app.Run();
