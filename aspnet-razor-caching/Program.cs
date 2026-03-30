using Microsoft.EntityFrameworkCore;
using BrightShelf.Data;
using BrightShelf.Services;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddRazorPages();

builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseNpgsql(builder.Configuration.GetConnectionString("DefaultConnection")));

// No caching configured yet - students will add:
// TODO: builder.Services.AddMemoryCache();
// TODO: builder.Services.AddOutputCache();

builder.Services.AddScoped<IProductService, ProductService>();

var app = builder.Build();

if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Error");
    app.UseHsts();
}

app.UseHttpsRedirection();
app.UseStaticFiles();
app.UseRouting();

// TODO: Students will add app.UseOutputCache();

app.UseAuthorization();

app.MapRazorPages();

using (var scope = app.Services.CreateScope())
{
    var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
    db.Database.EnsureCreated();
}

app.Run();
