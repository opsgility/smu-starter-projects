using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using BrightShelf.Data;
using BrightShelf.Models;

namespace BrightShelf.Pages.Products;

// TODO: Students will add [Authorize] attribute here
public class DetailsModel : PageModel
{
    private readonly AppDbContext _context;

    public DetailsModel(AppDbContext context)
    {
        _context = context;
    }

    public Product Product { get; set; } = default!;

    public async Task<IActionResult> OnGetAsync(int id)
    {
        var product = await _context.Products.FindAsync(id);
        if (product == null)
        {
            return NotFound();
        }
        Product = product;
        return Page();
    }
}
