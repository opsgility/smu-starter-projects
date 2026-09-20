using Microsoft.AspNetCore.Mvc.RazorPages;
using BrightShelf.Models;

namespace BrightShelf.Pages.Products;

public class IndexModel : PageModel
{
    public List<Product> Products { get; set; } = new();

    public void OnGet()
    {
        Products = ProductStore.Products;
    }
}
