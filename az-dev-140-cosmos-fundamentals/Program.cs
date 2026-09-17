using System.Net;
using Azure.Identity;
using Microsoft.Azure.Cosmos;

var endpoint = Environment.GetEnvironmentVariable("ANCHORLINE_COSMOS_ENDPOINT")
    ?? throw new InvalidOperationException("ANCHORLINE_COSMOS_ENDPOINT missing (e.g. https://anchorline-cosmos-xxx.documents.azure.com:443/)");
var dbName    = Environment.GetEnvironmentVariable("ANCHORLINE_COSMOS_DB") ?? "AnchorlineCatalog";
var contName  = Environment.GetEnvironmentVariable("ANCHORLINE_COSMOS_CONTAINER") ?? "products";

var cred = new DefaultAzureCredential();

var client = new CosmosClient(endpoint, cred, new CosmosClientOptions
{
    ApplicationName = "az-dev-140-cosmos-fundamentals",
    ConnectionMode = ConnectionMode.Direct
});

var db = (await client.CreateDatabaseIfNotExistsAsync(dbName)).Database;
var container = (await db.CreateContainerIfNotExistsAsync(new ContainerProperties(contName, "/category"))).Container;

Console.WriteLine($"Connected to {endpoint} / {dbName} / {contName}");

var mode = args.Length > 0 ? args[0] : "help";

switch (mode)
{
    case "seed":  await Seed(); break;
    case "read":  await ReadOne(); break;
    case "query": await Query(); break;
    case "upsert": await Upsert(); break;
    case "delete": await DeleteOne(); break;
    default: Console.WriteLine("Modes: seed | read | query | upsert | delete"); break;
}

async Task Seed()
{
    var products = new[]
    {
        new Product("prod-4s-tent",    "4-Season Tent",   "shelter", 599m,  4.8),
        new Product("prod-3s-tent",    "3-Season Tent",   "shelter", 399m,  4.6),
        new Product("prod-60l-pack",   "60L Backpack",    "carry",   189m,  4.7),
        new Product("prod-30l-pack",   "30L Daypack",     "carry",    99m,  4.5),
        new Product("prod-headlamp",   "300lm Headlamp",  "light",    49m,  4.4),
        new Product("prod-firestarter","Storm Firestarter","fire",    19m,  4.9),
    };

    double totalRu = 0;
    foreach (var p in products)
    {
        var resp = await container.UpsertItemAsync(p, new PartitionKey(p.category));
        totalRu += resp.RequestCharge;
        Console.WriteLine($"upsert {p.id,-18} -> {resp.StatusCode}, {resp.RequestCharge:0.00} RU");
    }
    Console.WriteLine($"TOTAL SEED: {products.Length} docs, {totalRu:0.00} RU");
}

async Task ReadOne()
{
    var resp = await container.ReadItemAsync<Product>("prod-4s-tent", new PartitionKey("shelter"));
    Console.WriteLine($"read prod-4s-tent -> {resp.StatusCode}, {resp.RequestCharge:0.00} RU");
    Console.WriteLine($"  {resp.Resource.name} in {resp.Resource.category}, {resp.Resource.price:C}, {resp.Resource.rating} stars");
}

async Task Query()
{
    var q = "SELECT * FROM c WHERE c.category = @cat AND c.rating >= @min ORDER BY c.rating DESC";
    var query = new QueryDefinition(q)
        .WithParameter("@cat", "carry")
        .WithParameter("@min", 4.5);

    using var iter = container.GetItemQueryIterator<Product>(query,
        requestOptions: new QueryRequestOptions { PartitionKey = new PartitionKey("carry") });

    double totalRu = 0;
    var rows = 0;
    while (iter.HasMoreResults)
    {
        var page = await iter.ReadNextAsync();
        totalRu += page.RequestCharge;
        foreach (var p in page)
        {
            rows++;
            Console.WriteLine($"  {p.id,-18} {p.name,-20} {p.rating} stars");
        }
    }
    Console.WriteLine($"QUERY: {rows} rows, {totalRu:0.00} RU total");
}

async Task Upsert()
{
    var updated = new Product("prod-4s-tent", "4-Season Tent (2026 refresh)", "shelter", 649m, 4.8);
    var resp = await container.UpsertItemAsync(updated, new PartitionKey(updated.category));
    Console.WriteLine($"upsert -> {resp.StatusCode}, {resp.RequestCharge:0.00} RU");
}

async Task DeleteOne()
{
    try
    {
        var resp = await container.DeleteItemAsync<Product>("prod-firestarter", new PartitionKey("fire"));
        Console.WriteLine($"delete -> {resp.StatusCode}, {resp.RequestCharge:0.00} RU");
    }
    catch (CosmosException ex) when (ex.StatusCode == HttpStatusCode.NotFound)
    {
        Console.WriteLine("delete -> 404 (already gone)");
    }
}

public record Product(string id, string name, string category, decimal price, double rating);
