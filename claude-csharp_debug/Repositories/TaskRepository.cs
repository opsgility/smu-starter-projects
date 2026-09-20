using DebugApi.Models;

namespace DebugApi.Repositories;

public class TaskRepository : ITaskRepository
{
    private readonly List<TaskItem> _tasks = new()
    {
        new TaskItem { Id = 1, Title = "Set up project", Description = "Initialize the API project", IsCompleted = true },
        new TaskItem { Id = 2, Title = "Add authentication", Description = "Implement JWT auth", IsCompleted = false },
        new TaskItem { Id = 3, Title = "Write tests", Description = "Add unit tests for services", IsCompleted = false }
    };
    private int _nextId = 4;

    public List<TaskItem> GetAll() => _tasks.ToList();

    // BUG 2: Uses First instead of FirstOrDefault — throws when not found
    public TaskItem GetById(int id) => _tasks.First(t => t.Id == id);

    public TaskItem Create(TaskItem task)
    {
        task.Id = _nextId++;
        task.CreatedAt = DateTime.UtcNow;
        _tasks.Add(task);
        return task;
    }

    public TaskItem Update(TaskItem task)
    {
        var existing = _tasks.FirstOrDefault(t => t.Id == task.Id);
        if (existing == null) return null!;
        existing.Title = task.Title;
        existing.Description = task.Description;
        existing.IsCompleted = task.IsCompleted;
        return existing;
    }

    public bool Delete(int id)
    {
        var task = _tasks.FirstOrDefault(t => t.Id == id);
        if (task == null) return false;
        _tasks.Remove(task);
        return true;
    }
}
