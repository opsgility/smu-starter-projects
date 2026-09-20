using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using BrightShelf.Data;
using BrightShelf.Models;

namespace BrightShelf.Pages.Products;

public class CreateModel : PageModel
{
    private readonly AppDbContext _context;

    public CreateModel(AppDbContext context)
    {
        _context = context;
    }

    [BindProperty]
    public Product Product { get; set; } = new();

    public void OnGet()
    {
        // TODO: Load categories for the dropdown
    }

    public IActionResult OnPost()
    {
        // TODO: Validate and save the product to the database
        return RedirectToPage("Index");
    }
}
