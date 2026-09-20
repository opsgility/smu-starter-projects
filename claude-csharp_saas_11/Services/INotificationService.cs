using TeamTrackr.DTOs;

namespace TeamTrackr.Services;

public interface INotificationService
{
    Task SendTaskCreated(TaskResponse taskResponse);
    Task SendTaskUpdated(TaskResponse taskResponse);
    Task SendTaskDeleted(int taskId, int projectId);
    Task SendCommentAdded(CommentResponse commentResponse);
}
