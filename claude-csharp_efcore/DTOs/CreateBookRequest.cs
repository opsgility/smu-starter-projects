using System.ComponentModel.DataAnnotations;

namespace BookLibrary.DTOs;

public class CreateBookRequest
{
    [Required] public string Title { get; set; } = string.Empty;
    [Required] public int AuthorId { get; set; }
    [Required] public string ISBN { get; set; } = string.Empty;
    [Range(1450, 2100)] public int PublicationYear { get; set; }
}
