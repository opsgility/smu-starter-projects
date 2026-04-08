package com.skillmeup.ecommerce.domain;

import com.skillmeup.ecommerce.model.*;
import org.junit.jupiter.api.*;
import java.math.BigDecimal;
import static org.junit.jupiter.api.Assertions.*;

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
    @DisplayName("New order belongs to customer")
    void newOrderBelongsToCustomer() {
        assertEquals(101L, order.getCustomerId());
    }

    // TODO Exercise 1: Implement newOrderHasEmptyItemsList
    // @Test
    // @DisplayName("New order has empty items list")
    // void newOrderHasEmptyItemsList() {
    //     assertTrue(order.getItems().isEmpty(),
    //         "A new order should have no items");
    // }

    // TODO Exercise 1: Implement addingItemIncreasesTotal
    // @Test
    // @DisplayName("Adding an item increases the order total")
    // void addingItemIncreasesTotal() {
    //     Product product = new Product("Test Item", new BigDecimal("29.99"), 10);
    //     OrderItem item = new OrderItem(product, 2, new BigDecimal("29.99"));
    //     order.addItem(item);
    //     assertEquals(0,
    //         new BigDecimal("59.98").compareTo(order.calculateTotal()),
    //         "Total should be 2 x 29.99 = 59.98");
    // }
}
