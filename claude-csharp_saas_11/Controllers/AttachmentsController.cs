using System.Security.Claims;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using TeamTrackr.Auth;
using TeamTrackr.Services;

namespace TeamTrackr.Controllers;

[ApiController]
[Route("api")]
[Authorize]
public class AttachmentsController : ControllerBase
{
    private readonly IFileStorageService _fileStorageService;
    private readonly ITenantProvider _tenantProvider;

    public AttachmentsController(IFileStorageService fileStorageService, ITenantProvider tenantProvider)
    {
        _fileStorageService = fileStorageService;
        _tenantProvider = tenantProvider;
    }

    private string GetUserId() =>
        User.FindFirstValue(ClaimTypes.NameIdentifier)
        ?? User.FindFirstValue("sub")
        ?? throw new UnauthorizedAccessException();

    /// <summary>
    /// Upload a file attachment to a task.
    /// </summary>
    [HttpPost("tasks/{taskId}/attachments")]
    public async Task<IActionResult> Upload(int taskId, IFormFile file)
    {
        var tenantId = _tenantProvider.GetCurrentTenantId();
        if (tenantId == 0) return Unauthorized();

        if (file == null || file.Length == 0)
            return BadRequest(new { error = "No file provided." });

        try
        {
            using var stream = file.OpenReadStream();
            var attachment = await _fileStorageService.UploadAsync(
                tenantId, taskId, file.FileName, file.ContentType, stream, GetUserId());

            return CreatedAtAction(nameof(Download), new { id = attachment.Id }, new
            {
                attachment.Id,
                attachment.FileName,
                attachment.ContentType,
                attachment.FileSizeBytes,
                attachment.TaskItemId,
                attachment.UploadedByUserId,
                attachment.UploadedAt
            });
        }
        catch (InvalidOperationException ex)
        {
            return BadRequest(new { error = ex.Message });
        }
    }

    /// <summary>
    /// Download a file attachment.
    /// </summary>
    [HttpGet("attachments/{id}/download")]
    public async Task<IActionResult> Download(int id)
    {
        var result = await _fileStorageService.DownloadAsync(id);
        if (result == null) return NotFound();

        var (stream, contentType, fileName) = result.Value;
        return File(stream, contentType, fileName);
    }

    /// <summary>
    /// Delete a file attachment.
    /// </summary>
    [HttpDelete("attachments/{id}")]
    public async Task<IActionResult> Delete(int id)
    {
        var deleted = await _fileStorageService.DeleteAsync(id);
        if (!deleted) return NotFound();
        return NoContent();
    }

    /// <summary>
    /// Get storage usage for the current tenant.
    /// </summary>
    [HttpGet("attachments/usage")]
    public async Task<IActionResult> GetUsage()
    {
        var tenantId = _tenantProvider.GetCurrentTenantId();
        if (tenantId == 0) return Unauthorized();

        var usageBytes = await _fileStorageService.GetStorageUsageAsync(tenantId);
        return Ok(new
        {
            UsedBytes = usageBytes,
            UsedMB = Math.Round(usageBytes / (1024.0 * 1024.0), 2)
        });
    }
}
