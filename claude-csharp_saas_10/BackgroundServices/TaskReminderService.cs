using Microsoft.EntityFrameworkCore;
using TeamTrackr.Auth;
using TeamTrackr.Data;
using TeamTrackr.Services;

namespace TeamTrackr.BackgroundServices;

public class TaskReminderService : BackgroundService
{
    private readonly IServiceProvider _serviceProvider;
    private readonly ILogger<TaskReminderService> _logger;
    private static readonly TimeSpan Interval = TimeSpan.FromHours(1);

    public TaskReminderService(IServiceProvider serviceProvider, ILogger<TaskReminderService> logger)
    {
        _serviceProvider = serviceProvider;
        _logger = logger;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        _logger.LogInformation("TaskReminderService started. Running every {Interval}.", Interval);

        while (!stoppingToken.IsCancellationRequested)
        {
            try
            {
                await CheckDueTasksAsync();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error occurred while checking due tasks.");
            }

            await Task.Delay(Interval, stoppingToken);
        }
    }

    private async Task CheckDueTasksAsync()
    {
        using var scope = _serviceProvider.CreateScope();
        var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
        var emailService = scope.ServiceProvider.GetRequiredService<IEmailService>();

        var now = DateTime.UtcNow;
        var in24Hours = now.AddHours(24);

        // Query tasks due within 24 hours that haven't been reminded yet
        // Using IgnoreQueryFilters to check across all tenants
        var dueTasks = await db.TaskItems
            .IgnoreQueryFilters()
            .Include(t => t.Assignee)
            .Where(t => t.DueDate.HasValue
                && t.DueDate.Value > now
                && t.DueDate.Value <= in24Hours
                && !t.ReminderSent
                && t.AssigneeId != null)
            .ToListAsync();

        _logger.LogInformation("Found {Count} tasks due within 24 hours.", dueTasks.Count);

        foreach (var task in dueTasks)
        {
            if (task.Assignee?.Email != null)
            {
                await emailService.SendTaskDueReminderEmail(
                    task.Assignee.Email,
                    task.Title,
                    task.DueDate!.Value);

                task.ReminderSent = true;
            }
        }

        if (dueTasks.Count > 0)
        {
            await db.SaveChangesAsync();
        }
    }
}
