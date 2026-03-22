using ECommerceApi.Models;

namespace ECommerceApi.Repositories;

public class OrderRepository : IOrderRepository
{
    private static readonly List<Order> _orders = new();
    private static int _nextId = 1;
    private static int _nextItemId = 1;

    public IEnumerable<Order> GetAll() => _orders.ToList();

    public Order? GetById(int id) => _orders.FirstOrDefault(o => o.Id == id);

    public Order Create(Order order)
    {
        order.Id = _nextId++;
        foreach (var item in order.Items)
        {
            item.Id = _nextItemId++;
            item.OrderId = order.Id;
        }
        _orders.Add(order);
        return order;
    }

    public IEnumerable<Order> GetByCustomerId(int customerId) =>
        _orders.Where(o => o.CustomerId == customerId).ToList();
}
