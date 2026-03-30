using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using BrightShelf.Models;
using BrightShelf.Services;

namespace BrightShelf.Pages.Products;

public class CreateModel : PageModel
{
    private readonly IProductService _productService;

    public CreateModel(IProductService productService)
    {
        _productService = productService;
    }

    [BindProperty]
    public Product Product { get; set; } = default!;

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

        await _productService.CreateAsync(Product);

        return RedirectToPage("Index");
    }
}
