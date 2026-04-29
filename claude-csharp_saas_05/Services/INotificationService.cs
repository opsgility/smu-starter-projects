using TeamTrackr.DTOs;

namespace TeamTrackr.Services;

// Stub interface — students implement NotificationService in Exercise 2 of this lab
public interface INotificationService
{
    Task SendTaskCreated(TaskResponse taskResponse);
    Task SendTaskUpdated(TaskResponse taskResponse);
    Task SendTaskDeleted(int taskId, int projectId);
    Task SendCommentAdded(CommentResponse commentResponse);
}
