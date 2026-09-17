using System.Diagnostics;
using Azure.Monitor.OpenTelemetry.AspNetCore;
using OpenTelemetry.Resources;
using OpenTelemetry.Trace;
using OpenTelemetry.Metrics;

var builder = WebApplication.CreateBuilder(args);
var workerBase = Environment.GetEnvironmentVariable("WORKER_BASE_URL") ?? "http://localhost:5003";

builder.Services.AddOpenTelemetry()
    .ConfigureResource(r => r.AddService("anchorline-api", serviceVersion: "1.0.0"))
    .WithTracing(t => t.AddAspNetCoreInstrumentation().AddHttpClientInstrumentation().AddSqlClientInstrumentation())
    .WithMetrics(m => m.AddAspNetCoreInstrumentation().AddHttpClientInstrumentation())
    .UseAzureMonitor();

builder.Services.AddHttpClient("worker", c => c.BaseAddress = new Uri(workerBase));

var app = builder.Build();
var source = new ActivitySource("Anchorline.Api", "1.0.0");

app.MapPost("/orders", async (IHttpClientFactory hcf) =>
{
    // TenantId flows in automatically via W3C baggage.
    var tenantId = Baggage.GetBaggage("TenantId") ?? "unknown";
    using var activity = source.StartActivity("Api.CreateOrder");
    activity?.SetTag("tenant.id", tenantId);
    activity?.SetTag("order.id", "ord-" + Random.Shared.Next(1000, 9999));

    // Downstream to Worker for fulfillment
    var client = hcf.CreateClient("worker");
    await client.PostAsync("/fulfill", null);

    return Results.Ok(new { id = activity?.GetTagItem("order.id"), tenant = tenantId });
});

app.Run("http://0.0.0.0:5002");
