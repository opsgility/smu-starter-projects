using System.Security.Claims;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using TeamTrackr.DTOs;
using TeamTrackr.Services;

namespace TeamTrackr.Controllers;

[ApiController]
[Route("api/tasks/{taskId}/comments")]
[Authorize]
public class CommentsController : ControllerBase
{
    private readonly ICommentService _commentService;
    private readonly INotificationService _notificationService;

    public CommentsController(ICommentService commentService, INotificationService notificationService)
    {
        _commentService = commentService;
        _notificationService = notificationService;
    }

    private string GetUserId() =>
        User.FindFirstValue(ClaimTypes.NameIdentifier)
        ?? User.FindFirstValue("sub")
        ?? throw new UnauthorizedAccessException();

    [HttpGet]
    public async Task<ActionResult<List<CommentResponse>>> GetAll(int taskId)
    {
        var comments = await _commentService.GetByTaskIdAsync(taskId);
        return Ok(comments);
    }

    [HttpGet("{id}")]
    public async Task<ActionResult<CommentResponse>> GetById(int taskId, int id)
    {
        var comment = await _commentService.GetByIdAsync(id);
        if (comment == null || comment.TaskItemId != taskId) return NotFound();
        return Ok(comment);
    }

    [HttpPost]
    public async Task<ActionResult<CommentResponse>> Create(int taskId, CreateCommentRequest request)
    {
        var comment = await _commentService.CreateAsync(taskId, request, GetUserId());
        await _notificationService.SendCommentAdded(comment);
        return CreatedAtAction(nameof(GetById), new { taskId, id = comment.Id }, comment);
    }

    [HttpDelete("{id}")]
    public async Task<IActionResult> Delete(int taskId, int id)
    {
        var comment = await _commentService.GetByIdAsync(id);
        if (comment == null || comment.TaskItemId != taskId) return NotFound();

        await _commentService.DeleteAsync(id);
        return NoContent();
    }
}
