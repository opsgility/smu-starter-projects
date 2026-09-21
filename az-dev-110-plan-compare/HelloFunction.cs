using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.Functions.Worker;

namespace Anchorline.Functions.PlanCompare;

// Single Hello function on a catch-all route so the same code answers
// /api/hello, /api/hello/warmup, /api/hello/probe1..N, /api/hello/load, etc.
// The exercise + content.test.yaml + LeftAgent instructions all use these
// paths — Function name stays "Hello" so `az functionapp function keys list
// --function-name Hello` resolves on both plans.
public class HelloFunction
{
    private readonly StartupInfo _startup;
    public HelloFunction(StartupInfo startup) => _startup = startup;

    [Function("Hello")]
    public IActionResult Run(
        [HttpTrigger(AuthorizationLevel.Function, "get", Route = "hello/{*probe}")] HttpRequest req,
        string? probe)
    {
        return new OkObjectResult(new
        {
            processStartedAt = _startup.ProcessStartedAt,
            now = DateTimeOffset.UtcNow,
            processAgeSeconds = (DateTimeOffset.UtcNow - _startup.ProcessStartedAt).TotalSeconds,
            hostname = Environment.MachineName,
            planLabel = Environment.GetEnvironmentVariable("PLAN_LABEL"),
            buildTag = Environment.GetEnvironmentVariable("AZ_DEV_110_BUILD_TAG"),
            probe = probe ?? ""
        });
    }
}
