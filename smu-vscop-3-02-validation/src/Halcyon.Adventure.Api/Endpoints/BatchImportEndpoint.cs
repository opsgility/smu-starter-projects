using Halcyon.Adventure.Api.Products;
using Halcyon.Adventure.Shared.Products;
using Microsoft.AspNetCore.Http.HttpResults;

namespace Halcyon.Adventure.Api.Endpoints;

// POST /products/batch-import — the one endpoint Lesson 4 Exercise 5 switches to
// FluentValidation. In the starter it uses built-in validation like every other
// endpoint; the Exercise 5 Edit-mode prompt adds .AddEndpointFilter<FluentValidationFilter<T>>()
// and .DisableValidation() on this map call.
public static class BatchImportEndpoint
{
    public static IEndpointRouteBuilder MapBatchImportEndpoint(this IEndpointRouteBuilder app)
    {
        app.MapPost("/products/batch-import", Handle)
            .WithName("BatchImportProducts")
            .WithSummary("Batch-import products")
            .WithTags("Products");

        return app;
    }

    private static Ok<BatchImportResult> Handle(BatchImportRequest request, IProductRepository repo)
    {
        var imported = 0;
        foreach (var item in request.Items)
        {
            repo.Add(new Product
            {
                Sku = item.Sku ?? string.Empty,
                Name = item.Name ?? string.Empty,
                Price = item.Price,
                Cost = item.Cost,
            });
            imported++;
        }

        return TypedResults.Ok(new BatchImportResult(imported));
    }

    public record BatchImportResult(int ImportedCount);
}
