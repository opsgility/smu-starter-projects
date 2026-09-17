using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.AspNetCore.Authorization;
using Microsoft.Identity.Web;
using Microsoft.Identity.Web.Resource;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddMicrosoftIdentityWebApi(builder.Configuration.GetSection("AzureAd"));

builder.Services.AddAuthorization(o =>
{
    o.AddPolicy("OrdersRead",  p => p.RequireAssertion(c =>
        c.User.HasClaim("scp", "Orders.Read") ||
        c.User.HasClaim("http://schemas.microsoft.com/identity/claims/scope", "Orders.Read") ||
        c.User.HasClaim("roles", "Orders.Reader")));
    o.AddPolicy("OrdersWrite", p => p.RequireAssertion(c =>
        c.User.HasClaim("scp", "Orders.Write") ||
        c.User.HasClaim("http://schemas.microsoft.com/identity/claims/scope", "Orders.Write") ||
        c.User.HasClaim("roles", "Orders.Writer")));
    o.AddPolicy("OrdersAdmin", p => p.RequireRole("Orders.Admin"));
});

var app = builder.Build();
app.UseAuthentication();
app.UseAuthorization();

var orders = new List<object>();

app.MapGet("/orders", () => Results.Ok(orders)).RequireAuthorization("OrdersRead");
app.MapPost("/orders", (dynamic body) => { orders.Add(body); return Results.Created($"/orders/{orders.Count}", body); })
    .RequireAuthorization("OrdersWrite");
app.MapDelete("/orders/{id:int}", (int id) => { orders.RemoveAt(id); return Results.NoContent(); })
    .RequireAuthorization("OrdersAdmin");

app.Run();
