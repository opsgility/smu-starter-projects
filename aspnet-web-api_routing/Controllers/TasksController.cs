using Microsoft.AspNetCore.Mvc;
using TaskFlow.Api.Models;

namespace TaskFlow.Api.Controllers;

[ApiController]
[Route("api/[controller]")]
public class TasksController : ControllerBase
{
    private static readonly List<TaskItem> _tasks = new()
    {
        new TaskItem
        {
            Id = 1,
            Title = "Set up development environment",
            Description = "Install .NET SDK and configure VS Code",
            IsComplete = true,
            Priority = "High",
            CreatedAt = DateTime.UtcNow.AddDays(-2)
        },
        new TaskItem
        {
            Id = 2,
            Title = "Build TaskFlow API",
            Description = "Create the initial Web API project",
            IsComplete = false,
            Priority = "High",
            CreatedAt = DateTime.UtcNow.AddDays(-1)
        }
    };

    private static int _nextId = 3;

    [HttpGet]
    public ActionResult<List<TaskItem>> GetAll()
    {
        return Ok(_tasks);
    }

    [HttpGet("{id}")]
    public ActionResult<TaskItem> GetById(int id)
    {
        var task = _tasks.FirstOrDefault(t => t.Id == id);

        if (task == null)
        {
            return NotFound();
        }

        return Ok(task);
    }

    [HttpPost]
    public ActionResult<TaskItem> Create(TaskItem task)
    {
        task.Id = _nextId++;
        task.CreatedAt = DateTime.UtcNow;
        _tasks.Add(task);

        return CreatedAtAction(nameof(GetById), new { id = task.Id }, task);
    }
}
