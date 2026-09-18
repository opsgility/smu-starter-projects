var builder = WebApplication.CreateBuilder(args);

builder.Services.AddRazorPages();
builder.Services.AddServerSideBlazor()
    .AddHubOptions(o => { o.MaximumReceiveMessageSize = 128 * 1024; });

var azureSignalR = builder.Configuration.GetConnectionString("AzureSignalR");
if (!string.IsNullOrEmpty(azureSignalR))
    builder.Services.AddSignalR().AddAzureSignalR(o => o.ConnectionString = azureSignalR);
else
    builder.Services.AddSignalR();

var app = builder.Build();

// Warm-up path — hit by App Service slot swap
app.MapGet("/health/ready", () => Results.Ok(new { status = "ready", env = app.Environment.EnvironmentName, host = Environment.MachineName }));
app.MapGet("/health/live",  () => Results.Ok(new { status = "live" }));

app.UseStaticFiles();
app.UseRouting();
app.MapBlazorHub();
app.MapFallbackToPage("/_Host");
app.Run();
