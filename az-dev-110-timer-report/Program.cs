using Azure.Identity;
using Azure.Storage.Blobs;
using Microsoft.Azure.Functions.Worker.Builder;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

var builder = FunctionsApplication.CreateBuilder(args);

builder.Services
    .AddApplicationInsightsTelemetryWorkerService()
    .ConfigureFunctionsApplicationInsights();

builder.Services.AddSingleton(sp =>
{
    var config = sp.GetRequiredService<IConfiguration>();
    var accountUrl = config["Anchorline:StorageAccountUrl"];
    if (string.IsNullOrEmpty(accountUrl))
    {
        return new BlobServiceClient(config["AzureWebJobsStorage"]);
    }
    return new BlobServiceClient(new Uri(accountUrl), new DefaultAzureCredential());
});

builder.Build().Run();
