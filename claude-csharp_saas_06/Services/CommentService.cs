using Microsoft.EntityFrameworkCore;
using TeamTrackr.Auth;
using TeamTrackr.Data;
using TeamTrackr.DTOs;
using TeamTrackr.Models;

namespace TeamTrackr.Services;

public class CommentService : ICommentService
{
    private readonly AppDbContext _db;
    private readonly ITenantProvider _tenantProvider;

    public CommentService(AppDbContext db, ITenantProvider tenantProvider)
    {
        _db = db;
        _tenantProvider = tenantProvider;
    }

    public async Task<List<CommentResponse>> GetByTaskIdAsync(int taskItemId)
    {
        return await _db.Comments
            .Include(c => c.Author)
            .Where(c => c.TaskItemId == taskItemId)
            .OrderByDescending(c => c.CreatedAt)
            .Select(c => new CommentResponse
            {
                Id = c.Id,
                TaskItemId = c.TaskItemId,
                AuthorId = c.AuthorId,
                AuthorName = c.Author.DisplayName,
                Content = c.Content,
                CreatedAt = c.CreatedAt
            })
            .ToListAsync();
    }

    public async Task<CommentResponse?> GetByIdAsync(int id)
    {
        return await _db.Comments
            .Include(c => c.Author)
            .Where(c => c.Id == id)
            .Select(c => new CommentResponse
            {
                Id = c.Id,
                TaskItemId = c.TaskItemId,
                AuthorId = c.AuthorId,
                AuthorName = c.Author.DisplayName,
                Content = c.Content,
                CreatedAt = c.CreatedAt
            })
            .FirstOrDefaultAsync();
    }

    public async Task<CommentResponse> CreateAsync(int taskItemId, CreateCommentRequest request, string authorId)
    {
        var tenantId = _tenantProvider.GetCurrentTenantId();

        var comment = new Comment
        {
            TenantId = tenantId,
            TaskItemId = taskItemId,
            AuthorId = authorId,
            Content = request.Content
        };

        _db.Comments.Add(comment);
        await _db.SaveChangesAsync();

        return (await GetByIdAsync(comment.Id))!;
    }

    public async Task<bool> DeleteAsync(int id)
    {
        var comment = await _db.Comments.FindAsync(id);
        if (comment == null) return false;

        _db.Comments.Remove(comment);
        await _db.SaveChangesAsync();
        return true;
    }
}
