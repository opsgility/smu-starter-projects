using System.Data;
using Azure.Core;
using Azure.Identity;
using Azure.Security.KeyVault.Secrets;
using Azure.Storage.Blobs;
using Microsoft.Azure.Cosmos;
using Microsoft.Data.SqlClient;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddSingleton<TokenCredential>(_ => new DefaultAzureCredential());

var app = builder.Build();

app.MapGet("/health", () => Results.Ok(new { status = "ok" }));

app.MapGet("/version", (IConfiguration config) => Results.Ok(new
{
    build = config["AZ_DEV_100_BUILD_TAG"] ?? "unknown",
    identity = "system-assigned"
}));

app.MapGet("/whoami", async (TokenCredential credential) =>
{
    try
    {
        var context = new TokenRequestContext(new[] { "https://management.azure.com/.default" });
        var token = await credential.GetTokenAsync(context, CancellationToken.None);
        var parts = token.Token.Split('.');
        var payload = System.Text.Encoding.UTF8.GetString(
            Convert.FromBase64String(PadBase64(parts[1])));
        return Results.Ok(new { tokenPayload = payload, expiresOn = token.ExpiresOn });
    }
    catch (Exception ex)
    {
        return Results.Problem($"Token acquisition failed: {ex.Message}");
    }

    static string PadBase64(string s) => s.PadRight(s.Length + (4 - s.Length % 4) % 4, '=')
                                          .Replace('-', '+').Replace('_', '/');
});

app.MapGet("/blobs", async (IConfiguration config, TokenCredential credential) =>
{
    var accountUrl = config["Anchorline:StorageAccountUrl"];
    var container = config["Anchorline:BlobContainer"] ?? "products";
    if (string.IsNullOrEmpty(accountUrl))
        return Results.Problem("Anchorline:StorageAccountUrl not configured");

    try
    {
        var client = new BlobServiceClient(new Uri(accountUrl), credential);
        var containerClient = client.GetBlobContainerClient(container);
        var names = new List<string>();
        await foreach (var blob in containerClient.GetBlobsAsync())
        {
            names.Add(blob.Name);
            if (names.Count >= 20) break;
        }
        return Results.Ok(new { container, count = names.Count, names });
    }
    catch (Exception ex)
    {
        return Results.Problem($"Blob list failed: {ex.Message}");
    }
});

app.MapGet("/secret/{name}", async (string name, IConfiguration config, TokenCredential credential) =>
{
    var vaultUrl = config["Anchorline:KeyVaultUrl"];
    if (string.IsNullOrEmpty(vaultUrl))
        return Results.Problem("Anchorline:KeyVaultUrl not configured");

    try
    {
        var client = new SecretClient(new Uri(vaultUrl), credential);
        var secret = await client.GetSecretAsync(name);
        var v = secret.Value.Value;
        var masked = v.Length > 8 ? v.Substring(0, 4) + "..." + v.Substring(v.Length - 4) : "****";
        return Results.Ok(new { name, valueMasked = masked, contentType = secret.Value.Properties.ContentType });
    }
    catch (Exception ex)
    {
        return Results.Problem($"Secret read failed: {ex.Message}");
    }
});

app.MapGet("/products", async (IConfiguration config, TokenCredential credential) =>
{
    var sqlServer = config["Anchorline:SqlServer"];
    var sqlDb = config["Anchorline:SqlDatabase"];
    if (string.IsNullOrEmpty(sqlServer) || string.IsNullOrEmpty(sqlDb))
        return Results.Problem("Anchorline:SqlServer / SqlDatabase not configured");

    try
    {
        var connStr = $"Server=tcp:{sqlServer},1433;Database={sqlDb};Encrypt=True;TrustServerCertificate=False;";
        await using var conn = new SqlConnection(connStr);
        var context = new TokenRequestContext(new[] { "https://database.windows.net/.default" });
        var token = await credential.GetTokenAsync(context, CancellationToken.None);
        conn.AccessToken = token.Token;
        await conn.OpenAsync();

        var products = new List<object>();
        await using var cmd = new SqlCommand("SELECT TOP 10 Id, Sku, Name, Price FROM dbo.Products", conn);
        await using var reader = await cmd.ExecuteReaderAsync();
        while (await reader.ReadAsync())
        {
            products.Add(new
            {
                id = reader.GetInt32(0),
                sku = reader.GetString(1),
                name = reader.GetString(2),
                price = reader.GetDecimal(3)
            });
        }
        return Results.Ok(products);
    }
    catch (Exception ex)
    {
        return Results.Problem($"SQL query failed: {ex.Message}");
    }
});

app.MapGet("/catalog", async (IConfiguration config, TokenCredential credential) =>
{
    var cosmosEndpoint = config["Anchorline:CosmosEndpoint"];
    var database = config["Anchorline:CosmosDatabase"] ?? "Anchorline";
    var container = config["Anchorline:CosmosContainer"] ?? "Catalog";
    if (string.IsNullOrEmpty(cosmosEndpoint))
        return Results.Problem("Anchorline:CosmosEndpoint not configured");

    try
    {
        var client = new CosmosClient(cosmosEndpoint, credential);
        var db = client.GetDatabase(database);
        var containerClient = db.GetContainer(container);
        var iterator = containerClient.GetItemQueryIterator<dynamic>("SELECT TOP 10 * FROM c");
        var items = new List<object>();
        while (iterator.HasMoreResults)
        {
            foreach (var item in await iterator.ReadNextAsync())
            {
                items.Add(item);
                if (items.Count >= 10) break;
            }
            if (items.Count >= 10) break;
        }
        return Results.Ok(new { database, container, count = items.Count, items });
    }
    catch (Exception ex)
    {
        return Results.Problem($"Cosmos query failed: {ex.Message}");
    }
});

app.Run();
