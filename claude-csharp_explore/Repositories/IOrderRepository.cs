using ECommerceApi.Models;

namespace ECommerceApi.Repositories;

public interface IOrderRepository
{
    IEnumerable<Order> GetAll();
    Order? GetById(int id);
    Order Create(Order order);
    IEnumerable<Order> GetByCustomerId(int customerId);
}
