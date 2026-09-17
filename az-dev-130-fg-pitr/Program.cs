using Azure.Core;
using Azure.Identity;
using Microsoft.Data.SqlClient;

var fgWrite = Environment.GetEnvironmentVariable("ANCHORLINE_FG_WRITE")
    ?? throw new InvalidOperationException("ANCHORLINE_FG_WRITE not set (failover group write listener)");
var database = Environment.GetEnvironmentVariable("ANCHORLINE_SQL_DATABASE") ?? "AnchorlineOrders";

var cred = new DefaultAzureCredential();
var token = await cred.GetTokenAsync(new TokenRequestContext(new[] { "https://database.windows.net/.default" }));

var mode = args.Length > 0 ? args[0] : "help";

switch (mode)
{
    case "setup":  await Setup(); break;
    case "burst":  await BurstWrites(30); break;
    case "read":   await ReadStatus(); break;
    default: Console.WriteLine("Modes: setup | burst | read"); break;
}

async Task Setup()
{
    await using var conn = Open(fgWrite);
    await using var cmd = conn.CreateCommand();
    cmd.CommandText = @"
IF OBJECT_ID('dbo.Heartbeats','U') IS NULL
CREATE TABLE dbo.Heartbeats(
    Id INT IDENTITY PRIMARY KEY,
    Server NVARCHAR(120) NOT NULL,
    WrittenUtc DATETIME2 NOT NULL);";
    await cmd.ExecuteNonQueryAsync();
    Console.WriteLine("Setup done on write listener.");
}

async Task BurstWrites(int seconds)
{
    var end = DateTime.UtcNow.AddSeconds(seconds);
    var writes = 0;
    var failed = 0;
    while (DateTime.UtcNow < end)
    {
        try
        {
            await using var conn = Open(fgWrite);
            await using var cmd = conn.CreateCommand();
            cmd.CommandText = "INSERT INTO dbo.Heartbeats(Server, WrittenUtc) VALUES(@@SERVERNAME, SYSUTCDATETIME())";
            await cmd.ExecuteNonQueryAsync();
            writes++;
        }
        catch (SqlException ex)
        {
            failed++;
            Console.WriteLine($"  fail: {ex.Number} {ex.Message.Substring(0, Math.Min(80, ex.Message.Length))}");
        }
        await Task.Delay(500);
    }
    Console.WriteLine($"Burst done. Writes={writes}, failed={failed}.");
}

async Task ReadStatus()
{
    await using var conn = Open(fgWrite);
    await using var cmd = conn.CreateCommand();
    cmd.CommandText = @"
SELECT TOP 15 Server, WrittenUtc
FROM dbo.Heartbeats
ORDER BY Id DESC";
    await using var r = await cmd.ExecuteReaderAsync();
    Console.WriteLine("Server                                     | WrittenUtc");
    while (await r.ReadAsync())
        Console.WriteLine($"{r["Server"],-40} | {r["WrittenUtc"]}");
}

SqlConnection Open(string server)
{
    var cs = $"Server=tcp:{server},1433;Database={database};Encrypt=True;Connection Timeout=30;";
    var c = new SqlConnection(cs) { AccessToken = token.Token };
    c.Open();
    return c;
}
