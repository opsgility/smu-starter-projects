namespace Halcyon.Adventure.Api.Products;

/// <summary>
/// Wire-level projection of <c>Production.Product</c> that the Products API
/// returns on reads. Separate from the EF entity so the storage shape can
/// evolve without breaking consumers.
/// </summary>
public record ProductDto(
    int ProductId,
    string Name,
    string ProductNumber,
    string? Color,
    decimal StandardCost,
    decimal ListPrice,
    string? Size,
    DateTime SellStartDate,
    DateTime? SellEndDate,
    DateTime? DiscontinuedDate);
