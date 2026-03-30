using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using BrightShelf.Models;
using BrightShelf.Services;

namespace BrightShelf.Pages.Products;

public class DeleteModel : PageModel
{
    private readonly IProductService _productService;

    public DeleteModel(IProductService productService)
    {
        _productService = productService;
    }

    [BindProperty]
    public Product Product { get; set; } = default!;

    public async Task<IActionResult> OnGetAsync(int id)
    {
        var product = await _productService.GetByIdAsync(id);
        if (product == null)
        {
            return NotFound();
        }
        Product = product;
        return Page();
    }

    public async Task<IActionResult> OnPostAsync()
    {
        await _productService.DeleteAsync(Product.Id);
        return RedirectToPage("Index");
    }
}
