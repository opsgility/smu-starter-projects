using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using BrightShelf.Models;

namespace BrightShelf.Pages.Products;

public class CreateModel : PageModel
{
    [BindProperty]
    public Product Product { get; set; } = new();

    public List<Category> Categories { get; set; } = new();

    public void OnGet()
    {
        Categories = ProductStore.GetCategories();
    }

    public IActionResult OnPost()
    {
        ProductStore.Add(Product);
        return RedirectToPage("Index");
    }
}
