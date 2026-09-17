// Container Apps Job - short-lived batch execution
// Reads JOB_MODE env var to decide what to do; exits with code 0 when done.
using System.Diagnostics;

var mode = Environment.GetEnvironmentVariable("JOB_MODE") ?? "etl";
var replicaName = Environment.GetEnvironmentVariable("CONTAINER_APP_REPLICA_NAME") ?? Environment.MachineName;
var sw = Stopwatch.StartNew();

Console.WriteLine($"[{replicaName}] Job start: mode={mode}, utc={DateTime.UtcNow:o}");

switch (mode)
{
    case "etl":
        // Simulate a nightly ETL — read source, transform, write target
        for (int i = 1; i <= 5; i++)
        {
            Console.WriteLine($"[{replicaName}] etl step {i}/5 ...");
            await Task.Delay(2000);
        }
        break;
    case "process":
        // Simulate processing a single work unit from a queue
        Console.WriteLine($"[{replicaName}] processing work item ...");
        await Task.Delay(3000);
        break;
    default:
        Console.WriteLine($"[{replicaName}] Unknown mode {mode}");
        Environment.Exit(1);
        return;
}

sw.Stop();
Console.WriteLine($"[{replicaName}] Job done: mode={mode}, elapsed={sw.Elapsed}");
