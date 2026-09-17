using Azure.Core;
using Azure.Identity;
using Microsoft.Data.SqlClient;

var builder = WebApplication.CreateBuilder(args);

var sqlServer = builder.Configuration["Anchorline:SqlServer"]
    ?? throw new InvalidOperationException("Anchorline:SqlServer missing");
var sqlDatabase = builder.Configuration["Anchorline:SqlDatabase"] ?? "AnchorlineSaaS";
var miClientId  = builder.Configuration["Anchorline:MiClientId"];

builder.Services.AddSingleton<TokenCredential>(_ =>
    string.IsNullOrEmpty(miClientId)
        ? new DefaultAzureCredential()
        : new DefaultAzureCredentialOptions { ManagedIdentityClientId = miClientId } is var opts
          ? new DefaultAzureCredential(opts)
          : new DefaultAzureCredential());

var app = builder.Build();

// Middleware: read tenant from X-Tenant-Id header (in prod this would come from the auth claim)
// and set SESSION_CONTEXT('TenantId') at connection open.
app.Use(async (context, next) =>
{
    var tenantHeader = context.Request.Headers["X-Tenant-Id"].ToString();
    if (int.TryParse(tenantHeader, out var tenantId))
        context.Items["TenantId"] = tenantId;
    await next();
});

async Task<SqlConnection> OpenTenantConnAsync(HttpContext ctx, TokenCredential cred)
{
    var conn = new SqlConnection($"Server=tcp:{sqlServer},1433;Database={sqlDatabase};Encrypt=True;");
    conn.AccessTokenCallback = async (info, ct) =>
    {
        var t = await cred.GetTokenAsync(new TokenRequestContext(new[] { "https://database.windows.net/.default" }), ct);
        return new SqlAuthenticationToken(t.Token, t.ExpiresOn);
    };
    await conn.OpenAsync();
    if (ctx.Items.TryGetValue("TenantId", out var val) && val is int tid)
    {
        await using var setCtx = conn.CreateCommand();
        setCtx.CommandText = "EXEC sp_set_session_context @key = N'TenantId', @value = @tid";
        setCtx.Parameters.Add(new SqlParameter("@tid", tid));
        await setCtx.ExecuteNonQueryAsync();
    }
    return conn;
}

app.MapGet("/", () => Results.Ok(new { app = "anchorline-saas", ok = true }));

app.MapGet("/whoami", async (HttpContext ctx, TokenCredential cred) =>
{
    await using var conn = await OpenTenantConnAsync(ctx, cred);
    await using var cmd = conn.CreateCommand();
    cmd.CommandText = @"SELECT USER_NAME() AS DbUser,
                              CONVERT(NVARCHAR(20), SESSION_CONTEXT(N'TenantId')) AS SessionTenantId";
    await using var r = await cmd.ExecuteReaderAsync();
    if (!await r.ReadAsync()) return Results.NotFound();
    return Results.Ok(new { dbUser = r["DbUser"], tenantIdInSession = r["SessionTenantId"] });
});

// Insert a customer for the current tenant.
app.MapPost("/customers", async (HttpContext ctx, CustomerReq body, TokenCredential cred) =>
{
    if (!ctx.Items.TryGetValue("TenantId", out var v) || v is not int tid)
        return Results.BadRequest("Missing X-Tenant-Id header");

    await using var conn = await OpenTenantConnAsync(ctx, cred);
    await using var cmd = conn.CreateCommand();
    cmd.CommandText = "INSERT dbo.Customer(TenantId, Name, Email) OUTPUT INSERTED.CustomerId VALUES(@tid, @n, @e)";
    cmd.Parameters.Add(new SqlParameter("@tid", tid));
    cmd.Parameters.Add(new SqlParameter("@n", body.Name));
    cmd.Parameters.Add(new SqlParameter("@e", body.Email));
    var newId = (int)(await cmd.ExecuteScalarAsync())!;
    return Results.Ok(new { customerId = newId, tenantId = tid });
});

// List customers — RLS scopes to the current SESSION_CONTEXT tenant.
app.MapGet("/customers", async (HttpContext ctx, TokenCredential cred) =>
{
    await using var conn = await OpenTenantConnAsync(ctx, cred);
    await using var cmd = conn.CreateCommand();
    cmd.CommandText = "SELECT CustomerId, TenantId, Name, Email FROM dbo.Customer ORDER BY CustomerId";
    await using var r = await cmd.ExecuteReaderAsync();
    var list = new List<object>();
    while (await r.ReadAsync())
        list.Add(new { customerId = r["CustomerId"], tenantId = r["TenantId"], name = r["Name"], email = r["Email"] });
    return Results.Ok(list);
});

// The "malicious bulk" endpoint — attempts SELECT with no explicit WHERE.
// RLS should still return only the tenant's rows.
app.MapGet("/leak-attempt", async (HttpContext ctx, TokenCredential cred) =>
{
    await using var conn = await OpenTenantConnAsync(ctx, cred);
    await using var cmd = conn.CreateCommand();
    cmd.CommandText = "SELECT COUNT(*) AS n FROM dbo.Customer";  // no WHERE
    var n = (int)(await cmd.ExecuteScalarAsync())!;
    return Results.Ok(new { visibleCustomers = n, note = "RLS filters even queries with no explicit WHERE" });
});

app.Run();

public record CustomerReq(string Name, string Email);
