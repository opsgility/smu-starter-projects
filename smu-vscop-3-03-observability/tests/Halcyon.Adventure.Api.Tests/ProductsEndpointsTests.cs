using System.Net;
using System.Net.Http.Json;
using FluentAssertions;
using Microsoft.AspNetCore.Mvc.Testing;
using Xunit;

namespace Halcyon.Adventure.Api.Tests;

/// <summary>
/// End-to-end integration tests over the Products API. Each test spins up the
/// full application through WebApplicationFactory so the built-in validation
/// filter, the HalcyonProblemDetailsService, and the versioned route groups
/// all run exactly as they would in production.
/// </summary>
public sealed class ProductsEndpointsTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly WebApplicationFactory<Program> _factory;

    public ProductsEndpointsTests(WebApplicationFactory<Program> factory)
    {
        _factory = factory;
    }

    [Fact]
    public async Task CreateProduct_HappyPath_Returns201AndEcho()
    {
        var client = _factory.CreateClient();
        var request = new
        {
            name = "Road-250 Red, 58",
            productNumber = "BK-R64R-58",
            standardCost = 1554.94m,
            listPrice = 2443.35m,
            sellStartDate = "2026-01-01",
            sellEndDate = (string?)null,
        };

        var response = await client.PostAsJsonAsync("/v1/products", request);

        response.StatusCode.Should().Be(HttpStatusCode.Created);
        var body = await response.Content.ReadFromJsonAsync<ProductDto>();
        body.Should().NotBeNull();
        body!.Name.Should().Be("Road-250 Red, 58");
        body.ListPrice.Should().Be(2443.35m);
    }

    [Fact]
    public async Task CreateProduct_MissingName_Returns400ProblemDetailsWithTraceId()
    {
        var client = _factory.CreateClient();
        var request = new
        {
            name = "",
            productNumber = "BK-R64R-58",
            standardCost = 1554.94m,
            listPrice = 2443.35m,
            sellStartDate = "2026-01-01",
        };

        var response = await client.PostAsJsonAsync("/v1/products", request);

        response.StatusCode.Should().Be(HttpStatusCode.BadRequest);
        response.Content.Headers.ContentType!.MediaType
            .Should().Be("application/problem+json");

        var problem = await response.Content.ReadFromJsonAsync<ProblemDetailsDto>();
        problem.Should().NotBeNull();
        problem!.Status.Should().Be(400);
        problem.Errors.Should().ContainKey("Name");
        problem.TraceId.Should().NotBeNullOrEmpty(
            "HalcyonProblemDetailsService must stamp every validation 400 with a trace id " +
            "so support can grep the application log in seconds.");
    }

    [Fact]
    public async Task CreateProduct_MarginBelow15Percent_Returns400WithMarginError()
    {
        var client = _factory.CreateClient();
        // Cost 1000, ListPrice 1100 = 10% margin — below Halcyon's 15% floor.
        var request = new
        {
            name = "Mountain-500 Black, 42",
            productNumber = "BK-M18B-42",
            standardCost = 1000m,
            listPrice = 1100m,
            sellStartDate = "2026-01-01",
            sellEndDate = (string?)null,
        };

        var response = await client.PostAsJsonAsync("/v1/products", request);

        response.StatusCode.Should().Be(HttpStatusCode.BadRequest);
        var problem = await response.Content.ReadFromJsonAsync<ProblemDetailsDto>();
        problem.Should().NotBeNull();
        problem!.Errors.Should().ContainKey("ListPrice");
        var listPriceErrors = problem.Errors["ListPrice"];
        listPriceErrors.Should().Contain(e =>
            e.Contains("Halcyon margin policy", StringComparison.OrdinalIgnoreCase));
    }

    private sealed record ProductDto(
        int ProductId,
        string Name,
        string ProductNumber,
        decimal StandardCost,
        decimal ListPrice);

    private sealed record ProblemDetailsDto(
        string? Type,
        string? Title,
        int? Status,
        string? TraceId,
        Dictionary<string, string[]> Errors);
}
