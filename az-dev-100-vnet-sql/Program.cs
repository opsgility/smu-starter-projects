// AZ-DEV-100 Module 6 — Anchorline storefront with private-endpoint SQL access.

using System.Net;
using Microsoft.Data.SqlClient;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/health", () => Results.Ok(new { status = "healthy", timestamp = DateTime.UtcNow }));

app.MapGet("/version", (IConfiguration config) => Results.Ok(new
{
    buildTag = config["AZ_DEV_100_BUILD_TAG"] ?? "unset",
    slotName = Environment.GetEnvironmentVariable("WEBSITE_SLOT_NAME") ?? "not-app-service",
    dotnetVersion = Environment.Version.ToString()
}));

// /dns — resolves the SQL hostname. On private-endpoint setup this returns a private IP.
app.MapGet("/dns", (IConfiguration config) =>
{
    var conn = config["Anchorline:SqlConnection"] ?? "";
    var host = new SqlConnectionStringBuilder(conn).DataSource;
    if (string.IsNullOrEmpty(host)) return Results.Ok(new { host = "unset", ips = Array.Empty<string>() });
    try
    {
        var addrs = Dns.GetHostAddresses(host).Select(a => a.ToString()).ToArray();
        return Results.Ok(new { host, ips = addrs, isPrivate = addrs.Any(a => a.StartsWith("10.") || a.StartsWith("172.") || a.StartsWith("192.168.")) });
    }
    catch (Exception ex) { return Results.Ok(new { host, error = ex.Message }); }
});

// /products — SELECT from the Products table via the SQL connection string.
app.MapGet("/products", async (IConfiguration config) =>
{
    var conn = config["Anchorline:SqlConnection"];
    if (string.IsNullOrWhiteSpace(conn)) return Results.BadRequest(new { error = "Anchorline:SqlConnection not set" });

    try
    {
        await using var db = new SqlConnection(conn);
        await db.OpenAsync();
        await using var cmd = new SqlCommand("SELECT TOP 10 Id, Name, Price FROM dbo.Products ORDER BY Id", db);
        await using var r = await cmd.ExecuteReaderAsync();
        var rows = new List<object>();
        while (await r.ReadAsync()) rows.Add(new { Id = r.GetInt32(0), Name = r.GetString(1), Price = r.GetDecimal(2) });
        return Results.Ok(new { count = rows.Count, products = rows });
    }
    catch (Exception ex) { return Results.Problem(ex.Message); }
});

app.MapGet("/", () => Results.Content("Anchorline VNet-SQL — /health /version /dns /products", "text/plain"));

app.Run();
