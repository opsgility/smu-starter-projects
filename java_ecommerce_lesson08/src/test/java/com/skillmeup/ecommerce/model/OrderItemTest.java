package com.skillmeup.ecommerce.model;

import org.junit.jupiter.api.*;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
import java.math.BigDecimal;
import static org.junit.jupiter.api.Assertions.*;

// Exercise 1: Run this test and observe it PASSES
// Exercise 2: Add a test: subtotalEqualsUnitPriceTimesQuantity()
// Exercise 3: Add @ParameterizedTest with @ValueSource(ints = {0, -1, 101}) to verify invalid quantities throw
// Exercise 4: Add a test: negativeUnitPriceThrowsException()
class OrderItemTest {

    @Test
    @DisplayName("Valid OrderItem is created successfully")
    void validOrderItemCreated() {
        Product product = new Product("Widget", new BigDecimal("9.99"), 50);
        OrderItem item = new OrderItem(product, 3, new BigDecimal("9.99"));
        assertNotNull(item);
        assertEquals(3, item.getQuantity());
    }

    // TODO Exercise 2: Add subtotalEqualsUnitPriceTimesQuantity()

    // TODO Exercise 3: Add @ParameterizedTest for invalid quantities

    // TODO Exercise 4: Add negativeUnitPriceThrowsException()
}
