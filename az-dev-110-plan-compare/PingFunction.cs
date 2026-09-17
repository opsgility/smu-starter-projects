using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.Functions.Worker;

namespace Anchorline.Functions.PlanCompare;

public class PingFunction
{
    private readonly StartupInfo _startup;
    public PingFunction(StartupInfo startup) => _startup = startup;

    [Function("Ping")]
    public IActionResult Run(
        [HttpTrigger(AuthorizationLevel.Function, "get", Route = "ping")] HttpRequest req)
    {
        return new OkObjectResult(new
        {
            processStartedAt = _startup.ProcessStartedAt,
            now = DateTimeOffset.UtcNow,
            processAge = (DateTimeOffset.UtcNow - _startup.ProcessStartedAt).TotalSeconds,
            hostname = Environment.MachineName
        });
    }
}
