// This lab centers on GitHub Actions federated login. This program prints setup checks.
Console.WriteLine("WIF checklist:");
Console.WriteLine("  ORDERS_APP_ID: " + (Environment.GetEnvironmentVariable("ORDERS_APP_ID") ?? "MISSING"));
Console.WriteLine("  TENANT_ID:     " + (Environment.GetEnvironmentVariable("TENANT_ID") ?? "MISSING"));
Console.WriteLine("  SUB_ID:        " + (Environment.GetEnvironmentVariable("SUB_ID") ?? "MISSING"));
Console.WriteLine("Now run the deploy-bicep.yml workflow in GitHub.");
