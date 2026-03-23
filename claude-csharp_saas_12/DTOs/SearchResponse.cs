namespace TeamTrackr.DTOs;

public class SearchResponse<T>
{
    public List<T> Items { get; set; } = new();
    public int TotalCount { get; set; }
    public int Page { get; set; }
    public int PageSize { get; set; }
    public bool HasMore { get; set; }
}

public class GlobalSearchResult
{
    public string Type { get; set; } = string.Empty; // "task" or "project"
    public int Id { get; set; }
    public string Title { get; set; } = string.Empty;
    public string Description { get; set; } = string.Empty;
}
