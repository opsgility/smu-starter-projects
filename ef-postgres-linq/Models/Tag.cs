using System.ComponentModel.DataAnnotations;

namespace DataForge.Models;

public class Tag
{
    public int Id { get; set; }
    [Required, MaxLength(50)]
    public string Name { get; set; } = string.Empty;
    public ICollection<Product> Products { get; set; } = new List<Product>();
}
