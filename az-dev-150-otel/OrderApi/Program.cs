using Azure.Monitor.OpenTelemetry.AspNetCore;

var builder = WebApplication.CreateBuilder(args);

// OTel with Azure Monitor exporter
builder.Services.AddOpenTelemetry().UseAzureMonitor();

builder.Services.AddHttpClient("processor", c =>
{
    var url = Environment.GetEnvironmentVariable("PROCESSOR_URL") ?? "http://localhost:5000";
    c.BaseAddress = new Uri(url);
});

var app = builder.Build();

app.MapGet("/", () => new { app = "order-api-otel", ok = true });

app.MapPost("/orders", async (OrderReq req, IHttpClientFactory http) =>
{
    var order = new { id = Guid.NewGuid().ToString("N")[..12], req.CustomerId, req.Amount, req.ProductId, PlacedUtc = DateTime.UtcNow };
    // Sync call to processor - traceparent auto-propagates
    var client = http.CreateClient("processor");
    var resp = await client.PostAsJsonAsync("/process", order);
    resp.EnsureSuccessStatusCode();
    return Results.Ok(new { orderId = order.id, downstream = await resp.Content.ReadAsStringAsync() });
});

app.Run("http://0.0.0.0:8080");

public record OrderReq(string CustomerId, decimal Amount, string ProductId);
