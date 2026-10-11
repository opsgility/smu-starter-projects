using FluentValidation;

namespace Halcyon.Adventure.Api.Products.Comparison;

/// <summary>
/// FluentValidation rules for the comparison endpoint. The margin rule mirrors
/// the one on CreateProductRequest.Validate so the student can diff the two
/// approaches without the behavior changing underneath.
/// </summary>
public sealed class FluentUpdateProductRequestValidator
    : AbstractValidator<FluentCreateProductRequest>
{
    public FluentUpdateProductRequestValidator()
    {
        RuleFor(x => x.Name)
            .NotEmpty()
            .Length(3, 50);

        RuleFor(x => x.ProductNumber)
            .NotEmpty()
            .Matches("^[A-Z]{2,4}-\\d{3,5}$")
            .WithMessage("ProductNumber must look like 'BK-1234' or 'ABCD-12345'.");

        RuleFor(x => x.StandardCost)
            .InclusiveBetween(0.01m, 100000m);

        RuleFor(x => x.ListPrice)
            .InclusiveBetween(0.01m, 100000m);

        RuleFor(x => x.SellEndDate)
            .GreaterThan(x => x.SellStartDate)
            .When(x => x.SellEndDate.HasValue)
            .WithMessage("SellEndDate must fall after SellStartDate.");

        RuleFor(x => x)
            .Must(HasRequiredMargin)
            .WithName("ListPrice")
            .WithMessage(x =>
            {
                var margin = x.StandardCost > 0
                    ? (x.ListPrice - x.StandardCost) / x.StandardCost
                    : 0m;
                return $"ListPrice must be at least " +
                    $"{CreateProductRequest.MinimumMarginPercent:P0} above StandardCost " +
                    $"(Halcyon margin policy). Observed margin: {margin:P2}.";
            });
    }

    private static bool HasRequiredMargin(FluentCreateProductRequest request)
    {
        if (request.StandardCost <= 0)
        {
            return true;
        }

        var margin = (request.ListPrice - request.StandardCost) / request.StandardCost;
        return margin >= CreateProductRequest.MinimumMarginPercent;
    }
}
