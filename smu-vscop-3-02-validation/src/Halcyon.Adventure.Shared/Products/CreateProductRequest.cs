namespace Halcyon.Adventure.Shared.Products;

// Payload for POST /products. Validation attributes land in Lesson 4 Exercise 2.
public record CreateProductRequest(
    string? Sku,
    string? Name,
    decimal Price,
    decimal Cost);
