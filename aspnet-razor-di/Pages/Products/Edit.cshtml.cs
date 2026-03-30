using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.AspNetCore.Mvc.Rendering;
using Microsoft.EntityFrameworkCore;
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

    public SelectList CategoryOptions { get; set; } = default!;

    public async Task<IActionResult> OnGetAsync(int id)
    {
        var product = await _context.Products.FindAsync(id);
        if (product == null)
        {
            return NotFound();
        }

        Product = product;
        var categories = await _context.Categories.ToListAsync();
        CategoryOptions = new SelectList(categories, "Id", "Name");
        return Page();
    }

    public async Task<IActionResult> OnPostAsync()
    {
        if (!ModelState.IsValid)
        {
            var categories = await _context.Categories.ToListAsync();
            CategoryOptions = new SelectList(categories, "Id", "Name");
            return Page();
        }

        _context.Attach(Product).State = EntityState.Modified;
        await _context.SaveChangesAsync();
        return RedirectToPage("Index");
    }
}
