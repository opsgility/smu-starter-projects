using Microsoft.EntityFrameworkCore;
using BrightShelf.Data;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddRazorPages();
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseNpgsql("Host=localhost;Database=brightshelf;Username=coder;Password=coder"));

var app = builder.Build();

app.UseStaticFiles();
app.UseRouting();
app.MapRazorPages();

app.Run();
