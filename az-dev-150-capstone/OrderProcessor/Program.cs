using Azure.Identity;
using Azure.Messaging.ServiceBus;

var host = Host.CreateApplicationBuilder(args);
var miClientId = Environment.GetEnvironmentVariable("MI_CLIENT_ID");
var sbFqdn = Environment.GetEnvironmentVariable("SB_NAMESPACE") ?? throw new InvalidOperationException("SB_NAMESPACE");
var queue = Environment.GetEnvironmentVariable("SB_QUEUE") ?? "orders";

var cred = string.IsNullOrEmpty(miClientId)
    ? new DefaultAzureCredential()
    : new DefaultAzureCredential(new DefaultAzureCredentialOptions { ManagedIdentityClientId = miClientId });

host.Services.AddSingleton(new ServiceBusClient(sbFqdn, cred));
host.Services.AddHostedService<Worker>();

var app = host.Build();
await app.RunAsync();

public class Worker(ServiceBusClient client, ILogger<Worker> log) : BackgroundService
{
    protected override async Task ExecuteAsync(CancellationToken ct)
    {
        var queue = Environment.GetEnvironmentVariable("SB_QUEUE") ?? "orders";
        var replica = Environment.GetEnvironmentVariable("CONTAINER_APP_REPLICA_NAME") ?? Environment.MachineName;
        log.LogInformation("[{r}] processor starting for {q}", replica, queue);

        var processor = client.CreateProcessor(queue, new ServiceBusProcessorOptions { MaxConcurrentCalls = 4 });
        processor.ProcessMessageAsync += async args =>
        {
            log.LogInformation("[{r}] processed: {body}", replica, args.Message.Body);
            await Task.Delay(500, ct);
            await args.CompleteMessageAsync(args.Message);
        };
        processor.ProcessErrorAsync += args => { log.LogError(args.Exception, "SB error"); return Task.CompletedTask; };
        await processor.StartProcessingAsync(ct);
        try { await Task.Delay(Timeout.Infinite, ct); }
        catch (OperationCanceledException) { }
        await processor.StopProcessingAsync();
    }
}
