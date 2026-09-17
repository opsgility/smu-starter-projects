using System.Diagnostics;
using Azure.Monitor.OpenTelemetry.AspNetCore;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddOpenTelemetry().UseAzureMonitor();

var app = builder.Build();
var activitySource = new ActivitySource("Anchorline.Processor");

app.MapGet("/", () => new { app = "order-processor-otel", ok = true });

app.MapPost("/process", async (Order order) =>
{
    // A custom activity - shows in the trace as a distinct span
    using var act = activitySource.StartActivity("simulate-persist-cosmos");
    act?.SetTag("order.id", order.id);
    act?.SetTag("order.amount", order.amount);

    // Simulate variable Cosmos latency
    await Task.Delay(Random.Shared.Next(50, 300));

    return new { received = order.id, processed = true };
});

app.Run("http://0.0.0.0:8080");

public record Order(string id, string customerId, decimal amount, string productId, DateTime placedUtc);
