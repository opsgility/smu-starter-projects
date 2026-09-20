using Microsoft.AspNetCore.Builder;
using Microsoft.OpenApi.Models;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(o =>
{
    o.SwaggerDoc("v1", new OpenApiInfo { Title = "Anchorline Orders", Version = "v1" });
});

var app = builder.Build();
app.UseSwagger();
app.UseSwaggerUI();

app.MapGet("/orders", () => new[] {
    new { id = "ord-001", customer = "cust-42", total = 249.50m },
    new { id = "ord-002", customer = "cust-42", total =  59.00m },
}).WithName("ListOrders");

app.MapGet("/orders/{id}", (string id) => Results.Ok(new { id, customer = "cust-42", total = 249.50m }))
   .WithName("GetOrder");

app.Run();
