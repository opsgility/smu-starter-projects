using Moq;
using Xunit;
using BrightShelf.Models;
using BrightShelf.Services;
using BrightShelf.Pages.Products;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace BrightShelf.Tests;

public class ProductPageTests
{
    // TODO: Test that the Index page loads all products
    [Fact]
    public async Task IndexPage_OnGet_PopulatesProducts()
    {
        // TODO: Arrange - Create a Mock<IProductService> and set up GetAllAsync
        // TODO: Act - Call OnGetAsync()
        // TODO: Assert - Verify Products list is populated

        Assert.True(false, "TODO: Implement this test");
    }

    // TODO: Test that the Create page creates a product and redirects
    [Fact]
    public async Task CreatePage_OnPost_ValidProduct_RedirectsToIndex()
    {
        // TODO: Arrange - Create a Mock<IProductService> and set up CreateAsync
        // TODO: Act - Set Product property and call OnPostAsync()
        // TODO: Assert - Verify redirect to Index page

        Assert.True(false, "TODO: Implement this test");
    }

    // TODO: Test that the Edit page returns NotFound for invalid ID
    [Fact]
    public async Task EditPage_OnGet_InvalidId_ReturnsNotFound()
    {
        // TODO: Arrange - Create a Mock<IProductService> that returns null for GetByIdAsync
        // TODO: Act - Call OnGetAsync with an invalid ID
        // TODO: Assert - Verify NotFoundResult is returned

        Assert.True(false, "TODO: Implement this test");
    }

    // TODO: Test that the Delete page deletes and redirects
    [Fact]
    public async Task DeletePage_OnPost_DeletesAndRedirects()
    {
        // TODO: Arrange - Create a Mock<IProductService> and set up DeleteAsync
        // TODO: Act - Set Product.Id and call OnPostAsync()
        // TODO: Assert - Verify DeleteAsync was called and result is redirect

        Assert.True(false, "TODO: Implement this test");
    }

    // TODO: Test that the Edit page loads existing product data
    [Fact]
    public async Task EditPage_OnGet_ValidId_LoadsProduct()
    {
        // TODO: Arrange - Create a Mock<IProductService> that returns a product
        // TODO: Act - Call OnGetAsync with a valid ID
        // TODO: Assert - Verify Product property is set correctly

        Assert.True(false, "TODO: Implement this test");
    }
}
