namespace DataForge.Models;

// TODO: Add validation annotations to the properties below.
// Suggested validations:
//   - Name: [Required], [StringLength(200, MinimumLength = 2)]
//   - Price: [Range(0.01, 99999.99)]
//   - Description: [StringLength(1000)]
//   - StockQuantity: [Range(0, int.MaxValue)]
//
// You'll need: using System.ComponentModel.DataAnnotations;

public class Product
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public decimal Price { get; set; }
    public string? Description { get; set; }
    public int StockQuantity { get; set; }

    public int CategoryId { get; set; }
    public Category Category { get; set; } = null!;

    public byte[] RowVersion { get; set; } = Array.Empty<byte>();

    // PostgreSQL concurrency token — EF Core uses this automatically
    // when UseXminAsConcurrencyToken() is configured in the DbContext
    public uint xmin { get; set; }
}
