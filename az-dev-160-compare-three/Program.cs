using System.Diagnostics;
using Azure;
using Azure.Identity;
using Azure.Messaging.EventGrid;
using Azure.Messaging.EventGrid.SystemEvents;
using Azure.Messaging.EventHubs.Producer;
using Azure.Messaging.ServiceBus;

var cred = new DefaultAzureCredential();

var mode = args.Length > 0 ? args[0] : "help";

switch (mode)
{
    case "sb":  await SendSB(); break;
    case "eg":  await SendEG(); break;
    case "eh":  await SendEH(); break;
    default: Console.WriteLine("Modes: sb | eg | eh"); break;
}

async Task SendSB()
{
    var ns = Environment.GetEnvironmentVariable("SB_NAMESPACE") ?? throw new InvalidOperationException("SB_NAMESPACE");
    var q  = Environment.GetEnvironmentVariable("SB_QUEUE") ?? "orders";
    await using var client = new ServiceBusClient(ns, cred);
    await using var sender = client.CreateSender(q);
    var sw = Stopwatch.StartNew();
    for (int i = 0; i < 100; i++)
        await sender.SendMessageAsync(new ServiceBusMessage($"order-{i}"));
    sw.Stop();
    Console.WriteLine($"SB: sent 100 messages in {sw.ElapsedMilliseconds} ms");
}

async Task SendEG()
{
    var topicEndpoint = Environment.GetEnvironmentVariable("EG_TOPIC_ENDPOINT") ?? throw new InvalidOperationException("EG_TOPIC_ENDPOINT");
    var topicKey = Environment.GetEnvironmentVariable("EG_TOPIC_KEY");
    var pub = string.IsNullOrEmpty(topicKey)
        ? new EventGridPublisherClient(new Uri(topicEndpoint), cred)
        : new EventGridPublisherClient(new Uri(topicEndpoint), new AzureKeyCredential(topicKey));

    var sw = Stopwatch.StartNew();
    var events = new List<EventGridEvent>();
    for (int i = 0; i < 100; i++)
        events.Add(new EventGridEvent(subject: $"orders/order-{i}", eventType: "Anchorline.OrderCreated", dataVersion: "1.0", data: new { orderId = $"ord-{i}", ts = DateTime.UtcNow }));
    await pub.SendEventsAsync(events);
    sw.Stop();
    Console.WriteLine($"EG: published 100 events in {sw.ElapsedMilliseconds} ms");
}

async Task SendEH()
{
    var ns = Environment.GetEnvironmentVariable("EH_NAMESPACE") ?? throw new InvalidOperationException("EH_NAMESPACE");
    var eh = Environment.GetEnvironmentVariable("EH_NAME") ?? "orders";
    await using var producer = new EventHubProducerClient(ns, eh, cred);
    var sw = Stopwatch.StartNew();
    using var batch = await producer.CreateBatchAsync();
    for (int i = 0; i < 100; i++)
        batch.TryAdd(new Azure.Messaging.EventHubs.EventData(System.Text.Encoding.UTF8.GetBytes($"order-{i}")));
    await producer.SendAsync(batch);
    sw.Stop();
    Console.WriteLine($"EH: sent 100 events in {sw.ElapsedMilliseconds} ms");
}
