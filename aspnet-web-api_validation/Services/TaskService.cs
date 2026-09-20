using AutoMapper;
using TaskFlow.Api.DTOs;
using TaskFlow.Api.Models;
using TaskFlow.Api.Repositories;

namespace TaskFlow.Api.Services;

public class TaskService : ITaskService
{
    private readonly ITaskRepository _repository;
    private readonly IMapper _mapper;

    public TaskService(ITaskRepository repository, IMapper mapper)
    {
        _repository = repository;
        _mapper = mapper;
    }

    public async Task<IEnumerable<TaskResponseDto>> GetTasksAsync(bool? isComplete = null, string? priority = null)
    {
        var tasks = await _repository.GetAllAsync(isComplete, priority);
        return _mapper.Map<IEnumerable<TaskResponseDto>>(tasks);
    }

    public async Task<TaskResponseDto?> GetTaskByIdAsync(int id)
    {
        var task = await _repository.GetByIdAsync(id);
        if (task == null)
            return null;

        return _mapper.Map<TaskResponseDto>(task);
    }

    public async Task<TaskResponseDto> CreateTaskAsync(CreateTaskDto dto)
    {
        var validPriorities = new[] { "Low", "Medium", "High", "Critical" };
        if (!validPriorities.Contains(dto.Priority))
            throw new ArgumentException($"Invalid priority '{dto.Priority}'. Must be one of: {string.Join(", ", validPriorities)}");

        var task = _mapper.Map<TaskItem>(dto);
        task.CreatedAt = DateTime.UtcNow;

        var created = await _repository.CreateAsync(task);
        return _mapper.Map<TaskResponseDto>(created);
    }

    public async Task<TaskResponseDto?> UpdateTaskAsync(int id, UpdateTaskDto dto)
    {
        var task = await _repository.GetByIdAsync(id);
        if (task == null)
            return null;

        if (dto.Priority != null)
        {
            var validPriorities = new[] { "Low", "Medium", "High", "Critical" };
            if (!validPriorities.Contains(dto.Priority))
                throw new ArgumentException($"Invalid priority '{dto.Priority}'. Must be one of: {string.Join(", ", validPriorities)}");
        }

        if (dto.Title != null) task.Title = dto.Title;
        if (dto.Description != null) task.Description = dto.Description;
        if (dto.IsComplete.HasValue) task.IsComplete = dto.IsComplete.Value;
        if (dto.Priority != null) task.Priority = dto.Priority;
        if (dto.DueDate.HasValue) task.DueDate = dto.DueDate;
        if (dto.CategoryId.HasValue) task.CategoryId = dto.CategoryId;

        var updated = await _repository.UpdateAsync(task);
        return _mapper.Map<TaskResponseDto>(updated);
    }

    public async Task<bool> DeleteTaskAsync(int id)
    {
        if (!await _repository.ExistsAsync(id))
            return false;

        await _repository.DeleteAsync(id);
        return true;
    }
}
