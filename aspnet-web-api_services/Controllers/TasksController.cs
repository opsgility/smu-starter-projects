using AutoMapper;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using TaskFlow.Api.Data;
using TaskFlow.Api.DTOs;
using TaskFlow.Api.Models;

namespace TaskFlow.Api.Controllers;

[ApiController]
[Route("api/[controller]")]
public class TasksController : ControllerBase
{
    private readonly TaskFlowDbContext _context;
    private readonly IMapper _mapper;

    public TasksController(TaskFlowDbContext context, IMapper mapper)
    {
        _context = context;
        _mapper = mapper;
    }

    [HttpGet]
    public async Task<ActionResult<IEnumerable<TaskResponseDto>>> GetAll(
        [FromQuery] bool? isComplete,
        [FromQuery] string? priority)
    {
        var query = _context.Tasks
            .Include(t => t.Category)
            .AsQueryable();

        if (isComplete.HasValue)
            query = query.Where(t => t.IsComplete == isComplete.Value);

        if (!string.IsNullOrEmpty(priority))
            query = query.Where(t => t.Priority == priority);

        var tasks = await query.ToListAsync();
        var taskDtos = _mapper.Map<IEnumerable<TaskResponseDto>>(tasks);
        return Ok(taskDtos);
    }

    [HttpGet("{id}")]
    public async Task<ActionResult<TaskResponseDto>> GetById(int id)
    {
        var task = await _context.Tasks
            .Include(t => t.Category)
            .FirstOrDefaultAsync(t => t.Id == id);

        if (task == null)
            return NotFound();

        var taskDto = _mapper.Map<TaskResponseDto>(task);
        return Ok(taskDto);
    }

    [HttpPost]
    public async Task<ActionResult<TaskResponseDto>> Create([FromBody] CreateTaskDto createDto)
    {
        var task = _mapper.Map<TaskItem>(createDto);
        task.CreatedAt = DateTime.UtcNow;

        _context.Tasks.Add(task);
        await _context.SaveChangesAsync();

        await _context.Entry(task).Reference(t => t.Category).LoadAsync();

        var taskDto = _mapper.Map<TaskResponseDto>(task);
        return CreatedAtAction(nameof(GetById), new { id = task.Id }, taskDto);
    }

    [HttpPut("{id}")]
    public async Task<ActionResult<TaskResponseDto>> Update(int id, [FromBody] UpdateTaskDto updateDto)
    {
        var task = await _context.Tasks
            .Include(t => t.Category)
            .FirstOrDefaultAsync(t => t.Id == id);

        if (task == null)
            return NotFound();

        if (updateDto.Title != null) task.Title = updateDto.Title;
        if (updateDto.Description != null) task.Description = updateDto.Description;
        if (updateDto.IsComplete.HasValue) task.IsComplete = updateDto.IsComplete.Value;
        if (updateDto.Priority != null) task.Priority = updateDto.Priority;
        if (updateDto.DueDate.HasValue) task.DueDate = updateDto.DueDate;
        if (updateDto.CategoryId.HasValue) task.CategoryId = updateDto.CategoryId;

        await _context.SaveChangesAsync();

        await _context.Entry(task).Reference(t => t.Category).LoadAsync();

        var taskDto = _mapper.Map<TaskResponseDto>(task);
        return Ok(taskDto);
    }

    [HttpDelete("{id}")]
    public async Task<IActionResult> Delete(int id)
    {
        var task = await _context.Tasks.FindAsync(id);
        if (task == null)
            return NotFound();

        _context.Tasks.Remove(task);
        await _context.SaveChangesAsync();

        return NoContent();
    }
}
