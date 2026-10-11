using Asp.Versioning;
using Halcyon.Adventure.Api.Data;
using Halcyon.Adventure.Api.Products;
using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);

// Register the AdventureWorks DbContext against the local SQL Server 2025 instance
// baked into VM type 11. The connection string lives in appsettings.json.
builder.Services.AddDbContext<AdventureWorksContext>(options =>
    options.UseSqlServer(
        builder.Configuration.GetConnectionString("AdventureWorks")
            ?? throw new InvalidOperationException(
                "ConnectionStrings:AdventureWorks is required.")));

// URL + header API versioning. The combined API version reader lets a caller
// either hit /api/v1/products OR send Api-Version: 1.0 on an unversioned URL.
// Default version is v1 so existing consumers that omit the version continue to work.
builder.Services.AddApiVersioning(options =>
{
    options.DefaultApiVersion = new ApiVersion(1, 0);
    options.AssumeDefaultVersionWhenUnspecified = true;
    options.ReportApiVersions = true;
    options.ApiVersionReader = ApiVersionReader.Combine(
        new UrlSegmentApiVersionReader(),
        new HeaderApiVersionReader("Api-Version"));
});

// .NET 10 ships OpenAPI 3.1 as the default document shape. Halcyon serves the
// contract from /openapi/v1.yaml so the Sales Portal + the DW ETL worker can
// generate clients from a committed path. Validation + problem-details plumbing
// is deliberately not wired yet; that is the Lesson 4 exercise.
builder.Services.AddOpenApi("v1");

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.MapOpenApi("/openapi/{documentName}.yaml");
    app.MapOpenApi("/openapi/{documentName}.json");
}

// Attach the versioned Products endpoints to a /api/v{apiVersion:apiVersion} group.
var versionSet = app.NewApiVersionSet()
    .HasApiVersion(new ApiVersion(1, 0))
    .ReportApiVersions()
    .Build();

var versionedGroup = app
    .MapGroup("/api/v{apiVersion:apiVersion}")
    .WithApiVersionSet(versionSet);

versionedGroup.MapProductsApi();

app.Run();
