var builder = WebApplication.CreateBuilder(args);

builder.Services.AddRazorPages();

// HttpClient is registered but no typed clients yet
// TODO: Students will create typed HttpClient services
// Example: builder.Services.AddHttpClient<WeatherService>(client => { ... });
builder.Services.AddHttpClient();

var app = builder.Build();

if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Error");
    app.UseHsts();
}

app.UseHttpsRedirection();
app.UseStaticFiles();
app.UseRouting();
app.UseAuthorization();

// Mock API endpoint - simulates a weather API
app.MapGet("/api/weather", () =>
{
    var forecasts = new[]
    {
        new { Date = DateTime.Today.AddDays(1).ToString("yyyy-MM-dd"), TemperatureC = 22, Summary = "Warm" },
        new { Date = DateTime.Today.AddDays(2).ToString("yyyy-MM-dd"), TemperatureC = 18, Summary = "Cool" },
        new { Date = DateTime.Today.AddDays(3).ToString("yyyy-MM-dd"), TemperatureC = 30, Summary = "Hot" },
        new { Date = DateTime.Today.AddDays(4).ToString("yyyy-MM-dd"), TemperatureC = 15, Summary = "Mild" },
        new { Date = DateTime.Today.AddDays(5).ToString("yyyy-MM-dd"), TemperatureC = 8, Summary = "Chilly" }
    };
    return Results.Ok(forecasts);
});

app.MapGet("/api/products", () =>
{
    var products = new[]
    {
        new { Id = 1, Name = "Desk Lamp", Price = 29.99 },
        new { Id = 2, Name = "Wireless Mouse", Price = 19.99 },
        new { Id = 3, Name = "Notebook", Price = 12.50 }
    };
    return Results.Ok(products);
});

app.MapRazorPages();

app.Run();
