namespace Halcyon.Adventure.Api.Products;

/// <summary>
/// Snapshot of an AdventureWorks product as exposed by the Halcyon Adventure API.
/// Shape mirrors Production.Product on the shared AdventureWorks2025 database.
/// </summary>
public record Product(
    int ProductId,
    string Name,
    string ProductNumber,
    decimal StandardCost,
    decimal ListPrice,
    DateOnly SellStartDate,
    DateOnly? SellEndDate,
    DateTime ModifiedDate);
