using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using BrightShelf.Models;

namespace BrightShelf.Pages.Products;

public class DetailsModel : PageModel
{
    public Product Product { get; set; } = new();

    public IActionResult OnGet(int id)
    {
        var product = ProductStore.GetById(id);
        if (product == null) return NotFound();
        Product = product;
        return Page();
    }
}
