package com.skillmeup.ecommerce.model;

import org.junit.jupiter.api.*;
import java.math.BigDecimal;
import static org.junit.jupiter.api.Assertions.*;

// Exercise 1: Run this test and observe it PASSES
// Exercise 2: Add a test: isInStockReturnsFalseWhenOutOfStock()
// Exercise 3: Add a test: reduceStockDecreasesQuantity()
// Exercise 4: Add a test: reduceStockThrowsWhenInsufficientStock()
// Exercise 5: Use assertAll() to verify multiple properties in a single test
class ProductTest {

    private Product product;

    @BeforeEach
    void setUp() {
        product = new Product("Widget", new BigDecimal("19.99"), 10);
    }

    @Test
    @DisplayName("Product with stock > 0 is in stock")
    void productWithStockIsInStock() {
        assertTrue(product.isInStock());
    }

    // TODO Exercise 2: Add isInStockReturnsFalseWhenOutOfStock()

    // TODO Exercise 3: Add reduceStockDecreasesQuantity()

    // TODO Exercise 4: Add reduceStockThrowsWhenInsufficientStock()

    // TODO Exercise 5: Use assertAll() test
}
