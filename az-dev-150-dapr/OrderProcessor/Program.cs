using Dapr;
using Dapr.Client;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddDaprClient();
builder.Services.AddControllers().AddDapr();

var app = builder.Build();

// Required for Dapr topic subscription discovery
app.UseCloudEvents();
app.MapSubscribeHandler();

app.MapGet("/", () => new { app = "order-processor", ok = true });

app.MapPost("/orders/created",
    [Topic("eventbus", "OrderCreated")]
    async (OrderEvent evt, DaprClient dapr, ILogger<Program> log) =>
{
    log.LogInformation("Received OrderCreated {id} customer={cust}", evt.Id, evt.CustomerId);
    // Persist via Dapr state store (Cosmos backend defined by component)
    await dapr.SaveStateAsync("statestore", $"order-{evt.Id}", evt);
    return Results.Ok();
});

app.MapGet("/orders/{id}", async (string id, DaprClient dapr) =>
{
    var order = await dapr.GetStateAsync<OrderEvent>("statestore", $"order-{id}");
    return order is null ? Results.NotFound() : Results.Ok(order);
});

app.Run("http://0.0.0.0:8080");

public record OrderEvent(string Id, string CustomerId, decimal Amount, string ProductId, DateTime PlacedUtc);
