using Azure.Identity;
using Azure.Storage.Blobs;
using Azure.Storage.Sas;

var builder = WebApplication.CreateBuilder(args);

var accountName = builder.Configuration["Anchorline:StorageAccount"]
    ?? throw new InvalidOperationException("Anchorline:StorageAccount missing");

builder.Services.AddSingleton(_ => new BlobServiceClient(
    new Uri($"https://{accountName}.blob.core.windows.net"),
    new DefaultAzureCredential()));

var app = builder.Build();
app.UseDefaultFiles();
app.UseStaticFiles();

app.MapGet("/health", () => Results.Ok(new { status = "ok" }));

app.MapPost("/api/upload/prepare", async (
    string tenantId,
    string name,
    BlobServiceClient service,
    ILogger<Program> log) =>
{
    if (!IsValidTenantId(tenantId) || !IsValidBlobName(name))
        return Results.BadRequest(new { error = "invalid tenantId or name" });

    var container = service.GetBlobContainerClient($"tenant-{tenantId}");
    await container.CreateIfNotExistsAsync();

    var validFor = TimeSpan.FromMinutes(15);
    var expiresOn = DateTimeOffset.UtcNow.Add(validFor);

    var udk = await service.GetUserDelegationKeyAsync(
        DateTimeOffset.UtcNow.AddMinutes(-5), expiresOn);

    var sasBuilder = new BlobSasBuilder
    {
        BlobContainerName = container.Name,
        BlobName = name,
        Resource = "b",
        ExpiresOn = expiresOn,
        Protocol = SasProtocol.Https
    };
    sasBuilder.SetPermissions(BlobSasPermissions.Write | BlobSasPermissions.Create);

    var sasToken = sasBuilder.ToSasQueryParameters(udk.Value, accountName).ToString();
    var uploadUrl = $"https://{accountName}.blob.core.windows.net/{container.Name}/{Uri.EscapeDataString(name)}?{sasToken}";

    log.LogInformation("Prepared SAS for tenant {TenantId} name {Name}", tenantId, name);
    return Results.Ok(new { tenantId, name, uploadUrl, expiresOn });
});

app.MapPost("/api/docs", async (
    DocumentRegistration reg,
    BlobServiceClient service,
    ILogger<Program> log) =>
{
    if (!IsValidTenantId(reg.tenantId) || !IsValidBlobName(reg.name))
        return Results.BadRequest(new { error = "invalid tenantId or name" });

    var container = service.GetBlobContainerClient($"tenant-{reg.tenantId}");
    var blob = container.GetBlobClient(reg.name);
    var exists = await blob.ExistsAsync();
    if (!exists.Value) return Results.NotFound(new { error = "blob not found" });

    var metadata = new Dictionary<string, string>
    {
        ["author"] = reg.author ?? "",
        ["department"] = reg.department ?? "",
        ["uploadedAt"] = DateTimeOffset.UtcNow.ToString("o")
    };
    await blob.SetMetadataAsync(metadata);

    var tags = new Dictionary<string, string>
    {
        ["tenantId"] = reg.tenantId,
        ["documentType"] = reg.documentType ?? "unknown",
        ["year"] = reg.year ?? DateTime.UtcNow.Year.ToString()
    };
    await blob.SetTagsAsync(tags);

    log.LogInformation("Registered doc {Name} for tenant {TenantId}", reg.name, reg.tenantId);
    return Results.Ok(new { reg.tenantId, reg.name, metadata, tags });
});

app.MapGet("/api/docs", async (
    string tenantId,
    string? documentType,
    string? year,
    BlobServiceClient service) =>
{
    if (!IsValidTenantId(tenantId))
        return Results.BadRequest(new { error = "invalid tenantId" });

    var filters = new List<string> { $"\"tenantId\" = '{tenantId}'" };
    if (!string.IsNullOrEmpty(documentType)) filters.Add($"\"documentType\" = '{documentType}'");
    if (!string.IsNullOrEmpty(year)) filters.Add($"\"year\" = '{year}'");
    var expr = string.Join(" AND ", filters);

    var results = new List<object>();
    await foreach (var match in service.FindBlobsByTagsAsync(expr))
    {
        results.Add(new { container = match.BlobContainerName, name = match.BlobName });
        if (results.Count >= 100) break;
    }
    return Results.Ok(new { expr, count = results.Count, results });
});

app.Run();

static bool IsValidTenantId(string tenantId) =>
    !string.IsNullOrWhiteSpace(tenantId) && tenantId.All(c => char.IsLetterOrDigit(c) || c == '-') && tenantId.Length <= 40;
static bool IsValidBlobName(string name) =>
    !string.IsNullOrWhiteSpace(name) && !name.Contains("..") && name.Length <= 512;

public record DocumentRegistration(string tenantId, string name, string? author, string? department, string? documentType, string? year);
