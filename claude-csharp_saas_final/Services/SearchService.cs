using Microsoft.EntityFrameworkCore;
using TeamTrackr.Data;
using TeamTrackr.DTOs;
using TeamTrackr.Models;

namespace TeamTrackr.Services;

public class SearchService : ISearchService
{
    private readonly AppDbContext _db;

    public SearchService(AppDbContext db)
    {
        _db = db;
    }

    public async Task<SearchResponse<TaskResponse>> SearchTasksAsync(SearchRequest request)
    {
        var query = _db.TaskItems
            .Include(t => t.Project)
            .Include(t => t.Assignee)
            .Include(t => t.TaskItemLabels)
                .ThenInclude(til => til.TaskLabel)
            .AsQueryable();

        // Full-text search across title and description
        if (!string.IsNullOrWhiteSpace(request.Query))
        {
            var searchTerm = request.Query.ToLower();
            query = query.Where(t =>
                t.Title.ToLower().Contains(searchTerm) ||
                t.Description.ToLower().Contains(searchTerm));
        }

        // Apply filters
        if (request.Status.HasValue)
            query = query.Where(t => t.Status == request.Status.Value);

        if (request.Priority.HasValue)
            query = query.Where(t => t.Priority == request.Priority.Value);

        if (!string.IsNullOrEmpty(request.AssigneeId))
            query = query.Where(t => t.AssigneeId == request.AssigneeId);

        if (request.ProjectId.HasValue)
            query = query.Where(t => t.ProjectId == request.ProjectId.Value);

        if (request.LabelId.HasValue)
            query = query.Where(t => t.TaskItemLabels.Any(til => til.TaskLabelId == request.LabelId.Value));

        if (request.DueBefore.HasValue)
            query = query.Where(t => t.DueDate != null && t.DueDate <= request.DueBefore.Value);

        if (request.DueAfter.HasValue)
            query = query.Where(t => t.DueDate != null && t.DueDate >= request.DueAfter.Value);

        var totalCount = await query.CountAsync();

        var items = await query
            .OrderByDescending(t => t.UpdatedAt)
            .Skip((request.Page - 1) * request.PageSize)
            .Take(request.PageSize)
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

        return new SearchResponse<TaskResponse>
        {
            Items = items,
            TotalCount = totalCount,
            Page = request.Page,
            PageSize = request.PageSize,
            HasMore = (request.Page * request.PageSize) < totalCount
        };
    }

    public async Task<SearchResponse<ProjectResponse>> SearchProjectsAsync(string query, int page = 1, int pageSize = 20)
    {
        var dbQuery = _db.Projects.AsQueryable();

        if (!string.IsNullOrWhiteSpace(query))
        {
            var searchTerm = query.ToLower();
            dbQuery = dbQuery.Where(p =>
                p.Name.ToLower().Contains(searchTerm) ||
                p.Description.ToLower().Contains(searchTerm));
        }

        var totalCount = await dbQuery.CountAsync();

        var items = await dbQuery
            .OrderByDescending(p => p.CreatedAt)
            .Skip((page - 1) * pageSize)
            .Take(pageSize)
            .Select(p => new ProjectResponse
            {
                Id = p.Id,
                Name = p.Name,
                Description = p.Description,
                Key = p.Key,
                CreatedAt = p.CreatedAt,
                IsArchived = p.IsArchived
            })
            .ToListAsync();

        return new SearchResponse<ProjectResponse>
        {
            Items = items,
            TotalCount = totalCount,
            Page = page,
            PageSize = pageSize,
            HasMore = (page * pageSize) < totalCount
        };
    }

    public async Task<SearchResponse<GlobalSearchResult>> GlobalSearchAsync(string query, int page = 1, int pageSize = 20)
    {
        var results = new List<GlobalSearchResult>();

        if (!string.IsNullOrWhiteSpace(query))
        {
            var searchTerm = query.ToLower();

            var taskResults = await _db.TaskItems
                .Where(t => t.Title.ToLower().Contains(searchTerm) ||
                            t.Description.ToLower().Contains(searchTerm))
                .Select(t => new GlobalSearchResult
                {
                    Type = "task",
                    Id = t.Id,
                    Title = t.Title,
                    Description = t.Description
                })
                .ToListAsync();

            var projectResults = await _db.Projects
                .Where(p => p.Name.ToLower().Contains(searchTerm) ||
                            p.Description.ToLower().Contains(searchTerm))
                .Select(p => new GlobalSearchResult
                {
                    Type = "project",
                    Id = p.Id,
                    Title = p.Name,
                    Description = p.Description
                })
                .ToListAsync();

            results.AddRange(taskResults);
            results.AddRange(projectResults);
        }

        var totalCount = results.Count;
        var pagedResults = results
            .Skip((page - 1) * pageSize)
            .Take(pageSize)
            .ToList();

        return new SearchResponse<GlobalSearchResult>
        {
            Items = pagedResults,
            TotalCount = totalCount,
            Page = page,
            PageSize = pageSize,
            HasMore = (page * pageSize) < totalCount
        };
    }
}
