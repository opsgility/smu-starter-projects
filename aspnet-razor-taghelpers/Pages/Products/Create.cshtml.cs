using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using BrightShelf.Models;

namespace BrightShelf.Pages.Products;

public class CreateModel : PageModel
{
    [BindProperty]
    public Product Product { get; set; } = new();

    public List<string> Categories { get; } = new()
    {
        "Fiction", "Science", "Technology", "History", "Biography", "Self-Help"
    };

    public void OnGet() { }

    public IActionResult OnPost()
    {
        Product.Id = ProductStore.GetNextId();
        Product.CreatedAt = DateTime.UtcNow;
        ProductStore.Products.Add(Product);
        return RedirectToPage("Index");
    }
}
