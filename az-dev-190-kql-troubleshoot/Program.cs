// Anchorline workload generator — synthesizes realistic traffic across 5 endpoints
// with intentional latency + error patterns so students can answer troubleshooting
// questions from App Insights using KQL.

using System.Diagnostics;
using Azure.Monitor.OpenTelemetry.AspNetCore;
using OpenTelemetry.Resources;
using OpenTelemetry.Trace;
using OpenTelemetry.Metrics;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddOpenTelemetry()
    .ConfigureResource(r => r.AddService("anchorline-kql-workload", serviceVersion: "1.0.0"))
    .WithTracing(t => t.AddAspNetCoreInstrumentation().AddHttpClientInstrumentation())
    .WithMetrics(m => m.AddAspNetCoreInstrumentation())
    .UseAzureMonitor();

var app = builder.Build();
var rand = Random.Shared;

// Fast endpoint — always < 50ms, 0% error.
app.MapGet("/products",  async () => { await Task.Delay(rand.Next(10, 50)); return Results.Ok(new[]{"kayak","paddle"}); });
// Medium — 100-500ms, 2% error.
app.MapGet("/orders",    async () => { await Task.Delay(rand.Next(100, 500)); if (rand.NextDouble() < 0.02) return Results.Problem(); return Results.Ok(); });
// Slow endpoint — 500-1500ms sometimes, spike to 3000ms 5% of calls, 5% errors.
app.MapGet("/reports",   async () =>
{
    var d = rand.NextDouble() < 0.05 ? rand.Next(2500, 3500) : rand.Next(500, 1500);
    await Task.Delay(d);
    if (rand.NextDouble() < 0.05) return Results.Problem();
    return Results.Ok();
});
// Failing dependency — inbound OK but internal HttpClient to bad host fails.
app.MapGet("/analytics", async (IHttpClientFactory hcf) =>
{
    var c = hcf.CreateClient(); c.Timeout = TimeSpan.FromSeconds(3);
    try { await c.GetAsync("http://anchorline-analytics-fake.local"); } catch { }
    return Results.Ok();
});
// Explosive — 20% throw
app.MapGet("/checkout",  () => { if (rand.NextDouble() < 0.20) throw new InvalidOperationException("payment gateway timeout"); return Results.Ok(); });

app.Services.GetRequiredService<IHostApplicationLifetime>().ApplicationStarted.Register(() =>
{
    _ = Task.Run(async () =>
    {
        using var client = new HttpClient { BaseAddress = new Uri("http://localhost:5000") };
        var routes = new[] { "/products", "/orders", "/reports", "/analytics", "/checkout" };
        while (true)
        {
            try { await client.GetAsync(routes[rand.Next(routes.Length)]); } catch { }
            await Task.Delay(rand.Next(50, 200));
        }
    });
});

builder.Services.AddHttpClient();
app.Run();
