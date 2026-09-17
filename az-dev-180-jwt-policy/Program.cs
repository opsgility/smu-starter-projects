using Azure.Core;
using Azure.Identity;

var resource = Environment.GetEnvironmentVariable("RESOURCE") ?? "api://anchor-orders";
var cred = new AzureCliCredential();
var token = await cred.GetTokenAsync(new TokenRequestContext(new[] { $"{resource}/.default" }));
Console.WriteLine(token.Token);
