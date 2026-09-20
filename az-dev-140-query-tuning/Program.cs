using Azure.Identity;
using Microsoft.Azure.Cosmos;

var endpoint = Environment.GetEnvironmentVariable("ANCHORLINE_COSMOS_ENDPOINT")
    ?? throw new InvalidOperationException("ANCHORLINE_COSMOS_ENDPOINT missing");
var dbName  = Environment.GetEnvironmentVariable("ANCHORLINE_COSMOS_DB") ?? "AnchorlineQueryTune";

var client = new CosmosClient(endpoint, new DefaultAzureCredential(), new CosmosClientOptions
{
    ApplicationName = "az-dev-140-query-tuning",
    AllowBulkExecution = true
});

var db = (await client.CreateDatabaseIfNotExistsAsync(dbName)).Database;
var container = (await db.CreateContainerIfNotExistsAsync(new ContainerProperties("products", "/category"), 400)).Container;

var mode = args.Length > 0 ? args[0] : "help";
switch (mode)
{
    case "seed":       await Seed(20000); break;
    case "query":      await MeasuredQuery(); break;
    case "avg100":     await Avg100(); break;
    case "add-index":  await AddCompositeIndex(); break;
    default: Console.WriteLine("Modes: seed | query | avg100 | add-index"); break;
}

async Task Seed(int count)
{
    var rnd = new Random(42);
    var cats = new[] { "shelter", "carry", "light", "fire", "food", "nav", "sleep" };
    for (int i = 0; i < count; i++)
    {
        var doc = new Product(
            $"prod-{i:D6}",
            $"Product {i}",
            cats[rnd.Next(cats.Length)],
            50 + (decimal)rnd.NextDouble() * 800,
            2.0 + rnd.NextDouble() * 3.0,
            new string('x', 200)
        );
        await container.CreateItemAsync(doc, new PartitionKey(doc.category));
        if ((i+1) % 2500 == 0) Console.WriteLine($"  seeded {i+1}");
    }
    Console.WriteLine($"seed done: {count} docs");
}

async Task MeasuredQuery()
{
    var q = new QueryDefinition("SELECT TOP 100 * FROM c WHERE c.category = @c AND c.rating >= 4 ORDER BY c.rating DESC")
        .WithParameter("@c", "carry");

    using var iter = container.GetItemQueryIterator<Product>(q,
        requestOptions: new QueryRequestOptions
        {
            PartitionKey = new PartitionKey("carry"),
            PopulateIndexMetrics = true
        });

    double ru = 0;
    var n = 0;
    string? metrics = null;
    while (iter.HasMoreResults)
    {
        var page = await iter.ReadNextAsync();
        ru += page.RequestCharge;
        metrics = page.IndexMetrics;
        foreach (var _ in page) n++;
    }
    Console.WriteLine($"Query: {n} rows, {ru:0.00} RU");
    Console.WriteLine("Index metrics:");
    Console.WriteLine(metrics);
}

async Task Avg100()
{
    double total = 0;
    for (int i = 0; i < 100; i++)
    {
        var q = new QueryDefinition("SELECT TOP 100 * FROM c WHERE c.category = @c AND c.rating >= 4 ORDER BY c.rating DESC")
            .WithParameter("@c", "carry");
        using var iter = container.GetItemQueryIterator<Product>(q,
            requestOptions: new QueryRequestOptions { PartitionKey = new PartitionKey("carry") });
        while (iter.HasMoreResults) { var p = await iter.ReadNextAsync(); total += p.RequestCharge; }
    }
    Console.WriteLine($"avg over 100 execs: {total/100:0.00} RU");
}

async Task AddCompositeIndex()
{
    var props = await container.ReadContainerAsync();
    var policy = props.Resource.IndexingPolicy;
    policy.CompositeIndexes.Clear();
    var composite = new Collection<CompositePath>
    {
        new() { Path = "/category", Order = CompositePathSortOrder.Ascending },
        new() { Path = "/rating",   Order = CompositePathSortOrder.Descending }
    };
    policy.CompositeIndexes.Add(composite);
    await container.ReplaceContainerAsync(props.Resource);
    Console.WriteLine("Added composite index (/category ASC, /rating DESC). Reindex begins in the background.");
}

public record Product(string id, string name, string category, decimal price, double rating, string padding);

class Collection<T> : System.Collections.ObjectModel.Collection<T> { }
