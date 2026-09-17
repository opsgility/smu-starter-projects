using System.Collections.ObjectModel;
using Azure.Identity;
using Microsoft.Azure.Cosmos;

var builder = WebApplication.CreateBuilder(args);
var endpoint = builder.Configuration["Anchorline:CosmosEndpoint"]
    ?? throw new InvalidOperationException("Anchorline:CosmosEndpoint missing");
var miClientId = builder.Configuration["Anchorline:MiClientId"];

builder.Services.AddSingleton(sp =>
{
    var cred = string.IsNullOrEmpty(miClientId)
        ? new DefaultAzureCredential()
        : new DefaultAzureCredential(new DefaultAzureCredentialOptions { ManagedIdentityClientId = miClientId });
    return new CosmosClient(endpoint, cred, new CosmosClientOptions
    {
        ApplicationName = "az-dev-140-capstone",
        AllowBulkExecution = true
    });
});

var app = builder.Build();

// Bootstrap: create DB and containers on startup
var client = app.Services.GetRequiredService<CosmosClient>();
var db = (await client.CreateDatabaseIfNotExistsAsync("AnchorlineSaaS")).Database;
var orders = (await db.CreateContainerIfNotExistsAsync(new ContainerProperties("orders",
    new List<string> { "/tenantId", "/customerId" }) { DefaultTimeToLive = -1 }, 400)).Container;
var summary = (await db.CreateContainerIfNotExistsAsync(new ContainerProperties("summary", "/tenantId"), 400)).Container;
var products = (await db.CreateContainerIfNotExistsAsync(new ContainerProperties("products", "/category")
{
    VectorEmbeddingPolicy = new VectorEmbeddingPolicy(new Collection<Embedding>
    {
        new() { Path = "/embedding", DataType = VectorDataType.Float32, DistanceFunction = DistanceFunction.Cosine, Dimensions = 8 }
    }),
    IndexingPolicy = new IndexingPolicy { VectorIndexes = { new VectorIndexPath { Path = "/embedding", Type = VectorIndexType.QuantizedFlat } } }
}, 400)).Container;

app.MapGet("/", () => Results.Ok(new { app = "anchorline-cosmos-saas", ok = true }));

app.MapPost("/api/orders", async (HttpContext ctx, OrderRequest req) =>
{
    if (string.IsNullOrEmpty(req.tenantId) || string.IsNullOrEmpty(req.customerId))
        return Results.BadRequest("tenantId and customerId required");

    var order = new OrderDoc(Guid.NewGuid().ToString("N")[..12], req.tenantId, req.customerId,
        DateTime.UtcNow, "Placed", req.amount, req.productId, req.productName);

    var resp = await orders.CreateItemAsync(order,
        new PartitionKeyBuilder().Add(req.tenantId).Add(req.customerId).Build());
    return Results.Ok(new { orderId = order.id, ru = resp.RequestCharge });
});

app.MapGet("/api/orders", async (string tenantId, string? customerId) =>
{
    if (customerId != null)
    {
        // scoped query - one logical partition
        var q = new QueryDefinition("SELECT * FROM c WHERE c.tenantId = @t AND c.customerId = @c ORDER BY c.placedUtc DESC")
            .WithParameter("@t", tenantId).WithParameter("@c", customerId);
        using var iter = orders.GetItemQueryIterator<OrderDoc>(q,
            requestOptions: new QueryRequestOptions
            {
                PartitionKey = new PartitionKeyBuilder().Add(tenantId).Add(customerId).Build()
            });
        var results = new List<OrderDoc>();
        double ru = 0;
        while (iter.HasMoreResults) { var p = await iter.ReadNextAsync(); ru += p.RequestCharge; results.AddRange(p); }
        return Results.Ok(new { count = results.Count, ru, results });
    }
    else
    {
        // tenant-scoped - only that tenant's partitions
        var q = new QueryDefinition("SELECT * FROM c WHERE c.tenantId = @t ORDER BY c.placedUtc DESC OFFSET 0 LIMIT 50")
            .WithParameter("@t", tenantId);
        using var iter = orders.GetItemQueryIterator<OrderDoc>(q,
            requestOptions: new QueryRequestOptions
            {
                PartitionKey = new PartitionKeyBuilder().Add(tenantId).Build()
            });
        var results = new List<OrderDoc>();
        double ru = 0;
        while (iter.HasMoreResults) { var p = await iter.ReadNextAsync(); ru += p.RequestCharge; results.AddRange(p); }
        return Results.Ok(new { count = results.Count, ru, results });
    }
});

app.MapPost("/api/products", async (ProductDoc p) =>
{
    var resp = await products.UpsertItemAsync(p, new PartitionKey(p.category));
    return Results.Ok(new { id = p.id, ru = resp.RequestCharge });
});

app.MapPost("/api/recommend", async (RecommendRequest req) =>
{
    var q = new QueryDefinition("SELECT TOP 5 c.id, c.name, c.category, VectorDistance(c.embedding, @q) AS score FROM c ORDER BY VectorDistance(c.embedding, @q)")
        .WithParameter("@q", req.queryVector);
    using var iter = products.GetItemQueryIterator<Recommendation>(q);
    var results = new List<Recommendation>();
    double ru = 0;
    while (iter.HasMoreResults) { var p = await iter.ReadNextAsync(); ru += p.RequestCharge; results.AddRange(p); }
    return Results.Ok(new { ru, results });
});

app.Run();

public record OrderRequest(string tenantId, string customerId, decimal amount, string productId, string productName);
public record OrderDoc(string id, string tenantId, string customerId, DateTime placedUtc, string status, decimal amount, string productId, string productName);
public record ProductDoc(string id, string name, string category, string description, float[] embedding);
public record RecommendRequest(float[] queryVector);
public record Recommendation(string id, string name, string category, double score);
