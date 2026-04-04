package com.skillmeup.ecommerce.service;

import com.skillmeup.ecommerce.model.Product;
import com.skillmeup.ecommerce.repository.ProductRepository;
import org.springframework.stereotype.Service;
import java.math.BigDecimal;
import java.util.List;

@Service
public class ProductService {
    private final ProductRepository productRepository;

    public ProductService(ProductRepository productRepository) {
        this.productRepository = productRepository;
    }

    public List<Product> getAllProducts() {
        return productRepository.findAll();
    }

    public List<Product> getAvailableProducts() {
        return productRepository.findByStockQuantityGreaterThan(0);
    }

    public Product getProductById(Long id) {
        return productRepository.findById(id)
            .orElseThrow(() -> new IllegalArgumentException("Product not found: " + id));
    }

    public Product createProduct(Product product) {
        if (product.getPrice().compareTo(BigDecimal.ZERO) < 0) {
            throw new IllegalArgumentException("Product price cannot be negative");
        }
        return productRepository.save(product);
    }

    public Product updateStock(Long productId, int delta) {
        Product product = getProductById(productId);
        int newStock = product.getStockQuantity() + delta;
        if (newStock < 0) {
            throw new IllegalStateException("Insufficient stock");
        }
        product.setStockQuantity(newStock);
        return productRepository.save(product);
    }
}
