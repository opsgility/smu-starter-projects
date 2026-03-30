using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using BrightShelf.Data;
using BrightShelf.Models;

namespace BrightShelf.Pages.Products;

public class DeleteModel : PageModel
{
    private readonly AppDbContext _context;

    public DeleteModel(AppDbContext context)
    {
        _context = context;
    }

    [BindProperty]
    public Product Product { get; set; } = new();

    public IActionResult OnGet(int id)
    {
        // TODO: Load the product from the database by id
        return Page();
    }

    public IActionResult OnPost()
    {
        // TODO: Delete the product from the database
        return RedirectToPage("Index");
    }
}
