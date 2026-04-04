package com.skillmeup.ecommerce.repository;

import com.skillmeup.ecommerce.model.Product;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import java.util.List;

public interface ProductRepository extends JpaRepository<Product, Long> {
    List<Product> findByStockQuantityGreaterThan(int quantity);

    @Query("SELECT p FROM Product p WHERE p.price <= :maxPrice ORDER BY p.price ASC")
    List<Product> findAffordableProducts(java.math.BigDecimal maxPrice);
}
