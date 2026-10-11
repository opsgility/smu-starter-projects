namespace Halcyon.Adventure.Api.Products;

/// <summary>
/// Payload for <c>PUT /api/v1/products/{productId}</c>.
/// Validation attributes are deliberately absent — Lesson 4 adds them.
/// </summary>
public record UpdateProductRequest(
    string Name,
    string ProductNumber,
    string? Color,
    decimal StandardCost,
    decimal ListPrice,
    string? Size,
    DateTime SellStartDate,
    DateTime? SellEndDate,
    DateTime? DiscontinuedDate);
