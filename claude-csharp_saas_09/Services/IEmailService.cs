namespace TeamTrackr.Services;

public interface IEmailService
{
    Task SendTaskAssignedEmail(string assigneeEmail, string taskTitle, string projectName);
    Task SendTaskDueReminderEmail(string assigneeEmail, string taskTitle, DateTime dueDate);
    Task SendDailyDigestEmail(string userEmail, List<string> overdueTasks, List<string> dueTodayTasks);
}
