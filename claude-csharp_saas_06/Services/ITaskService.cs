using TeamTrackr.DTOs;
using TeamTrackr.Models;

namespace TeamTrackr.Services;

public interface ITaskService
{
    Task<List<TaskResponse>> GetAllAsync(
        TaskItemStatus? status = null,
        TaskPriority? priority = null,
        string? assigneeId = null,
        int? projectId = null);
    Task<TaskResponse?> GetByIdAsync(int id);
    Task<TaskResponse> CreateAsync(CreateTaskRequest request, string userId);
    Task<TaskResponse?> UpdateAsync(int id, UpdateTaskRequest request);
    Task<bool> DeleteAsync(int id);
}
