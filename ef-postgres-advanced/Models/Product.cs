namespace DataForge.Models;

public class Product
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public string? SKU { get; set; }
    public decimal Price { get; set; }
    public int StockQuantity { get; set; }
    public bool IsDeleted { get; set; }

    public int CategoryId { get; set; }
    public Category Category { get; set; } = null!;

    public int SupplierId { get; set; }
    public Supplier Supplier { get; set; } = null!;

    // Many-to-many with Tag
    public List<Tag> Tags { get; set; } = new();
}
