using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using BrightShelf.Models;

namespace BrightShelf.Pages.Products;

public class EditModel : PageModel
{
    [BindProperty]
    public Product Product { get; set; } = new();

    public IActionResult OnGet(int id)
    {
        var product = ProductStore.GetById(id);
        if (product == null)
        {
            return NotFound();
        }
        Product = product;
        return Page();
    }

    public IActionResult OnPost()
    {
        // TODO: Add ModelState.IsValid check
        ProductStore.Update(Product);
        return RedirectToPage("Index");
    }
}
