using TaskFlow.Api.DTOs;

namespace TaskFlow.Api.Services;

public interface ITaskService
{
    Task<IEnumerable<TaskResponseDto>> GetTasksAsync(bool? isComplete = null, string? priority = null);
    Task<TaskResponseDto> GetTaskByIdAsync(int id);
    Task<TaskResponseDto> CreateTaskAsync(CreateTaskDto dto, int userId);
    Task<TaskResponseDto> UpdateTaskAsync(int id, UpdateTaskDto dto);
    Task DeleteTaskAsync(int id);
}
