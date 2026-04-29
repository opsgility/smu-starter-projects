using Microsoft.AspNetCore.SignalR;
using TeamTrackr.Auth;
using TeamTrackr.DTOs;
using TeamTrackr.Hubs;

namespace TeamTrackr.Services;

// Scaffolded stub — replace with real implementation in Exercise 2: Notification Service
public class NotificationService : INotificationService
{
    private readonly IHubContext<TaskHub> _hubContext;

    public NotificationService(IHubContext<TaskHub> hubContext)
    {
        _hubContext = hubContext;
    }

    public Task SendTaskCreated(TaskResponse taskResponse) => Task.CompletedTask;
    public Task SendTaskUpdated(TaskResponse taskResponse) => Task.CompletedTask;
    public Task SendTaskDeleted(int taskId, int projectId) => Task.CompletedTask;
    public Task SendCommentAdded(CommentResponse commentResponse) => Task.CompletedTask;
}
