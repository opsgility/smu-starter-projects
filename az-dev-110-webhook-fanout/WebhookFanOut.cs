using System.Text.Json;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.Functions.Worker;
using Microsoft.Extensions.Logging;

namespace Anchorline.Functions.WebhookFanOut;

public record OrderPayload(string id, string customerId, string sku, decimal total, DateTimeOffset receivedAt);

public class FanOutOutputs
{
    [CosmosDBOutput(databaseName: "Anchorline", containerName: "Orders", Connection = "CosmosConnection")]
    public required OrderPayload OrderDoc { get; set; }

    [BlobOutput("order-payloads/{OrderDoc.id}.json", Connection = "AnchorlineStorage")]
    public required string BlobPayload { get; set; }

    [ServiceBusOutput("order-notifications", Connection = "ServiceBusConnection")]
    public required string NotificationBody { get; set; }

    [HttpResult]
    public required IActionResult HttpResponse { get; set; }
}

public class WebhookFanOut
{
    private readonly ILogger<WebhookFanOut> _log;
    public WebhookFanOut(ILogger<WebhookFanOut> log) => _log = log;

    [Function("HandleOrderWebhook")]
    public async Task<FanOutOutputs> Run(
        [HttpTrigger(AuthorizationLevel.Function, "post", Route = "webhook/orders")] HttpRequest req)
    {
        var raw = await new StreamReader(req.Body).ReadToEndAsync();
        var body = JsonSerializer.Deserialize<JsonElement>(raw);

        var order = new OrderPayload(
            id: body.GetProperty("id").GetString() ?? Guid.NewGuid().ToString(),
            customerId: body.GetProperty("customerId").GetString() ?? "",
            sku: body.GetProperty("sku").GetString() ?? "",
            total: body.GetProperty("total").GetDecimal(),
            receivedAt: DateTimeOffset.UtcNow);

        _log.LogInformation("Fanning out order {Id} for customer {Cid}", order.id, order.customerId);

        return new FanOutOutputs
        {
            OrderDoc = order,
            BlobPayload = JsonSerializer.Serialize(order),
            NotificationBody = order.id,
            HttpResponse = new AcceptedResult($"/api/webhook/orders/{order.id}", new { received = order.id })
        };
    }
}
