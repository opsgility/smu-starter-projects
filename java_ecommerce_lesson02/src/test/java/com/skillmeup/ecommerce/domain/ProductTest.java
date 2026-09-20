package com.skillmeup.ecommerce.domain;

import com.skillmeup.ecommerce.model.OrderItem;
import com.skillmeup.ecommerce.model.Product;
import org.junit.jupiter.api.*;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
import java.math.BigDecimal;
import static org.junit.jupiter.api.Assertions.*;

class ProductTest {

    private Product product;

    @BeforeEach
    void setUp() {
        product = new Product("Test Widget", new BigDecimal("25.00"), 10);
    }

    // TODO Exercise 3: Implement productWithStockIsInStock
    // @Test
    // @DisplayName("Product with stock is in stock")
    // void productWithStockIsInStock() {
    //     assertTrue(product.isInStock(),
    //         "Product with stockQuantity=10 should report isInStock()=true");
    // }

    // TODO Exercise 3: Implement productWithZeroStockIsNotInStock
    // @Test
    // @DisplayName("Product with zero stock is not in stock")
    // void productWithZeroStockIsNotInStock() {
    //     Product outOfStock = new Product("Empty Widget", new BigDecimal("25.00"), 0);
    //     assertFalse(outOfStock.isInStock(),
    //         "Product with stockQuantity=0 should report isInStock()=false");
    // }

    // TODO Exercise 3: Implement invalidQuantitiesAreRejected using @ParameterizedTest
    // @ParameterizedTest(name = "Quantity {0} should be rejected")
    // @ValueSource(ints = {0, -1, -100, 101})
    // @DisplayName("Invalid quantities are rejected by OrderItem constructor")
    // void invalidQuantitiesAreRejected(int quantity) {
    //     assertThrows(
    //         IllegalArgumentException.class,
    //         () -> new OrderItem(product, quantity, new BigDecimal("25.00")),
    //         "Quantity " + quantity + " should throw IllegalArgumentException"
    //     );
    // }

    // TODO Exercise 3: Implement reduceStockThrowsWhenInsufficient
    // @Test
    // @DisplayName("reduceStock throws when quantity exceeds available stock")
    // void reduceStockThrowsWhenInsufficient() {
    //     assertThrows(
    //         IllegalStateException.class,
    //         () -> product.reduceStock(11),
    //         "reduceStock(11) should throw when only 10 in stock"
    //     );
    // }
}
