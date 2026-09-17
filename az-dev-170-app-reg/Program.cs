// This lab is primarily az CLI / portal-driven. Verifier prints the resulting appIds.
var idOrders = Environment.GetEnvironmentVariable("ORDERS_APP_ID");
var idSpa = Environment.GetEnvironmentVariable("SPA_APP_ID");
Console.WriteLine($"Orders API app id: {idOrders ?? "<not set>"}");
Console.WriteLine($"SPA app id:        {idSpa ?? "<not set>"}");
if (idOrders is null || idSpa is null)
{
    Console.WriteLine("Register the apps via `az ad app create` and export the env vars.");
    return 1;
}
Console.WriteLine("Both apps registered.");
return 0;
