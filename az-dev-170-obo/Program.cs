using Microsoft.AspNetCore.Authentication.OpenIdConnect;
using Microsoft.AspNetCore.Authorization;
using Microsoft.Identity.Abstractions;
using Microsoft.Identity.Web;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddAuthentication(OpenIdConnectDefaults.AuthenticationScheme)
    .AddMicrosoftIdentityWebApp(builder.Configuration.GetSection("AzureAd"))
    .EnableTokenAcquisitionToCallDownstreamApi(new[] { "User.Read" })
    .AddDownstreamApi("Graph", builder.Configuration.GetSection("Graph"))
    .AddDownstreamApi("OrdersApi", builder.Configuration.GetSection("OrdersApi"))
    .AddInMemoryTokenCaches();

builder.Services.AddRazorPages();
builder.Services.AddAuthorization(o => o.FallbackPolicy = o.DefaultPolicy);

var app = builder.Build();

app.MapGet("/me", async (IDownstreamApi api) =>
{
    var me = await api.CallApiForUserAsync<Dictionary<string,object>>("Graph");
    return Results.Json(me);
}).RequireAuthorization();

app.MapGet("/orders", async (IDownstreamApi api) =>
{
    try
    {
        var orders = await api.CallApiForUserAsync<List<object>>("OrdersApi");
        return Results.Json(orders);
    }
    catch (MicrosoftIdentityWebChallengeUserException)
    {
        return Results.Challenge();
    }
}).RequireAuthorization();

app.UseAuthentication();
app.UseAuthorization();
app.MapRazorPages();
app.Run();
