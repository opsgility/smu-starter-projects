using AutoMapper;
using Microsoft.AspNetCore.Mvc;
using TaskFlow.Api.DTOs;
using TaskFlow.Api.Models;

namespace TaskFlow.Api.Controllers;

[ApiController]
[Route("api/[controller]")]
public class TasksController : ControllerBase
{
    private static readonly List<TaskItem> _tasks = new()
    {
        new TaskItem { Id = 1, Title = "Learn ASP.NET Core", Description = "Study Web API fundamentals", Priority = "High", CreatedAt = DateTime.UtcNow.AddDays(-3) },
        new TaskItem { Id = 2, Title = "Build a REST API", Description = "Create TaskFlow API project", Priority = "Medium", CreatedAt = DateTime.UtcNow.AddDays(-1) },
        new TaskItem { Id = 3, Title = "Write unit tests", IsComplete = true, Priority = "Low", CreatedAt = DateTime.UtcNow }
    };
    private static int _nextId = 4;

    private readonly IMapper _mapper;

    public TasksController(IMapper mapper)
    {
        _mapper = mapper;
    }

    [HttpGet]
    public ActionResult<IEnumerable<TaskResponseDto>> GetAll(
        [FromQuery] bool? isComplete,
        [FromQuery] string? priority)
    {
        var tasks = _tasks.AsEnumerable();

        if (isComplete.HasValue)
            tasks = tasks.Where(t => t.IsComplete == isComplete.Value);

        if (!string.IsNullOrEmpty(priority))
            tasks = tasks.Where(t => t.Priority.Equals(priority, StringComparison.OrdinalIgnoreCase));

        var taskDtos = _mapper.Map<IEnumerable<TaskResponseDto>>(tasks);
        return Ok(taskDtos);
    }

    [HttpGet("{id}")]
    public ActionResult<TaskResponseDto> GetById(int id)
    {
        var task = _tasks.FirstOrDefault(t => t.Id == id);
        if (task == null)
            return NotFound();

        var taskDto = _mapper.Map<TaskResponseDto>(task);
        return Ok(taskDto);
    }

    [HttpPost]
    public ActionResult<TaskResponseDto> Create([FromBody] CreateTaskDto createDto)
    {
        var task = _mapper.Map<TaskItem>(createDto);
        task.Id = _nextId++;
        task.CreatedAt = DateTime.UtcNow;

        _tasks.Add(task);

        var taskDto = _mapper.Map<TaskResponseDto>(task);
        return CreatedAtAction(nameof(GetById), new { id = task.Id }, taskDto);
    }

    [HttpPut("{id}")]
    public ActionResult<TaskResponseDto> Update(int id, [FromBody] UpdateTaskDto updateDto)
    {
        var task = _tasks.FirstOrDefault(t => t.Id == id);
        if (task == null)
            return NotFound();

        if (updateDto.Title != null) task.Title = updateDto.Title;
        if (updateDto.Description != null) task.Description = updateDto.Description;
        if (updateDto.IsComplete.HasValue) task.IsComplete = updateDto.IsComplete.Value;
        if (updateDto.Priority != null) task.Priority = updateDto.Priority;
        if (updateDto.DueDate.HasValue) task.DueDate = updateDto.DueDate;

        var taskDto = _mapper.Map<TaskResponseDto>(task);
        return Ok(taskDto);
    }

    [HttpDelete("{id}")]
    public IActionResult Delete(int id)
    {
        var task = _tasks.FirstOrDefault(t => t.Id == id);
        if (task == null)
            return NotFound();

        _tasks.Remove(task);
        return NoContent();
    }
}
