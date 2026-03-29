using System.ComponentModel.DataAnnotations;

namespace DataForge.Models;

public class Supplier
{
    public int Id { get; set; }
    [Required, MaxLength(200)]
    public string CompanyName { get; set; } = string.Empty;
    [MaxLength(200)]
    public string? ContactEmail { get; set; }
    [MaxLength(20)]
    public string? Phone { get; set; }
}
