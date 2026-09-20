using System.ComponentModel.DataAnnotations;

namespace DataForge.Models;

public class Tag
{
    public int Id { get; set; }
    [Required, MaxLength(50)]
    public string Name { get; set; } = string.Empty;
    // TODO: Add navigation property for many-to-many with Product
}
