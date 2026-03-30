namespace BrightShelf.Models;

// TODO: Add data annotation attributes for validation
// - Name should be required with a max length
// - Price should be required with a range
// - Description should have a max length
public class Product
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public decimal Price { get; set; }
    public string Description { get; set; } = string.Empty;
}
