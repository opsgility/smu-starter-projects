// Anchorline Orders — deliberate hot path so the Profiler snapshot shows an easy win.
// Endpoint /report/full serializes a 5000-item catalog and instantiates a fresh
// JsonSerializerOptions per request; Profiler will flag both allocations.

using System.Text.Json;
using Azure.Monitor.OpenTelemetry.AspNetCore;
using OpenTelemetry.Resources;
using OpenTelemetry.Trace;
using OpenTelemetry.Metrics;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddOpenTelemetry()
    .ConfigureResource(r => r.AddService("anchorline-orders-profiler", serviceVersion: "1.0.0"))
    .WithTracing(t => t.AddAspNetCoreInstrumentation())
    .WithMetrics(m => m.AddAspNetCoreInstrumentation())
    .UseAzureMonitor();

var app = builder.Build();

var catalog = Enumerable.Range(1, 5000)
    .Select(i => new Product($"prod-{i:D5}", $"Anchorline Product {i}",
        i * 1.5m, Enumerable.Range(1, 10).Select(k => $"tag-{k}").ToArray()))
    .ToArray();

// Anti-pattern on purpose: options constructed per request; catalog re-materialized.
app.MapGet("/report/full", () =>
{
    var opts = new JsonSerializerOptions { WriteIndented = true, PropertyNamingPolicy = JsonNamingPolicy.CamelCase };
    var snap = catalog.Select(p => new { p.Id, p.Name, p.Price, tags = p.Tags.ToList() }).ToArray();
    var json = JsonSerializer.Serialize(snap, opts);
    return Results.Text(json, "application/json");
});

// Fixed variant — SAME behavior, cached options + no ToList().
var cached = new JsonSerializerOptions { WriteIndented = true, PropertyNamingPolicy = JsonNamingPolicy.CamelCase };
app.MapGet("/report/full-fixed", () =>
{
    var json = JsonSerializer.Serialize(catalog, cached);
    return Results.Text(json, "application/json");
});

app.Run();

record Product(string Id, string Name, decimal Price, string[] Tags);
