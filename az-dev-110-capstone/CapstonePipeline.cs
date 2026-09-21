using System.Diagnostics;
using System.Diagnostics.Metrics;
using System.Net;
using System.Text.Json;
using Microsoft.Azure.Cosmos;
using Microsoft.Azure.Functions.Worker;
using Microsoft.Azure.Functions.Worker.Http;
using Microsoft.DurableTask;
using Microsoft.DurableTask.Client;
using Microsoft.Extensions.Logging;

namespace Anchorline.Functions.Capstone;

public record OrderRequest(string OrderId, string CustomerId, string Sku, int Quantity, decimal Total);
public record OrderRecord
{
    public required string id { get; set; }
    public required string CustomerId { get; set; }
    public required string Sku { get; set; }
    public required int Quantity { get; set; }
    public required decimal Total { get; set; }
    public required string Status { get; set; }
    public required string ProcessedAt { get; set; }
    public required string OrchestrationInstanceId { get; set; }
}

public class CapstoneApi
{
    private readonly Counter<int> _ordersReceived;
    public CapstoneApi(Meter meter)
    {
        _ordersReceived = meter.CreateCounter<int>("anchorline.capstone.orders_received");
    }

    [Function("StartOrder")]
    public async Task<HttpResponseData> StartOrder(
        [HttpTrigger(AuthorizationLevel.Function, "post", Route = "orders")] HttpRequestData req,
        [DurableClient] DurableTaskClient client,
        FunctionContext ctx)
    {
        var log = ctx.GetLogger<CapstoneApi>();
        var opts = new JsonSerializerOptions { PropertyNameCaseInsensitive = true };
        var order = await JsonSerializer.DeserializeAsync<OrderRequest>(req.Body, opts);
        if (order is null)
        {
            var bad = req.CreateResponse(HttpStatusCode.BadRequest);
            await bad.WriteStringAsync("invalid body");
            return bad;
        }
        _ordersReceived.Add(1);
        var instanceId = await client.ScheduleNewOrchestrationInstanceAsync(nameof(OrderPipelineOrchestrator), order);
        log.LogInformation("StartOrder {OrderId} -> orchestration {Id}", order.OrderId, instanceId);
        var statusUri = $"{req.Url.GetLeftPart(UriPartial.Authority)}/api/orders/{instanceId}";
        var resp = req.CreateResponse(HttpStatusCode.Accepted);
        resp.Headers.Add("Location", statusUri);
        await resp.WriteAsJsonAsync(new
        {
            instanceId,
            orderId = order.OrderId,
            statusQueryGetUri = statusUri
        });
        return resp;
    }

    [Function("GetOrderStatus")]
    public async Task<HttpResponseData> Status(
        [HttpTrigger(AuthorizationLevel.Function, "get", Route = "orders/{instanceId}")] HttpRequestData req,
        string instanceId,
        [DurableClient] DurableTaskClient client)
    {
        var m = await client.GetInstanceAsync(instanceId, getInputsAndOutputs: true);
        if (m is null)
        {
            return req.CreateResponse(HttpStatusCode.NotFound);
        }
        var ok = req.CreateResponse(HttpStatusCode.OK);
        await ok.WriteAsJsonAsync(new
        {
            instanceId,
            runtimeStatus = m.RuntimeStatus.ToString(),
            m.CreatedAt,
            m.LastUpdatedAt,
            output = m.SerializedOutput
        });
        return ok;
    }
}

public class OrderPipelineOrchestrator
{
    [Function(nameof(OrderPipelineOrchestrator))]
    public async Task<string> Run([OrchestrationTrigger] TaskOrchestrationContext ctx)
    {
        var order = ctx.GetInput<OrderRequest>()!;
        var validated = await ctx.CallActivityAsync<bool>(nameof(OrderPipelineActivities.ValidateActivity), order);
        if (!validated) return "Invalid";
        var record = new OrderRecord
        {
            id = order.OrderId,
            CustomerId = order.CustomerId,
            Sku = order.Sku,
            Quantity = order.Quantity,
            Total = order.Total,
            Status = "Confirmed",
            ProcessedAt = ctx.CurrentUtcDateTime.ToString("o"),
            OrchestrationInstanceId = ctx.InstanceId
        };
        await ctx.CallActivityAsync(nameof(OrderPipelineActivities.WriteToCosmosActivity), record);
        return "Confirmed";
    }
}

public class OrderPipelineActivities
{
    private readonly Histogram<double> _validationLatency;
    private readonly Counter<int> _cosmosWrites;
    private readonly ActivitySource _activitySource;
    private readonly ILogger<OrderPipelineActivities> _log;
    private readonly CosmosClient _cosmos;
    private readonly string _databaseName;
    private readonly string _containerName;

    public OrderPipelineActivities(
        Meter meter,
        ActivitySource activitySource,
        ILogger<OrderPipelineActivities> log,
        CosmosClient cosmos)
    {
        _validationLatency = meter.CreateHistogram<double>("anchorline.capstone.validation_ms");
        _cosmosWrites = meter.CreateCounter<int>("anchorline.capstone.cosmos_writes");
        _activitySource = activitySource;
        _log = log;
        _cosmos = cosmos;
        _databaseName = Environment.GetEnvironmentVariable("COSMOS_DATABASE") ?? "Anchorline";
        _containerName = Environment.GetEnvironmentVariable("COSMOS_CONTAINER") ?? "Orders";
    }

    [Function(nameof(ValidateActivity))]
    public async Task<bool> ValidateActivity([ActivityTrigger] OrderRequest order)
    {
        using var activity = _activitySource.StartActivity("validate-order");
        var sw = Stopwatch.StartNew();
        await Task.Delay(Random.Shared.Next(30, 80));
        _validationLatency.Record(sw.Elapsed.TotalMilliseconds);
        var ok = order.Quantity > 0 && order.Total > 0;
        _log.LogInformation("Validate order {OrderId} ok={Ok}", order.OrderId, ok);
        return ok;
    }

    [Function(nameof(WriteToCosmosActivity))]
    public async Task<OrderRecord> WriteToCosmosActivity([ActivityTrigger] OrderRecord record)
    {
        using var activity = _activitySource.StartActivity("cosmos-write");
        var container = _cosmos.GetContainer(_databaseName, _containerName);
        await container.UpsertItemAsync(record, new PartitionKey(record.id));
        _cosmosWrites.Add(1);
        _log.LogInformation("Cosmos write {Id}", record.id);
        return record;
    }
}
