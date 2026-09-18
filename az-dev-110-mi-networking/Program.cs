using Azure.Core;
using Azure.Identity;
using Azure.Security.KeyVault.Secrets;
using Azure.Storage.Blobs;
using Microsoft.Azure.Functions.Worker;
using Microsoft.Azure.Functions.Worker.Builder;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

var builder = FunctionsApplication.CreateBuilder(args);
builder.ConfigureFunctionsWebApplication();
builder.Services
    .AddApplicationInsightsTelemetryWorkerService()
    .ConfigureFunctionsApplicationInsights();

builder.Services.AddSingleton<TokenCredential>(_ => new DefaultAzureCredential());

builder.Services.AddSingleton(sp =>
{
    var config = sp.GetRequiredService<IConfiguration>();
    var url = config["Anchorline:StorageBlobUri"] ?? throw new InvalidOperationException("Anchorline:StorageBlobUri missing");
    return new BlobServiceClient(new Uri(url), sp.GetRequiredService<TokenCredential>());
});

builder.Services.AddSingleton(sp =>
{
    var config = sp.GetRequiredService<IConfiguration>();
    var url = config["Anchorline:KeyVaultUri"] ?? throw new InvalidOperationException("Anchorline:KeyVaultUri missing");
    return new SecretClient(new Uri(url), sp.GetRequiredService<TokenCredential>());
});

builder.Build().Run();
