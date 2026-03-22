using DebugApi.Models;
using DebugApi.Repositories;

namespace DebugApi.Services;

public class TaskService : ITaskService
{
    private readonly ITaskRepository _repository;

    public TaskService(ITaskRepository repository)
    {
        _repository = repository;
    }

    // BUG 3: Uses .Result instead of await — potential deadlock
    public Task<List<TaskItem>> GetAllAsync()
    {
        var result = Task.Run(() => _repository.GetAll()).Result;
        return Task.FromResult(result);
    }

    public Task<TaskItem> GetByIdAsync(int id)
    {
        return Task.FromResult(_repository.GetById(id));
    }

    public Task<TaskItem> CreateAsync(TaskItem task)
    {
        return Task.FromResult(_repository.Create(task));
    }

    // BUG 4: Only checks max length, allows empty titles
    public Task<TaskItem> UpdateAsync(TaskItem task)
    {
        if (task.Title.Length > 200)
            throw new ArgumentException("Title must be 200 characters or less");
        return Task.FromResult(_repository.Update(task));
    }

    public Task<bool> DeleteAsync(int id)
    {
        return Task.FromResult(_repository.Delete(id));
    }
}
