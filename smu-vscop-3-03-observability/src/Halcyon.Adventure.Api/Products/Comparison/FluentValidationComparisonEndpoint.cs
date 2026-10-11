using FluentValidation;
using Microsoft.AspNetCore.Http.HttpResults;
using Microsoft.AspNetCore.Routing;

namespace Halcyon.Adventure.Api.Products.Comparison;

/// <summary>
/// POST /v1/products/create-with-fluent-validation — the comparison endpoint.
/// Behavior matches POST /v1/products but the validation path runs through
/// FluentValidation's IValidator{T} instead of AddValidation + DataAnnotations.
/// Lesson 3 walks the student through diffing the two.
/// </summary>
public static class FluentValidationComparisonEndpoint
{
    public static RouteGroupBuilder Map(RouteGroupBuilder group)
    {
        group.MapPost("/create-with-fluent-validation", CreateWithFluentValidation)
            .WithName("CreateProductFluent")
            .WithSummary(
                "Comparison endpoint. Same POST shape as /products but validated " +
                "through FluentValidation to let you feel the delta against the " +
                "in-box AddValidation path.")
            .DisableValidation();

        return group;
    }

    private static async Task<Results<Created<Product>, ValidationProblem>>
        CreateWithFluentValidation(
            FluentCreateProductRequest request,
            IValidator<FluentCreateProductRequest> validator,
            IProductRepository repo,
            CancellationToken cancellationToken)
    {
        var validation = await validator.ValidateAsync(request, cancellationToken);
        if (!validation.IsValid)
        {
            var errors = validation.Errors
                .GroupBy(f => f.PropertyName)
                .ToDictionary(
                    g => g.Key,
                    g => g.Select(f => f.ErrorMessage).ToArray());
            return TypedResults.ValidationProblem(errors);
        }

        var created = repo.Create(new CreateProductRequest(
            request.Name,
            request.ProductNumber,
            request.StandardCost,
            request.ListPrice,
            request.SellStartDate,
            request.SellEndDate));
        return TypedResults.Created($"/products/{created.ProductId}", created);
    }
}
