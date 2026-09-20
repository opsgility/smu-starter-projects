using TeamTrackr.DTOs;

namespace TeamTrackr.Services;

public interface ILabelService
{
    Task<List<LabelResponse>> GetAllAsync();
    Task<LabelResponse?> GetByIdAsync(int id);
    Task<LabelResponse> CreateAsync(CreateLabelRequest request);
    Task<bool> DeleteAsync(int id);
    Task<bool> AssignToTaskAsync(int taskItemId, int labelId);
    Task<bool> RemoveFromTaskAsync(int taskItemId, int labelId);
}
