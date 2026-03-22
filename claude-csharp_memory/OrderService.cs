using MemoryApp.Models;

namespace MemoryApp;

// Uses explicit types, underscore prefix, PARTIAL XML docs, specific exceptions
public class OrderService
{
    private readonly List<Order> _orders = new();
    private int _nextId = 1;

    /// <summary>
    /// Gets an order by its identifier.
    /// </summary>
    public Order GetById(int id)
    {
        Order order = _orders.FirstOrDefault(o => o.Id == id)!;
        if (order == null) throw new KeyNotFoundException("Order not found");
        return order;
    }

    // No XML doc here (inconsistent with GetById)
    public Order Create(int userId, decimal total)
    {
        Order order = new Order
        {
            Id = _nextId++,
            UserId = userId,
            OrderDate = DateTime.UtcNow,
            Total = total
        };
        _orders.Add(order);
        return order;
    }

    public List<Order> GetAll()
    {
        List<Order> allOrders = _orders.ToList();
        return allOrders;
    }
}
