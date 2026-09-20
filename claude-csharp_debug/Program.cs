using DebugApi.Repositories;
using DebugApi.Services;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

// BUG 1: Scoped repository consumed by Singleton service
builder.Services.AddScoped<ITaskRepository, TaskRepository>();
builder.Services.AddSingleton<ITaskService, TaskService>();

var app = builder.Build();
app.UseSwagger();
app.UseSwaggerUI();
app.MapControllers();
app.Run();
