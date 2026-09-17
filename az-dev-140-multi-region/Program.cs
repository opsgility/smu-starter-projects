using Azure.Identity;
using Microsoft.Azure.Cosmos;

var endpoint = Environment.GetEnvironmentVariable("ANCHORLINE_COSMOS_ENDPOINT")
    ?? throw new InvalidOperationException("ANCHORLINE_COSMOS_ENDPOINT missing");
var region1 = Environment.GetEnvironmentVariable("ANCHORLINE_REGION_1") ?? "East US 2";
var region2 = Environment.GetEnvironmentVariable("ANCHORLINE_REGION_2") ?? "West US 2";

var cred = new DefaultAzureCredential();

CosmosClient MakeClient(string preferredRegion)
{
    return new CosmosClient(endpoint, cred, new CosmosClientOptions
    {
        ApplicationName = "az-dev-140-multi-region",
        ApplicationPreferredRegions = new List<string> { preferredRegion }
    });
}

var clientR1 = MakeClient(region1);
var clientR2 = MakeClient(region2);

var db1 = (await clientR1.CreateDatabaseIfNotExistsAsync("AnchorlineMultiRegion")).Database;
var products1 = (await db1.CreateContainerIfNotExistsAsync(new ContainerProperties("products", "/id"), 400)).Container;
var products2 = clientR2.GetContainer("AnchorlineMultiRegion", "products");

var mode = args.Length > 0 ? args[0] : "help";
switch (mode)
{
    case "seed":            await Seed(); break;
    case "conflict-lww":    await ConflictLww(); break;
    case "show":            await Show(); break;
    default: Console.WriteLine("Modes: seed | conflict-lww | show"); break;
}

async Task Seed()
{
    var product = new Product("prod-4s-tent", "4-Season Tent", 599m, "shelter");
    await products1.UpsertItemAsync(product, new PartitionKey(product.id));
    Console.WriteLine("Seeded prod-4s-tent = $599 from region 1");
}

async Task ConflictLww()
{
    Console.WriteLine($"Region 1 writing price=$650 via {region1}...");
    var t1 = products1.UpsertItemAsync(new Product("prod-4s-tent", "4-Season Tent", 650m, "shelter"),
        new PartitionKey("prod-4s-tent"));

    Console.WriteLine($"Region 2 writing price=$625 via {region2}...");
    var t2 = products2.UpsertItemAsync(new Product("prod-4s-tent", "4-Season Tent", 625m, "shelter"),
        new PartitionKey("prod-4s-tent"));

    await Task.WhenAll(t1, t2);
    Console.WriteLine("Both writes acknowledged in their local region.");

    await Task.Delay(10_000);
    var readR1 = await products1.ReadItemAsync<Product>("prod-4s-tent", new PartitionKey("prod-4s-tent"));
    var readR2 = await products2.ReadItemAsync<Product>("prod-4s-tent", new PartitionKey("prod-4s-tent"));
    Console.WriteLine($"After 10s replication -- region 1 sees ${readR1.Resource.price}, region 2 sees ${readR2.Resource.price}");
    Console.WriteLine($"LWW winner: {(readR1.Resource.price == readR2.Resource.price ? "both regions converged" : "still diverging")}");
}

async Task Show()
{
    var r1 = await products1.ReadItemAsync<Product>("prod-4s-tent", new PartitionKey("prod-4s-tent"));
    var r2 = await products2.ReadItemAsync<Product>("prod-4s-tent", new PartitionKey("prod-4s-tent"));
    Console.WriteLine($"{region1,-15}: ${r1.Resource.price}");
    Console.WriteLine($"{region2,-15}: ${r2.Resource.price}");
}

public record Product(string id, string name, decimal price, string category);
