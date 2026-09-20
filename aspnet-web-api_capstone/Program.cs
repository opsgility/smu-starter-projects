var builder = WebApplication.CreateBuilder(args);

var app = builder.Build();

app.MapGet("/", () => "BookShelf API - Ready to build!");

app.Run();
