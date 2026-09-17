using Microsoft.AspNetCore.Authentication.OpenIdConnect;
using Microsoft.Identity.Abstractions;
using Microsoft.Identity.Web;
using Microsoft.Identity.Web.UI;

var builder = WebApplication.CreateBuilder(args);

// AzureAd:ClientCredentials points to a KV-backed cert (set in appsettings)
builder.Services.AddAuthentication(OpenIdConnectDefaults.AuthenticationScheme)
    .AddMicrosoftIdentityWebApp(builder.Configuration.GetSection("AzureAd"))
    .EnableTokenAcquisitionToCallDownstreamApi()
    .AddDownstreamApi("OrdersApi", builder.Configuration.GetSection("OrdersApi"))
    .AddInMemoryTokenCaches();

builder.Services.AddAuthorization(o => o.FallbackPolicy = o.DefaultPolicy);
builder.Services.AddRazorPages().AddMicrosoftIdentityUI();

var app = builder.Build();
app.UseAuthentication();
app.UseAuthorization();

app.MapPost("/orders/refund", async (IDownstreamApi api) =>
{
    try
    {
        var r = await api.CallApiForUserAsync<object>("OrdersApi",
            downstream => downstream.RelativePath = "orders/refund");
        return Results.Ok(r);
    }
    catch (MicrosoftIdentityWebChallengeUserException)
    {
        return Results.Challenge();  // triggers CA step-up
    }
}).RequireAuthorization();

app.MapRazorPages();
app.Run();
