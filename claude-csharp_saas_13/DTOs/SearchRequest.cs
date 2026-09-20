using TeamTrackr.Models;

namespace TeamTrackr.DTOs;

public class SearchRequest
{
    public string Query { get; set; } = string.Empty;
    public TaskItemStatus? Status { get; set; }
    public TaskPriority? Priority { get; set; }
    public string? AssigneeId { get; set; }
    public int? ProjectId { get; set; }
    public int? LabelId { get; set; }
    public DateTime? DueBefore { get; set; }
    public DateTime? DueAfter { get; set; }
    public int Page { get; set; } = 1;
    public int PageSize { get; set; } = 20;
}
