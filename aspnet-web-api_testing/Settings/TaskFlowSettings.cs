namespace TaskFlow.Api.Settings;

public class TaskFlowSettings
{
    public int MaxPageSize { get; set; } = 50;
    public int DefaultPageSize { get; set; } = 10;
    public string ApiName { get; set; } = "TaskFlow";
}
