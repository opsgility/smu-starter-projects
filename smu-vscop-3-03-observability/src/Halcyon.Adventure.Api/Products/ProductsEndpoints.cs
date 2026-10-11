using Microsoft.AspNetCore.Http.HttpResults;
using Microsoft.AspNetCore.Routing;

namespace Halcyon.Adventure.Api.Products;

/// <summary>
/// Products CRUD. Scaffolded in Lesson 2 against AdventureWorks.Production.Product
/// with the /scaffold-crud prompt file. The in-memory store keeps the lab
/// self-contained; Section 2 wires a real DbContext in a follow-on course.
/// </summary>
public static class ProductsEndpoints
{
    public static RouteGroupBuilder Map(RouteGroupBuilder group)
    {
        group.MapGet("/", GetAll)
            .WithName("ListProducts")
            .WithSummary("List every product currently on the Halcyon Adventure catalog.");

        group.MapGet("/{id:int}", GetById)
            .WithName("GetProduct");

        group.MapPost("/", Create)
            .WithName("CreateProduct");

        group.MapPut("/{id:int}", Update)
            .WithName("UpdateProduct");

        group.MapDelete("/{id:int}", Delete)
            .WithName("DeleteProduct");

        return group;
    }

    private static Ok<IReadOnlyCollection<Product>> GetAll(IProductRepository repo) =>
        TypedResults.Ok(repo.GetAll());

    private static Results<Ok<Product>, NotFound> GetById(int id, IProductRepository repo) =>
        repo.TryGet(id, out var product)
            ? TypedResults.Ok(product!)
            : TypedResults.NotFound();

    private static Results<Created<Product>, ValidationProblem> Create(
        CreateProductRequest request,
        IProductRepository repo)
    {
        var created = repo.Create(request);
        return TypedResults.Created($"/products/{created.ProductId}", created);
    }

    private static Results<Ok<Product>, NotFound, ValidationProblem> Update(
        int id,
        UpdateProductRequest request,
        IProductRepository repo)
    {
        if (!repo.TryGet(id, out _))
        {
            return TypedResults.NotFound();
        }

        var updated = repo.Update(id, request);
        return TypedResults.Ok(updated);
    }

    private static Results<NoContent, NotFound> Delete(int id, IProductRepository repo) =>
        repo.Delete(id) ? TypedResults.NoContent() : TypedResults.NotFound();
}
