using Asp.Versioning;
using Halcyon.Adventure.Api.Data;
using Microsoft.AspNetCore.Http.HttpResults;
using Microsoft.EntityFrameworkCore;

namespace Halcyon.Adventure.Api.Products;

/// <summary>
/// Minimal-API module for <c>Production.Product</c>. Generated in Lesson 2
/// via the <c>/scaffold-crud</c> prompt file. All handlers return
/// <see cref="TypedResults"/> so the OpenAPI document picks up the response
/// shape without extra <c>Produces&lt;T&gt;</c> annotations.
/// </summary>
public static class ProductsApi
{
    public static RouteGroupBuilder MapProductsApi(this RouteGroupBuilder parent)
    {
        var group = parent
            .MapGroup("/products")
            .HasApiVersion(new ApiVersion(1, 0))
            .WithTags("Products");

        group.MapGet("/", GetAllAsync)
            .WithName("ListProducts")
            .WithSummary("List products")
            .WithDescription("Returns every product in Production.Product.");

        group.MapGet("/{productId:int}", GetByIdAsync)
            .WithName("GetProduct")
            .WithSummary("Get a product by id")
            .WithDescription("Returns a single product or 404 if the id does not exist.");

        group.MapPost("/", CreateAsync)
            .WithName("CreateProduct")
            .WithSummary("Create a product")
            .WithDescription("Inserts a new Production.Product row and returns it.");

        group.MapPut("/{productId:int}", UpdateAsync)
            .WithName("UpdateProduct")
            .WithSummary("Update a product")
            .WithDescription("Updates an existing Production.Product row.");

        group.MapDelete("/{productId:int}", DeleteAsync)
            .WithName("DeleteProduct")
            .WithSummary("Delete a product")
            .WithDescription("Deletes a Production.Product row by id.");

        return parent;
    }

    private static async Task<Ok<IEnumerable<ProductDto>>> GetAllAsync(
        AdventureWorksContext db,
        CancellationToken ct)
    {
        var products = await db.Products
            .AsNoTracking()
            .OrderBy(p => p.ProductID)
            .Select(p => ToDto(p))
            .ToListAsync(ct);

        return TypedResults.Ok<IEnumerable<ProductDto>>(products);
    }

    private static async Task<Results<Ok<ProductDto>, NotFound>> GetByIdAsync(
        int productId,
        AdventureWorksContext db,
        CancellationToken ct)
    {
        var product = await db.Products.AsNoTracking()
            .FirstOrDefaultAsync(p => p.ProductID == productId, ct);

        return product is null
            ? TypedResults.NotFound()
            : TypedResults.Ok(ToDto(product));
    }

    private static async Task<Created<ProductDto>> CreateAsync(
        CreateProductRequest request,
        AdventureWorksContext db,
        CancellationToken ct)
    {
        var entity = new Product
        {
            Name = request.Name,
            ProductNumber = request.ProductNumber,
            Color = request.Color,
            StandardCost = request.StandardCost,
            ListPrice = request.ListPrice,
            Size = request.Size,
            SellStartDate = request.SellStartDate,
            MakeFlag = true,
            FinishedGoodsFlag = true,
            SafetyStockLevel = 500,
            ReorderPoint = 375,
            ModifiedDate = DateTime.UtcNow,
            rowguid = Guid.NewGuid(),
        };

        db.Products.Add(entity);
        await db.SaveChangesAsync(ct);

        return TypedResults.Created($"/api/v1/products/{entity.ProductID}", ToDto(entity));
    }

    private static async Task<Results<Ok<ProductDto>, NotFound>> UpdateAsync(
        int productId,
        UpdateProductRequest request,
        AdventureWorksContext db,
        CancellationToken ct)
    {
        var entity = await db.Products.FirstOrDefaultAsync(p => p.ProductID == productId, ct);
        if (entity is null)
        {
            return TypedResults.NotFound();
        }

        entity.Name = request.Name;
        entity.ProductNumber = request.ProductNumber;
        entity.Color = request.Color;
        entity.StandardCost = request.StandardCost;
        entity.ListPrice = request.ListPrice;
        entity.Size = request.Size;
        entity.SellStartDate = request.SellStartDate;
        entity.SellEndDate = request.SellEndDate;
        entity.DiscontinuedDate = request.DiscontinuedDate;
        entity.ModifiedDate = DateTime.UtcNow;

        await db.SaveChangesAsync(ct);
        return TypedResults.Ok(ToDto(entity));
    }

    private static async Task<Results<NoContent, NotFound>> DeleteAsync(
        int productId,
        AdventureWorksContext db,
        CancellationToken ct)
    {
        var entity = await db.Products.FirstOrDefaultAsync(p => p.ProductID == productId, ct);
        if (entity is null)
        {
            return TypedResults.NotFound();
        }

        db.Products.Remove(entity);
        await db.SaveChangesAsync(ct);
        return TypedResults.NoContent();
    }

    private static ProductDto ToDto(Product p) => new(
        p.ProductID,
        p.Name,
        p.ProductNumber,
        p.Color,
        p.StandardCost,
        p.ListPrice,
        p.Size,
        p.SellStartDate,
        p.SellEndDate,
        p.DiscontinuedDate);
}
