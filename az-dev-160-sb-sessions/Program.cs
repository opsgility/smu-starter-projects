using Azure.Identity;
using Azure.Messaging.ServiceBus;

var ns = Environment.GetEnvironmentVariable("SB_NAMESPACE") ?? throw new InvalidOperationException("SB_NAMESPACE");
var q  = Environment.GetEnvironmentVariable("SB_QUEUE") ?? "orders-sessions";

var mode = args.Length > 0 ? args[0] : "help";

await using var client = new ServiceBusClient(ns, new DefaultAzureCredential());

switch (mode)
{
    case "send-interleaved": await SendInterleaved(); break;
    case "process":  await Process(); break;
    case "poison":   await SendPoison(); break;
    case "dlq":      await ReadDlq(); break;
    default: Console.WriteLine("Modes: send-interleaved | process | poison | dlq"); break;
}

async Task SendInterleaved()
{
    await using var sender = client.CreateSender(q);
    var customers = new[] { "acme", "nova", "zenith" };
    var msgs = new List<ServiceBusMessage>();
    for (int i = 0; i < 5; i++)
    {
        foreach (var cust in customers)
            msgs.Add(new ServiceBusMessage($"order-{cust}-{i}") { SessionId = cust });
    }
    await sender.SendMessagesAsync(msgs);
    Console.WriteLine($"Sent {msgs.Count} messages across {customers.Length} sessions");
}

async Task Process()
{
    var sessionProc = client.CreateSessionProcessor(q, new ServiceBusSessionProcessorOptions
    {
        MaxConcurrentSessions = 3,
        MaxConcurrentCallsPerSession = 1
    });

    sessionProc.ProcessMessageAsync += async args =>
    {
        Console.WriteLine($"[session={args.Message.SessionId}] {args.Message.Body}");
        await Task.Delay(300);
        await args.CompleteMessageAsync(args.Message);
    };
    sessionProc.ProcessErrorAsync += args => { Console.WriteLine($"ERR {args.Exception.Message}"); return Task.CompletedTask; };

    await sessionProc.StartProcessingAsync();
    Console.WriteLine("Session processor running. Ctrl-C to stop.");
    await Task.Delay(-1);
}

async Task SendPoison()
{
    await using var sender = client.CreateSender(q);
    // Same MessageId sent twice — dedup drops the second
    await sender.SendMessageAsync(new ServiceBusMessage("poison-payload") { SessionId = "poison-session", MessageId = "poison-1" });
    await sender.SendMessageAsync(new ServiceBusMessage("poison-payload") { SessionId = "poison-session", MessageId = "poison-1" });
    Console.WriteLine("Sent 2 messages with same MessageId (poison-1). Dedup should drop the second.");
}

async Task ReadDlq()
{
    var receiver = client.CreateReceiver(q, new ServiceBusReceiverOptions { SubQueue = SubQueue.DeadLetter });
    var msgs = await receiver.ReceiveMessagesAsync(50, TimeSpan.FromSeconds(5));
    Console.WriteLine($"DLQ contains {msgs.Count} messages");
    foreach (var m in msgs)
        Console.WriteLine($"  {m.SessionId} : {m.Body} -- reason: {m.DeadLetterReason}");
}
