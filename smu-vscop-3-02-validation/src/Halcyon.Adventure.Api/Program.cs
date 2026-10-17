using Halcyon.Adventure.Api.Endpoints;
using Halcyon.Adventure.Api.Middleware;
using Halcyon.Adventure.Api.Products;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddSingleton<IProductRepository, InMemoryProductRepository>();

// .NET 10 built-in OpenAPI 3.1 document generation. Served from /openapi/v1.yaml.
builder.Services.AddOpenApi("v1");

// Problem-details is registered with no customization today. Lesson 4 Exercise 4
// replaces this bare call with the AddProblemDetails(options => ...) overload that
// forwards the correlation id (set by CorrelationIdMiddleware) onto every response's
// extensions.halcyonTraceId field.
builder.Services.AddProblemDetails();

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.MapOpenApi("/openapi/{documentName}.yaml");
    app.MapOpenApi("/openapi/{documentName}.json");
}

// CorrelationIdMiddleware runs FIRST so every downstream handler + log line + response
// body carries the id. Exercise 4 relies on this ordering — the custom
// problem-details delegate reads HttpContext.Items["HalcyonCorrelationId"] which the
// middleware populates here, before any endpoint runs.
app.UseMiddleware<CorrelationIdMiddleware>();

app.MapProductsEndpoints();
app.MapBatchImportEndpoint();

app.Run();

// WebApplicationFactory<Program> in the tests project requires Program to be
// accessible. Top-level statements implicitly generate an internal Program class;
// expose it with a partial class declaration.
public partial class Program;
