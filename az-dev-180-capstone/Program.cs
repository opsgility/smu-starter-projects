// Five tiny mock backends for the capstone: Orders, Customers, Payments, Support, Analytics.
async Task StartAsync(int port, Action<WebApplication> map)
{
    var b = WebApplication.CreateBuilder();
    var a = b.Build();
    map(a);
    _ = a.RunAsync($"http://0.0.0.0:{port}");
    await Task.CompletedTask;
}

await StartAsync(5091, a => a.MapGet("/orders",    () => new[] { new { id="ord-001", total=249.5m } }));
await StartAsync(5092, a => a.MapGet("/customers", () => new[] { new { id="cust-42", name="Ada" } }));
await StartAsync(5093, a => a.MapGet("/payments",  () => new[] { new { id="pay-001", amount=249.5m } }));
await StartAsync(5094, a => a.MapGet("/support",   () => Array.Empty<object>()));
await StartAsync(5095, a => a.MapGet("/analytics", () => new { visits=1234, conv=0.023 }));

Console.WriteLine("All five backends running on :5091-:5095. Ctrl-C to stop.");
await Task.Delay(-1);
