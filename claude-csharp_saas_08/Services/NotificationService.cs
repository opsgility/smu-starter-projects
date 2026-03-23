using Microsoft.AspNetCore.SignalR;
using TeamTrackr.Auth;
using TeamTrackr.DTOs;
using TeamTrackr.Hubs;

namespace TeamTrackr.Services;

public class NotificationService : INotificationService
{
    private readonly IHubContext<TaskHub> _hubContext;
    private readonly ITenantProvider _tenantProvider;

    public NotificationService(IHubContext<TaskHub> hubContext, ITenantProvider tenantProvider)
    {
        _hubContext = hubContext;
        _tenantProvider = tenantProvider;
    }

    public async Task SendTaskCreated(TaskResponse taskResponse)
    {
        var tenantId = _tenantProvider.GetCurrentTenantId();
        await _hubContext.Clients.Group($"tenant_{tenantId}")
            .SendAsync("TaskCreated", taskResponse);
    }

    public async Task SendTaskUpdated(TaskResponse taskResponse)
    {
        var tenantId = _tenantProvider.GetCurrentTenantId();
        await _hubContext.Clients.Group($"tenant_{tenantId}")
            .SendAsync("TaskUpdated", taskResponse);
    }

    public async Task SendTaskDeleted(int taskId, int projectId)
    {
        await _hubContext.Clients.Group($"project_{projectId}")
            .SendAsync("TaskDeleted", new { TaskId = taskId, ProjectId = projectId });
    }

    public async Task SendCommentAdded(CommentResponse commentResponse)
    {
        await _hubContext.Clients.Group($"task_{commentResponse.TaskItemId}")
            .SendAsync("CommentAdded", commentResponse);
    }
}
