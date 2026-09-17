// Anchorline Orders — custom telemetry with ActivitySource, Meter, Counter, Histogram.
// Emits domain-level signals so operators can answer business questions from App Insights.

using System.Diagnostics;
using System.Diagnostics.Metrics;
using Azure.Monitor.OpenTelemetry.AspNetCore;
using OpenTelemetry.Resources;
using OpenTelemetry.Trace;
using OpenTelemetry.Metrics;

var builder = WebApplication.CreateBuilder(args);

// Anchorline domain instrumentation surface.
var ordersSource = new ActivitySource("Anchorline.Orders", "1.0.0");
var meter = new Meter("Anchorline.Orders", "1.0.0");
var received = meter.CreateCounter<long>("orders.received.total",
    unit: "{order}", description: "Total orders received by the Orders API.");
var processingDuration = meter.CreateHistogram<double>("orders.processing.duration.ms",
    unit: "ms", description: "Wall-clock time to validate + persist an order.");
var validationFailures = meter.CreateCounter<long>("orders.validation.failures.total",
    unit: "{failure}", description: "Orders rejected by validation.");
long inflight = 0;
meter.CreateObservableGauge("orders.inflight",
    () => Interlocked.Read(ref inflight),
    unit: "{order}", description: "Orders currently being processed.");

builder.Services.AddOpenTelemetry()
    .ConfigureResource(r => r.AddService("anchorline-orders", serviceVersion: "1.0.0"))
    .WithTracing(t => t
        .AddSource("Anchorline.Orders")
        .AddAspNetCoreInstrumentation()
        .AddHttpClientInstrumentation())
    .WithMetrics(m => m
        .AddMeter("Anchorline.Orders")
        .AddAspNetCoreInstrumentation())
    .UseAzureMonitor();

var app = builder.Build();

app.MapPost("/orders", async (OrderRequest req, ILogger<Program> log) =>
{
    received.Add(1,
        new KeyValuePair<string, object?>("channel", req.Channel),
        new KeyValuePair<string, object?>("region",  req.Region));
    Interlocked.Increment(ref inflight);

    using var activity = ordersSource.StartActivity("Orders.Validate");
    activity?.SetTag("order.id",         req.OrderId);
    activity?.SetTag("order.customerId", req.CustomerId);
    activity?.SetTag("order.total",      (double)req.TotalAmount);

    var sw = Stopwatch.StartNew();
    try
    {
        if (req.TotalAmount <= 0)
        {
            validationFailures.Add(1,
                new KeyValuePair<string, object?>("reason", "non-positive-total"));
            activity?.AddEvent(new ActivityEvent("orders.validation.failed",
                tags: new ActivityTagsCollection { { "reason", "non-positive-total" } }));
            activity?.SetStatus(ActivityStatusCode.Error, "invalid total");
            return Results.BadRequest(new { error = "total must be > 0" });
        }

        await Task.Delay(25); // simulate persistence
        log.LogInformation("Order {OrderId} for {CustomerId} accepted at {Total}",
            req.OrderId, req.CustomerId, req.TotalAmount);
        return Results.Accepted($"/orders/{req.OrderId}", new { req.OrderId, status = "Accepted" });
    }
    finally
    {
        sw.Stop();
        processingDuration.Record(sw.Elapsed.TotalMilliseconds,
            new KeyValuePair<string, object?>("route", "/orders"));
        Interlocked.Decrement(ref inflight);
    }
});

app.Run();

record OrderRequest(string OrderId, string CustomerId, decimal TotalAmount,
                    string Channel = "web", string Region = "US");
