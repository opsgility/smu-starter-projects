using DebugApi.Models;
using DebugApi.Services;
using Microsoft.AspNetCore.Mvc;

namespace DebugApi.Controllers;

[ApiController]
[Route("api/[controller]")]
public class TasksController : ControllerBase
{
    private readonly ITaskService _taskService;

    public TasksController(ITaskService taskService)
    {
        _taskService = taskService;
    }

    [HttpGet]
    public async Task<ActionResult<List<TaskItem>>> GetAll()
    {
        var tasks = await _taskService.GetAllAsync();
        return Ok(tasks);
    }

    [HttpGet("{id}")]
    public async Task<ActionResult<TaskItem>> GetById(int id)
    {
        var task = await _taskService.GetByIdAsync(id);
        return Ok(task);
    }

    [HttpPost]
    public async Task<ActionResult<TaskItem>> Create(TaskItem task)
    {
        var created = await _taskService.CreateAsync(task);
        // BUG 5: Returns Ok (200) instead of CreatedAtAction (201)
        return Ok(created);
    }

    [HttpPut("{id}")]
    public async Task<ActionResult<TaskItem>> Update(int id, TaskItem task)
    {
        task.Id = id;
        var updated = await _taskService.UpdateAsync(task);
        return Ok(updated);
    }

    [HttpDelete("{id}")]
    public async Task<ActionResult> Delete(int id)
    {
        var result = await _taskService.DeleteAsync(id);
        if (!result) return NotFound();
        return NoContent();
    }
}
