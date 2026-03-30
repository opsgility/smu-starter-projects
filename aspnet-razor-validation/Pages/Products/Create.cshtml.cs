using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using BrightShelf.Models;

namespace BrightShelf.Pages.Products;

public class CreateModel : PageModel
{
    [BindProperty]
    public Product Product { get; set; } = new();

    public void OnGet()
    {
    }

    public IActionResult OnPost()
    {
        // TODO: Add ModelState.IsValid check
        ProductStore.Add(Product);
        return RedirectToPage("Index");
    }
}
