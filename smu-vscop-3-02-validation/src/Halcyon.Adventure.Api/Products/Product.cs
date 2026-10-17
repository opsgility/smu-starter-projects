namespace Halcyon.Adventure.Api.Products;

// Domain entity. In-memory for lab scope; a future refactor swaps the repository
// for the EF Core 10 scaffold against Production.Product in Course 4.
public sealed class Product
{
    public int Id { get; set; }
    public string Sku { get; set; } = string.Empty;
    public string Name { get; set; } = string.Empty;
    public decimal Price { get; set; }
    public decimal Cost { get; set; }
}
