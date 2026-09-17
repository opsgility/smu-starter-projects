using Azure.Identity;
using Microsoft.Azure.Cosmos;

var endpoint = Environment.GetEnvironmentVariable("ANCHORLINE_COSMOS_ENDPOINT")
    ?? throw new InvalidOperationException("ANCHORLINE_COSMOS_ENDPOINT missing");
var dbName  = Environment.GetEnvironmentVariable("ANCHORLINE_COSMOS_DB") ?? "AnchorlineModeling";

var client = new CosmosClient(endpoint, new DefaultAzureCredential(), new CosmosClientOptions
{
    ApplicationName = "az-dev-140-data-modeling",
    AllowBulkExecution = true
});

var db = (await client.CreateDatabaseIfNotExistsAsync(dbName)).Database;
// Option A - embedded order lines
var ordersEmbed  = (await db.CreateContainerIfNotExistsAsync(new ContainerProperties("orders_embed", "/customerId"))).Container;
// Option B - referenced order lines
var ordersRef    = (await db.CreateContainerIfNotExistsAsync(new ContainerProperties("orders_ref", "/customerId"))).Container;
var linesRef     = (await db.CreateContainerIfNotExistsAsync(new ContainerProperties("lines_ref", "/orderId"))).Container;

var mode = args.Length > 0 ? args[0] : "help";
switch (mode)
{
    case "seed-embed": await SeedEmbed(5000); break;
    case "seed-ref":   await SeedRef(5000); break;
    case "query-embed": await QueryEmbed(); break;
    case "query-ref":   await QueryRef(); break;
    default: Console.WriteLine("Modes: seed-embed | seed-ref | query-embed | query-ref"); break;
}

async Task SeedEmbed(int count)
{
    Console.WriteLine($"Seeding {count} orders EMBED style...");
    double totalRu = 0;
    var tasks = new List<Task<double>>();
    var rnd = new Random(42);
    for (int i = 0; i < count; i++)
    {
        var custId  = $"cus-{i % 100:D4}";
        var order   = BuildOrder($"ord-e-{i:D6}", custId, rnd);
        var embeddedLines = Enumerable.Range(0, 2 + rnd.Next(6))
            .Select(_ => BuildEmbeddedLine(rnd))
            .ToList();
        var doc = new OrderEmbed(order.id, custId, order.placedUtc, order.status, embeddedLines);
        tasks.Add(WriteEmbed(doc));
        if (tasks.Count == 500)
        {
            foreach (var t in await WhenAll(tasks)) totalRu += t;
            tasks.Clear();
        }
    }
    foreach (var t in await WhenAll(tasks)) totalRu += t;
    Console.WriteLine($"seed-embed done, {totalRu:0} total RU, avg {totalRu/count:0.00} RU/order");
}

async Task<double> WriteEmbed(OrderEmbed doc)
{
    var resp = await ordersEmbed.CreateItemAsync(doc, new PartitionKey(doc.customerId));
    return resp.RequestCharge;
}

async Task SeedRef(int count)
{
    Console.WriteLine($"Seeding {count} orders REFERENCE style...");
    double orderRu = 0, lineRu = 0;
    var rnd = new Random(42);
    for (int i = 0; i < count; i++)
    {
        var custId = $"cus-{i % 100:D4}";
        var orderId = $"ord-r-{i:D6}";
        var nLines = 2 + rnd.Next(6);
        var lineIds = Enumerable.Range(0, nLines).Select(k => $"{orderId}-l{k}").ToList();
        var order = new OrderRef(orderId, custId, DateTime.UtcNow, "Placed", lineIds);

        var oResp = await ordersRef.CreateItemAsync(order, new PartitionKey(custId));
        orderRu += oResp.RequestCharge;

        foreach (var lid in lineIds)
        {
            var line = new LineRef(lid, orderId, "prod-4s-tent", "4-Season Tent", 1, 599);
            var lResp = await linesRef.CreateItemAsync(line, new PartitionKey(orderId));
            lineRu += lResp.RequestCharge;
        }
    }
    Console.WriteLine($"seed-ref done: orders {orderRu:0} RU, lines {lineRu:0} RU, avg total {(orderRu+lineRu)/count:0.00} RU/order");
}

async Task QueryEmbed()
{
    var custId = "cus-0007";
    var q = new QueryDefinition("SELECT TOP 10 * FROM c WHERE c.customerId = @c ORDER BY c.placedUtc DESC")
        .WithParameter("@c", custId);
    using var iter = ordersEmbed.GetItemQueryIterator<OrderEmbed>(q,
        requestOptions: new QueryRequestOptions { PartitionKey = new PartitionKey(custId) });

    double ru = 0;
    var count = 0;
    while (iter.HasMoreResults)
    {
        var page = await iter.ReadNextAsync();
        ru += page.RequestCharge;
        foreach (var o in page) count++;
    }
    Console.WriteLine($"EMBED query: {count} orders returned, {ru:0.00} RU total ({ru/count:0.00} RU/order)");
}

async Task QueryRef()
{
    var custId = "cus-0007";
    var q = new QueryDefinition("SELECT TOP 10 * FROM c WHERE c.customerId = @c ORDER BY c.placedUtc DESC")
        .WithParameter("@c", custId);
    using var iter = ordersRef.GetItemQueryIterator<OrderRef>(q,
        requestOptions: new QueryRequestOptions { PartitionKey = new PartitionKey(custId) });

    double ru = 0;
    var orders = new List<OrderRef>();
    while (iter.HasMoreResults)
    {
        var page = await iter.ReadNextAsync();
        ru += page.RequestCharge;
        orders.AddRange(page);
    }

    foreach (var o in orders)
    {
        foreach (var lid in o.lineIds)
        {
            var lResp = await linesRef.ReadItemAsync<LineRef>(lid, new PartitionKey(o.id));
            ru += lResp.RequestCharge;
        }
    }
    Console.WriteLine($"REF query: {orders.Count} orders + all their lines, {ru:0.00} RU total ({ru/Math.Max(1,orders.Count):0.00} RU/order)");
}

static async Task<double[]> WhenAll(List<Task<double>> tasks)
{
    return await Task.WhenAll(tasks);
}

static (string id, string customerId, DateTime placedUtc, string status) BuildOrder(string id, string cust, Random rnd)
    => (id, cust, DateTime.UtcNow.AddMinutes(-rnd.Next(60*24*365)), "Placed");

static LineEmbed BuildEmbeddedLine(Random rnd)
{
    var products = new[] {
        ("prod-4s-tent",  "4-Season Tent",  599m),
        ("prod-3s-tent",  "3-Season Tent",  399m),
        ("prod-60l-pack", "60L Backpack",   189m),
        ("prod-30l-pack", "30L Daypack",     99m),
        ("prod-headlamp", "300lm Headlamp",  49m),
    };
    var p = products[rnd.Next(products.Length)];
    return new LineEmbed(p.Item1, p.Item2, 1 + rnd.Next(3), p.Item3);
}

public record LineEmbed(string productId, string productName, int qty, decimal unitPrice);
public record OrderEmbed(string id, string customerId, DateTime placedUtc, string status, List<LineEmbed> lines);
public record OrderRef(string id, string customerId, DateTime placedUtc, string status, List<string> lineIds);
public record LineRef(string id, string orderId, string productId, string productName, int qty, decimal unitPrice);
