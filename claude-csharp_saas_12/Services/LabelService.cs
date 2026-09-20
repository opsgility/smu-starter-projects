using Microsoft.EntityFrameworkCore;
using TeamTrackr.Auth;
using TeamTrackr.Data;
using TeamTrackr.DTOs;
using TeamTrackr.Models;

namespace TeamTrackr.Services;

public class LabelService : ILabelService
{
    private readonly AppDbContext _db;
    private readonly ITenantProvider _tenantProvider;

    public LabelService(AppDbContext db, ITenantProvider tenantProvider)
    {
        _db = db;
        _tenantProvider = tenantProvider;
    }

    public async Task<List<LabelResponse>> GetAllAsync()
    {
        return await _db.TaskLabels
            .Select(l => new LabelResponse
            {
                Id = l.Id,
                Name = l.Name,
                Color = l.Color
            })
            .ToListAsync();
    }

    public async Task<LabelResponse?> GetByIdAsync(int id)
    {
        return await _db.TaskLabels
            .Where(l => l.Id == id)
            .Select(l => new LabelResponse
            {
                Id = l.Id,
                Name = l.Name,
                Color = l.Color
            })
            .FirstOrDefaultAsync();
    }

    public async Task<LabelResponse> CreateAsync(CreateLabelRequest request)
    {
        var tenantId = _tenantProvider.GetCurrentTenantId();

        var label = new TaskLabel
        {
            TenantId = tenantId,
            Name = request.Name,
            Color = request.Color
        };

        _db.TaskLabels.Add(label);
        await _db.SaveChangesAsync();

        return new LabelResponse
        {
            Id = label.Id,
            Name = label.Name,
            Color = label.Color
        };
    }

    public async Task<bool> DeleteAsync(int id)
    {
        var label = await _db.TaskLabels.FindAsync(id);
        if (label == null) return false;

        _db.TaskLabels.Remove(label);
        await _db.SaveChangesAsync();
        return true;
    }

    public async Task<bool> AssignToTaskAsync(int taskItemId, int labelId)
    {
        var exists = await _db.TaskItemLabels
            .AnyAsync(til => til.TaskItemId == taskItemId && til.TaskLabelId == labelId);

        if (exists) return true;

        _db.TaskItemLabels.Add(new TaskItemLabel
        {
            TaskItemId = taskItemId,
            TaskLabelId = labelId
        });

        await _db.SaveChangesAsync();
        return true;
    }

    public async Task<bool> RemoveFromTaskAsync(int taskItemId, int labelId)
    {
        var link = await _db.TaskItemLabels
            .FirstOrDefaultAsync(til => til.TaskItemId == taskItemId && til.TaskLabelId == labelId);

        if (link == null) return false;

        _db.TaskItemLabels.Remove(link);
        await _db.SaveChangesAsync();
        return true;
    }
}
