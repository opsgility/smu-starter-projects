using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.Functions.Worker;
using Microsoft.DurableTask;
using Microsoft.DurableTask.Client;
using Microsoft.Extensions.Logging;

namespace Anchorline.Functions.DurableOrders;

public record Order(string OrderId, string CustomerId, string Sku, int Quantity, decimal Total);
public record OrderResult(string OrderId, string Status, string? Reason);

public class OrderApi
{
    [Function("StartOrderProcess")]
    public async Task<IActionResult> Start(
        [HttpTrigger(AuthorizationLevel.Function, "post", Route = "orders")] HttpRequest req,
        [DurableClient] DurableTaskClient client,
        ILogger<OrderApi> log)
    {
        var order = await System.Text.Json.JsonSerializer.DeserializeAsync<Order>(req.Body);
        if (order is null) return new BadRequestObjectResult("invalid body");

        var instanceId = await client.ScheduleNewOrchestrationInstanceAsync(nameof(OrderOrchestrator), order);
        log.LogInformation("Started orchestration {InstanceId} for order {OrderId}", instanceId, order.OrderId);
        return new OkObjectResult(new { instanceId, orderId = order.OrderId });
    }

    [Function("GetOrderStatus")]
    public async Task<IActionResult> Status(
        [HttpTrigger(AuthorizationLevel.Function, "get", Route = "orders/{instanceId}")] HttpRequest req,
        string instanceId,
        [DurableClient] DurableTaskClient client)
    {
        var metadata = await client.GetInstanceAsync(instanceId, getInputsAndOutputs: true);
        if (metadata is null) return new NotFoundObjectResult(new { instanceId });
        return new OkObjectResult(new
        {
            instanceId,
            metadata.RuntimeStatus,
            createdAt = metadata.CreatedAt,
            lastUpdatedAt = metadata.LastUpdatedAt,
            input = metadata.SerializedInput,
            output = metadata.SerializedOutput
        });
    }

    [Function("ApproveOrder")]
    public async Task<IActionResult> Approve(
        [HttpTrigger(AuthorizationLevel.Function, "post", Route = "orders/{instanceId}/approve")] HttpRequest req,
        string instanceId,
        [DurableClient] DurableTaskClient client)
    {
        var body = await new StreamReader(req.Body).ReadToEndAsync();
        var approved = body.Contains("true", StringComparison.OrdinalIgnoreCase);
        await client.RaiseEventAsync(instanceId, "ApprovalReceived", approved);
        return new OkObjectResult(new { instanceId, sentApproval = approved });
    }
}

public class OrderOrchestrator
{
    [Function(nameof(OrderOrchestrator))]
    public async Task<OrderResult> Run([OrchestrationTrigger] TaskOrchestrationContext ctx)
    {
        var order = ctx.GetInput<Order>()!;
        var log = ctx.CreateReplaySafeLogger<OrderOrchestrator>();

        log.LogInformation("Validating stock for {OrderId}", order.OrderId);
        var inStock = await ctx.CallActivityAsync<bool>(nameof(OrderActivities.ValidateStockActivity), order);
        if (!inStock) return new OrderResult(order.OrderId, "OutOfStock", "no inventory");

        log.LogInformation("Charging card for {OrderId}", order.OrderId);
        var charged = await ctx.CallActivityAsync<bool>(nameof(OrderActivities.ChargeCardActivity), order);
        if (!charged) return new OrderResult(order.OrderId, "PaymentFailed", "card declined");

        if (order.Total > 10_000m)
        {
            log.LogInformation("High-value order {OrderId} — waiting for manager approval", order.OrderId);
            using var cts = new CancellationTokenSource();
            var approvalTask = ctx.WaitForExternalEvent<bool>("ApprovalReceived", TimeSpan.FromDays(3), cts.Token);
            var timeoutTask = ctx.CreateTimer(ctx.CurrentUtcDateTime.AddDays(3), CancellationToken.None);
            var winner = await Task.WhenAny(approvalTask, timeoutTask);
            if (winner == timeoutTask)
            {
                return new OrderResult(order.OrderId, "TimedOut", "no manager approval in 3 days");
            }
            cts.Cancel();
            if (!approvalTask.Result)
            {
                return new OrderResult(order.OrderId, "Rejected", "manager rejected");
            }
        }

        log.LogInformation("Fanning out fulfillment for {OrderId}", order.OrderId);
        var fanOut = new[]
        {
            ctx.CallActivityAsync(nameof(OrderActivities.NotifyWarehouseActivity), order),
            ctx.CallActivityAsync(nameof(OrderActivities.BookShippingActivity), order),
            ctx.CallActivityAsync(nameof(OrderActivities.SendEmailActivity), order)
        };
        await Task.WhenAll(fanOut);

        return new OrderResult(order.OrderId, "Confirmed", null);
    }
}

public class OrderActivities
{
    private readonly ILogger<OrderActivities> _log;
    public OrderActivities(ILogger<OrderActivities> log) => _log = log;

    [Function(nameof(ValidateStockActivity))]
    public async Task<bool> ValidateStockActivity([ActivityTrigger] Order order)
    {
        _log.LogInformation("Validating stock for {Sku} qty {Qty}", order.Sku, order.Quantity);
        await Task.Delay(200);
        return order.Quantity <= 100;
    }

    [Function(nameof(ChargeCardActivity))]
    public async Task<bool> ChargeCardActivity([ActivityTrigger] Order order)
    {
        _log.LogInformation("Charging card for {OrderId} total {Total:C}", order.OrderId, order.Total);
        await Task.Delay(300);
        return order.Total < 100_000m;
    }

    [Function(nameof(NotifyWarehouseActivity))]
    public async Task NotifyWarehouseActivity([ActivityTrigger] Order order)
    {
        _log.LogInformation("Notifying warehouse for {OrderId}", order.OrderId);
        await Task.Delay(150);
    }

    [Function(nameof(BookShippingActivity))]
    public async Task BookShippingActivity([ActivityTrigger] Order order)
    {
        _log.LogInformation("Booking shipping for {OrderId}", order.OrderId);
        await Task.Delay(200);
    }

    [Function(nameof(SendEmailActivity))]
    public async Task SendEmailActivity([ActivityTrigger] Order order)
    {
        _log.LogInformation("Sending confirmation email to customer {Cid}", order.CustomerId);
        await Task.Delay(100);
    }
}
