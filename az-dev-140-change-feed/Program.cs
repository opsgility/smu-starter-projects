using Azure.Identity;
using Microsoft.Azure.Cosmos;

var endpoint = Environment.GetEnvironmentVariable("ANCHORLINE_COSMOS_ENDPOINT")
    ?? throw new InvalidOperationException("ANCHORLINE_COSMOS_ENDPOINT missing");
var dbName = Environment.GetEnvironmentVariable("ANCHORLINE_COSMOS_DB") ?? "AnchorlineChangeFeed";

var client = new CosmosClient(endpoint, new DefaultAzureCredential(), new CosmosClientOptions
{
    ApplicationName = "az-dev-140-change-feed"
});

var db = (await client.CreateDatabaseIfNotExistsAsync(dbName)).Database;
var orders   = (await db.CreateContainerIfNotExistsAsync(new ContainerProperties("orders",   "/customerId"), 400)).Container;
var summary  = (await db.CreateContainerIfNotExistsAsync(new ContainerProperties("summary",  "/customerId"), 400)).Container;
var lease    = (await db.CreateContainerIfNotExistsAsync(new ContainerProperties("lease",    "/id"),         400)).Container;

var mode = args.Length > 0 ? args[0] : "help";
switch (mode)
{
    case "burst":     await Burst(10000); break;
    case "processor": await StartProcessor(); break;
    case "summary":   await ShowSummary(); break;
    default: Console.WriteLine("Modes: burst | processor | summary"); break;
}

async Task Burst(int count)
{
    Console.WriteLine($"Burst-writing {count} orders...");
    var rnd = new Random(42);
    for (int i = 0; i < count; i++)
    {
        var cust = $"cus-{rnd.Next(200):D4}";
        var order = new Order($"ord-{i:D6}", cust, DateTime.UtcNow, 25 + (decimal)(rnd.NextDouble() * 400));
        await orders.CreateItemAsync(order, new PartitionKey(cust));
        if ((i+1) % 1000 == 0) Console.WriteLine($"  {i+1} written");
    }
    Console.WriteLine($"burst done - {count}");
}

async Task StartProcessor()
{
    var processor = orders
        .GetChangeFeedProcessorBuilder<Order>("OrderProjector", HandleChanges)
        .WithInstanceName(Environment.MachineName + "-" + Guid.NewGuid().ToString("N")[..8])
        .WithLeaseContainer(lease)
        .Build();

    await processor.StartAsync();
    Console.WriteLine("Processor running. Ctrl-C to stop.");
    await Task.Delay(-1);

    async Task HandleChanges(ChangeFeedProcessorContext ctx, IReadOnlyCollection<Order> changes, CancellationToken ct)
    {
        var byCustomer = changes.GroupBy(o => o.customerId);
        foreach (var group in byCustomer)
        {
            var custId = group.Key;
            var incCount = group.Count();
            var incTotal = group.Sum(o => o.amount);

            CustomerSummary current;
            try
            {
                var read = await summary.ReadItemAsync<CustomerSummary>(custId, new PartitionKey(custId), cancellationToken: ct);
                current = read.Resource;
            }
            catch (CosmosException ex) when (ex.StatusCode == System.Net.HttpStatusCode.NotFound)
            {
                current = new CustomerSummary(custId, custId, 0, 0);
            }

            var updated = current with
            {
                orderCount = current.orderCount + incCount,
                totalSpent = current.totalSpent + incTotal
            };
            await summary.UpsertItemAsync(updated, new PartitionKey(custId), cancellationToken: ct);
        }
        Console.WriteLine($"  processed batch of {changes.Count} -> {byCustomer.Count()} customers updated");
    }
}

async Task ShowSummary()
{
    using var iter = summary.GetItemQueryIterator<CustomerSummary>("SELECT * FROM c ORDER BY c.totalSpent DESC OFFSET 0 LIMIT 10");
    Console.WriteLine("customer  | orders | totalSpent");
    while (iter.HasMoreResults)
    {
        var page = await iter.ReadNextAsync();
        foreach (var s in page)
            Console.WriteLine($"{s.customerId} | {s.orderCount,6} | {s.totalSpent:C}");
    }
}

public record Order(string id, string customerId, DateTime placedUtc, decimal amount);
public record CustomerSummary(string id, string customerId, int orderCount, decimal totalSpent);
