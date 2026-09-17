using Azure.Core;
using Azure.Identity;
using Microsoft.Data.SqlClient;

var builder = WebApplication.CreateBuilder(args);

var sqlServer = builder.Configuration["Anchorline:SqlServer"]
    ?? throw new InvalidOperationException("Anchorline:SqlServer missing (e.g. anchorline-sql-xxx.database.windows.net)");
var sqlDatabase = builder.Configuration["Anchorline:SqlDatabase"] ?? "AnchorlineOrders";
var miClientId  = builder.Configuration["Anchorline:MiClientId"];

builder.Services.AddSingleton<TokenCredential>(_ =>
    string.IsNullOrEmpty(miClientId)
        ? new DefaultAzureCredential()
        : new DefaultAzureCredential(new DefaultAzureCredentialOptions { ManagedIdentityClientId = miClientId }));

var app = builder.Build();

app.MapGet("/", () => Results.Ok(new { app = "anchorline-mi-api", ok = true }));

app.MapGet("/whoami", async (TokenCredential cred, ILogger<Program> log) =>
{
    var connString = $"Server=tcp:{sqlServer},1433;Database={sqlDatabase};Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;";

    await using var conn = new SqlConnection(connString);
    conn.AccessTokenCallback = async (ctx, ct) =>
    {
        var t = await cred.GetTokenAsync(
            new TokenRequestContext(new[] { "https://database.windows.net/.default" }), ct);
        return new SqlAuthenticationToken(t.Token, t.ExpiresOn);
    };

    try
    {
        await conn.OpenAsync();
        await using var cmd = conn.CreateCommand();
        cmd.CommandText = @"
SELECT
    SUSER_SNAME()   AS EntraIdentity,
    USER_NAME()     AS DatabaseUser,
    DB_NAME()       AS DatabaseName,
    IS_ROLEMEMBER('db_datareader') AS IsDbReader,
    IS_ROLEMEMBER('db_datawriter') AS IsDbWriter,
    SYSDATETIMEOFFSET() AS ServerTime;";
        await using var reader = await cmd.ExecuteReaderAsync();
        if (!await reader.ReadAsync()) return Results.NotFound();
        return Results.Ok(new
        {
            entraIdentity = reader["EntraIdentity"],
            databaseUser  = reader["DatabaseUser"],
            databaseName  = reader["DatabaseName"],
            isDbReader    = Convert.ToInt32(reader["IsDbReader"]) == 1,
            isDbWriter    = Convert.ToInt32(reader["IsDbWriter"]) == 1,
            serverTime    = reader["ServerTime"]
        });
    }
    catch (SqlException ex)
    {
        log.LogError(ex, "SQL error");
        return Results.Problem(title: "SQL failure", detail: ex.Message, statusCode: 500);
    }
});

app.Run();
