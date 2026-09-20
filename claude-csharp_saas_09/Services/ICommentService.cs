using TeamTrackr.DTOs;

namespace TeamTrackr.Services;

public interface ICommentService
{
    Task<List<CommentResponse>> GetByTaskIdAsync(int taskItemId);
    Task<CommentResponse?> GetByIdAsync(int id);
    Task<CommentResponse> CreateAsync(int taskItemId, CreateCommentRequest request, string authorId);
    Task<bool> DeleteAsync(int id);
}
