using System.Security.Claims;
using System.Text.Json;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using TeamTrackr.Auth;
using TeamTrackr.Data;
using TeamTrackr.DTOs;
using TeamTrackr.Models;
using TeamTrackr.Services;

namespace TeamTrackr.Controllers;

[ApiController]
[Route("api/[controller]")]
[Authorize]
public class SearchController : ControllerBase
{
    private readonly ISearchService _searchService;
    private readonly AppDbContext _db;
    private readonly ITenantProvider _tenantProvider;

    public SearchController(ISearchService searchService, AppDbContext db, ITenantProvider tenantProvider)
    {
        _searchService = searchService;
        _db = db;
        _tenantProvider = tenantProvider;
    }

    private string GetUserId() =>
        User.FindFirstValue(ClaimTypes.NameIdentifier)
        ?? User.FindFirstValue("sub")
        ?? throw new UnauthorizedAccessException();

    [HttpPost("tasks")]
    public async Task<ActionResult<SearchResponse<TaskResponse>>> SearchTasks(SearchRequest request)
    {
        var results = await _searchService.SearchTasksAsync(request);
        return Ok(results);
    }

    [HttpPost("global")]
    public async Task<ActionResult<SearchResponse<GlobalSearchResult>>> GlobalSearch([FromBody] SearchRequest request)
    {
        var results = await _searchService.GlobalSearchAsync(request.Query, request.Page, request.PageSize);
        return Ok(results);
    }

    [HttpGet("saved")]
    public async Task<ActionResult<List<SavedFilter>>> GetSavedFilters()
    {
        var userId = GetUserId();
        var filters = await _db.SavedFilters
            .Where(f => f.UserId == userId)
            .OrderByDescending(f => f.CreatedAt)
            .ToListAsync();
        return Ok(filters);
    }

    [HttpPost("saved")]
    public async Task<ActionResult<SavedFilter>> SaveFilter([FromBody] SaveFilterRequest request)
    {
        var filter = new SavedFilter
        {
            TenantId = _tenantProvider.GetCurrentTenantId(),
            UserId = GetUserId(),
            Name = request.Name,
            FilterJson = JsonSerializer.Serialize(request.Filter)
        };

        _db.SavedFilters.Add(filter);
        await _db.SaveChangesAsync();
        return CreatedAtAction(nameof(GetSavedFilters), filter);
    }

    [HttpDelete("saved/{id}")]
    public async Task<IActionResult> DeleteSavedFilter(int id)
    {
        var userId = GetUserId();
        var filter = await _db.SavedFilters
            .FirstOrDefaultAsync(f => f.Id == id && f.UserId == userId);

        if (filter == null) return NotFound();

        _db.SavedFilters.Remove(filter);
        await _db.SaveChangesAsync();
        return NoContent();
    }
}

public class SaveFilterRequest
{
    public string Name { get; set; } = string.Empty;
    public SearchRequest Filter { get; set; } = new();
}
