using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using TeamTrackr.Data;

namespace TeamTrackr.Controllers;

[ApiController]
[Route("api/[controller]")]
public class HealthController : ControllerBase
{
    private readonly AppDbContext _db;

    public HealthController(AppDbContext db)
    {
        _db = db;
    }

    [HttpGet]
    public async Task<ActionResult<HealthResponse>> GetHealth()
    {
        var response = new HealthResponse();

        // Check database
        try
        {
            await _db.Database.ExecuteSqlRawAsync("SELECT 1");
            response.Database = new ComponentHealth { Status = "healthy" };
        }
        catch (Exception ex)
        {
            response.Database = new ComponentHealth { Status = "unhealthy", Error = ex.Message };
            response.Status = "degraded";
        }

        // Check file storage (basic disk check)
        try
        {
            var tempFile = Path.GetTempFileName();
            await System.IO.File.WriteAllTextAsync(tempFile, "health-check");
            System.IO.File.Delete(tempFile);
            response.FileStorage = new ComponentHealth { Status = "healthy" };
        }
        catch (Exception ex)
        {
            response.FileStorage = new ComponentHealth { Status = "unhealthy", Error = ex.Message };
            response.Status = "degraded";
        }

        // Background services check (basic — reports healthy if app is running)
        response.BackgroundServices = new ComponentHealth { Status = "healthy" };

        return Ok(response);
    }
}

public class HealthResponse
{
    public string Status { get; set; } = "healthy";
    public ComponentHealth Database { get; set; } = new();
    public ComponentHealth FileStorage { get; set; } = new();
    public ComponentHealth BackgroundServices { get; set; } = new();
    public DateTime Timestamp { get; set; } = DateTime.UtcNow;
}

public class ComponentHealth
{
    public string Status { get; set; } = "healthy";
    public string? Error { get; set; }
}
