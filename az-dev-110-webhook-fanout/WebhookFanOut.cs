using System.Net;
using System.Text;
using System.Text.Json;
using Azure.Messaging.ServiceBus;
using Azure.Storage.Blobs;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.Cosmos;
using Microsoft.Azure.Functions.Worker;
using Microsoft.Extensions.Logging;

namespace Anchorline.Functions.WebhookFanOut;

public record OrderItem(string sku, int qty);

public record OrderPayload(
    string id,
    string orderId,
    string customerId,
    List<OrderItem> items,
    DateTimeOffset receivedAt);

public class WebhookFanOut
{
    // Order archive lives in its own container so it stays separate from the
    // Functions runtime's `app-package` deployment container.
    private const string ArchiveContainer = "order-payloads";

    private readonly ILogger<WebhookFanOut> _log;
    private readonly CosmosClient _cosmos;
    private readonly BlobServiceClient _blob;
    private readonly ServiceBusClient _sb;
    private readonly string _cosmosDb;
    private readonly string _cosmosContainer;
    private readonly string _sbQueue;

    public WebhookFanOut(
        ILogger<WebhookFanOut> log,
        CosmosClient cosmos,
        BlobServiceClient blob,
        ServiceBusClient sb)
    {
        _log = log;
        _cosmos = cosmos;
        _blob = blob;
        _sb = sb;
        _cosmosDb = Environment.GetEnvironmentVariable("COSMOS_DATABASE") ?? "Anchorline";
        _cosmosContainer = Environment.GetEnvironmentVariable("COSMOS_CONTAINER") ?? "Orders";
        _sbQueue = Environment.GetEnvironmentVariable("SERVICEBUS_QUEUE") ?? "order-notifications";
    }

    /// <summary>
    /// POST /api/webhooks/orders — accepts an order payload and fans it out
    /// to Cosmos (Anchorline.Orders), Blob (order-payloads/orders/{id}.json),
    /// and Service Bus (order-notifications) via SDK-direct writes using MI auth.
    /// </summary>
    [Function("PlaceOrder")]
    public async Task<IActionResult> PlaceOrder(
        [HttpTrigger(AuthorizationLevel.Function, "post", Route = "webhooks/orders")] HttpRequest req)
    {
        var raw = await new StreamReader(req.Body).ReadToEndAsync();
        JsonElement body;
        try
        {
            body = JsonSerializer.Deserialize<JsonElement>(raw);
        }
        catch (JsonException)
        {
            return new BadRequestObjectResult(new { error = "Request body must be JSON." });
        }

        var orderId = body.TryGetProperty("orderId", out var oid) && oid.ValueKind == JsonValueKind.String
            ? oid.GetString()!
            : Guid.NewGuid().ToString();

        var customerId = body.TryGetProperty("customerId", out var cid) && cid.ValueKind == JsonValueKind.String
            ? cid.GetString()!
            : "";

        var items = new List<OrderItem>();
        if (body.TryGetProperty("items", out var itemsEl) && itemsEl.ValueKind == JsonValueKind.Array)
        {
            foreach (var el in itemsEl.EnumerateArray())
            {
                items.Add(new OrderItem(
                    sku: el.TryGetProperty("sku", out var s) && s.ValueKind == JsonValueKind.String
                        ? s.GetString()! : "",
                    qty: el.TryGetProperty("qty", out var q) && q.ValueKind == JsonValueKind.Number
                        ? q.GetInt32() : 1));
            }
        }

        // Cosmos partition key is /id — mirror orderId into id.
        var order = new OrderPayload(
            id: orderId,
            orderId: orderId,
            customerId: customerId,
            items: items,
            receivedAt: DateTimeOffset.UtcNow);

        _log.LogInformation("Fanning out order {OrderId} for customer {Cid} ({Items} items)",
            order.orderId, order.customerId, order.items.Count);

        // 1. Cosmos — Anchorline.Orders
        var container = _cosmos.GetContainer(_cosmosDb, _cosmosContainer);
        await container.UpsertItemAsync(order, new PartitionKey(order.id));

        // 2. Blob — order-payloads/orders/{orderId}.json
        var archive = _blob.GetBlobContainerClient(ArchiveContainer);
        await archive.CreateIfNotExistsAsync();
        var blobClient = archive.GetBlobClient($"orders/{order.orderId}.json");
        var json = JsonSerializer.Serialize(order);
        using (var ms = new MemoryStream(Encoding.UTF8.GetBytes(json)))
        {
            await blobClient.UploadAsync(ms, overwrite: true);
        }

        // 3. Service Bus — order-notifications
        var sender = _sb.CreateSender(_sbQueue);
        try
        {
            var message = new ServiceBusMessage(JsonSerializer.Serialize(new
            {
                orderId = order.orderId,
                customerId = order.customerId,
                itemCount = order.items.Count,
                receivedAt = order.receivedAt,
            }))
            {
                ContentType = "application/json",
                Subject = "OrderPlaced",
            };
            await sender.SendMessageAsync(message);
        }
        finally
        {
            await sender.DisposeAsync();
        }

        return new AcceptedResult(
            $"/api/webhooks/orders/{order.orderId}",
            new { received = order.orderId });
    }

    /// <summary>
    /// GET /api/webhooks/orders/{orderId} — reads back the archived order from Cosmos.
    /// Doubles as a data-plane verification hook for tests (since
    /// `az cosmosdb sql query` was removed in az CLI 2.75+).
    /// </summary>
    [Function("GetOrder")]
    public async Task<IActionResult> GetOrder(
        [HttpTrigger(AuthorizationLevel.Function, "get", Route = "webhooks/orders/{orderId}")] HttpRequest req,
        string orderId)
    {
        var container = _cosmos.GetContainer(_cosmosDb, _cosmosContainer);
        try
        {
            var response = await container.ReadItemAsync<OrderPayload>(orderId, new PartitionKey(orderId));
            return new OkObjectResult(response.Resource);
        }
        catch (CosmosException ex) when (ex.StatusCode == HttpStatusCode.NotFound)
        {
            return new NotFoundObjectResult(new { orderId, message = "Not found in Anchorline.Orders." });
        }
    }
}
