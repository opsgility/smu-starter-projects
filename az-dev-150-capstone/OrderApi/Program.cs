using Azure.Identity;
using Azure.Messaging.ServiceBus;
using Azure.Monitor.OpenTelemetry.AspNetCore;
using Microsoft.Azure.Cosmos;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddOpenTelemetry().UseAzureMonitor();

var miClientId = builder.Configuration["MI_CLIENT_ID"];
var cosmosEp = builder.Configuration["COSMOS_ENDPOINT"] ?? "";
var sbFqdn = builder.Configuration["SB_NAMESPACE"] ?? "";
var queue = builder.Configuration["SB_QUEUE"] ?? "orders";
var appVersion = builder.Configuration["APP_VERSION"] ?? "v1";

var cred = string.IsNullOrEmpty(miClientId)
    ? new DefaultAzureCredential()
    : new DefaultAzureCredential(new DefaultAzureCredentialOptions { ManagedIdentityClientId = miClientId });

builder.Services.AddSingleton(new CosmosClient(cosmosEp, cred));
builder.Services.AddSingleton(new ServiceBusClient(sbFqdn, cred));

var app = builder.Build();

app.MapGet("/", () => new { app = "anchorline-orderapi", version = appVersion, revision = Environment.GetEnvironmentVariable("CONTAINER_APP_REVISION") });

app.MapPost("/orders", async (OrderReq req, CosmosClient cosmos, ServiceBusClient sbClient) =>
{
    var order = new { id = Guid.NewGuid().ToString("N")[..12], req.CustomerId, req.Amount, req.ProductId, PlacedUtc = DateTime.UtcNow };
    // Save to Cosmos
    var container = cosmos.GetContainer("AnchorlineCapstone", "orders");
    await container.UpsertItemAsync(order, new PartitionKey(req.CustomerId));
    // Publish to Service Bus
    await using var sender = sbClient.CreateSender(queue);
    await sender.SendMessageAsync(new ServiceBusMessage(System.Text.Json.JsonSerializer.Serialize(order)));
    return Results.Ok(new { orderId = order.id, version = appVersion });
});

app.Run("http://0.0.0.0:8080");

public record OrderReq(string CustomerId, decimal Amount, string ProductId);
