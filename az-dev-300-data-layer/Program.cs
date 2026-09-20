using Azure.Core;
using Azure.Identity;
using Microsoft.Azure.Cosmos;
using Microsoft.Data.SqlClient;
using Microsoft.EntityFrameworkCore;

var sqlServer = Environment.GetEnvironmentVariable("SQL_SERVER") ?? throw new("SQL_SERVER");
var sqlDb     = Environment.GetEnvironmentVariable("SQL_DB")     ?? "TaskForge";
var cosmosEp  = Environment.GetEnvironmentVariable("COSMOS_ENDPOINT") ?? throw new("COSMOS_ENDPOINT");

var cred = new DefaultAzureCredential();

// ----- SQL: RLS + SESSION_CONTEXT -----
var token = (await cred.GetTokenAsync(new TokenRequestContext(new[] { "https://database.windows.net/.default" }), default)).Token;
using (var sql = new SqlConnection($"Server=tcp:{sqlServer},1433;Database={sqlDb};Encrypt=True"))
{
    sql.AccessToken = token;
    await sql.OpenAsync();

    // Set tenantId in SESSION_CONTEXT (this is the interceptor's job in the real app)
    using (var setCtx = sql.CreateCommand())
    {
        setCtx.CommandText = "EXEC sp_set_session_context N'tenantId', @tid";
        setCtx.Parameters.AddWithValue("@tid", "a0000000-0000-0000-0000-000000000001");
        await setCtx.ExecuteNonQueryAsync();
    }
    using (var q = sql.CreateCommand())
    {
        q.CommandText = "SELECT COUNT(*) FROM Tasks";
        var n = (int)(await q.ExecuteScalarAsync() ?? 0);
        Console.WriteLine($"Tenant A sees {n} tasks (RLS-filtered)");
    }
}

// ----- Cosmos: hierarchical partition key -----
using var cosmos = new CosmosClient(cosmosEp, cred);
var container = cosmos.GetContainer("TaskForge", "tasks");
var pk = new PartitionKeyBuilder().Add("a0000000-0000-0000-0000-000000000001").Add("proj-001").Build();
try
{
    var task = new { id = "tsk-" + Guid.NewGuid().ToString("n"), tenantId = "a0000000-0000-0000-0000-000000000001", projectId = "proj-001", title = "Seeded from starter", status = "active" };
    var r = await container.CreateItemAsync(task, pk);
    Console.WriteLine($"Cosmos write RU: {r.RequestCharge}");
}
catch (CosmosException ex) when (ex.StatusCode == System.Net.HttpStatusCode.NotFound)
{
    Console.WriteLine("Container not yet created — run the ARM template or `az cosmosdb sql container create`.");
}
