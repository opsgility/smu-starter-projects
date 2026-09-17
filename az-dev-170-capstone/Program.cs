using Azure.Identity;
using Azure.Messaging.ServiceBus;
using Azure.Storage.Blobs;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.Azure.Cosmos;
using Microsoft.Identity.Web;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddMicrosoftIdentityWebApi(builder.Configuration.GetSection("AzureAd"));

builder.Services.AddAuthorization(o =>
{
    o.AddPolicy("OrdersRead",  p => p.RequireAssertion(c => c.User.HasClaim("scp","Orders.Read")  || c.User.HasClaim("roles","Orders.Reader")));
    o.AddPolicy("OrdersWrite", p => p.RequireAssertion(c => c.User.HasClaim("scp","Orders.Write") || c.User.HasClaim("roles","Orders.Writer")));
});

var cred = new DefaultAzureCredential();
builder.Services.AddSingleton(_ => new BlobServiceClient(new Uri($"https://{builder.Configuration["Storage"]}.blob.core.windows.net"), cred));
builder.Services.AddSingleton(_ => new ServiceBusClient(builder.Configuration["ServiceBus"]!, cred));
builder.Services.AddSingleton(_ => new CosmosClient(builder.Configuration["Cosmos"]!, cred));

var app = builder.Build();
app.UseAuthentication();
app.UseAuthorization();

app.MapGet("/health", () => Results.Ok(new { status = "ok", zeroSecrets = true }));
app.MapGet("/orders", (CosmosClient c) => Results.Ok(new[] { new { id = "demo", status = "ok" } }))
    .RequireAuthorization("OrdersRead");
app.MapPost("/orders", async (BlobServiceClient s, ServiceBusClient sb, dynamic body) =>
{
    var container = s.GetBlobContainerClient("orders");
    await container.CreateIfNotExistsAsync();
    var name = $"order-{Guid.NewGuid():N}.json";
    await container.GetBlobClient(name).UploadAsync(BinaryData.FromString(System.Text.Json.JsonSerializer.Serialize((object)body)), overwrite: true);
    var sender = sb.CreateSender("orders");
    await sender.SendMessageAsync(new ServiceBusMessage(name));
    return Results.Accepted($"/orders/{name}");
}).RequireAuthorization("OrdersWrite");

app.Run();
