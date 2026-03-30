using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
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

    public async Task<IActionResult> OnGetAsync(int id)
    {
        var product = await _context.Products
            .Include(p => p.Category)
            .FirstOrDefaultAsync(p => p.Id == id);

        if (product == null)
        {
            return NotFound();
        }

        Product = product;
        return Page();
    }

    public async Task<IActionResult> OnPostAsync()
    {
        var product = await _context.Products.FindAsync(Product.Id);
        if (product != null)
        {
            _context.Products.Remove(product);
            await _context.SaveChangesAsync();
        }
        return RedirectToPage("Index");
    }
}
