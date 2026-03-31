using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using BrightShelf.Models;

namespace BrightShelf.Pages.Products;

public class EditModel : PageModel
{
    [BindProperty]
    public Product Product { get; set; } = new();

    public List<string> Categories { get; } = new()
    {
        "Fiction", "Science", "Technology", "History", "Biography", "Self-Help"
    };

    public IActionResult OnGet(int id)
    {
        var product = ProductStore.GetById(id);
        if (product == null) return NotFound();
        Product = new Product
        {
            Id = product.Id, Name = product.Name, Author = product.Author,
            Category = product.Category, Price = product.Price,
            Description = product.Description, CreatedAt = product.CreatedAt
        };
        return Page();
    }

    public IActionResult OnPost()
    {
        ProductStore.Update(Product);
        return RedirectToPage("Index");
    }
}
