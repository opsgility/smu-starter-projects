using Azure.Messaging.ServiceBus;
using Microsoft.Azure.Functions.Worker;
using Microsoft.Extensions.Logging;

namespace TaskForge.Background;

public sealed class CommandHandlers(ILogger<CommandHandlers> log)
{
    // Session-enabled queue trigger — per-tenant FIFO.
    [Function(nameof(HandleCreateTask))]
    public async Task HandleCreateTask(
        [ServiceBusTrigger("commands", IsSessionsEnabled = true, Connection = "SB_ConnectionString")]
        ServiceBusReceivedMessage msg,
        CancellationToken ct)
    {
        var correlation = msg.CorrelationId;
        log.LogInformation("Handling command corr={Corr} session={Session}", correlation, msg.SessionId);
        // TODO: idempotency check via IIdempotencyStore
        // TODO: parse msg.Body as CreateTaskCommand, write to Cosmos with hierarchical PK
        // TODO: broadcast TaskCreatedEvent via SignalR to group $"tenant-{tenantId}"
        await Task.CompletedTask;
    }
}
