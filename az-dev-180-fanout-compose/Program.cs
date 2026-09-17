// Three tiny mock backends serving /orders, /payments, /support on different ports.
var b1 = WebApplication.CreateBuilder(); var a1 = b1.Build();
a1.MapGet("/orders/{cid}",   (string cid) => new { customer = cid, orders   = new[] { new { id = "ord-001", total = 249.5 } } });
_ = a1.RunAsync("http://0.0.0.0:5081");

var b2 = WebApplication.CreateBuilder(); var a2 = b2.Build();
a2.MapGet("/payments/{cid}", (string cid) => new { customer = cid, payments = new[] { new { id = "pay-001", amount = 249.5 } } });
_ = a2.RunAsync("http://0.0.0.0:5082");

var b3 = WebApplication.CreateBuilder(); var a3 = b3.Build();
a3.MapGet("/support/{cid}",  (string cid) => new { customer = cid, tickets  = Array.Empty<object>() });
await a3.RunAsync("http://0.0.0.0:5083");
