namespace TeamTrackr.DTOs;

public class CreateCommentRequest
{
    public string Content { get; set; } = string.Empty;
}

public class CommentResponse
{
    public int Id { get; set; }
    public int TaskItemId { get; set; }
    public string AuthorId { get; set; } = string.Empty;
    public string AuthorName { get; set; } = string.Empty;
    public string Content { get; set; } = string.Empty;
    public DateTime CreatedAt { get; set; }
}
