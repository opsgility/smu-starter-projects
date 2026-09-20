using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using BrightShelf.Models;
using BrightShelf.Services;
using System.Diagnostics;

namespace BrightShelf.Pages.Products;

// TODO: Students will add caching here
public class DetailsModel : PageModel
{
    private readonly IProductService _productService;

    public DetailsModel(IProductService productService)
    {
        _productService = productService;
    }

    public Product Product { get; set; } = default!;
    public long LoadTimeMs { get; set; }

    public async Task<IActionResult> OnGetAsync(int id)
    {
        var sw = Stopwatch.StartNew();

        var product = await _productService.GetProductByIdAsync(id);

        sw.Stop();
        LoadTimeMs = sw.ElapsedMilliseconds;

        if (product == null)
        {
            return NotFound();
        }

        Product = product;
        return Page();
    }
}
