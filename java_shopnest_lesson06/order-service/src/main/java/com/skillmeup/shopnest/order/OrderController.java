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
    // TODO (lesson06 Exercise 1): Externalize this URL to application.properties as product.service.url
    // Then inject it with @Value("${product.service.url}") private String productServiceUrl;
    private static final String PRODUCT_SERVICE_URL = "http://localhost:8081/api/products";

    public OrderController(OrderRepository repo, RestTemplate restTemplate) {
        this.repo=repo; this.restTemplate=restTemplate;
    }

    @GetMapping public List<Order> getAll() { return repo.findAll(); }

    @GetMapping("/{id}") public ResponseEntity<Order> getById(@PathVariable Long id) {
        return repo.findById(id).map(ResponseEntity::ok).orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    // TODO (lesson08 Exercise 1): Add @CircuitBreaker(name="productService", fallbackMethod="createOrderFallback")
    public ResponseEntity<Order> createOrder(@RequestBody OrderRequest request) {
        @SuppressWarnings("unchecked")
        Map<String,Object> product = restTemplate.getForObject(PRODUCT_SERVICE_URL + "/" + request.productId, Map.class);
        if (product == null) return ResponseEntity.notFound().build();
        double price = ((Number) product.get("price")).doubleValue();
        Order order = new Order(request.productId, request.quantity, price * request.quantity);
        return ResponseEntity.status(201).body(repo.save(order));
    }

    // TODO (lesson08 Exercise 2): Add fallback method
    // public ResponseEntity<Order> createOrderFallback(OrderRequest req, Throwable t) {
    //     return ResponseEntity.status(503).body(null);
    // }

    @DeleteMapping("/{id}") public ResponseEntity<Void> delete(@PathVariable Long id) {
        repo.deleteById(id); return ResponseEntity.noContent().build();
    }
}
