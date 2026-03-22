using ECommerceApi.Models;
using ECommerceApi.Repositories;

namespace ECommerceApi.Services;

public class OrderService : IOrderService
{
    private readonly IOrderRepository _orderRepository;
    private readonly IProductRepository _productRepository;

    private const decimal TaxRate = 0.08m;

    // TODO: Add email notification when order is placed

    public OrderService(IOrderRepository orderRepository, IProductRepository productRepository)
    {
        _orderRepository = orderRepository;
        _productRepository = productRepository;
    }

    public Order CreateOrder(Order order)
    {
        decimal subtotal = 0;

        foreach (var item in order.Items)
        {
            var product = _productRepository.GetById(item.ProductId);
            if (product == null)
                throw new InvalidOperationException($"Product with ID {item.ProductId} not found.");

            if (product.StockQuantity < item.Quantity)
                throw new InvalidOperationException($"Insufficient stock for product '{product.Name}'. Available: {product.StockQuantity}, Requested: {item.Quantity}.");

            item.UnitPrice = product.Price;
            product.StockQuantity -= item.Quantity;
            subtotal += item.UnitPrice * item.Quantity;
        }

        order.TotalAmount = subtotal + (subtotal * TaxRate);
        order.OrderDate = DateTime.UtcNow;
        order.Status = "Pending";

        return _orderRepository.Create(order);
    }

    public Order? GetById(int id) => _orderRepository.GetById(id);

    public IEnumerable<Order> GetByCustomerId(int customerId) =>
        _orderRepository.GetByCustomerId(customerId);
}
