using System.Diagnostics;
using Azure.Core;
using Azure.Identity;
using Microsoft.Data.SqlClient;
using Microsoft.EntityFrameworkCore;
using Anchorline.Orders;

var server = Environment.GetEnvironmentVariable("ANCHORLINE_SQL_SERVER")
    ?? throw new InvalidOperationException("ANCHORLINE_SQL_SERVER not set");
var database = Environment.GetEnvironmentVariable("ANCHORLINE_SQL_DATABASE") ?? "AnchorlineOrders";

var credential = new DefaultAzureCredential();
var token = await credential.GetTokenAsync(
    new TokenRequestContext(new[] { "https://database.windows.net/.default" }));

var connString = $"Server=tcp:{server},1433;Database={database};Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;";

var sqlConn = new SqlConnection(connString) { AccessToken = token.Token };
var opts = new DbContextOptionsBuilder<OrderContext>()
    .UseSqlServer(sqlConn, sql => sql.EnableRetryOnFailure(5, TimeSpan.FromSeconds(15), null))
    .Options;

var mode = args.Length > 0 ? args[0] : "seed";

await using (var db = new OrderContext(opts))
{
    if (mode == "seed") await Seed(db);
    else if (mode == "list") await ListOrders(db);
    else if (mode == "hot")  await HotReadDemo(db);
    else Console.WriteLine("Modes: seed | list | hot");
}

static async Task Seed(OrderContext db)
{
    if (!await db.Customers.AnyAsync())
    {
        var alice = new Customer { Name = "Alice Waters", Email = "alice@example.com" };
        var bob   = new Customer { Name = "Bob Rivers",   Email = "bob@example.com" };
        var tent  = new Product  { Name = "4-Season Tent", Sku = "TNT-4S-01", Price = 599.00m };
        var pack  = new Product  { Name = "60L Backpack",  Sku = "BPK-60-02", Price = 189.00m };
        db.AddRange(alice, bob, tent, pack);
        await db.SaveChangesAsync();

        db.Orders.Add(new Order
        {
            CustomerId = alice.CustomerId,
            PlacedUtc = DateTime.UtcNow,
            Status = "New",
            OrderLines = new()
            {
                new OrderLine { ProductId = tent.ProductId, Quantity = 1, UnitPrice = tent.Price },
                new OrderLine { ProductId = pack.ProductId, Quantity = 1, UnitPrice = pack.Price }
            }
        });
        await db.SaveChangesAsync();
    }
    Console.WriteLine("Seed complete.");
}

static async Task ListOrders(OrderContext db)
{
    var orders = await db.Orders.AsNoTracking()
        .AsSplitQuery()
        .Include(o => o.Customer)
        .Include(o => o.OrderLines).ThenInclude(l => l.Product)
        .ToListAsync();

    foreach (var o in orders)
    {
        var total = o.OrderLines.Sum(l => l.Quantity * l.UnitPrice);
        Console.WriteLine($"Order {o.OrderId} for {o.Customer.Name} - {o.OrderLines.Count} lines, total {total:C}");
    }
}

// Compiled query: cached LINQ translation. Best for hot paths.
static readonly Func<OrderContext, int, IAsyncEnumerable<Order>> GetOrderById =
    EF.CompileAsyncQuery((OrderContext db, int id) =>
        db.Orders.AsNoTracking().Where(o => o.OrderId == id));

static async Task HotReadDemo(OrderContext db)
{
    var anyOrder = await db.Orders.AsNoTracking().Select(o => o.OrderId).FirstOrDefaultAsync();
    if (anyOrder == 0) { Console.WriteLine("Seed first."); return; }

    var sw = Stopwatch.StartNew();
    for (int i = 0; i < 500; i++)
    {
        await foreach (var _ in GetOrderById(db, anyOrder)) { }
    }
    sw.Stop();
    Console.WriteLine($"Compiled query x500 : {sw.ElapsedMilliseconds} ms ({sw.ElapsedMilliseconds / 500.0:F2} ms/query)");

    sw.Restart();
    for (int i = 0; i < 500; i++)
    {
        await db.Orders.AsNoTracking().Where(o => o.OrderId == anyOrder).ToListAsync();
    }
    sw.Stop();
    Console.WriteLine($"LINQ query x500     : {sw.ElapsedMilliseconds} ms ({sw.ElapsedMilliseconds / 500.0:F2} ms/query)");
}
