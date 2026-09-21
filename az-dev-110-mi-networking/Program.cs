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
    // ARM injects the storage account NAME via AzureWebJobsStorage__accountName (used by the
    // Functions host itself for the runtime storage). We reuse the same name for the data-plane
    // BlobServiceClient so there is exactly ONE storage account and it is reached via MI only.
    var accountName = config["AzureWebJobsStorage__accountName"]
        ?? throw new InvalidOperationException("AzureWebJobsStorage__accountName missing (set by ARM template).");
    var blobUri = new Uri($"https://{accountName}.blob.core.windows.net");
    return new BlobServiceClient(blobUri, sp.GetRequiredService<TokenCredential>());
});

builder.Services.AddSingleton(sp =>
{
    var config = sp.GetRequiredService<IConfiguration>();
    var url = config["KEY_VAULT_URI"]
        ?? throw new InvalidOperationException("KEY_VAULT_URI missing (set by ARM template).");
    return new SecretClient(new Uri(url), sp.GetRequiredService<TokenCredential>());
});

builder.Build().Run();
