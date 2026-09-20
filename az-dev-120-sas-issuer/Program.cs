using Azure.Identity;
using Azure.Storage.Blobs;
using Azure.Storage.Sas;

var builder = WebApplication.CreateBuilder(args);

var accountName = builder.Configuration["Anchorline:StorageAccount"]
    ?? throw new InvalidOperationException("Anchorline:StorageAccount missing");
var containerName = builder.Configuration["Anchorline:Container"] ?? "customer-uploads";

builder.Services.AddSingleton(_ => new BlobServiceClient(
    new Uri($"https://{accountName}.blob.core.windows.net"),
    new DefaultAzureCredential()));

var app = builder.Build();
app.UseDefaultFiles();
app.UseStaticFiles();

app.MapGet("/health", () => Results.Ok(new { status = "ok" }));

app.MapPost("/api/upload/prepare", async (
    string name,
    BlobServiceClient serviceClient,
    ILogger<Program> log) =>
{
    if (string.IsNullOrWhiteSpace(name) || name.Contains("..") || name.Contains("/"))
    {
        return Results.BadRequest(new { error = "invalid name" });
    }

    var validFor = TimeSpan.FromMinutes(15);
    var expiresOn = DateTimeOffset.UtcNow.Add(validFor);

    var udk = await serviceClient.GetUserDelegationKeyAsync(
        DateTimeOffset.UtcNow.AddMinutes(-5), expiresOn);

    var sasBuilder = new BlobSasBuilder
    {
        BlobContainerName = containerName,
        BlobName = name,
        Resource = "b",
        ExpiresOn = expiresOn,
        Protocol = SasProtocol.Https
    };
    sasBuilder.SetPermissions(BlobSasPermissions.Write | BlobSasPermissions.Create);

    var sasToken = sasBuilder.ToSasQueryParameters(udk.Value, accountName).ToString();
    var uploadUrl = $"https://{accountName}.blob.core.windows.net/{containerName}/{Uri.EscapeDataString(name)}?{sasToken}";

    log.LogInformation("Issued user-delegation SAS for {Name}, expires {ExpiresOn}", name, expiresOn);
    return Results.Ok(new { name, uploadUrl, expiresOn });
});

app.Run();
