using Azure.Core;
using Azure.Identity;
using Microsoft.Data.SqlClient;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using Anchorline.Resiliency;

var server = Environment.GetEnvironmentVariable("ANCHORLINE_SQL_SERVER")
    ?? throw new InvalidOperationException("ANCHORLINE_SQL_SERVER not set");
var database = Environment.GetEnvironmentVariable("ANCHORLINE_SQL_DATABASE") ?? "AnchorlineOrders";

using var loggerFactory = LoggerFactory.Create(b => b.AddSimpleConsole(o => o.SingleLine = true).SetMinimumLevel(LogLevel.Information));
var log = loggerFactory.CreateLogger("resiliency");

var cred = new DefaultAzureCredential();
var token = await cred.GetTokenAsync(new TokenRequestContext(new[] { "https://database.windows.net/.default" }));

var connString = $"Server=tcp:{server},1433;Database={database};Encrypt=True;Connection Timeout=30;Max Pool Size=100;";

DbContextOptions<ResilContext> BuildOptions(bool withRetry, int transientFailures)
{
    var sqlConn = new SqlConnection(connString) { AccessToken = token.Token };
    var b = new DbContextOptionsBuilder<ResilContext>()
        .LogTo(m => log.LogInformation("EF: {msg}", m), LogLevel.Information);

    if (withRetry)
        b.UseSqlServer(sqlConn, sql => sql.EnableRetryOnFailure(6, TimeSpan.FromSeconds(15), null));
    else
        b.UseSqlServer(sqlConn);

    if (transientFailures > 0)
        b.AddInterceptors(new TransientInjector(transientFailures, log));

    return b.Options;
}

var mode = args.Length > 0 ? args[0] : "help";
switch (mode)
{
    case "setup":  await Setup(); break;
    case "noretry": await Run(withRetry: false, transientFailures: 2); break;
    case "retry":   await Run(withRetry: true,  transientFailures: 3); break;
    case "tx":      await RunTx(withRetry: true, transientFailures: 2); break;
    default:
        Console.WriteLine("Modes: setup | noretry | retry | tx");
        break;
}

async Task Setup()
{
    await using var db = new ResilContext(BuildOptions(withRetry: true, transientFailures: 0));
    await db.Database.EnsureCreatedAsync();
    if (!await db.Counters.AnyAsync())
    {
        db.Counters.Add(new Counter { Id = 1, Value = 0 });
        await db.SaveChangesAsync();
    }
    log.LogInformation("Setup complete: Pings + Counters ready.");
}

async Task Run(bool withRetry, int transientFailures)
{
    await using var db = new ResilContext(BuildOptions(withRetry, transientFailures));
    try
    {
        db.Pings.Add(new Ping { SentUtc = DateTime.UtcNow, Payload = $"withRetry={withRetry}" });
        await db.SaveChangesAsync();
        log.LogInformation("Insert succeeded (withRetry={r})", withRetry);
    }
    catch (Exception ex)
    {
        log.LogError(ex, "Insert failed (withRetry={r})", withRetry);
    }
}

async Task RunTx(bool withRetry, int transientFailures)
{
    await using var db = new ResilContext(BuildOptions(withRetry, transientFailures));
    var strategy = db.Database.CreateExecutionStrategy();
    try
    {
        await strategy.ExecuteAsync(async () =>
        {
            using var tx = await db.Database.BeginTransactionAsync();
            db.Pings.Add(new Ping { SentUtc = DateTime.UtcNow, Payload = "tx-demo" });
            await db.SaveChangesAsync();
            await db.Database.ExecuteSqlRawAsync("UPDATE Counters SET Value = Value + 1 WHERE Id = 1");
            await tx.CommitAsync();
        });
        var counter = await db.Counters.AsNoTracking().FirstAsync(c => c.Id == 1);
        log.LogInformation("Tx succeeded. Counter now = {v}", counter.Value);
    }
    catch (Exception ex)
    {
        log.LogError(ex, "Tx failed");
    }
}
