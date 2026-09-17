using Azure.Identity;
using Azure.Messaging.ServiceBus;

var host = Host.CreateApplicationBuilder(args);
var ns = Environment.GetEnvironmentVariable("SB_NAMESPACE")
    ?? throw new InvalidOperationException("SB_NAMESPACE missing (e.g. anchorline-sb-xxx.servicebus.windows.net)");
var queueName = Environment.GetEnvironmentVariable("SB_QUEUE") ?? "orders";

host.Services.AddSingleton(sp =>
    new ServiceBusClient(ns, new DefaultAzureCredential()));

host.Services.AddHostedService<OrderProcessor>();

var app = host.Build();
await app.RunAsync();

public class OrderProcessor(ServiceBusClient client, ILogger<OrderProcessor> log, IHostApplicationLifetime lifetime) : BackgroundService
{
    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        var queueName = Environment.GetEnvironmentVariable("SB_QUEUE") ?? "orders";
        var replicaName = Environment.GetEnvironmentVariable("CONTAINER_APP_REPLICA_NAME") ?? Environment.MachineName;
        log.LogInformation("Replica {r} starting to consume {q}", replicaName, queueName);

        var processor = client.CreateProcessor(queueName, new ServiceBusProcessorOptions
        {
            MaxConcurrentCalls = 4,
            AutoCompleteMessages = false
        });

        processor.ProcessMessageAsync += async args =>
        {
            var body = args.Message.Body.ToString();
            log.LogInformation("[{r}] processed: {b}", replicaName, body);
            await Task.Delay(200, stoppingToken); // Simulate work
            await args.CompleteMessageAsync(args.Message);
        };
        processor.ProcessErrorAsync += args =>
        {
            log.LogError(args.Exception, "SB error");
            return Task.CompletedTask;
        };

        await processor.StartProcessingAsync(stoppingToken);
        await Task.Delay(Timeout.Infinite, stoppingToken).ContinueWith(_ => { });
        await processor.StopProcessingAsync();
    }
}
