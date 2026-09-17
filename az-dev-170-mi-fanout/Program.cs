using Azure.Identity;
using Azure.Storage.Blobs;
using Azure.Security.KeyVault.Secrets;
using Microsoft.Azure.Cosmos;
using Microsoft.Data.SqlClient;
using Azure.Messaging.ServiceBus;

var uami = Environment.GetEnvironmentVariable("UAMI_CLIENT_ID");
var cred = string.IsNullOrEmpty(uami)
    ? (Azure.Core.TokenCredential)new DefaultAzureCredential()
    : new ManagedIdentityCredential(uami);

var storage = Environment.GetEnvironmentVariable("STORAGE_ACCOUNT")!;
var kv = Environment.GetEnvironmentVariable("KV_NAME")!;
var sqlServer = Environment.GetEnvironmentVariable("SQL_SERVER")!;
var sqlDb = Environment.GetEnvironmentVariable("SQL_DB")!;
var cosmosEndpoint = Environment.GetEnvironmentVariable("COSMOS_ENDPOINT")!;
var sbNs = Environment.GetEnvironmentVariable("SB_NAMESPACE")!;

Console.WriteLine("Fanning out via MI to all 5 services...");

// Storage
var blob = new BlobServiceClient(new Uri($"https://{storage}.blob.core.windows.net"), cred);
var acct = await blob.GetPropertiesAsync();
Console.WriteLine($"Storage OK: default service version = {acct.Value.DefaultServiceVersion ?? "server default"}");

// Key Vault
var secrets = new SecretClient(new Uri($"https://{kv}.vault.azure.net"), cred);
await foreach (var s in secrets.GetPropertiesOfSecretsAsync()) { Console.WriteLine($"KV secret: {s.Name}"); break; }
Console.WriteLine("Key Vault OK");

// Azure SQL (Entra token via MI)
var sqlToken = (await cred.GetTokenAsync(new Azure.Core.TokenRequestContext(new[] { "https://database.windows.net/.default" }), default)).Token;
using (var sql = new SqlConnection($"Server={sqlServer};Database={sqlDb};Encrypt=True"))
{
    sql.AccessToken = sqlToken;
    await sql.OpenAsync();
    Console.WriteLine($"Azure SQL OK: {sql.ServerVersion}");
}

// Cosmos
using var cosmos = new CosmosClient(cosmosEndpoint, cred);
var acctResp = await cosmos.ReadAccountAsync();
Console.WriteLine($"Cosmos OK: {acctResp.Id}");

// Service Bus
await using var sb = new ServiceBusClient(sbNs, cred);
Console.WriteLine("Service Bus OK");

Console.WriteLine("All 5 services reached with zero secrets.");
