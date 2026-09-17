using System.Collections.ObjectModel;
using Azure.Identity;
using Microsoft.Azure.Cosmos;

var endpoint = Environment.GetEnvironmentVariable("ANCHORLINE_COSMOS_ENDPOINT")
    ?? throw new InvalidOperationException("ANCHORLINE_COSMOS_ENDPOINT missing");
var dbName = Environment.GetEnvironmentVariable("ANCHORLINE_COSMOS_DB") ?? "AnchorlineVector";

var client = new CosmosClient(endpoint, new DefaultAzureCredential(), new CosmosClientOptions
{
    ApplicationName = "az-dev-140-vector-search"
});
var db = (await client.CreateDatabaseIfNotExistsAsync(dbName)).Database;

const int Dims = 8;
var containerProps = new ContainerProperties("products", "/category")
{
    VectorEmbeddingPolicy = new VectorEmbeddingPolicy(new Collection<Embedding>
    {
        new() { Path = "/embedding", DataType = VectorDataType.Float32, DistanceFunction = DistanceFunction.Cosine, Dimensions = Dims }
    }),
    IndexingPolicy = new IndexingPolicy
    {
        VectorIndexes = { new VectorIndexPath { Path = "/embedding", Type = VectorIndexType.QuantizedFlat } }
    }
};

var container = (await db.CreateContainerIfNotExistsAsync(containerProps, 400)).Container;

var mode = args.Length > 0 ? args[0] : "help";
switch (mode)
{
    case "seed":   await Seed(); break;
    case "search": await Search(args.Length > 1 ? args[1] : "warm"); break;
    default: Console.WriteLine("Modes: seed | search <keyword>"); break;
}

async Task Seed()
{
    var products = new[]
    {
        new Product("prod-4s-tent",     "4-Season Tent",       "shelter", "insulated winter shelter",    Embed("warm winter shelter")),
        new Product("prod-3s-tent",     "3-Season Tent",       "shelter", "breathable summer tent",       Embed("summer ventilated shelter")),
        new Product("prod-sleep-warm",  "Down Sleeping Bag",   "sleep",   "-15C down insulated bag",     Embed("warm down insulated bag")),
        new Product("prod-sleep-summer","Summer Bag",          "sleep",   "10C lightweight summer bag",  Embed("summer light bag")),
        new Product("prod-headlamp",    "300lm Headlamp",      "light",   "led headlamp red mode",       Embed("light illumination lamp")),
        new Product("prod-fire",        "Storm Firestarter",   "fire",    "waterproof fire starter",     Embed("warm fire ignition")),
        new Product("prod-pack",        "60L Backpack",        "carry",   "hiking backpack 60L",         Embed("backpack carry gear")),
        new Product("prod-down-jacket", "Down Jacket",         "apparel", "warm down insulated jacket",  Embed("warm down insulated apparel")),
    };

    double totalRu = 0;
    foreach (var p in products)
    {
        var resp = await container.UpsertItemAsync(p, new PartitionKey(p.category));
        totalRu += resp.RequestCharge;
        Console.WriteLine($"  {p.id,-20} {resp.RequestCharge:0.00} RU");
    }
    Console.WriteLine($"Seeded {products.Length} products, {totalRu:0.00} RU total.");
}

async Task Search(string keyword)
{
    var queryEmb = Embed(keyword);
    var q = new QueryDefinition("SELECT TOP 5 c.id, c.name, c.category, c.description, VectorDistance(c.embedding, @q) AS score FROM c ORDER BY VectorDistance(c.embedding, @q)")
        .WithParameter("@q", queryEmb);

    using var iter = container.GetItemQueryIterator<SearchResult>(q);
    double ru = 0;
    Console.WriteLine($"Query: \"{keyword}\"");
    Console.WriteLine("id                   | category | score  | name / description");
    while (iter.HasMoreResults)
    {
        var page = await iter.ReadNextAsync();
        ru += page.RequestCharge;
        foreach (var r in page)
            Console.WriteLine($"{r.id,-20} | {r.category,-8} | {r.score:0.000} | {r.name} - {r.description}");
    }
    Console.WriteLine($"[{ru:0.00} RU]");
}

// Deterministic mock embedder - maps text -> 8-dim vector by hashing keywords.
// Real system would call Azure OpenAI text-embedding-3-large.
static float[] Embed(string text)
{
    var vec = new float[8];
    var words = text.ToLowerInvariant().Split(new[] {' ', '-'}, StringSplitOptions.RemoveEmptyEntries);
    foreach (var w in words)
    {
        // Simple keyword -> dimension mapping so semantically similar terms cluster
        if (w.Contains("warm") || w.Contains("winter") || w.Contains("insulated") || w.Contains("down"))  vec[0] += 1;
        if (w.Contains("summer") || w.Contains("light") || w.Contains("breath")) vec[1] += 1;
        if (w.Contains("shelter") || w.Contains("tent")) vec[2] += 1;
        if (w.Contains("bag") || w.Contains("sleep")) vec[3] += 1;
        if (w.Contains("illumination") || w.Contains("lamp") || w.Contains("led") || w.Contains("light")) vec[4] += 1;
        if (w.Contains("fire") || w.Contains("ignition")) vec[5] += 1;
        if (w.Contains("carry") || w.Contains("pack") || w.Contains("backpack")) vec[6] += 1;
        if (w.Contains("apparel") || w.Contains("jacket")) vec[7] += 1;
    }
    // Normalize
    var mag = Math.Sqrt(vec.Sum(v => v * v));
    if (mag > 0) for (int i = 0; i < vec.Length; i++) vec[i] = (float)(vec[i] / mag);
    return vec;
}

public record Product(string id, string name, string category, string description, float[] embedding);
public record SearchResult(string id, string name, string category, string description, double score);
