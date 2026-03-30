using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using BrightShelf.Models;

namespace BrightShelf.Pages.Products;

public class EditModel : PageModel
{
    [BindProperty]
    public Product Product { get; set; } = new();

    public List<Category> Categories { get; set; } = new();

    public IActionResult OnGet(int id)
    {
        var product = ProductStore.GetById(id);
        if (product == null)
        {
            return NotFound();
        }
        Product = product;
        Categories = ProductStore.GetCategories();
        return Page();
    }

    public IActionResult OnPost()
    {
        ProductStore.Update(Product);
        return RedirectToPage("Index");
    }
}
