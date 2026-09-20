namespace TeamTrackr.Models;

public class TaskItem
{
    public int Id { get; set; }
    public int TenantId { get; set; }
    public int ProjectId { get; set; }
    public Project Project { get; set; } = null!;
    public string Title { get; set; } = string.Empty;
    public string Description { get; set; } = string.Empty;
    public TaskItemStatus Status { get; set; } = TaskItemStatus.Todo;
    public TaskPriority Priority { get; set; } = TaskPriority.None;
    public string? AssigneeId { get; set; }
    public AppUser? Assignee { get; set; }
    public string CreatedByUserId { get; set; } = string.Empty;
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    public DateTime UpdatedAt { get; set; } = DateTime.UtcNow;
    public DateTime? DueDate { get; set; }
    public bool ReminderSent { get; set; }
    public List<TaskItemLabel> TaskItemLabels { get; set; } = new();
}
