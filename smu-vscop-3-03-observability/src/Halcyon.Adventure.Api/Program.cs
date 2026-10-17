using Asp.Versioning;
using FluentValidation;
using Halcyon.Adventure.Api.Infrastructure;
using Halcyon.Adventure.Api.Middleware;
using Halcyon.Adventure.Api.Products;
using Halcyon.Adventure.Api.Products.Comparison;
using Microsoft.AspNetCore.Http;
using Serilog;

var builder = WebApplication.CreateBuilder(args);

// Serilog is the Halcyon house logger. The console sink is enough for the lab
// VM — Course 7 wires the OpenTelemetry sink to Application Insights.
builder.Host.UseSerilog((context, services, configuration) => configuration
    .ReadFrom.Configuration(context.Configuration)
    .ReadFrom.Services(services)
    .Enrich.FromLogContext()
    .WriteTo.Console(outputTemplate:
        "[{Timestamp:HH:mm:ss} {Level:u3}] {Message:lj} {Properties:j}{NewLine}{Exception}"));

// OpenAPI 3.1 (default in .NET 10).
builder.Services.AddOpenApi();

// Problem Details (RFC 9457). The custom HalcyonProblemDetailsService adds
// a correlation trace id and a Halcyon-tagged type URI so support engineers
// can find the exact failure in the application logs within seconds.
builder.Services.AddHttpContextAccessor();
builder.Services.AddProblemDetails();
builder.Services.AddSingleton<IProblemDetailsService, HalcyonProblemDetailsService>();

// In-memory product store seeded with four canonical Adventure Works bikes.
// Course 4 (EF Core) swaps this for a real DbContext behind the same interface.
builder.Services.AddSingleton<IProductRepository, ProductRepository>();

// Built-in validation for minimal APIs (new in .NET 10). AddValidation triggers
// the source generator for every validatable type declared in this assembly.
builder.Services.AddValidation();

// FluentValidation registered only to drive the comparison endpoint in
// Products.Comparison. The rest of the API uses .NET 10 built-in validation.
builder.Services.AddValidatorsFromAssemblyContaining<FluentUpdateProductRequestValidator>();

// URL + header versioning via Asp.Versioning.Http. v1 is on /v1/products,
// v2 can be reached on /v2/products or by header X-Api-Version: 2.0.
builder.Services
    .AddApiVersioning(options =>
    {
        options.DefaultApiVersion = new ApiVersion(1, 0);
        options.AssumeDefaultVersionWhenUnspecified = true;
        options.ReportApiVersions = true;
        options.ApiVersionReader = ApiVersionReader.Combine(
            new UrlSegmentApiVersionReader(),
            new HeaderApiVersionReader("X-Api-Version"));
    });

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();
}

app.UseExceptionHandler();
app.UseStatusCodePages();
app.UseHttpsRedirection();

// Correlation id runs outermost so every downstream handler + log line + response
// body carries the id. Lesson 6 Exercise 2 reviews the pre-staged middleware
// with Copilot Agent mode. Lesson 6 Exercise 3 chains .RequireRateLimiting() on
// the versioned endpoint groups below; UseRateLimiter() must follow UseRouting
// — the student adds the two UseRouting/UseRateLimiter lines there.
app.UseCorrelationId();

var versions = app.NewApiVersionSet()
    .HasApiVersion(new ApiVersion(1, 0))
    .HasApiVersion(new ApiVersion(2, 0))
    .ReportApiVersions()
    .Build();

var v1 = app
    .MapGroup("/v{version:apiVersion}/products")
    .WithApiVersionSet(versions)
    .MapToApiVersion(1, 0)
    .WithTags("Products v1");

ProductsEndpoints.Map(v1);

var v2 = app
    .MapGroup("/v{version:apiVersion}/products")
    .WithApiVersionSet(versions)
    .MapToApiVersion(2, 0)
    .WithTags("Products v2");

ProductsEndpoints.Map(v2);

// Comparison endpoint. Same /create-with-fluent-validation shape as the primary
// POST /products but validated through FluentValidation instead of built-in
// data annotations. Lesson 3 teaches when to pick which.
var comparison = app
    .MapGroup("/v{version:apiVersion}/products")
    .WithApiVersionSet(versions)
    .MapToApiVersion(1, 0)
    .WithTags("Products v1 (FluentValidation comparison)");

FluentValidationComparisonEndpoint.Map(comparison);

app.Run();

/// <summary>
/// Marker type used by WebApplicationFactory in the test project.
/// </summary>
public partial class Program;
