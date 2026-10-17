namespace Halcyon.Adventure.Shared.Products;

// Payload for POST /products/batch-import. FluentValidation lands in Lesson 4 Exercise 5.
public record BatchImportRequest(IReadOnlyList<BatchImportItem> Items);

public record BatchImportItem(
    string? Sku,
    string? Name,
    decimal Price,
    decimal Cost);
