package com.skillmeup.ecommerce;

import com.skillmeup.ecommerce.model.*;
import com.skillmeup.ecommerce.repository.*;
import com.skillmeup.ecommerce.service.*;
import org.junit.jupiter.api.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.transaction.annotation.Transactional;
import java.math.BigDecimal;
import java.util.List;
import static org.junit.jupiter.api.Assertions.*;

// Exercise 1: Run this test — @SpringBootTest loads the FULL application context
// Exercise 2: Add a test: fullOrderLifecycle_createConfirmShip() using all three service calls
// Exercise 3: Add a test: cancelledOrderCannotBeConfirmed() - verify the exception propagates
// Exercise 4: Add a test: productStockReducedAfterOrderCreation()
// Exercise 5: Observe that @Transactional rolls back — verify the DB is clean after each test
@SpringBootTest
@ActiveProfiles("test")
@Transactional
class OrderIntegrationTest {

    @Autowired
    private OrderService orderService;

    @Autowired
    private ProductService productService;

    @Autowired
    private ProductRepository productRepository;

    @Autowired
    private OrderRepository orderRepository;

    private Product savedProduct;

    @BeforeEach
    void setUp() {
        savedProduct = productRepository.save(
            new Product("Integration Widget", new BigDecimal("25.00"), 100)
        );
    }

    @Test
    @DisplayName("Create order sets status to PENDING")
    void createOrderSetsPendingStatus() {
        List<OrderService.OrderItemRequest> items =
            List.of(new OrderService.OrderItemRequest(savedProduct.getId(), 2));

        Order order = orderService.createOrder(1L, items);

        assertNotNull(order.getId());
        assertEquals(OrderStatus.PENDING, order.getStatus());
        assertEquals(new BigDecimal("50.00"), order.calculateTotal());
    }

    // TODO Exercise 2: fullOrderLifecycle_createConfirmShip()

    // TODO Exercise 3: cancelledOrderCannotBeConfirmed()

    // TODO Exercise 4: productStockReducedAfterOrderCreation()

    // TODO Exercise 5: (observation — note how @Transactional rolls back between tests)
}
