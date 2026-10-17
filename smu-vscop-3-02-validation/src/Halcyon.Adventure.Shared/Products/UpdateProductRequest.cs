namespace Halcyon.Adventure.Shared.Products;

// Payload for PUT /products/{id}. Validation attributes land in Lesson 4 Exercise 2.
public record UpdateProductRequest(
    string? Name,
    decimal Price,
    decimal Cost);
