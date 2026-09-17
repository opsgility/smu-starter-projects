using Azure.Core;
using Azure.Identity;
using Microsoft.Data.SqlClient;

var server = Environment.GetEnvironmentVariable("ANCHORLINE_SQL_SERVER")
    ?? throw new InvalidOperationException("ANCHORLINE_SQL_SERVER not set (fully-qualified server, e.g. anchorline-sql-abc.database.windows.net)");
var database = Environment.GetEnvironmentVariable("ANCHORLINE_SQL_DATABASE") ?? "AnchorlineOrders";

var credential = new DefaultAzureCredential(new DefaultAzureCredentialOptions
{
    ExcludeInteractiveBrowserCredential = false
});

var token = await credential.GetTokenAsync(
    new TokenRequestContext(new[] { "https://database.windows.net/.default" }));

var connectionString = $"Server=tcp:{server},1433;Database={database};Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;";

await using var conn = new SqlConnection(connectionString);
conn.AccessToken = token.Token;
await conn.OpenAsync();

Console.WriteLine($"Connected to {server}/{database} as Entra ID identity.");

await using var cmd = conn.CreateCommand();
cmd.CommandText = @"
SELECT
  SUSER_SNAME() AS EntraIdentity,
  DB_NAME() AS DatabaseName,
  @@VERSION AS ServerVersion,
  SYSDATETIMEOFFSET() AS ServerTime;";

await using var reader = await cmd.ExecuteReaderAsync();
while (await reader.ReadAsync())
{
    Console.WriteLine($"  Identity : {reader["EntraIdentity"]}");
    Console.WriteLine($"  Database : {reader["DatabaseName"]}");
    Console.WriteLine($"  Version  : {reader["ServerVersion"]}");
    Console.WriteLine($"  Time     : {reader["ServerTime"]}");
}
