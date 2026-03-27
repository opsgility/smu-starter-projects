using System.ComponentModel.DataAnnotations;

namespace TaskFlow.Api.DTOs;

public class CreateTaskDto
{
    [Required]
    public string Title { get; set; } = string.Empty;
    public string? Description { get; set; }
    public string Priority { get; set; } = "Medium";
    public DateTime? DueDate { get; set; }
}
