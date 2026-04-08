package com.skillmeup.ecommerce.integration;

import com.skillmeup.ecommerce.model.*;
import com.skillmeup.ecommerce.repository.ProductRepository;
import com.skillmeup.ecommerce.service.OrderService;
import org.junit.jupiter.api.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.transaction.annotation.Transactional;
import java.math.BigDecimal;
import java.util.List;
import static org.junit.jupiter.api.Assertions.*;

// Exercise 1: Run this test to confirm @SpringBootTest + @Transactional rollback works
// Exercise 2: Add a test: createOrderWithMultipleItemsCalculatesTotalCorrectly()
// Exercise 3: Add Testcontainers PostgreSQL support (replace H2 with real Postgres)
// Exercise 4: Add a test: invalidProductIdReturns404()
@SpringBootTest
@Transactional
class OrderIntegrationTest {

    @Autowired
    private OrderService orderService;

    @Autowired
    private ProductRepository productRepository;

    private Product testProduct;

    @BeforeEach
    void setUp() {
        testProduct = productRepository.save(
            new Product("Integration Test Widget", new BigDecimal("49.99"), 100));
    }

    @Test
    @DisplayName("createOrder sets status to PENDING")
    void createOrderSetsPendingStatus() {
        List<OrderService.OrderItemRequest> requests = List.of(
            new OrderService.OrderItemRequest(testProduct.getId(), 2)
        );

        Order order = orderService.createOrder(1L, requests);

        assertNotNull(order.getId(), "Saved order should have a database ID");
        assertEquals(OrderStatus.PENDING, order.getStatus());
        assertEquals(1L, order.getCustomerId());
    }

    // TODO Exercise 2: createOrderWithMultipleItemsCalculatesTotalCorrectly()

    // TODO Exercise 3: Replace H2 with Testcontainers PostgreSQL
    //   Add @Testcontainers to class
    //   Add @Container static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16")
    //   Add @DynamicPropertySource to register datasource URL/username/password

    // TODO Exercise 4: invalidProductIdThrowsException()
    //   Call orderService.createOrder() with a non-existent productId
    //   Assert that an exception is thrown
}
