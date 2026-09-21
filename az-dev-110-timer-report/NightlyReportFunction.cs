using Azure;
using Azure.Storage.Blobs;
using Azure.Storage.Blobs.Specialized;
using Microsoft.Azure.Functions.Worker;
using Microsoft.Extensions.Logging;

namespace Anchorline.Functions.TimerReport;

public class NightlyReportFunction
{
    private readonly BlobServiceClient _blobs;
    private readonly ILogger<NightlyReportFunction> _log;

    public NightlyReportFunction(BlobServiceClient blobs, ILogger<NightlyReportFunction> log)
    {
        _blobs = blobs;
        _log = log;
    }

    [Function("NightlyReport")]
    public async Task Run(
        [TimerTrigger("%TIMER_SCHEDULE%", RunOnStartup = false)] TimerInfo timer)
    {
        _log.LogInformation("NightlyReport fired at {Now}. IsPastDue={IsPastDue}. Next={Next}",
            DateTimeOffset.UtcNow, timer.IsPastDue, timer.ScheduleStatus?.Next);

        // EXERCISE 2 will add the singleton blob-lease pattern around the work below.

        await GenerateReportAsync();
    }

    private async Task GenerateReportAsync()
    {
        _log.LogInformation("Generating nightly inventory reconciliation report...");

        // Simulated work
        await Task.Delay(TimeSpan.FromSeconds(3));

        var reports = _blobs.GetBlobContainerClient("nightly-reports");
        await reports.CreateIfNotExistsAsync();

        var reportName = $"anchorline-inventory-{DateTimeOffset.UtcNow:yyyy-MM-ddTHH-mm-ss}.txt";
        var body = $"Anchorline nightly inventory report\nGenerated: {DateTimeOffset.UtcNow:O}\nRows reconciled: 8,432\n";
        await reports.UploadBlobAsync(reportName, BinaryData.FromString(body));

        _log.LogInformation("Wrote report {Name}", reportName);
    }
}
