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
    public ActionResult<List<TaskItem>> GetAll(
        [FromQuery] string? status,
        [FromQuery] string? priority,
        [FromQuery] string? search)
    {
        var results = _tasks.AsEnumerable();

        if (!string.IsNullOrEmpty(status))
        {
            results = status.ToLower() switch
            {
                "complete" => results.Where(t => t.IsComplete),
                "incomplete" => results.Where(t => !t.IsComplete),
                _ => results
            };
        }

        if (!string.IsNullOrEmpty(priority))
        {
            results = results.Where(t =>
                t.Priority.Equals(priority, StringComparison.OrdinalIgnoreCase));
        }

        if (!string.IsNullOrEmpty(search))
        {
            results = results.Where(t =>
                t.Title.Contains(search, StringComparison.OrdinalIgnoreCase) ||
                (t.Description != null && t.Description.Contains(search, StringComparison.OrdinalIgnoreCase)));
        }

        return Ok(results.ToList());
    }

    [HttpGet("{id:int}")]
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
    public ActionResult<TaskItem> Create(
        TaskItem task,
        [FromHeader(Name = "X-Request-Id")] string? requestId)
    {
        if (requestId != null)
        {
            Console.WriteLine($"Processing request {requestId}");
        }

        task.Id = _nextId++;
        task.CreatedAt = DateTime.UtcNow;
        _tasks.Add(task);

        return CreatedAtAction(nameof(GetById), new { id = task.Id }, task);
    }

    [HttpPut("{id:int}")]
    public ActionResult<TaskItem> Update(int id, TaskItem updatedTask)
    {
        var task = _tasks.FirstOrDefault(t => t.Id == id);

        if (task == null)
        {
            return NotFound();
        }

        task.Title = updatedTask.Title;
        task.Description = updatedTask.Description;
        task.IsComplete = updatedTask.IsComplete;
        task.Priority = updatedTask.Priority;

        return Ok(task);
    }

    [HttpDelete("{id:int}")]
    public IActionResult Delete(int id)
    {
        var task = _tasks.FirstOrDefault(t => t.Id == id);

        if (task == null)
        {
            return NotFound();
        }

        _tasks.Remove(task);

        return NoContent();
    }
}
