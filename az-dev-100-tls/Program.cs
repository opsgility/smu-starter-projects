var builder = WebApplication.CreateBuilder(args);

var app = builder.Build();

// EXERCISE 3 will add UseHsts() and UseHttpsRedirection() here.

app.MapGet("/health", () => Results.Ok(new { status = "ok" }));

app.MapGet("/version", (IConfiguration config) => Results.Ok(new
{
    build = config["AZ_DEV_100_BUILD_TAG"] ?? "unknown"
}));

app.MapGet("/tls", (HttpContext ctx) => Results.Ok(new
{
    scheme = ctx.Request.Scheme,
    isHttps = ctx.Request.IsHttps,
    xForwardedProto = ctx.Request.Headers["X-Forwarded-Proto"].ToString(),
    xForwardedTlsVersion = ctx.Request.Headers["X-Forwarded-TlsVersion"].ToString()
}));

app.MapGet("/headers", (HttpContext ctx) =>
{
    var headers = ctx.Response.Headers
        .ToDictionary(h => h.Key, h => h.Value.ToString());
    return Results.Ok(new { responseHeadersServerWillSend = headers });
});

app.Run();
