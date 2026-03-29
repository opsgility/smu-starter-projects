namespace DataForge.Models;

public class ProductDetail
{
    public int Id { get; set; }
    public double Weight { get; set; }
    public string? Dimensions { get; set; }
    public int ProductId { get; set; }
    // TODO: Add navigation property back to Product
}
