using System.Diagnostics;
using System.Diagnostics.Metrics;
using Azure.Monitor.OpenTelemetry.AspNetCore;

var builder = WebApplication.CreateBuilder(args);

// EXERCISE 1 will uncomment this to enable code-based OTel:
// builder.Services.AddOpenTelemetry().UseAzureMonitor();

var app = builder.Build();

var meter = new Meter("Anchorline.Storefront", "1.0.0");
var checkoutCounter = meter.CreateCounter<int>("anchorline.checkout.requests");
var checkoutDuration = meter.CreateHistogram<double>("anchorline.checkout.duration_ms");

var activitySource = new ActivitySource("Anchorline.Storefront");

app.MapGet("/health", () => Results.Ok(new { status = "ok" }));

app.MapGet("/version", (IConfiguration config) => Results.Ok(new
{
    build = config["AZ_DEV_100_BUILD_TAG"] ?? "unknown"
}));

app.MapGet("/fast", async () =>
{
    await Task.Delay(Random.Shared.Next(20, 60));
    return Results.Ok(new { latencyClass = "fast" });
});

app.MapGet("/slow", async () =>
{
    var d = Random.Shared.Next(800, 1500);
    await Task.Delay(d);
    return Results.Ok(new { latencyClass = "slow", intendedMs = d });
});

app.MapGet("/checkout", async () =>
{
    using var activity = activitySource.StartActivity("checkout");
    var start = Stopwatch.GetTimestamp();

    using (activitySource.StartActivity("inventory-lookup"))
    {
        await Task.Delay(Random.Shared.Next(100, 200));
    }
    using (activitySource.StartActivity("payment-authorize"))
    {
        await Task.Delay(Random.Shared.Next(400, 800));
    }
    using (activitySource.StartActivity("order-persist"))
    {
        await Task.Delay(Random.Shared.Next(50, 150));
    }

    if (Random.Shared.NextDouble() < 0.05)
    {
        throw new InvalidOperationException("payment authorization declined");
    }

    var elapsed = Stopwatch.GetElapsedTime(start).TotalMilliseconds;
    checkoutCounter.Add(1);
    checkoutDuration.Record(elapsed);
    return Results.Ok(new { status = "confirmed", elapsedMs = elapsed });
});

app.MapGet("/fail", () => Results.Problem("intentional 500 for alert testing"));

app.Run();
