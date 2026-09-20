using System.Diagnostics;
using Azure.Identity;
using Microsoft.Azure.Cosmos;

var endpoint = Environment.GetEnvironmentVariable("ANCHORLINE_COSMOS_ENDPOINT")
    ?? throw new InvalidOperationException("ANCHORLINE_COSMOS_ENDPOINT missing");
var dbName = Environment.GetEnvironmentVariable("ANCHORLINE_COSMOS_DB") ?? "AnchorlineConsistency";

var mode = args.Length > 0 ? args[0] : "help";

switch (mode)
{
    case "bench":  await Bench(); break;
    case "override": await OverrideDemo(); break;
    default: Console.WriteLine("Modes: bench | override"); break;
}

async Task Bench()
{
    Console.WriteLine("Level              | write ms (p50/p99) | write RU | read ms (p50/p99) | read RU");
    Console.WriteLine(new string('-', 90));
    var levels = new[]
    {
        (ConsistencyLevel.Strong,           "Strong"),
        (ConsistencyLevel.BoundedStaleness, "BoundedStaleness"),
        (ConsistencyLevel.Session,          "Session"),
        (ConsistencyLevel.ConsistentPrefix, "ConsistentPrefix"),
        (ConsistencyLevel.Eventual,         "Eventual")
    };
    foreach (var (level, name) in levels)
    {
        try { await Sample(level, name); }
        catch (CosmosException ex) { Console.WriteLine($"{name,-18} | ERROR {ex.StatusCode}: {ex.Message.Substring(0, Math.Min(40, ex.Message.Length))}"); }
        catch (Exception ex)       { Console.WriteLine($"{name,-18} | ERROR {ex.Message.Substring(0, Math.Min(40, ex.Message.Length))}"); }
    }
}

async Task Sample(ConsistencyLevel level, string name)
{
    using var client = new CosmosClient(endpoint, new DefaultAzureCredential(), new CosmosClientOptions
    {
        ApplicationName = "az-dev-140-consistency",
        ConsistencyLevel = level
    });
    var db = (await client.CreateDatabaseIfNotExistsAsync(dbName)).Database;
    var container = (await db.CreateContainerIfNotExistsAsync(new ContainerProperties("bench", "/id"), 400)).Container;

    // Warmup
    for (int i = 0; i < 5; i++)
    {
        var w = await container.UpsertItemAsync(new Item($"warm-{i}", 0), new PartitionKey($"warm-{i}"));
        await container.ReadItemAsync<Item>($"warm-{i}", new PartitionKey($"warm-{i}"));
    }

    // Actual measurement
    var writeMs = new List<double>();
    var readMs  = new List<double>();
    double writeRu = 0, readRu = 0;
    for (int i = 0; i < 50; i++)
    {
        var sw = Stopwatch.StartNew();
        var w = await container.UpsertItemAsync(new Item($"bench-{i}", i), new PartitionKey($"bench-{i}"));
        sw.Stop();
        writeMs.Add(sw.Elapsed.TotalMilliseconds); writeRu += w.RequestCharge;

        sw.Restart();
        var r = await container.ReadItemAsync<Item>($"bench-{i}", new PartitionKey($"bench-{i}"));
        sw.Stop();
        readMs.Add(sw.Elapsed.TotalMilliseconds); readRu += r.RequestCharge;
    }

    writeMs.Sort(); readMs.Sort();
    var wp50 = writeMs[writeMs.Count/2]; var wp99 = writeMs[(int)(writeMs.Count*0.99)];
    var rp50 = readMs [readMs.Count/2];  var rp99 = readMs [(int)(readMs.Count*0.99)];
    Console.WriteLine($"{name,-18} | {wp50,6:0.0}/{wp99,6:0.0} ms      | {writeRu/50,6:0.00}    | {rp50,6:0.0}/{rp99,6:0.0} ms       | {readRu/50,5:0.00}");
}

async Task OverrideDemo()
{
    using var client = new CosmosClient(endpoint, new DefaultAzureCredential(), new CosmosClientOptions
    {
        ConsistencyLevel = ConsistencyLevel.Session
    });
    var db = (await client.CreateDatabaseIfNotExistsAsync(dbName)).Database;
    var container = (await db.CreateContainerIfNotExistsAsync(new ContainerProperties("bench", "/id"), 400)).Container;

    await container.UpsertItemAsync(new Item("prod-hot", 42), new PartitionKey("prod-hot"));

    var sessionRead = await container.ReadItemAsync<Item>("prod-hot", new PartitionKey("prod-hot"));
    Console.WriteLine($"Account-default Session read: {sessionRead.RequestCharge:0.00} RU, {sessionRead.Diagnostics}");

    var eventualRead = await container.ReadItemAsync<Item>("prod-hot", new PartitionKey("prod-hot"),
        new ItemRequestOptions { ConsistencyLevel = ConsistencyLevel.Eventual });
    Console.WriteLine($"Per-request Eventual read:    {eventualRead.RequestCharge:0.00} RU");
}

public record Item(string id, int value);
