package com.skillmeup.ecommerce.repository;

import com.skillmeup.ecommerce.model.*;
import org.junit.jupiter.api.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.boot.test.autoconfigure.orm.jpa.TestEntityManager;
import java.util.List;
import static org.junit.jupiter.api.Assertions.*;

// Exercise 1: Confirm this test passes as-is.
// Exercise 2: Add findByStatus_returnsOnlyMatchingOrders() — persist orders with different statuses
// Exercise 3: Add findByStatus_withPagination() — use Pageable and verify Page metadata
// Exercise 4: Add ProductRepository low-stock query test in ProductRepositoryTest.java
@DataJpaTest
class OrderRepositoryTest {

    @Autowired
    private TestEntityManager em;

    @Autowired
    private OrderRepository orderRepository;

    @Test
    @DisplayName("findByCustomerId returns orders for that customer")
    void findByCustomerIdReturnsOrders() {
        // Arrange: persist 2 orders for customer 1 and 1 order for customer 2
        Order order1 = em.persistAndFlush(new Order(1L));
        Order order2 = em.persistAndFlush(new Order(1L));
        Order order3 = em.persistAndFlush(new Order(2L));

        // Act
        List<Order> customer1Orders = orderRepository.findByCustomerId(1L);

        // Assert
        assertEquals(2, customer1Orders.size(),
            "Customer 1 should have 2 orders");
        assertTrue(customer1Orders.stream().allMatch(o -> o.getCustomerId().equals(1L)));
    }

    // TODO Exercise 2: findByStatus_returnsOnlyMatchingOrders()

    // TODO Exercise 3: findByStatus_withPagination()
}
