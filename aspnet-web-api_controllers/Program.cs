var builder = WebApplication.CreateBuilder(args);

builder.Services.AddOpenApi();

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();
    app.UseSwaggerUI(options =>
    {
        options.SwaggerEndpoint("/openapi/v1.json", "TaskFlow API");
    });
}

app.UseHttpsRedirection();

app.MapGet("/", () => "TaskFlow API is running!");

app.MapGet("/api/status", () => new { status = "healthy", version = "1.0" });

app.MapGet("/hello/{name}", (string name) => $"Hello, {name}!");

app.Run();
