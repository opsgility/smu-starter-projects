using Microsoft.EntityFrameworkCore;
using TeamTrackr.Auth;
using TeamTrackr.Data;
using TeamTrackr.Models;
using TeamTrackr.Services;

namespace TeamTrackr.BackgroundServices;

public class DailyDigestService : BackgroundService
{
    private readonly IServiceProvider _serviceProvider;
    private readonly ILogger<DailyDigestService> _logger;

    public DailyDigestService(IServiceProvider serviceProvider, ILogger<DailyDigestService> logger)
    {
        _serviceProvider = serviceProvider;
        _logger = logger;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        _logger.LogInformation("DailyDigestService started. Runs daily at 8:00 AM UTC.");

        while (!stoppingToken.IsCancellationRequested)
        {
            var delay = GetDelayUntilNext8AmUtc();
            _logger.LogInformation("Next daily digest will run in {Delay}.", delay);

            await Task.Delay(delay, stoppingToken);

            try
            {
                await SendDailyDigestsAsync();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error occurred while sending daily digests.");
            }
        }
    }

    private static TimeSpan GetDelayUntilNext8AmUtc()
    {
        var now = DateTime.UtcNow;
        var next8Am = now.Date.AddHours(8);

        if (now >= next8Am)
        {
            next8Am = next8Am.AddDays(1);
        }

        return next8Am - now;
    }

    private async Task SendDailyDigestsAsync()
    {
        using var scope = _serviceProvider.CreateScope();
        var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
        var emailService = scope.ServiceProvider.GetRequiredService<IEmailService>();

        var today = DateTime.UtcNow.Date;
        var tomorrow = today.AddDays(1);

        // Get all tasks with assignees, ignoring tenant filters for background processing
        var tasks = await db.TaskItems
            .IgnoreQueryFilters()
            .Include(t => t.Assignee)
            .Where(t => t.AssigneeId != null
                && t.Status != TaskItemStatus.Done
                && t.DueDate.HasValue)
            .ToListAsync();

        // Group by assignee
        var tasksByUser = tasks
            .GroupBy(t => t.AssigneeId!)
            .ToList();

        foreach (var group in tasksByUser)
        {
            var user = group.First().Assignee;
            if (user?.Email == null) continue;

            var overdueTasks = group
                .Where(t => t.DueDate!.Value.Date < today)
                .Select(t => t.Title)
                .ToList();

            var dueTodayTasks = group
                .Where(t => t.DueDate!.Value.Date == today)
                .Select(t => t.Title)
                .ToList();

            if (overdueTasks.Count > 0 || dueTodayTasks.Count > 0)
            {
                await emailService.SendDailyDigestEmail(user.Email, overdueTasks, dueTodayTasks);
            }
        }

        _logger.LogInformation("Daily digest processing complete.");
    }
}
