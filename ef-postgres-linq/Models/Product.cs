using System.ComponentModel.DataAnnotations;

namespace DataForge.Models;

public class Product
{
    public int Id { get; set; }
    [Required, MaxLength(200)]
    public string Name { get; set; } = string.Empty;
    public decimal Price { get; set; }
    [MaxLength(1000)]
    public string? Description { get; set; }
    public int StockQuantity { get; set; }
    public bool IsActive { get; set; } = true;
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    public int CategoryId { get; set; }
    public Category? Category { get; set; }
    public int SupplierId { get; set; }
    public Supplier? Supplier { get; set; }
    public ICollection<Tag> Tags { get; set; } = new List<Tag>();
}
