using System.Net;
using System.Net.Http.Json;
using Halcyon.Adventure.Shared.Products;
using Microsoft.AspNetCore.Mvc.Testing;

namespace Halcyon.Adventure.Api.Tests.Products;

// Baseline tests from the Lesson 2 ship. Lesson 4 adds the ValidationTests nested
// class in Exercise 2 and the margin-rule tests in Exercise 3.
public class ProductsEndpointsTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly WebApplicationFactory<Program> _factory;

    public ProductsEndpointsTests(WebApplicationFactory<Program> factory)
    {
        _factory = factory;
    }

    [Fact]
    public async Task Get_Products_Returns_Ok_With_Seeded_Rows()
    {
        var client = _factory.CreateClient();

        var products = await client.GetFromJsonAsync<ProductDto[]>("/products");

        Assert.NotNull(products);
        Assert.NotEmpty(products);
    }

    [Fact]
    public async Task Get_Product_By_Unknown_Id_Returns_NotFound()
    {
        var client = _factory.CreateClient();

        var response = await client.GetAsync("/products/999999");

        Assert.Equal(HttpStatusCode.NotFound, response.StatusCode);
    }

    [Fact]
    public async Task Post_Product_With_Valid_Payload_Returns_Created()
    {
        var client = _factory.CreateClient();
        var payload = new CreateProductRequest(
            Sku: "AW-TEST-001",
            Name: "Test Product",
            Price: 120.00m,
            Cost: 100.00m);

        var response = await client.PostAsJsonAsync("/products", payload);

        Assert.Equal(HttpStatusCode.Created, response.StatusCode);
    }
}
