// AZ-DEV-100 Module 5 — autoscale target with /burn and /consume endpoints.

using Azure.Identity;
using Azure.Messaging.ServiceBus;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/health", () => Results.Ok(new { status = "healthy", timestamp = DateTime.UtcNow }));

app.MapGet("/version", (IConfiguration config) => Results.Ok(new
{
    buildTag = config["AZ_DEV_100_BUILD_TAG"] ?? "unset",
    slotName = Environment.GetEnvironmentVariable("WEBSITE_SLOT_NAME") ?? "not-app-service",
    hostName = Environment.MachineName,
    dotnetVersion = Environment.Version.ToString()
}));

// /burn — spin CPU for N seconds. Use to drive the CpuPercentage metric.
app.MapGet("/burn", (int seconds) =>
{
    var end = DateTime.UtcNow.AddSeconds(Math.Min(Math.Max(seconds, 1), 60));
    long n = 0;
    while (DateTime.UtcNow < end) { n++; if ((n % 1_000_000) == 0) { /* tiny yield */ Thread.SpinWait(1); } }
    return Results.Ok(new { burned = seconds, iterations = n, host = Environment.MachineName });
});

// /consume — pulls one message off the Service Bus queue via Managed Identity.
app.MapGet("/consume", async (IConfiguration config) =>
{
    var ns = Environment.GetEnvironmentVariable("SERVICE_BUS_NAMESPACE");
    var queue = Environment.GetEnvironmentVariable("QUEUE_NAME") ?? "anchorline-orders";
    if (string.IsNullOrWhiteSpace(ns)) return Results.BadRequest(new { error = "SERVICE_BUS_NAMESPACE env not set" });

    await using var client = new ServiceBusClient($"{ns}.servicebus.windows.net", new DefaultAzureCredential());
    await using var receiver = client.CreateReceiver(queue);
    var msg = await receiver.ReceiveMessageAsync(maxWaitTime: TimeSpan.FromSeconds(2));
    if (msg is null) return Results.Ok(new { consumed = false, host = Environment.MachineName });
    await receiver.CompleteMessageAsync(msg);
    return Results.Ok(new { consumed = true, body = msg.Body.ToString(), host = Environment.MachineName });
});

app.MapGet("/", () => Results.Content("Anchorline autoscale target — try /health /version /burn?seconds=30 /consume", "text/plain"));

app.Run();
