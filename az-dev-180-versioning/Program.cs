// One backend serving BOTH shapes. v2 returns totalCents; the APIM v1 policy translates back to `total`.
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/orders/{id}", (string id) =>
    Results.Ok(new { id, customer = "cust-42", totalCents = 24950 }));

app.Run();
