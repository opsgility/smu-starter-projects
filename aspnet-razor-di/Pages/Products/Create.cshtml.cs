using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.AspNetCore.Mvc.Rendering;
using Microsoft.EntityFrameworkCore;
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

    public SelectList CategoryOptions { get; set; } = default!;

    public async Task OnGetAsync()
    {
        var categories = await _context.Categories.ToListAsync();
        CategoryOptions = new SelectList(categories, "Id", "Name");
    }

    public async Task<IActionResult> OnPostAsync()
    {
        if (!ModelState.IsValid)
        {
            var categories = await _context.Categories.ToListAsync();
            CategoryOptions = new SelectList(categories, "Id", "Name");
            return Page();
        }

        _context.Products.Add(Product);
        await _context.SaveChangesAsync();
        return RedirectToPage("Index");
    }
}
