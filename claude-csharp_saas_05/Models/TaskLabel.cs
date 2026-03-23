namespace TeamTrackr.Models;

public class TaskLabel
{
    public int Id { get; set; }
    public int TenantId { get; set; }
    public string Name { get; set; } = string.Empty;
    public string Color { get; set; } = "#000000";
    public List<TaskItemLabel> TaskItemLabels { get; set; } = new();
}
