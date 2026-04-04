package com.skillmeup.shopnest.product;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController @RequestMapping("/api/products")
public class ProductController {
    private final ProductRepository repo;
    public ProductController(ProductRepository repo) { this.repo=repo; }

    // TODO Exercise 1: Implement GET /api/products — return all products
    @GetMapping
    public List<Product> getAll() { return List.of(); }

    // TODO Exercise 2: Implement GET /api/products/{id} — return product or 404
    @GetMapping("/{id}")
    public ResponseEntity<Product> getById(@PathVariable Long id) { return ResponseEntity.notFound().build(); }

    // TODO Exercise 3: Implement POST /api/products — create and return 201
    // DELETE /api/products/{id} — delete and return 204
    @PostMapping
    public ResponseEntity<Product> create(@RequestBody Product p) { return ResponseEntity.status(201).body(null); }
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) { return ResponseEntity.noContent().build(); }
}
