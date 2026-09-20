using System.Security.Claims;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using TaskFlow.Api.Authorization;
using TaskFlow.Api.DTOs;
using TaskFlow.Api.Services;

namespace TaskFlow.Api.Controllers;

[ApiController]
[Route("api/[controller]")]
[Authorize]
public class TasksController : ControllerBase
{
    private readonly ITaskService _taskService;
    private readonly IAuthorizationService _authorizationService;

    public TasksController(ITaskService taskService, IAuthorizationService authorizationService)
    {
        _taskService = taskService;
        _authorizationService = authorizationService;
    }

    private string GetUserId() =>
        User.FindFirst(ClaimTypes.NameIdentifier)?.Value ?? throw new UnauthorizedAccessException();

    [HttpGet]
    public async Task<ActionResult<IEnumerable<TaskResponseDto>>> GetMyTasks(
        [FromQuery] bool? isComplete,
        [FromQuery] string? priority)
    {
        var userId = GetUserId();
        var tasks = await _taskService.GetTasksByUserAsync(userId, isComplete, priority);
        return Ok(tasks);
    }

    [HttpGet("all")]
    [Authorize(Roles = "Admin")]
    public async Task<ActionResult<IEnumerable<TaskResponseDto>>> GetAll(
        [FromQuery] bool? isComplete,
        [FromQuery] string? priority)
    {
        var tasks = await _taskService.GetTasksAsync(isComplete, priority);
        return Ok(tasks);
    }

    [HttpGet("{id}")]
    public async Task<ActionResult<TaskResponseDto>> GetById(int id)
    {
        var task = await _taskService.GetTaskByIdAsync(id);
        if (task == null)
            return NotFound();

        // Check ownership (admins can see any task)
        if (!User.IsInRole("Admin") && task.UserId != GetUserId())
            return Forbid();

        return Ok(task);
    }

    [HttpPost]
    public async Task<ActionResult<TaskResponseDto>> Create([FromBody] CreateTaskDto createDto)
    {
        var userId = GetUserId();
        var task = await _taskService.CreateTaskAsync(createDto, userId);
        return CreatedAtAction(nameof(GetById), new { id = task.Id }, task);
    }

    [HttpPut("{id}")]
    public async Task<ActionResult<TaskResponseDto>> Update(int id, [FromBody] UpdateTaskDto updateDto)
    {
        var existing = await _taskService.GetTaskByIdAsync(id);
        if (existing == null)
            return NotFound();

        if (!User.IsInRole("Admin") && existing.UserId != GetUserId())
            return Forbid();

        var task = await _taskService.UpdateTaskAsync(id, updateDto);
        return Ok(task);
    }

    [HttpDelete("{id}")]
    [Authorize(Roles = "Admin")]
    public async Task<IActionResult> Delete(int id)
    {
        var result = await _taskService.DeleteTaskAsync(id);
        if (!result)
            return NotFound();

        return NoContent();
    }
}
