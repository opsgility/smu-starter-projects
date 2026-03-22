using ECommerceApi.Models;
using ECommerceApi.Services;
using Microsoft.AspNetCore.Mvc;

namespace ECommerceApi.Controllers;

[ApiController]
[Route("api/[controller]")]
public class ProductsController : ControllerBase
{
    private readonly IProductService _productService;

    public ProductsController(IProductService productService)
    {
        _productService = productService;
    }

    [HttpGet]
    public ActionResult<IEnumerable<Product>> GetAll()
    {
        try
        {
            var products = _productService.GetAll();
            return Ok(products);
        }
        catch (Exception ex)
        {
            return StatusCode(500, new { error = "An error occurred while processing your request.", details = ex.Message });
        }
    }

    [HttpGet("{id}")]
    public ActionResult<Product> GetById(int id)
    {
        try
        {
            var product = _productService.GetById(id);
            if (product == null)
                return NotFound(new { error = $"Product with ID {id} not found." });
            return Ok(product);
        }
        catch (Exception ex)
        {
            return StatusCode(500, new { error = "An error occurred while processing your request.", details = ex.Message });
        }
    }

    [HttpPost]
    public ActionResult<Product> Create([FromBody] Product product)
    {
        try
        {
            var created = _productService.Create(product);
            return CreatedAtAction(nameof(GetById), new { id = created.Id }, created);
        }
        catch (Exception ex)
        {
            return StatusCode(500, new { error = "An error occurred while processing your request.", details = ex.Message });
        }
    }

    [HttpPut("{id}")]
    public ActionResult<Product> Update(int id, [FromBody] Product product)
    {
        try
        {
            product.Id = id;
            var updated = _productService.Update(product);
            if (updated == null)
                return NotFound(new { error = $"Product with ID {id} not found." });
            return Ok(updated);
        }
        catch (Exception ex)
        {
            return StatusCode(500, new { error = "An error occurred while processing your request.", details = ex.Message });
        }
    }

    [HttpDelete("{id}")]
    public ActionResult Delete(int id)
    {
        try
        {
            var deleted = _productService.Delete(id);
            if (!deleted)
                return NotFound(new { error = $"Product with ID {id} not found." });
            return NoContent();
        }
        catch (Exception ex)
        {
            return StatusCode(500, new { error = "An error occurred while processing your request.", details = ex.Message });
        }
    }

    [HttpGet("category/{category}")]
    public ActionResult<IEnumerable<Product>> GetByCategory(string category)
    {
        try
        {
            var products = _productService.GetByCategory(category);
            return Ok(products);
        }
        catch (Exception ex)
        {
            return StatusCode(500, new { error = "An error occurred while processing your request.", details = ex.Message });
        }
    }

    [HttpGet("search")]
    public ActionResult<IEnumerable<Product>> SearchByName([FromQuery] string name)
    {
        try
        {
            var products = _productService.SearchByName(name);
            return Ok(products);
        }
        catch (Exception ex)
        {
            return StatusCode(500, new { error = "An error occurred while processing your request.", details = ex.Message });
        }
    }
}
