namespace TeamTrackr.Models;

public class TaskItemLabel
{
    public int TaskItemId { get; set; }
    public TaskItem TaskItem { get; set; } = null!;
    public int TaskLabelId { get; set; }
    public TaskLabel TaskLabel { get; set; } = null!;
}
