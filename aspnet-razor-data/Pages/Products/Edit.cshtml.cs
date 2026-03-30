using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using BrightShelf.Data;
using BrightShelf.Models;

namespace BrightShelf.Pages.Products;

public class EditModel : PageModel
{
    private readonly AppDbContext _context;

    public EditModel(AppDbContext context)
    {
        _context = context;
    }

    [BindProperty]
    public Product Product { get; set; } = new();

    public IActionResult OnGet(int id)
    {
        // TODO: Load the product from the database by id
        // TODO: Load categories for the dropdown
        return Page();
    }

    public IActionResult OnPost()
    {
        // TODO: Validate and update the product in the database
        return RedirectToPage("Index");
    }
}
