using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.Functions.Worker;
using Microsoft.Extensions.Logging;

namespace Anchorline.Functions;

public class HelloAnchorline
{
    private readonly ILogger<HelloAnchorline> _logger;

    public HelloAnchorline(ILogger<HelloAnchorline> logger)
    {
        _logger = logger;
    }

    [Function("HelloAnchorline")]
    public IActionResult Run(
        [HttpTrigger(AuthorizationLevel.Function, "get", "post", Route = "hello/{name?}")]
        HttpRequest req,
        string? name)
    {
        var who = string.IsNullOrEmpty(name) ? "adventurer" : name;
        _logger.LogInformation("HelloAnchorline invoked with name={Name}", who);
        return new ContentResult
        {
            Content = $"Hello, {who}. Anchorline Outdoors welcomes you.",
            ContentType = "text/plain",
            StatusCode = 200
        };
    }
}
