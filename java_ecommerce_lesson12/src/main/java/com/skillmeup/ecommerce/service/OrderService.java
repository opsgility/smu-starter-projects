package com.skillmeup.ecommerce.service;

import com.skillmeup.ecommerce.model.*;
import com.skillmeup.ecommerce.repository.OrderRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;

@Service
public class OrderService {
    private final OrderRepository orderRepository;
    private final ProductService productService;

    public OrderService(OrderRepository orderRepository, ProductService productService) {
        this.orderRepository = orderRepository;
        this.productService = productService;
    }

    public Order getOrderById(Long id) {
        return orderRepository.findById(id)
            .orElseThrow(() -> new IllegalArgumentException("Order not found: " + id));
    }

    public List<Order> getOrdersByCustomer(Long customerId) {
        return orderRepository.findByCustomerId(customerId);
    }

    @Transactional
    public Order createOrder(Long customerId, List<OrderItemRequest> itemRequests) {
        Order order = new Order(customerId);
        for (OrderItemRequest req : itemRequests) {
            Product product = productService.getProductById(req.productId());
            product.reduceStock(req.quantity());
            OrderItem item = new OrderItem(product, req.quantity(), product.getPrice());
            order.addItem(item);
        }
        return orderRepository.save(order);
    }

    @Transactional
    public Order confirmOrder(Long orderId) {
        Order order = getOrderById(orderId);
        order.confirm();
        return orderRepository.save(order);
    }

    @Transactional
    public Order cancelOrder(Long orderId) {
        Order order = getOrderById(orderId);
        order.cancel();
        return orderRepository.save(order);
    }

    public record OrderItemRequest(Long productId, int quantity) {}
}
