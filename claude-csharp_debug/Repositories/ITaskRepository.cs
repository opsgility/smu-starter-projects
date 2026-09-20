using DebugApi.Models;

namespace DebugApi.Repositories;

public interface ITaskRepository
{
    List<TaskItem> GetAll();
    TaskItem GetById(int id);
    TaskItem Create(TaskItem task);
    TaskItem Update(TaskItem task);
    bool Delete(int id);
}
