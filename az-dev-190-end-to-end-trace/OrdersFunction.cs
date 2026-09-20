// Companion Function code — deploy separately to the pre-provisioned Function App.
// Triggered by the same SB queue; writes to Cosmos + calls a downstream HTTP endpoint.
// Because OTel + SB SDK auto-propagate traceparent, the same trace surfaces on this hop.
using System.Diagnostics;
using Azure.Identity;
using Microsoft.Azure.Functions.Worker;
using Microsoft.Extensions.Logging;
using Microsoft.Azure.Cosmos;

namespace Anchorline.E2eTrace;

public class OrdersFunction
{
    private static readonly ActivitySource Source = new("Anchorline.E2E.Function", "1.0.0");
    private readonly HttpClient _http;
    private readonly CosmosClient _cosmos;
    private readonly ILogger<OrdersFunction> _log;

    public OrdersFunction(IHttpClientFactory hcf, ILogger<OrdersFunction> log)
    {
        _http = hcf.CreateClient();
        _cosmos = new CosmosClient(Environment.GetEnvironmentVariable("COSMOS_ENDPOINT"), new DefaultAzureCredential());
        _log = log;
    }

    [Function("ProcessOrder")]
    public async Task Run([ServiceBusTrigger("orders", Connection = "ServiceBus")] string body, FunctionContext ctx)
    {
        using var activity = Source.StartActivity("Function.ProcessOrder");
        var order = System.Text.Json.JsonSerializer.Deserialize<Order>(body)!;
        activity?.SetTag("order.id", order.Id);

        var container = _cosmos.GetContainer("Anchorline", "orders");
        await container.UpsertItemAsync(new { id = order.Id, order.CustomerId, order.Total },
            new PartitionKey(order.CustomerId));
        activity?.AddEvent(new ActivityEvent("cosmos.upserted"));

        // Downstream HTTP call — auto-instrumentation continues the same TraceId.
        await _http.PostAsync($"https://{Environment.GetEnvironmentVariable("DOWNSTREAM_HOST")}/notify",
            new StringContent(order.Id));
    }

    public record Order(string Id, string CustomerId, decimal Total);
}
