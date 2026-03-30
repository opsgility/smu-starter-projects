using Microsoft.AspNetCore.Mvc.RazorPages;
using BrightShelf.Data;
using BrightShelf.Models;

namespace BrightShelf.Pages.Products;

public class IndexModel : PageModel
{
    private readonly AppDbContext _context;

    public IndexModel(AppDbContext context)
    {
        _context = context;
    }

    public List<Product> Products { get; set; } = new();

    public void OnGet()
    {
        // TODO: Query products from the database using _context
        // Include the Category navigation property
    }
}
