package com.skillmeup.ecommerce.model;

import org.junit.jupiter.api.*;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
import java.math.BigDecimal;
import static org.junit.jupiter.api.Assertions.*;

// Exercise 1: Run this test class and observe all tests PASS
// Exercise 2: Add a test: newOrderHasEmptyItemsList()
// Exercise 3: Add a test: addingItemIncreasesTotal() - add an item, verify calculateTotal() returns unitPrice * quantity
// Exercise 4: Add a test: confirmingEmptyOrderThrowsException() using assertThrows
// Exercise 5: Add a test: cannotShipUnconfirmedOrder() - ship() on PENDING order throws IllegalStateException
// Exercise 6: Add @ParameterizedTest using @ValueSource to test that ship() fails for PENDING, CANCELLED, DELIVERED statuses
class OrderTest {

    private Order order;

    @BeforeEach
    void setUp() {
        order = new Order(101L);
    }

    @Test
    @DisplayName("New order has PENDING status")
    void newOrderHasPendingStatus() {
        assertEquals(OrderStatus.PENDING, order.getStatus());
    }

    @Test
    @DisplayName("New order belongs to the correct customer")
    void newOrderBelongsToCustomer() {
        assertEquals(101L, order.getCustomerId());
    }

    // TODO Exercise 2: Add newOrderHasEmptyItemsList() test

    // TODO Exercise 3: Add addingItemIncreasesTotal() test

    // TODO Exercise 4: Add confirmingEmptyOrderThrowsException() test

    // TODO Exercise 5: Add cannotShipUnconfirmedOrder() test

    // TODO Exercise 6: Add @ParameterizedTest for invalid ship() statuses
}
