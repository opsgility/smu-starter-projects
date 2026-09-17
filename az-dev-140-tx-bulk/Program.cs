using System.Diagnostics;
using Azure.Identity;
using Microsoft.Azure.Cosmos;

var endpoint = Environment.GetEnvironmentVariable("ANCHORLINE_COSMOS_ENDPOINT")
    ?? throw new InvalidOperationException("ANCHORLINE_COSMOS_ENDPOINT missing");
var dbName = Environment.GetEnvironmentVariable("ANCHORLINE_COSMOS_DB") ?? "AnchorlineTxBulk";

var mode = args.Length > 0 ? args[0] : "help";

switch (mode)
{
    case "bulk":   await BulkIngest(100_000); break;
    case "batch":  await AtomicOrder(); break;
    case "batch-fail": await AtomicOrderWithFailure(); break;
    default: Console.WriteLine("Modes: bulk | batch | batch-fail"); break;
}

async Task BulkIngest(int count)
{
    var client = new CosmosClient(endpoint, new DefaultAzureCredential(), new CosmosClientOptions
    {
        ApplicationName = "az-dev-140-tx-bulk",
        AllowBulkExecution = true
    });
    var db = (await client.CreateDatabaseIfNotExistsAsync(dbName)).Database;
    var container = (await db.CreateContainerIfNotExistsAsync(
        new ContainerProperties("events", "/tenantId"), 10000)).Container;

    var rnd = new Random(42);
    var sw = Stopwatch.StartNew();
    var tasks = new List<Task<ItemResponse<Event>>>(count);
    for (int i = 0; i < count; i++)
    {
        var doc = new Event($"evt-{i:D8}", $"tenant-{rnd.Next(50):D2}", DateTime.UtcNow, $"payload-{i}");
        tasks.Add(container.CreateItemAsync(doc, new PartitionKey(doc.tenantId)));
        if (tasks.Count == 5000)
        {
            var results = await Task.WhenAll(tasks);
            tasks.Clear();
        }
    }
    if (tasks.Count > 0) await Task.WhenAll(tasks);
    sw.Stop();
    Console.WriteLine($"Bulk ingest: {count} docs in {sw.Elapsed.TotalSeconds:0.0}s = {count/sw.Elapsed.TotalSeconds:0} docs/sec");
}

async Task AtomicOrder()
{
    var client = new CosmosClient(endpoint, new DefaultAzureCredential());
    var db = (await client.CreateDatabaseIfNotExistsAsync(dbName)).Database;
    var container = (await db.CreateContainerIfNotExistsAsync(
        new ContainerProperties("orders", "/customerId"), 400)).Container;

    var customerId = "cus-atomic-42";
    var orderId = $"ord-{Guid.NewGuid().ToString("N")[..8]}";
    var order = new OrderDoc(orderId, customerId, "order", DateTime.UtcNow, "Placed");
    var lines = Enumerable.Range(0, 4)
        .Select(i => new LineDoc($"{orderId}-l{i}", customerId, "line", orderId, "prod-4s-tent", 1, 599m))
        .ToArray();

    var batch = container.CreateTransactionalBatch(new PartitionKey(customerId));
    batch.CreateItem(order);
    foreach (var l in lines) batch.CreateItem(l);
    var resp = await batch.ExecuteAsync();
    Console.WriteLine($"Batch: {resp.StatusCode}, {resp.RequestCharge:0.00} RU total, {lines.Length + 1} operations");
    if (!resp.IsSuccessStatusCode)
    {
        Console.WriteLine("Batch failed:");
        foreach (var op in resp) Console.WriteLine($"  {op.StatusCode}");
    }
    else
    {
        Console.WriteLine("All operations committed atomically.");
    }
}

async Task AtomicOrderWithFailure()
{
    var client = new CosmosClient(endpoint, new DefaultAzureCredential());
    var db = (await client.CreateDatabaseIfNotExistsAsync(dbName)).Database;
    var container = (await db.CreateContainerIfNotExistsAsync(
        new ContainerProperties("orders", "/customerId"), 400)).Container;

    var customerId = "cus-atomic-99";
    var orderId = $"ord-{Guid.NewGuid().ToString("N")[..8]}";

    // Pre-write one of the "line" ids so the batch will conflict on that create.
    var conflictLineId = $"{orderId}-l1";
    await container.UpsertItemAsync(new LineDoc(conflictLineId, customerId, "line", orderId, "prod-preexisting", 1, 0), new PartitionKey(customerId));

    var order = new OrderDoc(orderId, customerId, "order", DateTime.UtcNow, "Placed");
    var batch = container.CreateTransactionalBatch(new PartitionKey(customerId));
    batch.CreateItem(order);
    for (int i = 0; i < 4; i++)
        batch.CreateItem(new LineDoc($"{orderId}-l{i}", customerId, "line", orderId, "prod-4s-tent", 1, 599m));
    var resp = await batch.ExecuteAsync();

    Console.WriteLine($"Batch: {resp.StatusCode}");
    for (int i = 0; i < resp.Count; i++)
        Console.WriteLine($"  op {i}: {resp[i].StatusCode}");

    // Prove the order was NOT written (atomic rollback)
    try
    {
        var readOrder = await container.ReadItemAsync<OrderDoc>(orderId, new PartitionKey(customerId));
        Console.WriteLine($"ORDER FOUND (unexpected): {readOrder.Resource.id}");
    }
    catch (CosmosException ex) when (ex.StatusCode == System.Net.HttpStatusCode.NotFound)
    {
        Console.WriteLine($"Order {orderId} is NOT present - batch rolled back atomically.");
    }
}

public record Event(string id, string tenantId, DateTime tsUtc, string payload);
public record OrderDoc(string id, string customerId, string type, DateTime placedUtc, string status);
public record LineDoc(string id, string customerId, string type, string orderId, string productId, int qty, decimal unitPrice);
