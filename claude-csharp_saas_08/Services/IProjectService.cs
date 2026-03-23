using TeamTrackr.DTOs;

namespace TeamTrackr.Services;

public interface IProjectService
{
    Task<List<ProjectResponse>> GetAllAsync();
    Task<ProjectResponse?> GetByIdAsync(int id);
    Task<ProjectResponse> CreateAsync(CreateProjectRequest request, string userId);
    Task<ProjectResponse?> UpdateAsync(int id, UpdateProjectRequest request);
    Task<bool> DeleteAsync(int id);
    Task<List<TaskResponse>> GetTasksByProjectAsync(int projectId);
}
