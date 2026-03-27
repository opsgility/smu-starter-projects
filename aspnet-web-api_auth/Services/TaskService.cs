using AutoMapper;
using FluentValidation;
using TaskFlow.Api.DTOs;
using TaskFlow.Api.Exceptions;
using TaskFlow.Api.Models;
using TaskFlow.Api.Repositories;

namespace TaskFlow.Api.Services;

public class TaskService : ITaskService
{
    private readonly ITaskRepository _repository;
    private readonly IMapper _mapper;
    private readonly IValidator<CreateTaskDto> _createValidator;
    private readonly IValidator<UpdateTaskDto> _updateValidator;

    public TaskService(
        ITaskRepository repository,
        IMapper mapper,
        IValidator<CreateTaskDto> createValidator,
        IValidator<UpdateTaskDto> updateValidator)
    {
        _repository = repository;
        _mapper = mapper;
        _createValidator = createValidator;
        _updateValidator = updateValidator;
    }

    public async Task<IEnumerable<TaskResponseDto>> GetTasksAsync(bool? isComplete = null, string? priority = null)
    {
        var tasks = await _repository.GetAllAsync(isComplete, priority);
        return _mapper.Map<IEnumerable<TaskResponseDto>>(tasks);
    }

    public async Task<TaskResponseDto> GetTaskByIdAsync(int id)
    {
        var task = await _repository.GetByIdAsync(id);
        if (task == null)
            throw new NotFoundException($"Task with ID {id} was not found.");

        return _mapper.Map<TaskResponseDto>(task);
    }

    public async Task<TaskResponseDto> CreateTaskAsync(CreateTaskDto dto)
    {
        var validationResult = await _createValidator.ValidateAsync(dto);
        if (!validationResult.IsValid)
        {
            var errors = validationResult.Errors
                .GroupBy(e => e.PropertyName)
                .ToDictionary(g => g.Key, g => g.Select(e => e.ErrorMessage).ToArray());
            throw new Exceptions.ValidationException(errors);
        }

        var task = _mapper.Map<TaskItem>(dto);
        task.CreatedAt = DateTime.UtcNow;

        var created = await _repository.CreateAsync(task);
        return _mapper.Map<TaskResponseDto>(created);
    }

    public async Task<TaskResponseDto> UpdateTaskAsync(int id, UpdateTaskDto dto)
    {
        var task = await _repository.GetByIdAsync(id);
        if (task == null)
            throw new NotFoundException($"Task with ID {id} was not found.");

        var validationResult = await _updateValidator.ValidateAsync(dto);
        if (!validationResult.IsValid)
        {
            var errors = validationResult.Errors
                .GroupBy(e => e.PropertyName)
                .ToDictionary(g => g.Key, g => g.Select(e => e.ErrorMessage).ToArray());
            throw new Exceptions.ValidationException(errors);
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

    public async Task DeleteTaskAsync(int id)
    {
        if (!await _repository.ExistsAsync(id))
            throw new NotFoundException($"Task with ID {id} was not found.");

        await _repository.DeleteAsync(id);
    }
}
