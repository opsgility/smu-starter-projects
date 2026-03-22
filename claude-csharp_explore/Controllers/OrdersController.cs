using ECommerceApi.Models;
using ECommerceApi.Services;
using Microsoft.AspNetCore.Mvc;

namespace ECommerceApi.Controllers;

[ApiController]
[Route("api/[controller]")]
public class OrdersController : ControllerBase
{
    private readonly IOrderService _orderService;

    public OrdersController(IOrderService orderService)
    {
        _orderService = orderService;
    }

    [HttpPost]
    public ActionResult<Order> Create([FromBody] Order order)
    {
        try
        {
            var created = _orderService.CreateOrder(order);
            return CreatedAtAction(nameof(GetById), new { id = created.Id }, created);
        }
        catch (InvalidOperationException ex)
        {
            return BadRequest(new { error = ex.Message });
        }
        catch (Exception ex)
        {
            return StatusCode(500, new { error = "An error occurred while processing your request.", details = ex.Message });
        }
    }

    [HttpGet("{id}")]
    public ActionResult<Order> GetById(int id)
    {
        try
        {
            var order = _orderService.GetById(id);
            if (order == null)
                return NotFound(new { error = $"Order with ID {id} not found." });
            return Ok(order);
        }
        catch (Exception ex)
        {
            return StatusCode(500, new { error = "An error occurred while processing your request.", details = ex.Message });
        }
    }

    [HttpGet("customer/{customerId}")]
    public ActionResult<IEnumerable<Order>> GetByCustomerId(int customerId)
    {
        try
        {
            var orders = _orderService.GetByCustomerId(customerId);
            return Ok(orders);
        }
        catch (Exception ex)
        {
            return StatusCode(500, new { error = "An error occurred while processing your request.", details = ex.Message });
        }
    }
}
