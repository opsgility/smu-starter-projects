namespace Halcyon.Adventure.Api.Products.Comparison;

/// <summary>
/// Same shape as CreateProductRequest, but validated through FluentValidation
/// instead of .NET 10 built-in AddValidation. The comparison endpoint lets the
/// student feel the delta — rule objects + chained validators vs attributes +
/// IValidatableObject. The in-box path is the Halcyon default; FluentValidation
/// earns its place when a rule touches multiple services or spans an aggregate.
/// </summary>
public record FluentCreateProductRequest(
    string Name,
    string ProductNumber,
    decimal StandardCost,
    decimal ListPrice,
    DateOnly SellStartDate,
    DateOnly? SellEndDate);
