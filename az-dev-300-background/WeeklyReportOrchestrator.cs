using Microsoft.Azure.Functions.Worker;
using Microsoft.DurableTask;
using Microsoft.Extensions.Logging;

namespace TaskForge.Background;

public sealed class WeeklyReportOrchestrator
{
    [Function(nameof(RunOrchestrator))]
    public async Task<int> RunOrchestrator(
        [OrchestrationTrigger] TaskOrchestrationContext context)
    {
        var tenants = await context.CallActivityAsync<string[]>(nameof(GetActiveTenants), input: null);
        var tasks = tenants.Select(t => context.CallActivityAsync<int>(nameof(GenerateReport), t));
        var results = await Task.WhenAll(tasks);
        await context.CallActivityAsync(nameof(SendDigest), results);
        return results.Length;
    }

    [Function(nameof(GetActiveTenants))]
    public string[] GetActiveTenants([ActivityTrigger] object _) =>
        new[] { "contoso-store", "apex-fitness", "riverside-clinic" };

    [Function(nameof(GenerateReport))]
    public int GenerateReport([ActivityTrigger] string tenantId, ILogger log)
    {
        log.LogInformation("Report for {TenantId}", tenantId);
        return 42;   // number of tasks in the report; wire real query later
    }

    [Function(nameof(SendDigest))]
    public void SendDigest([ActivityTrigger] int[] counts, ILogger log)
    {
        log.LogInformation("Digest sent: {Total} tasks across {Tenants} tenants", counts.Sum(), counts.Length);
    }

    // Client: timer trigger fires every Sunday 06:00 UTC
    [Function(nameof(FireWeekly))]
    public async Task FireWeekly(
        [TimerTrigger("0 0 6 * * 0")] TimerInfo timer,
        [DurableClient] DurableTaskClient client)
    {
        var instanceId = await client.ScheduleNewOrchestrationInstanceAsync(nameof(RunOrchestrator));
        Console.WriteLine($"Scheduled orchestration {instanceId}");
    }
}
