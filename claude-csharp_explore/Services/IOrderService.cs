using ECommerceApi.Models;

namespace ECommerceApi.Services;

public interface IOrderService
{
    Order CreateOrder(Order order);
    Order? GetById(int id);
    IEnumerable<Order> GetByCustomerId(int customerId);
}
