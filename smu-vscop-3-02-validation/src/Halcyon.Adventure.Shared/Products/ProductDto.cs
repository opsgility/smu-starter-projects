namespace Halcyon.Adventure.Shared.Products;

// Wire-level projection of a Product that the API returns on reads.
public record ProductDto(
    int Id,
    string Sku,
    string Name,
    decimal Price,
    decimal Cost);
