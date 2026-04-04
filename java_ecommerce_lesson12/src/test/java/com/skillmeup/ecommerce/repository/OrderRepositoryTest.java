package com.skillmeup.ecommerce.repository;

import com.skillmeup.ecommerce.model.*;
import org.junit.jupiter.api.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.boot.test.autoconfigure.orm.jpa.TestEntityManager;
import java.math.BigDecimal;
import java.util.List;
import static org.junit.jupiter.api.Assertions.*;

// Exercise 1: Run this test — @DataJpaTest loads only JPA layer with embedded H2
// Exercise 2: Add a test: findByStatusReturnsPendingOrders()
// Exercise 3: Add a test: findByCustomerIdWithItemsLoadsItems() using findByCustomerIdWithItems()
// Exercise 4: Add a test: saveOrderPersistsItems() — save an order with items, flush, reload
@DataJpaTest
class OrderRepositoryTest {

    @Autowired
    private TestEntityManager em;

    @Autowired
    private OrderRepository orderRepository;

    @Test
    @DisplayName("findByCustomerId returns orders for that customer")
    void findByCustomerIdReturnsOrders() {
        Order order = new Order(99L);
        em.persistAndFlush(order);

        List<Order> results = orderRepository.findByCustomerId(99L);

        assertEquals(1, results.size());
        assertEquals(99L, results.get(0).getCustomerId());
    }

    // TODO Exercise 2: findByStatusReturnsPendingOrders()

    // TODO Exercise 3: findByCustomerIdWithItemsLoadsItems()

    // TODO Exercise 4: saveOrderPersistsItems()
}
