namespace TaskFlow.Api.DTOs;

public class UpdateTaskDto
{
    public string? Title { get; set; }
    public string? Description { get; set; }
    public bool? IsComplete { get; set; }
    public string? Priority { get; set; }
    public DateTime? DueDate { get; set; }
    public int? CategoryId { get; set; }
}
