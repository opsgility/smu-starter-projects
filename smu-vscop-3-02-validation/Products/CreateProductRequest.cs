namespace Halcyon.Adventure.Api.Products;

/// <summary>
/// Payload for <c>POST /api/v1/products</c>.
/// Validation attributes are deliberately absent — Lesson 4 adds them.
/// </summary>
public record CreateProductRequest(
    string Name,
    string ProductNumber,
    string? Color,
    decimal StandardCost,
    decimal ListPrice,
    string? Size,
    DateTime SellStartDate);
