using Azure.Core;
using Azure.Identity;
using Azure.Security.KeyVault.Secrets;
using Azure.Storage.Blobs;
using Microsoft.Azure.Cosmos;

var builder = WebApplication.CreateBuilder(args);
var miClientId = builder.Configuration["MI_CLIENT_ID"];
var kvName     = builder.Configuration["KV_NAME"];
var storage    = builder.Configuration["STORAGE_ACCOUNT"];
var cosmosEp   = builder.Configuration["COSMOS_ENDPOINT"];

TokenCredential cred = string.IsNullOrEmpty(miClientId)
    ? new DefaultAzureCredential()
    : new DefaultAzureCredential(new DefaultAzureCredentialOptions { ManagedIdentityClientId = miClientId });

builder.Services.AddSingleton<TokenCredential>(cred);

var app = builder.Build();

app.MapGet("/", () => new { app = "anchorline-mi-app", ok = true });

app.MapGet("/kv/{secretName}", async (string secretName) =>
{
    if (string.IsNullOrEmpty(kvName)) return Results.BadRequest("KV_NAME not set");
    var client = new SecretClient(new Uri($"https://{kvName}.vault.azure.net"), cred);
    var s = await client.GetSecretAsync(secretName);
    return Results.Ok(new { name = s.Value.Name, value = s.Value.Value });
});

app.MapGet("/storage/list", async () =>
{
    if (string.IsNullOrEmpty(storage)) return Results.BadRequest("STORAGE_ACCOUNT not set");
    var svc = new BlobServiceClient(new Uri($"https://{storage}.blob.core.windows.net"), cred);
    var containers = new List<string>();
    await foreach (var c in svc.GetBlobContainersAsync()) containers.Add(c.Name);
    return Results.Ok(new { containers });
});

app.MapGet("/cosmos/dbs", async () =>
{
    if (string.IsNullOrEmpty(cosmosEp)) return Results.BadRequest("COSMOS_ENDPOINT not set");
    var client = new CosmosClient(cosmosEp, cred);
    var dbs = new List<string>();
    using var iter = client.GetDatabaseQueryIterator<DatabaseProperties>("SELECT * FROM c");
    while (iter.HasMoreResults)
    {
        var page = await iter.ReadNextAsync();
        foreach (var d in page) dbs.Add(d.Id);
    }
    return Results.Ok(new { databases = dbs });
});

app.Run("http://0.0.0.0:8080");
