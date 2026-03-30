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
    public Product Product { get; set; } = default!;

    // TODO: Students will add [BindProperty] for IFormFile Upload property

    public IActionResult OnGet()
    {
        return Page();
    }

    public async Task<IActionResult> OnPostAsync()
    {
        if (!ModelState.IsValid)
        {
            return Page();
        }

        // TODO: Students will add file upload handling here
        // - Check if Upload is not null
        // - Generate unique filename
        // - Save to wwwroot/uploads/
        // - Set Product.ImagePath

        _context.Products.Add(Product);
        await _context.SaveChangesAsync();

        return RedirectToPage("Index");
    }
}
