using Microsoft.EntityFrameworkCore;
using TeamTrackr.Auth;
using TeamTrackr.Data;
using TeamTrackr.DTOs;
using TeamTrackr.Models;

namespace TeamTrackr.Services;

public class TaskService : ITaskService
{
    private readonly AppDbContext _db;
    private readonly ITenantProvider _tenantProvider;

    public TaskService(AppDbContext db, ITenantProvider tenantProvider)
    {
        _db = db;
        _tenantProvider = tenantProvider;
    }

    public async Task<List<TaskResponse>> GetAllAsync(
        TaskItemStatus? status = null,
        TaskPriority? priority = null,
        string? assigneeId = null,
        int? projectId = null)
    {
        var query = _db.TaskItems
            .Include(t => t.Project)
            .Include(t => t.Assignee)
            .Include(t => t.TaskItemLabels)
                .ThenInclude(til => til.TaskLabel)
            .AsQueryable();

        if (status.HasValue)
            query = query.Where(t => t.Status == status.Value);
        if (priority.HasValue)
            query = query.Where(t => t.Priority == priority.Value);
        if (assigneeId != null)
            query = query.Where(t => t.AssigneeId == assigneeId);
        if (projectId.HasValue)
            query = query.Where(t => t.ProjectId == projectId.Value);

        return await query.Select(t => new TaskResponse
        {
            Id = t.Id,
            ProjectId = t.ProjectId,
            ProjectName = t.Project.Name,
            Title = t.Title,
            Description = t.Description,
            Status = t.Status,
            Priority = t.Priority,
            AssigneeId = t.AssigneeId,
            AssigneeName = t.Assignee != null ? t.Assignee.DisplayName : null,
            CreatedByUserId = t.CreatedByUserId,
            CreatedAt = t.CreatedAt,
            UpdatedAt = t.UpdatedAt,
            DueDate = t.DueDate,
            Labels = t.TaskItemLabels.Select(til => new LabelResponse
            {
                Id = til.TaskLabel.Id,
                Name = til.TaskLabel.Name,
                Color = til.TaskLabel.Color
            }).ToList()
        }).ToListAsync();
    }

    public async Task<TaskResponse?> GetByIdAsync(int id)
    {
        return await _db.TaskItems
            .Include(t => t.Project)
            .Include(t => t.Assignee)
            .Include(t => t.TaskItemLabels)
                .ThenInclude(til => til.TaskLabel)
            .Where(t => t.Id == id)
            .Select(t => new TaskResponse
            {
                Id = t.Id,
                ProjectId = t.ProjectId,
                ProjectName = t.Project.Name,
                Title = t.Title,
                Description = t.Description,
                Status = t.Status,
                Priority = t.Priority,
                AssigneeId = t.AssigneeId,
                AssigneeName = t.Assignee != null ? t.Assignee.DisplayName : null,
                CreatedByUserId = t.CreatedByUserId,
                CreatedAt = t.CreatedAt,
                UpdatedAt = t.UpdatedAt,
                DueDate = t.DueDate,
                Labels = t.TaskItemLabels.Select(til => new LabelResponse
                {
                    Id = til.TaskLabel.Id,
                    Name = til.TaskLabel.Name,
                    Color = til.TaskLabel.Color
                }).ToList()
            })
            .FirstOrDefaultAsync();
    }

    public async Task<TaskResponse> CreateAsync(CreateTaskRequest request, string userId)
    {
        var tenantId = _tenantProvider.GetCurrentTenantId();

        var task = new TaskItem
        {
            TenantId = tenantId,
            ProjectId = request.ProjectId,
            Title = request.Title,
            Description = request.Description,
            Status = request.Status,
            Priority = request.Priority,
            AssigneeId = request.AssigneeId,
            CreatedByUserId = userId,
            DueDate = request.DueDate
        };

        _db.TaskItems.Add(task);
        await _db.SaveChangesAsync();

        // Email notification will be implemented in the Background Jobs lab

        // Reload with navigation properties
        return (await GetByIdAsync(task.Id))!;
    }

    public async Task<TaskResponse?> UpdateAsync(int id, UpdateTaskRequest request)
    {
        var task = await _db.TaskItems.FindAsync(id);
        if (task == null) return null;

        var previousAssigneeId = task.AssigneeId;

        if (request.Title != null) task.Title = request.Title;
        if (request.Description != null) task.Description = request.Description;
        if (request.Status.HasValue) task.Status = request.Status.Value;
        if (request.Priority.HasValue) task.Priority = request.Priority.Value;
        if (request.AssigneeId != null) task.AssigneeId = request.AssigneeId;
        if (request.DueDate.HasValue) task.DueDate = request.DueDate.Value;

        task.UpdatedAt = DateTime.UtcNow;

        await _db.SaveChangesAsync();

        // Email notification will be implemented in the Background Jobs lab

        return await GetByIdAsync(id);
    }

    public async Task<bool> DeleteAsync(int id)
    {
        var task = await _db.TaskItems.FindAsync(id);
        if (task == null) return false;

        _db.TaskItems.Remove(task);
        await _db.SaveChangesAsync();
        return true;
    }
}
