using Azure.Identity;
using Microsoft.Azure.Cosmos;
using Microsoft.Azure.Functions.Worker;
using Microsoft.Azure.Functions.Worker.Builder;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

var builder = FunctionsApplication.CreateBuilder(args);

builder.Services
    .AddApplicationInsightsTelemetryWorkerService()
    .ConfigureFunctionsApplicationInsights();

// Cosmos client — identity-based (Flex Consumption + disableLocalAuth=true).
// Endpoint comes from the COSMOS_ENDPOINT app setting the ARM template already publishes.
builder.Services.AddSingleton(sp =>
{
    var endpoint = Environment.GetEnvironmentVariable("COSMOS_ENDPOINT")
        ?? throw new InvalidOperationException("COSMOS_ENDPOINT app setting is required.");
    return new CosmosClient(endpoint, new DefaultAzureCredential());
});

builder.Build().Run();
