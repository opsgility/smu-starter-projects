using System.Security.Claims;
using Microsoft.AspNetCore.Http.HttpResults;

namespace Halcyon.Adventure.Api.Products;

// Products CRUD. Scaffolded in Lesson 2 as a minimal-API endpoint group against
// the shape of AdventureWorks.Production.Product. Lesson 4 landed validation,
// IValidatableObject margin rule, and the custom HalcyonProblemDetailsService.
//
// Lesson 6 Exercise 2 adds a pre-staged ILogger business-id scope on the Create
// handler that attaches ProductId + MerchantId to every log line. Exercise 4
// surfaces a deliberately-broken scope key via the @debugger agent and lands
// the one-line fix through Edit mode.
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
        IProductRepository repo,
        ILogger<Program> logger,
        HttpContext http)
    {
        var created = repo.Create(request);
        var merchantId = http.User.FindFirst("merchant_id")?.Value ?? "anonymous";

        // Pre-staged business-id scope. Exercise 4 will unskip a test that proves
        // the "ProductId" key is populated — the deliberate bug (lowercase 'd' in
        // "Productid") only surfaces when the student removes the [Skip] attribute
        // and runs the test under the @debugger agent.
        using (logger.BeginScope(new Dictionary<string, object>
        {
            ["Productid"] = created.ProductId,
            ["MerchantId"] = merchantId,
        }))
        {
            logger.LogInformation(
                "Product {ProductId} created by merchant {MerchantId}",
                created.ProductId,
                merchantId);
        }

        return TypedResults.Created($"/products/{created.ProductId}", created);
    }

    private static Results<Ok<Product>, NotFound, ValidationProblem> Update(
        int id,
        UpdateProductRequest request,
        IProductRepository repo,
        ILogger<Program> logger,
        HttpContext http)
    {
        if (!repo.TryGet(id, out _))
        {
            return TypedResults.NotFound();
        }

        var merchantId = http.User.FindFirst("merchant_id")?.Value ?? "anonymous";

        using (logger.BeginScope(new Dictionary<string, object>
        {
            ["ProductId"] = id,
            ["MerchantId"] = merchantId,
        }))
        {
            var updated = repo.Update(id, request);
            logger.LogInformation(
                "Product {ProductId} updated by merchant {MerchantId}",
                id,
                merchantId);

            return TypedResults.Ok(updated);
        }
    }

    private static Results<NoContent, NotFound> Delete(
        int id,
        IProductRepository repo,
        ILogger<Program> logger,
        HttpContext http)
    {
        if (!repo.Delete(id))
        {
            return TypedResults.NotFound();
        }

        var merchantId = http.User.FindFirst("merchant_id")?.Value ?? "anonymous";

        using (logger.BeginScope(new Dictionary<string, object>
        {
            ["ProductId"] = id,
            ["MerchantId"] = merchantId,
        }))
        {
            logger.LogInformation(
                "Product {ProductId} deleted by merchant {MerchantId}",
                id,
                merchantId);
        }

        return TypedResults.NoContent();
    }
}
