// Anchorline capstone — 4-service system with unified OTel to App Insights + SLO instrumentation.
// This is the API-tier program; Web, Worker, Function are companion projects deployed via the ARM template.

using System.Diagnostics;
using System.Diagnostics.Metrics;
using Azure.Identity;
using Azure.Messaging.ServiceBus;
using Microsoft.Azure.Cosmos;
using Azure.Monitor.OpenTelemetry.AspNetCore;
using OpenTelemetry.Resources;
using OpenTelemetry.Trace;
using OpenTelemetry.Metrics;

var builder = WebApplication.CreateBuilder(args);
var sbNs = Environment.GetEnvironmentVariable("SERVICE_BUS_NAMESPACE")!;
var cosmosEndpoint = Environment.GetEnvironmentVariable("COSMOS_ENDPOINT")!;

// SLO instrumentation
var meter = new Meter("Anchorline.Capstone.Orders", "1.0.0");
var slo = meter.CreateHistogram<double>("orders.duration.ms", "ms");

builder.Services.AddOpenTelemetry()
    .ConfigureResource(r => r
        .AddService("anchorline-orders-api", serviceVersion: "1.0.0")
        .AddAttributes(new Dictionary<string, object>
        {
            ["deployment.environment"] = builder.Environment.EnvironmentName,
            ["anchorline.slo.target"]  = "99.5%<500ms",
            ["anchorline.team"]        = "platform"
        }))
    .WithTracing(t => t
        .AddSource("Anchorline.Capstone.*")
        .AddAspNetCoreInstrumentation()
        .AddHttpClientInstrumentation())
    .WithMetrics(m => m
        .AddMeter("Anchorline.Capstone.Orders")
        .AddAspNetCoreInstrumentation())
    .UseAzureMonitor();

builder.Services.AddSingleton(new ServiceBusClient(sbNs, new DefaultAzureCredential()));
builder.Services.AddSingleton(new CosmosClient(cosmosEndpoint, new DefaultAzureCredential()));

var app = builder.Build();
var source = new ActivitySource("Anchorline.Capstone.Orders", "1.0.0");
int cosmosSlowdownMs = 0;

app.MapPost("/orders", async (Order order, ServiceBusClient sb, CosmosClient cos) =>
{
    var sw = Stopwatch.StartNew();
    using var activity = source.StartActivity("Orders.Create");
    activity?.SetTag("order.id", order.Id);
    try
    {
        // Cosmos write with an inducible slowdown for capstone injection.
        var container = cos.GetContainer("Anchorline", "orders");
        await Task.Delay(cosmosSlowdownMs);
        await container.UpsertItemAsync(new { id = order.Id, order.CustomerId, order.Total },
            new PartitionKey(order.CustomerId));

        // Enqueue for fulfillment
        var sender = sb.CreateSender("fulfillment");
        await sender.SendMessageAsync(new ServiceBusMessage(order.Id));

        return Results.Accepted($"/orders/{order.Id}");
    }
    finally
    {
        sw.Stop();
        slo.Record(sw.Elapsed.TotalMilliseconds, new KeyValuePair<string, object?>("route", "/orders"));
    }
});

app.MapPost("/simulate/cosmos-slow/{ms:int}", (int ms) => { cosmosSlowdownMs = ms; return Results.Ok(new { cosmosSlowdownMs }); });
app.MapPost("/simulate/cosmos-heal",          ()      => { cosmosSlowdownMs = 0;   return Results.Ok(new { cosmosSlowdownMs }); });

app.Run();

record Order(string Id, string CustomerId, decimal Total);
