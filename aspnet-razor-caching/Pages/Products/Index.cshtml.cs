using Microsoft.AspNetCore.Mvc.RazorPages;
using BrightShelf.Models;
using BrightShelf.Services;
using System.Diagnostics;

namespace BrightShelf.Pages.Products;

// TODO: Students will add [ResponseCache] or [OutputCache] attributes here
public class IndexModel : PageModel
{
    private readonly IProductService _productService;

    public IndexModel(IProductService productService)
    {
        _productService = productService;
    }

    public IList<Product> Products { get; set; } = new List<Product>();
    public long LoadTimeMs { get; set; }

    public async Task OnGetAsync()
    {
        var sw = Stopwatch.StartNew();

        // This calls the slow service every time - no caching
        Products = await _productService.GetAllProductsAsync();

        sw.Stop();
        LoadTimeMs = sw.ElapsedMilliseconds;
    }
}
