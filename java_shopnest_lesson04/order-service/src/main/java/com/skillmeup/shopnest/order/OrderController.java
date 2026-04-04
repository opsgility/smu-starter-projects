package com.skillmeup.shopnest.order;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import java.util.List;
import java.util.Map;

@RestController @RequestMapping("/api/orders")
public class OrderController {
    private final OrderRepository repo;
    private final RestTemplate restTemplate;
    private static final String PRODUCT_SERVICE_URL = "http://localhost:8081/api/products";

    public OrderController(OrderRepository repo, RestTemplate restTemplate) {
        this.repo=repo; this.restTemplate=restTemplate;
    }

    @GetMapping public List<Order> getAll() { return repo.findAll(); }

    // TODO Exercise 1: Implement GET /api/orders/{id} — return order or 404
    @GetMapping("/{id}") public ResponseEntity<Order> getById(@PathVariable Long id) {
        return ResponseEntity.notFound().build(); // TODO: implement
    }

    // TODO Exercise 2: Implement POST /api/orders
    // - Call restTemplate.getForObject(PRODUCT_SERVICE_URL + "/" + request.productId, Map.class)
    // - If product not found (null), return 404
    // - Calculate totalPrice = product.price * request.quantity
    // - Save order and return 201
    @PostMapping public ResponseEntity<Order> createOrder(@RequestBody OrderRequest request) {
        return ResponseEntity.status(201).body(null); // TODO: implement
    }

    // TODO Exercise 3: Implement DELETE /api/orders/{id} — delete and return 204
    @DeleteMapping("/{id}") public ResponseEntity<Void> delete(@PathVariable Long id) {
        return ResponseEntity.noContent().build(); // TODO: implement
    }
}
