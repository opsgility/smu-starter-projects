using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using BrightShelf.Data;
using BrightShelf.Models;

namespace BrightShelf.Pages.Products;

// TODO: Students will add [Authorize] attribute here
public class IndexModel : PageModel
{
    private readonly AppDbContext _context;

    public IndexModel(AppDbContext context)
    {
        _context = context;
    }

    public IList<Product> Products { get; set; } = new List<Product>();

    public async Task OnGetAsync()
    {
        Products = await _context.Products.ToListAsync();
    }
}
