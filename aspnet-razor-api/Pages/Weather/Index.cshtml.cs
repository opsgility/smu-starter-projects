using System.Text.Json;
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace BrightShelf.Pages.Weather;

public class IndexModel : PageModel
{
    private readonly IHttpClientFactory _httpClientFactory;

    public IndexModel(IHttpClientFactory httpClientFactory)
    {
        _httpClientFactory = httpClientFactory;
    }

    public List<WeatherForecast> Forecasts { get; set; } = new();

    public async Task OnGetAsync()
    {
        // TODO: Students will replace this with a typed HttpClient service
        var client = _httpClientFactory.CreateClient();

        // Using the built-in mock API endpoint
        var request = new HttpRequestMessage(HttpMethod.Get,
            $"{Request.Scheme}://{Request.Host}/api/weather");

        try
        {
            var response = await client.SendAsync(request);
            if (response.IsSuccessStatusCode)
            {
                var json = await response.Content.ReadAsStringAsync();
                Forecasts = JsonSerializer.Deserialize<List<WeatherForecast>>(json,
                    new JsonSerializerOptions { PropertyNameCaseInsensitive = true }) ?? new();
            }
        }
        catch (HttpRequestException)
        {
            // API unavailable - Forecasts stays empty
        }
    }
}

public class WeatherForecast
{
    public string Date { get; set; } = string.Empty;
    public int TemperatureC { get; set; }
    public int TemperatureF => 32 + (int)(TemperatureC / 0.5556);
    public string Summary { get; set; } = string.Empty;
}
