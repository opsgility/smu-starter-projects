using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using TeamTrackr.DTOs;
using TeamTrackr.Services;

namespace TeamTrackr.Controllers;

[ApiController]
[Route("api/[controller]")]
[Authorize]
public class LabelsController : ControllerBase
{
    private readonly ILabelService _labelService;

    public LabelsController(ILabelService labelService)
    {
        _labelService = labelService;
    }

    [HttpGet]
    public async Task<ActionResult<List<LabelResponse>>> GetAll()
    {
        var labels = await _labelService.GetAllAsync();
        return Ok(labels);
    }

    [HttpGet("{id}")]
    public async Task<ActionResult<LabelResponse>> GetById(int id)
    {
        var label = await _labelService.GetByIdAsync(id);
        if (label == null) return NotFound();
        return Ok(label);
    }

    [HttpPost]
    public async Task<ActionResult<LabelResponse>> Create(CreateLabelRequest request)
    {
        var label = await _labelService.CreateAsync(request);
        return CreatedAtAction(nameof(GetById), new { id = label.Id }, label);
    }

    [HttpDelete("{id}")]
    public async Task<IActionResult> Delete(int id)
    {
        var deleted = await _labelService.DeleteAsync(id);
        if (!deleted) return NotFound();
        return NoContent();
    }

    [HttpPost("/api/tasks/{taskId}/labels/{labelId}")]
    public async Task<IActionResult> AssignToTask(int taskId, int labelId)
    {
        var result = await _labelService.AssignToTaskAsync(taskId, labelId);
        if (!result) return NotFound();
        return Ok();
    }

    [HttpDelete("/api/tasks/{taskId}/labels/{labelId}")]
    public async Task<IActionResult> RemoveFromTask(int taskId, int labelId)
    {
        var result = await _labelService.RemoveFromTaskAsync(taskId, labelId);
        if (!result) return NotFound();
        return NoContent();
    }
}
