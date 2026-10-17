using System.ComponentModel.DataAnnotations;

namespace Halcyon.Adventure.Api.Products;

/// <summary>
/// Request shape for POST /v{1,2}/products. Validated by .NET 10 built-in
/// validation (AddValidation) using DataAnnotations plus one IValidatableObject
/// cross-field rule enforcing Halcyon's price-vs-cost margin policy.
/// </summary>
public record CreateProductRequest(
    [Required]
    [StringLength(50, MinimumLength = 3)]
    string Name,

    [Required]
    [RegularExpression(@"^[A-Z]{2,4}-\d{3,5}$",
        ErrorMessage = "ProductNumber must look like 'BK-1234' or 'ABCD-12345'.")]
    string ProductNumber,

    [Range(typeof(decimal), "0.01", "100000.00",
        ErrorMessage = "StandardCost must be between $0.01 and $100,000.")]
    decimal StandardCost,

    [Range(typeof(decimal), "0.01", "100000.00",
        ErrorMessage = "ListPrice must be between $0.01 and $100,000.")]
    decimal ListPrice,

    DateOnly SellStartDate,

    DateOnly? SellEndDate
) : IValidatableObject
{
    /// <summary>
    /// Halcyon margin policy. ListPrice must be at least 15 percent above
    /// StandardCost. Director Christopher Jones' pricing memo (2026-Q3) sets
    /// this floor; the margin rule lives on the request record so the API
    /// enforces it uniformly across every create path.
    /// </summary>
    public const decimal MinimumMarginPercent = 0.15m;

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
        if (margin < MinimumMarginPercent)
        {
            yield return new ValidationResult(
                $"ListPrice must be at least {MinimumMarginPercent:P0} above StandardCost " +
                $"(Halcyon margin policy). Observed margin: {margin:P2}.",
                [nameof(ListPrice), nameof(StandardCost)]);
        }
    }
}
