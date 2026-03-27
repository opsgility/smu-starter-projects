var builder = WebApplication.CreateBuilder(args);

var app = builder.Build();

app.MapGet("/", () => "TaskFlow API is running!");

app.Run();
