using Azure.Identity;
using Azure.Messaging.ServiceBus;
using Azure.Messaging.ServiceBus.Administration;

var ns = Environment.GetEnvironmentVariable("SB_NAMESPACE") ?? throw new InvalidOperationException("SB_NAMESPACE");
var topic = Environment.GetEnvironmentVariable("SB_TOPIC") ?? "orders-topic";

await using var client = new ServiceBusClient(ns, new DefaultAzureCredential());
var admin = new ServiceBusAdministrationClient(ns, new DefaultAzureCredential());

var mode = args.Length > 0 ? args[0] : "help";
switch (mode)
{
    case "setup-rules": await SetupRules(); break;
    case "publish":     await Publish(1000); break;
    case "read":        await Read(args.Length > 1 ? args[1] : "acme-sub"); break;
    default: Console.WriteLine("Modes: setup-rules | publish | read <subName>"); break;
}

async Task SetupRules()
{
    foreach (var sub in new[] { "acme-sub", "contoso-sub", "priority-sub" })
    {
        try { await admin.DeleteRuleAsync(topic, sub, "$Default"); } catch { }
    }
    await admin.CreateRuleAsync(topic, "acme-sub",     new CreateRuleOptions("acme-only",    new SqlRuleFilter("Tenant = 'acme'")));
    await admin.CreateRuleAsync(topic, "contoso-sub",  new CreateRuleOptions("contoso-only", new SqlRuleFilter("Tenant = 'contoso'")));
    await admin.CreateRuleAsync(topic, "priority-sub", new CreateRuleOptions("priority",     new SqlRuleFilter("OrderTotal > 10000")));
    Console.WriteLine("Rules created");
}

async Task Publish(int count)
{
    await using var sender = client.CreateSender(topic);
    var tenants = new[] { "acme", "contoso", "zenith" };
    var rnd = new Random(42);
    var msgs = new List<ServiceBusMessage>();
    for (int i = 0; i < count; i++)
    {
        var m = new ServiceBusMessage($"order-{i}");
        m.ApplicationProperties["Tenant"] = tenants[rnd.Next(tenants.Length)];
        m.ApplicationProperties["OrderTotal"] = rnd.Next(50, 20000);
        msgs.Add(m);
        if (msgs.Count == 100)
        {
            await sender.SendMessagesAsync(msgs);
            msgs.Clear();
        }
    }
    if (msgs.Count > 0) await sender.SendMessagesAsync(msgs);
    Console.WriteLine($"Published {count} messages");
}

async Task Read(string sub)
{
    var receiver = client.CreateReceiver(topic, sub);
    var msgs = await receiver.ReceiveMessagesAsync(1000, TimeSpan.FromSeconds(10));
    Console.WriteLine($"Sub {sub} got {msgs.Count} messages");
    var tenantCounts = msgs.GroupBy(m => m.ApplicationProperties["Tenant"]?.ToString() ?? "?").ToDictionary(g => g.Key, g => g.Count());
    foreach (var kv in tenantCounts) Console.WriteLine($"  {kv.Key}: {kv.Value}");
    foreach (var m in msgs) await receiver.CompleteMessageAsync(m);
}
