using System.Security.Cryptography;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using TeamTrackr.Auth;
using TeamTrackr.Data;
using TeamTrackr.Models;

namespace TeamTrackr.Controllers;

[ApiController]
[Route("api/[controller]")]
[Authorize]
public class ApiKeysController : ControllerBase
{
    private readonly AppDbContext _db;
    private readonly ITenantProvider _tenantProvider;

    public ApiKeysController(AppDbContext db, ITenantProvider tenantProvider)
    {
        _db = db;
        _tenantProvider = tenantProvider;
    }

    [HttpGet]
    public async Task<ActionResult<List<ApiKeyResponse>>> GetAll()
    {
        var tenantId = _tenantProvider.GetCurrentTenantId();
        var keys = await _db.ApiKeys
            .Where(k => k.TenantId == tenantId)
            .OrderByDescending(k => k.CreatedAt)
            .Select(k => new ApiKeyResponse
            {
                Id = k.Id,
                Name = k.Name,
                KeyPrefix = k.Key.Substring(0, 8) + "...",
                CreatedAt = k.CreatedAt,
                LastUsedAt = k.LastUsedAt,
                IsActive = k.IsActive
            })
            .ToListAsync();

        return Ok(keys);
    }

    [HttpPost]
    public async Task<ActionResult<ApiKeyCreatedResponse>> Create([FromBody] CreateApiKeyRequest request)
    {
        var tenantId = _tenantProvider.GetCurrentTenantId();

        var keyBytes = new byte[32];
        using var rng = RandomNumberGenerator.Create();
        rng.GetBytes(keyBytes);
        var keyValue = Convert.ToBase64String(keyBytes).Replace("+", "").Replace("/", "").Replace("=", "");

        var apiKey = new ApiKey
        {
            TenantId = tenantId,
            Key = keyValue,
            Name = request.Name
        };

        _db.ApiKeys.Add(apiKey);
        await _db.SaveChangesAsync();

        return CreatedAtAction(nameof(GetAll), new ApiKeyCreatedResponse
        {
            Id = apiKey.Id,
            Name = apiKey.Name,
            Key = keyValue,
            CreatedAt = apiKey.CreatedAt
        });
    }

    [HttpDelete("{id}")]
    public async Task<IActionResult> Revoke(int id)
    {
        var tenantId = _tenantProvider.GetCurrentTenantId();
        var apiKey = await _db.ApiKeys
            .FirstOrDefaultAsync(k => k.Id == id && k.TenantId == tenantId);

        if (apiKey == null) return NotFound();

        apiKey.IsActive = false;
        await _db.SaveChangesAsync();
        return NoContent();
    }
}

public class CreateApiKeyRequest
{
    public string Name { get; set; } = string.Empty;
}

public class ApiKeyResponse
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public string KeyPrefix { get; set; } = string.Empty;
    public DateTime CreatedAt { get; set; }
    public DateTime? LastUsedAt { get; set; }
    public bool IsActive { get; set; }
}

public class ApiKeyCreatedResponse
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public string Key { get; set; } = string.Empty;
    public DateTime CreatedAt { get; set; }
}
