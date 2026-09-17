using System.Net;
using Azure.Identity;
using Microsoft.Azure.Cosmos;

var endpoint = Environment.GetEnvironmentVariable("ANCHORLINE_COSMOS_ENDPOINT")
    ?? throw new InvalidOperationException("ANCHORLINE_COSMOS_ENDPOINT missing");
var dbName  = Environment.GetEnvironmentVariable("ANCHORLINE_COSMOS_DB") ?? "AnchorlinePartition";

var client = new CosmosClient(endpoint, new DefaultAzureCredential(), new CosmosClientOptions
{
    ApplicationName = "az-dev-140-partitioning",
    AllowBulkExecution = true
});

var db = (await client.CreateDatabaseIfNotExistsAsync(dbName)).Database;
// Bad key - low cardinality
var eventsBadResp = await db.CreateContainerIfNotExistsAsync(
    new ContainerProperties("events_bad_key", "/eventType"),
    throughput: 400);
var eventsBad = eventsBadResp.Container;

// Good key - hierarchical
var eventsGoodResp = await db.CreateContainerIfNotExistsAsync(
    new ContainerProperties("events_hierarchical", new List<string> { "/tenantId", "/customerId" }),
    throughput: 400);
var eventsGood = eventsGoodResp.Container;

var mode = args.Length > 0 ? args[0] : "help";
switch (mode)
{
    case "load-bad":   await LoadBad(50000); break;
    case "load-good":  await LoadGood(50000); break;
    case "query-bad":  await QueryBad(); break;
    case "query-good": await QueryGood(); break;
    default: Console.WriteLine("Modes: load-bad | load-good | query-bad | query-good"); break;
}

async Task LoadBad(int count)
{
    var rnd = new Random(42);
    var eventTypes = new[] { "page_view", "add_to_cart", "checkout", "order_placed", "sign_in" };
    // page_view is 65% of the traffic
    var weights = new[] { 65, 15, 5, 5, 10 };
    string PickType()
    {
        var r = rnd.Next(100);
        var c = 0;
        for (int i = 0; i < weights.Length; i++) { c += weights[i]; if (r < c) return eventTypes[i]; }
        return eventTypes[0];
    }

    double totalRu = 0;
    var throttles = 0;
    var perType = new Dictionary<string, (double ru, int n)>();
    for (int i = 0; i < count; i++)
    {
        var type = PickType();
        var doc = new EventBadKey($"evt-{i:D8}", type, $"cus-{rnd.Next(1000):D4}", $"tenant-{rnd.Next(3)}", DateTime.UtcNow);
        try
        {
            var r = await eventsBad.CreateItemAsync(doc, new PartitionKey(type));
            totalRu += r.RequestCharge;
            var cur = perType.TryGetValue(type, out var v) ? v : (0d, 0);
            perType[type] = (cur.ru + r.RequestCharge, cur.n + 1);
        }
        catch (CosmosException ex) when (ex.StatusCode == HttpStatusCode.TooManyRequests) { throttles++; }
        if ((i+1) % 5000 == 0) Console.WriteLine($"  bad-key: {i+1} written, {throttles} throttles, {totalRu:0} RU total");
    }
    Console.WriteLine($"LOAD-BAD: {count} writes, {throttles} throttles, {totalRu:0} RU");
    foreach (var (t, v) in perType.OrderByDescending(x => x.Value.n))
        Console.WriteLine($"  {t,-14} {v.n,6} docs, {v.ru:0} RU");
}

async Task LoadGood(int count)
{
    var rnd = new Random(42);
    double totalRu = 0;
    var throttles = 0;
    for (int i = 0; i < count; i++)
    {
        var tid = $"tenant-{rnd.Next(3)}";
        var cid = $"cus-{rnd.Next(1000):D4}";
        var doc = new EventGoodKey($"evt-{i:D8}", tid, cid, "page_view", DateTime.UtcNow);
        try
        {
            var r = await eventsGood.CreateItemAsync(doc,
                new PartitionKeyBuilder().Add(tid).Add(cid).Build());
            totalRu += r.RequestCharge;
        }
        catch (CosmosException ex) when (ex.StatusCode == HttpStatusCode.TooManyRequests) { throttles++; }
        if ((i+1) % 5000 == 0) Console.WriteLine($"  good-key: {i+1} written, {throttles} throttles");
    }
    Console.WriteLine($"LOAD-GOOD: {count} writes, {throttles} throttles, {totalRu:0} RU");
}

async Task QueryBad()
{
    // "recent page_views" - hits ONE partition (the hot one)
    var q = new QueryDefinition("SELECT TOP 100 * FROM c WHERE c.eventType = 'page_view' ORDER BY c.tsUtc DESC");
    using var iter = eventsBad.GetItemQueryIterator<EventBadKey>(q,
        requestOptions: new QueryRequestOptions { PartitionKey = new PartitionKey("page_view") });
    double ru = 0;
    var n = 0;
    while (iter.HasMoreResults) { var p = await iter.ReadNextAsync(); ru += p.RequestCharge; foreach (var _ in p) n++; }
    Console.WriteLine($"QUERY-BAD (page_view partition): {n} rows, {ru:0.00} RU");
}

async Task QueryGood()
{
    var q = new QueryDefinition("SELECT TOP 100 * FROM c WHERE c.tenantId = 'tenant-0' AND c.customerId = 'cus-0007' ORDER BY c.tsUtc DESC");
    using var iter = eventsGood.GetItemQueryIterator<EventGoodKey>(q,
        requestOptions: new QueryRequestOptions
        {
            PartitionKey = new PartitionKeyBuilder().Add("tenant-0").Add("cus-0007").Build()
        });
    double ru = 0;
    var n = 0;
    while (iter.HasMoreResults) { var p = await iter.ReadNextAsync(); ru += p.RequestCharge; foreach (var _ in p) n++; }
    Console.WriteLine($"QUERY-GOOD (hierarchical scoped): {n} rows, {ru:0.00} RU");
}

public record EventBadKey(string id, string eventType, string customerId, string tenantId, DateTime tsUtc);
public record EventGoodKey(string id, string tenantId, string customerId, string eventType, DateTime tsUtc);
