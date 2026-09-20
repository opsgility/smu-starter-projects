using System.Security.Claims;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using TaskFlow.Api.Authorization;
using TaskFlow.Api.DTOs;
using TaskFlow.Api.Services;

namespace TaskFlow.Api.Controllers;

/// <summary>
/// Manages task items with user-scoped access and role-based authorization.
/// </summary>
[ApiController]
[Route("api/[controller]")]
[Authorize]
[Produces("application/json")]
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

    /// <summary>
    /// Get all tasks for the authenticated user.
    /// </summary>
    /// <param name="isComplete">Filter by completion status</param>
    /// <param name="priority">Filter by priority (Low, Medium, High, Critical)</param>
    /// <returns>A list of the user's tasks</returns>
    [HttpGet]
    [ProducesResponseType(typeof(IEnumerable<TaskResponseDto>), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    public async Task<ActionResult<IEnumerable<TaskResponseDto>>> GetMyTasks(
        [FromQuery] bool? isComplete,
        [FromQuery] string? priority)
    {
        var userId = GetUserId();
        var tasks = await _taskService.GetTasksByUserAsync(userId, isComplete, priority);
        return Ok(tasks);
    }

    /// <summary>
    /// Get all tasks across all users. Requires Admin role.
    /// </summary>
    /// <param name="isComplete">Filter by completion status</param>
    /// <param name="priority">Filter by priority (Low, Medium, High, Critical)</param>
    /// <returns>A list of all tasks in the system</returns>
    [HttpGet("all")]
    [Authorize(Roles = "Admin")]
    [ProducesResponseType(typeof(IEnumerable<TaskResponseDto>), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    [ProducesResponseType(StatusCodes.Status403Forbidden)]
    public async Task<ActionResult<IEnumerable<TaskResponseDto>>> GetAll(
        [FromQuery] bool? isComplete,
        [FromQuery] string? priority)
    {
        var tasks = await _taskService.GetTasksAsync(isComplete, priority);
        return Ok(tasks);
    }

    /// <summary>
    /// Get a specific task by ID.
    /// </summary>
    /// <param name="id">The task ID</param>
    /// <returns>The requested task</returns>
    [HttpGet("{id}")]
    [ProducesResponseType(typeof(TaskResponseDto), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    [ProducesResponseType(StatusCodes.Status403Forbidden)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<ActionResult<TaskResponseDto>> GetById(int id)
    {
        var task = await _taskService.GetTaskByIdAsync(id);
        if (task == null)
            return NotFound();

        if (!User.IsInRole("Admin") && task.UserId != GetUserId())
            return Forbid();

        return Ok(task);
    }

    /// <summary>
    /// Create a new task for the authenticated user.
    /// </summary>
    /// <param name="createDto">Task creation details</param>
    /// <returns>The newly created task</returns>
    [HttpPost]
    [ProducesResponseType(typeof(TaskResponseDto), StatusCodes.Status201Created)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    public async Task<ActionResult<TaskResponseDto>> Create([FromBody] CreateTaskDto createDto)
    {
        var userId = GetUserId();
        var task = await _taskService.CreateTaskAsync(createDto, userId);
        return CreatedAtAction(nameof(GetById), new { id = task.Id }, task);
    }

    /// <summary>
    /// Update an existing task.
    /// </summary>
    /// <param name="id">The task ID to update</param>
    /// <param name="updateDto">Fields to update</param>
    /// <returns>The updated task</returns>
    [HttpPut("{id}")]
    [ProducesResponseType(typeof(TaskResponseDto), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    [ProducesResponseType(StatusCodes.Status403Forbidden)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
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

    /// <summary>
    /// Delete a task. Requires Admin role.
    /// </summary>
    /// <param name="id">The task ID to delete</param>
    [HttpDelete("{id}")]
    [Authorize(Roles = "Admin")]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    [ProducesResponseType(StatusCodes.Status403Forbidden)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> Delete(int id)
    {
        var result = await _taskService.DeleteTaskAsync(id);
        if (!result)
            return NotFound();

        return NoContent();
    }
}
