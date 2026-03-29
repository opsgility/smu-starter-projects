namespace DataForge.Models;

public class Supplier
{
    public int Id { get; set; }
    public string CompanyName { get; set; } = string.Empty;
    public string? ContactEmail { get; set; }
    public string? Phone { get; set; }

    public List<Product> Products { get; set; } = new();
}
