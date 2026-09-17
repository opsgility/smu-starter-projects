// Anchorline end-to-end tracing — HTTP intake → Service Bus → Function → Cosmos → downstream HTTP.
// This starter is the HTTP intake side; the SB-triggered Function lives in the Function App the ARM template deploys.

using System.Diagnostics;
using Azure.Identity;
using Azure.Messaging.ServiceBus;
using Azure.Monitor.OpenTelemetry.AspNetCore;
using OpenTelemetry.Resources;
using OpenTelemetry.Trace;
using OpenTelemetry.Metrics;

var builder = WebApplication.CreateBuilder(args);
var sbNs = Environment.GetEnvironmentVariable("SERVICE_BUS_NAMESPACE")!;   // e.g. sb-anchor-e2e-abc123.servicebus.windows.net
var queue = Environment.GetEnvironmentVariable("SERVICE_BUS_QUEUE") ?? "orders";

builder.Services.AddOpenTelemetry()
    .ConfigureResource(r => r.AddService("anchorline-e2e-intake", serviceVersion: "1.0.0"))
    .WithTracing(t => t
        .AddSource("Azure.*")
        .AddSource("Anchorline.E2E")
        .AddAspNetCoreInstrumentation()
        .AddHttpClientInstrumentation())
    .WithMetrics(m => m.AddAspNetCoreInstrumentation())
    .UseAzureMonitor();

builder.Services.AddSingleton(new ServiceBusClient(sbNs, new DefaultAzureCredential()));

var app = builder.Build();
var source = new ActivitySource("Anchorline.E2E", "1.0.0");

app.MapPost("/orders", async (Order order, ServiceBusClient sb) =>
{
    using var activity = source.StartActivity("Intake.EnqueueOrder");
    activity?.SetTag("order.id", order.Id);
    activity?.SetTag("order.customerId", order.CustomerId);

    var sender = sb.CreateSender(queue);
    var msg = new ServiceBusMessage(System.Text.Json.JsonSerializer.Serialize(order))
    {
        ContentType = "application/json"
    };
    // The SB SDK auto-propagates traceparent as an ApplicationProperty; the downstream Function
    // sees the same TraceId when it dequeues.
    await sender.SendMessageAsync(msg);
    return Results.Accepted($"/orders/{order.Id}");
});

app.Run();

record Order(string Id, string CustomerId, decimal Total);
