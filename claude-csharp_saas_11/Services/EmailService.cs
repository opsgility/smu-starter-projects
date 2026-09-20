namespace TeamTrackr.Services;

public class EmailService : IEmailService
{
    private readonly ILogger<EmailService> _logger;

    public EmailService(ILogger<EmailService> logger)
    {
        _logger = logger;
    }

    public Task SendTaskAssignedEmail(string assigneeEmail, string taskTitle, string projectName)
    {
        _logger.LogInformation(
            "[Email] Task assigned notification sent to {Email}: '{Task}' in project '{Project}'",
            assigneeEmail, taskTitle, projectName);
        return Task.CompletedTask;
    }

    public Task SendTaskDueReminderEmail(string assigneeEmail, string taskTitle, DateTime dueDate)
    {
        _logger.LogInformation(
            "[Email] Due reminder sent to {Email}: '{Task}' due on {DueDate}",
            assigneeEmail, taskTitle, dueDate.ToString("yyyy-MM-dd"));
        return Task.CompletedTask;
    }

    public Task SendDailyDigestEmail(string userEmail, List<string> overdueTasks, List<string> dueTodayTasks)
    {
        _logger.LogInformation(
            "[Email] Daily digest sent to {Email}: {OverdueCount} overdue, {DueTodayCount} due today",
            userEmail, overdueTasks.Count, dueTodayTasks.Count);
        return Task.CompletedTask;
    }
}
