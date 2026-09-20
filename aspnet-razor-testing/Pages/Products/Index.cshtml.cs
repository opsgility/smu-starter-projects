using Microsoft.AspNetCore.Mvc.RazorPages;
using BrightShelf.Models;
using BrightShelf.Services;

namespace BrightShelf.Pages.Products;

public class IndexModel : PageModel
{
    private readonly IProductService _productService;

    public IndexModel(IProductService productService)
    {
        _productService = productService;
    }

    public IList<Product> Products { get; set; } = new List<Product>();

    public async Task OnGetAsync()
    {
        Products = await _productService.GetAllAsync();
    }
}
