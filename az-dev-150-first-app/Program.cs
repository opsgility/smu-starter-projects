using System.Net.NetworkInformation;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/", () => Results.Ok(new
{
    app = "anchorline-first-app",
    version = Environment.GetEnvironmentVariable("APP_VERSION") ?? "v1",
    hostname = Environment.MachineName,
    utc = DateTimeOffset.UtcNow
}));

app.MapGet("/health", () => Results.Ok(new { status = "ok" }));

app.MapGet("/whoami", () =>
{
    var props = IPGlobalProperties.GetIPGlobalProperties();
    return Results.Ok(new
    {
        hostname = Environment.MachineName,
        domain = props.DomainName,
        env = new
        {
            containerAppName = Environment.GetEnvironmentVariable("CONTAINER_APP_NAME"),
            containerAppReplicaName = Environment.GetEnvironmentVariable("CONTAINER_APP_REPLICA_NAME"),
            containerAppRevision = Environment.GetEnvironmentVariable("CONTAINER_APP_REVISION"),
        }
    });
});

app.Run("http://0.0.0.0:8080");
