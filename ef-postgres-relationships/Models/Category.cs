using System.ComponentModel.DataAnnotations;

namespace DataForge.Models;

public class Category
{
    public int Id { get; set; }
    [Required, MaxLength(100)]
    public string Name { get; set; } = string.Empty;
    [MaxLength(500)]
    public string? Description { get; set; }
    // TODO: Add navigation property for Products collection
}
