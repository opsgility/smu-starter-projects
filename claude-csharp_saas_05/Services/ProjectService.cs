using Microsoft.EntityFrameworkCore;
using TeamTrackr.Auth;
using TeamTrackr.Data;
using TeamTrackr.DTOs;
using TeamTrackr.Models;

namespace TeamTrackr.Services;

public class ProjectService : IProjectService
{
    private readonly AppDbContext _db;
    private readonly ITenantProvider _tenantProvider;

    public ProjectService(AppDbContext db, ITenantProvider tenantProvider)
    {
        _db = db;
        _tenantProvider = tenantProvider;
    }

    public async Task<List<ProjectResponse>> GetAllAsync()
    {
        return await _db.Projects
            .Select(p => new ProjectResponse
            {
                Id = p.Id,
                Name = p.Name,
                Description = p.Description,
                Key = p.Key,
                CreatedAt = p.CreatedAt,
                CreatedByUserId = p.CreatedByUserId,
                IsArchived = p.IsArchived
            })
            .ToListAsync();
    }

    public async Task<ProjectResponse?> GetByIdAsync(int id)
    {
        return await _db.Projects
            .Where(p => p.Id == id)
            .Select(p => new ProjectResponse
            {
                Id = p.Id,
                Name = p.Name,
                Description = p.Description,
                Key = p.Key,
                CreatedAt = p.CreatedAt,
                CreatedByUserId = p.CreatedByUserId,
                IsArchived = p.IsArchived
            })
            .FirstOrDefaultAsync();
    }

    public async Task<ProjectResponse> CreateAsync(CreateProjectRequest request, string userId)
    {
        var tenantId = _tenantProvider.GetCurrentTenantId();

        var project = new Project
        {
            TenantId = tenantId,
            Name = request.Name,
            Description = request.Description,
            Key = request.Key.ToUpperInvariant(),
            CreatedByUserId = userId
        };

        _db.Projects.Add(project);
        await _db.SaveChangesAsync();

        return new ProjectResponse
        {
            Id = project.Id,
            Name = project.Name,
            Description = project.Description,
            Key = project.Key,
            CreatedAt = project.CreatedAt,
            CreatedByUserId = project.CreatedByUserId,
            IsArchived = project.IsArchived
        };
    }

    public async Task<ProjectResponse?> UpdateAsync(int id, UpdateProjectRequest request)
    {
        var project = await _db.Projects.FindAsync(id);
        if (project == null) return null;

        if (request.Name != null) project.Name = request.Name;
        if (request.Description != null) project.Description = request.Description;
        if (request.IsArchived.HasValue) project.IsArchived = request.IsArchived.Value;

        await _db.SaveChangesAsync();

        return new ProjectResponse
        {
            Id = project.Id,
            Name = project.Name,
            Description = project.Description,
            Key = project.Key,
            CreatedAt = project.CreatedAt,
            CreatedByUserId = project.CreatedByUserId,
            IsArchived = project.IsArchived
        };
    }

    public async Task<bool> DeleteAsync(int id)
    {
        var project = await _db.Projects.FindAsync(id);
        if (project == null) return false;

        _db.Projects.Remove(project);
        await _db.SaveChangesAsync();
        return true;
    }

    public async Task<List<TaskResponse>> GetTasksByProjectAsync(int projectId)
    {
        return await _db.TaskItems
            .Include(t => t.Project)
            .Include(t => t.Assignee)
            .Include(t => t.TaskItemLabels)
                .ThenInclude(til => til.TaskLabel)
            .Where(t => t.ProjectId == projectId)
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
            .ToListAsync();
    }
}
