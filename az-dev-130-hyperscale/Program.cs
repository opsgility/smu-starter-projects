using Azure.Core;
using Azure.Identity;
using Microsoft.Data.SqlClient;

var primary = Environment.GetEnvironmentVariable("ANCHORLINE_SQL_PRIMARY")
    ?? throw new InvalidOperationException("ANCHORLINE_SQL_PRIMARY not set (primary server FQDN)");
var replica = Environment.GetEnvironmentVariable("ANCHORLINE_SQL_REPLICA")
    ?? throw new InvalidOperationException("ANCHORLINE_SQL_REPLICA not set (named-replica server FQDN)");
var database = Environment.GetEnvironmentVariable("ANCHORLINE_SQL_DATABASE") ?? "AnchorlineOrders";

var cred = new DefaultAzureCredential();
var token = await cred.GetTokenAsync(new TokenRequestContext(new[] { "https://database.windows.net/.default" }));

var mode = args.Length > 0 ? args[0] : "help";

switch (mode)
{
    case "setup":  await Setup(); break;
    case "write":  await Write(); break;
    case "read":   await Read(); break;
    case "readonly": await ReadOnlyIntent(); break;
    default:
        Console.WriteLine("Modes: setup | write | read | readonly");
        break;
}

async Task Setup()
{
    await using var conn = Open(primary);
    await using var cmd = conn.CreateCommand();
    cmd.CommandText = @"
IF OBJECT_ID('dbo.Signals','U') IS NULL
CREATE TABLE dbo.Signals(
    SignalId INT IDENTITY PRIMARY KEY,
    WrittenUtc DATETIME2 NOT NULL,
    Origin NVARCHAR(80) NOT NULL,
    Payload NVARCHAR(200) NOT NULL);";
    await cmd.ExecuteNonQueryAsync();
    Console.WriteLine("Setup on primary complete.");
}

async Task Write()
{
    await using var conn = Open(primary);
    await using var cmd = conn.CreateCommand();
    cmd.CommandText = "INSERT INTO dbo.Signals(WrittenUtc, Origin, Payload) VALUES(SYSUTCDATETIME(), @@SERVERNAME, @p)";
    cmd.Parameters.Add(new SqlParameter("@p", $"write from {Environment.MachineName}"));
    var n = await cmd.ExecuteNonQueryAsync();
    Console.WriteLine($"Inserted {n} row on {conn.DataSource}");

    // Confirm which server the connection sat on
    var who = conn.CreateCommand();
    who.CommandText = "SELECT @@SERVERNAME AS ServerName";
    Console.WriteLine($"@@SERVERNAME = {await who.ExecuteScalarAsync()}");
}

async Task Read()
{
    await using var conn = Open(replica);
    await using var cmd = conn.CreateCommand();
    cmd.CommandText = @"
SELECT @@SERVERNAME AS ServerName, COUNT(*) AS SignalCount FROM dbo.Signals";
    await using var r = await cmd.ExecuteReaderAsync();
    while (await r.ReadAsync())
        Console.WriteLine($"Read from replica -- @@SERVERNAME={r["ServerName"]}, SignalCount={r["SignalCount"]}");
}

async Task ReadOnlyIntent()
{
    // Prove that trying to write to the replica FAILS.
    await using var conn = Open(replica);
    await using var cmd = conn.CreateCommand();
    cmd.CommandText = "INSERT INTO dbo.Signals(WrittenUtc, Origin, Payload) VALUES(SYSUTCDATETIME(), @@SERVERNAME, 'attempted from replica')";
    try
    {
        await cmd.ExecuteNonQueryAsync();
        Console.WriteLine("UNEXPECTED: write to replica succeeded (should have failed)");
    }
    catch (SqlException ex)
    {
        Console.WriteLine($"Expected failure on replica write: {ex.Number} {ex.Message}");
    }
}

SqlConnection Open(string serverFqdn)
{
    var cs = $"Server=tcp:{serverFqdn},1433;Database={database};Encrypt=True;Connection Timeout=30;";
    var c = new SqlConnection(cs) { AccessToken = token.Token };
    c.Open();
    return c;
}
