using Dapr.Client;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddDaprClient();
var app = builder.Build();

app.MapGet("/", () => new { app = "order-api", ok = true });

app.MapPost("/orders", async (Order req, DaprClient dapr) =>
{
    var order = req with { Id = Guid.NewGuid().ToString("N")[..12], PlacedUtc = DateTime.UtcNow };
    // Publish to Dapr pub/sub - the sidecar delivers to Service Bus
    await dapr.PublishEventAsync("eventbus", "OrderCreated", order);
    return Results.Ok(new { published = order.Id });
});

app.Run("http://0.0.0.0:8080");

public record Order(string CustomerId, decimal Amount, string ProductId, string Id = "", DateTime? PlacedUtc = null);
