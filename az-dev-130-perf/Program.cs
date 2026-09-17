using System.Diagnostics;
using Azure.Core;
using Azure.Identity;
using Microsoft.Data.SqlClient;

var server = Environment.GetEnvironmentVariable("ANCHORLINE_SQL_SERVER")
    ?? throw new InvalidOperationException("ANCHORLINE_SQL_SERVER not set");
var database = Environment.GetEnvironmentVariable("ANCHORLINE_SQL_DATABASE") ?? "AnchorlineOrders";

var cred = new DefaultAzureCredential();
var token = await cred.GetTokenAsync(new TokenRequestContext(new[] { "https://database.windows.net/.default" }));
var connString = $"Server=tcp:{server},1433;Database={database};Encrypt=True;Connection Timeout=30;";

SqlConnection Conn()
{
    var c = new SqlConnection(connString) { AccessToken = token.Token };
    c.Open();
    return c;
}

var mode = args.Length > 0 ? args[0] : "help";

switch (mode)
{
    case "seed":  Seed(1_000_000); break;
    case "slow":  RunQuery("slow"); break;
    case "fast":  RunQuery("fast"); break;
    case "top":   ShowTopQueryStore(); break;
    default: Console.WriteLine("Modes: seed | slow | fast | top"); break;
}

void Seed(int rows)
{
    using var c = Conn();
    ExecNonQuery(c, @"
IF OBJECT_ID('dbo.LoadOrders','U') IS NULL
CREATE TABLE dbo.LoadOrders(
    OrderId    INT IDENTITY PRIMARY KEY CLUSTERED,
    CustomerId INT NOT NULL,
    Status     NVARCHAR(30) NOT NULL,
    PlacedUtc  DATETIME2 NOT NULL,
    Region     NVARCHAR(30) NOT NULL,
    Total      DECIMAL(10,2) NOT NULL,
    Notes      NVARCHAR(400) NULL
);");
    var have = ExecScalar<int>(c, "SELECT COUNT(*) FROM dbo.LoadOrders");
    if (have >= rows) { Console.WriteLine($"Already have {have} rows."); return; }

    Console.WriteLine($"Seeding to {rows} rows (batches of 10k)...");
    var sw = Stopwatch.StartNew();
    var statuses = new[] { "New", "Pending", "Shipped", "Delivered", "Cancelled" };
    var regions  = new[] { "West", "East", "North", "South", "Central" };
    var rnd = new Random(42);
    var batch = 10_000;
    while (have < rows)
    {
        using var tx = c.BeginTransaction();
        using var cmd = c.CreateCommand();
        cmd.Transaction = tx;
        var sb = new System.Text.StringBuilder();
        sb.AppendLine("INSERT INTO dbo.LoadOrders(CustomerId, Status, PlacedUtc, Region, Total, Notes) VALUES");
        var values = new List<string>();
        for (int i = 0; i < batch; i++)
        {
            var cust = rnd.Next(1, 50_000);
            var status = statuses[rnd.Next(statuses.Length)];
            var region = regions[rnd.Next(regions.Length)];
            var placed = DateTime.UtcNow.AddDays(-rnd.Next(0, 365));
            var total  = (decimal)(rnd.NextDouble() * 500 + 10);
            values.Add($"({cust}, '{status}', '{placed:o}', '{region}', {total:0.00}, NULL)");
        }
        sb.Append(string.Join(",\n", values));
        cmd.CommandText = sb.ToString();
        cmd.CommandTimeout = 60;
        cmd.ExecuteNonQuery();
        tx.Commit();
        have += batch;
        if (have % 100_000 == 0) Console.WriteLine($"  {have} rows...");
    }
    sw.Stop();
    Console.WriteLine($"Seed done in {sw.Elapsed}.");
}

void RunQuery(string mode)
{
    var query = @"
/*QLABEL:perf-search*/
SELECT OrderId, CustomerId, PlacedUtc, Region, Total
FROM dbo.LoadOrders
WHERE Status = @status AND PlacedUtc > DATEADD(DAY, -30, SYSUTCDATETIME())
ORDER BY PlacedUtc DESC";

    // Same query text in both modes; index difference alone drives the plan change.
    using var c = Conn();
    var sw = Stopwatch.StartNew();
    using var cmd = c.CreateCommand();
    cmd.CommandText = query;
    cmd.Parameters.Add(new SqlParameter("@status", "Pending"));
    using var reader = cmd.ExecuteReader();
    var rows = 0;
    while (reader.Read()) rows++;
    sw.Stop();
    Console.WriteLine($"{mode}: {rows} rows in {sw.ElapsedMilliseconds} ms");
}

void ShowTopQueryStore()
{
    using var c = Conn();
    var q = @"
SELECT TOP 5
    qsq.query_id,
    LEFT(qsqt.query_sql_text, 120) AS sql_preview,
    SUM(rs.avg_duration * rs.count_executions) / 1000.0 AS total_ms,
    SUM(rs.count_executions) AS total_execs,
    AVG(rs.avg_duration) / 1000.0 AS avg_ms_per_exec
FROM sys.query_store_runtime_stats rs
JOIN sys.query_store_plan qp ON qp.plan_id = rs.plan_id
JOIN sys.query_store_query qsq ON qsq.query_id = qp.query_id
JOIN sys.query_store_query_text qsqt ON qsqt.query_text_id = qsq.query_text_id
WHERE qsqt.query_sql_text LIKE '%QLABEL:perf-search%'
GROUP BY qsq.query_id, qsqt.query_sql_text
ORDER BY total_ms DESC;";

    using var cmd = c.CreateCommand();
    cmd.CommandText = q;
    cmd.CommandTimeout = 30;
    using var r = cmd.ExecuteReader();
    Console.WriteLine("QueryId | AvgMs | Execs | TotalMs | SQL");
    while (r.Read())
        Console.WriteLine($"{r["query_id"]} | {Convert.ToDouble(r["avg_ms_per_exec"]):F2} | {r["total_execs"]} | {Convert.ToDouble(r["total_ms"]):F0} | {r["sql_preview"]}");
}

void ExecNonQuery(SqlConnection c, string sql)
{
    using var cmd = c.CreateCommand();
    cmd.CommandText = sql;
    cmd.CommandTimeout = 60;
    cmd.ExecuteNonQuery();
}

T ExecScalar<T>(SqlConnection c, string sql)
{
    using var cmd = c.CreateCommand();
    cmd.CommandText = sql;
    return (T)Convert.ChangeType(cmd.ExecuteScalar()!, typeof(T));
}
