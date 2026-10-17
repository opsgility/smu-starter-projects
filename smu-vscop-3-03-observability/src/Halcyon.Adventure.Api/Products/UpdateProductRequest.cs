using System.ComponentModel.DataAnnotations;

namespace Halcyon.Adventure.Api.Products;

/// <summary>
/// Request shape for PUT /v{1,2}/products/{id}. Same validation surface as
/// CreateProductRequest, with the margin rule reused through composition.
/// </summary>
public record UpdateProductRequest(
    [Required]
    [StringLength(50, MinimumLength = 3)]
    string Name,

    [Range(typeof(decimal), "0.01", "100000.00")]
    decimal StandardCost,

    [Range(typeof(decimal), "0.01", "100000.00")]
    decimal ListPrice,

    DateOnly SellStartDate,

    DateOnly? SellEndDate
) : IValidatableObject
{
    public IEnumerable<ValidationResult> Validate(ValidationContext validationContext)
    {
        if (SellEndDate is DateOnly end && end <= SellStartDate)
        {
            yield return new ValidationResult(
                "SellEndDate must fall after SellStartDate.",
                [nameof(SellEndDate)]);
        }

        if (StandardCost <= 0)
        {
            yield break;
        }

        var margin = (ListPrice - StandardCost) / StandardCost;
        if (margin < CreateProductRequest.MinimumMarginPercent)
        {
            yield return new ValidationResult(
                $"ListPrice must be at least {CreateProductRequest.MinimumMarginPercent:P0} " +
                $"above StandardCost (Halcyon margin policy). Observed margin: {margin:P2}.",
                [nameof(ListPrice), nameof(StandardCost)]);
        }
    }
}
