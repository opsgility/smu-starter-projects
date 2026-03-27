namespace TaskFlow.Api.Models;

public class TaskItem
{
    public int Id { get; set; }
    public string Title { get; set; } = string.Empty;
    public string? Description { get; set; }
    public bool IsComplete { get; set; }
    public string Priority { get; set; } = "Medium";
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    public DateTime? DueDate { get; set; }
    public int? CategoryId { get; set; }
    public Category? Category { get; set; }
    public int UserId { get; set; }
}
