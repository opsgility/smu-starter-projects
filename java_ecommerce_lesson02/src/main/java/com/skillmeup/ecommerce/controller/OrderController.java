package com.skillmeup.ecommerce.controller;

import com.skillmeup.ecommerce.model.Order;
import com.skillmeup.ecommerce.service.OrderService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/orders")
public class OrderController {
    private final OrderService orderService;

    public OrderController(OrderService orderService) {
        this.orderService = orderService;
    }

    @GetMapping("/{id}")
    public ResponseEntity<Order> getOrder(@PathVariable Long id) {
        return ResponseEntity.ok(orderService.getOrderById(id));
    }

    @GetMapping("/customer/{customerId}")
    public ResponseEntity<List<Order>> getOrdersByCustomer(@PathVariable Long customerId) {
        return ResponseEntity.ok(orderService.getOrdersByCustomer(customerId));
    }

    @PostMapping
    public ResponseEntity<Order> createOrder(@RequestBody CreateOrderRequest request) {
        List<OrderService.OrderItemRequest> itemRequests = request.items().stream()
            .map(i -> new OrderService.OrderItemRequest(i.productId(), i.quantity()))
            .toList();
        Order order = orderService.createOrder(request.customerId(), itemRequests);
        return ResponseEntity.status(201).body(order);
    }

    @PostMapping("/{id}/confirm")
    public ResponseEntity<Order> confirmOrder(@PathVariable Long id) {
        return ResponseEntity.ok(orderService.confirmOrder(id));
    }

    @PostMapping("/{id}/cancel")
    public ResponseEntity<Order> cancelOrder(@PathVariable Long id) {
        return ResponseEntity.ok(orderService.cancelOrder(id));
    }

    public record CreateOrderRequest(Long customerId, List<ItemRequest> items) {}
    public record ItemRequest(Long productId, int quantity) {}
}
