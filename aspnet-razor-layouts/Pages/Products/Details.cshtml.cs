using Microsoft.AspNetCore.Mvc.RazorPages;

namespace BrightShelf.Pages.Products;

public class DetailsModel : PageModel
{
    public int Id { get; set; }

    public void OnGet(int id)
    {
        Id = id;
    }
}
