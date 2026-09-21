using Azure.Identity;
using Azure.Messaging.ServiceBus;
using Azure.Storage.Blobs;
using Microsoft.Azure.Cosmos;
using Microsoft.Azure.Functions.Worker;
using Microsoft.Azure.Functions.Worker.Builder;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

var builder = FunctionsApplication.CreateBuilder(args);
builder.ConfigureFunctionsWebApplication();
builder.Services
    .AddApplicationInsightsTelemetryWorkerService()
    .ConfigureFunctionsApplicationInsights();

// One shared credential for every downstream — the Function App's system-assigned MI
// in production; DefaultAzureCredential also picks up `az login` / VS creds locally.
var cred = new DefaultAzureCredential();

// Cosmos: ARM sets COSMOS_ENDPOINT to the account's documentEndpoint. disableLocalAuth=true,
// so keys are unavailable — MI-only.
builder.Services.AddSingleton(_ => new CosmosClient(
    accountEndpoint: Environment.GetEnvironmentVariable("COSMOS_ENDPOINT")
        ?? throw new InvalidOperationException("COSMOS_ENDPOINT is not set."),
    tokenCredential: cred));

// Blob: reuse the same account the Functions runtime uses.
// ARM sets AzureWebJobsStorage__accountName (identity-based Functions storage).
builder.Services.AddSingleton(_ =>
{
    var account = Environment.GetEnvironmentVariable("AzureWebJobsStorage__accountName")
        ?? throw new InvalidOperationException("AzureWebJobsStorage__accountName is not set.");
    return new BlobServiceClient(new Uri($"https://{account}.blob.core.windows.net"), cred);
});

// Service Bus: ARM sets SERVICEBUS_FULLYQUALIFIEDNAMESPACE (namespace has disableLocalAuth=true).
builder.Services.AddSingleton(_ => new ServiceBusClient(
    fullyQualifiedNamespace: Environment.GetEnvironmentVariable("SERVICEBUS_FULLYQUALIFIEDNAMESPACE")
        ?? throw new InvalidOperationException("SERVICEBUS_FULLYQUALIFIEDNAMESPACE is not set."),
    credential: cred));

builder.Build().Run();
