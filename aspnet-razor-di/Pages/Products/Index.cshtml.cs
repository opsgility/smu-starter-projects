using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
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

    public async Task OnGetAsync()
    {
        Products = await _context.Products
            .Include(p => p.Category)
            .ToListAsync();
    }
}
