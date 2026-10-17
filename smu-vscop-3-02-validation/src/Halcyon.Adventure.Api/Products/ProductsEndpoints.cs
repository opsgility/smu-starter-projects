using Halcyon.Adventure.Shared.Products;
using Microsoft.AspNetCore.Http.HttpResults;

namespace Halcyon.Adventure.Api.Products;

// Minimal-API module for the Products aggregate. All handlers return TypedResults
// so the OpenAPI 3.1 document describes the response shape without extra attributes.
//
// Lesson 4 keeps this file read-only — the request-record validation attributes land
// on the shared records (Exercise 2), and the custom problem-details delegate lands
// in Program.cs (Exercise 4). The handlers below do not change.
public static class ProductsEndpoints
{
    public static IEndpointRouteBuilder MapProductsEndpoints(this IEndpointRouteBuilder app)
    {
        var group = app.MapGroup("/products").WithTags("Products");

        group.MapGet("/", GetAll)
            .WithName("ListProducts")
            .WithSummary("List products");

        group.MapGet("/{id:int}", GetById)
            .WithName("GetProduct")
            .WithSummary("Get a product by id");

        group.MapPost("/", Create)
            .WithName("CreateProduct")
            .WithSummary("Create a product");

        group.MapPut("/{id:int}", Update)
            .WithName("UpdateProduct")
            .WithSummary("Update a product");

        group.MapDelete("/{id:int}", Delete)
            .WithName("DeleteProduct")
            .WithSummary("Delete a product");

        return app;
    }

    private static Ok<IReadOnlyList<ProductDto>> GetAll(IProductRepository repo) =>
        TypedResults.Ok<IReadOnlyList<ProductDto>>(
            repo.GetAll().Select(ToDto).ToList());

    private static Results<Ok<ProductDto>, NotFound> GetById(int id, IProductRepository repo)
    {
        var product = repo.Get(id);
        return product is null
            ? TypedResults.NotFound()
            : TypedResults.Ok(ToDto(product));
    }

    private static Created<ProductDto> Create(CreateProductRequest request, IProductRepository repo)
    {
        var product = repo.Add(new Product
        {
            Sku = request.Sku ?? string.Empty,
            Name = request.Name ?? string.Empty,
            Price = request.Price,
            Cost = request.Cost,
        });

        return TypedResults.Created($"/products/{product.Id}", ToDto(product));
    }

    private static Results<Ok<ProductDto>, NotFound> Update(
        int id,
        UpdateProductRequest request,
        IProductRepository repo)
    {
        var updated = repo.Update(id, p =>
        {
            p.Name = request.Name ?? p.Name;
            p.Price = request.Price;
            p.Cost = request.Cost;
        });

        return updated
            ? TypedResults.Ok(ToDto(repo.Get(id)!))
            : TypedResults.NotFound();
    }

    private static Results<NoContent, NotFound> Delete(int id, IProductRepository repo) =>
        repo.Delete(id) ? TypedResults.NoContent() : TypedResults.NotFound();

    private static ProductDto ToDto(Product p) => new(p.Id, p.Sku, p.Name, p.Price, p.Cost);
}
