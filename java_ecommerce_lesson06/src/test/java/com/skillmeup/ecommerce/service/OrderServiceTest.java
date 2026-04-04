package com.skillmeup.ecommerce.service;

import com.skillmeup.ecommerce.model.*;
import com.skillmeup.ecommerce.repository.OrderRepository;
import org.junit.jupiter.api.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.*;
import org.mockito.junit.jupiter.MockitoExtension;
import java.math.BigDecimal;
import java.util.List;
import java.util.Optional;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

// Exercise 1: Run this test — observe the mock setup pattern
// Exercise 2: Add a test: createOrderCallsProductServiceForEachItem()
// Exercise 3: Add a test: getOrderByIdThrowsWhenNotFound() — stub findById to return Optional.empty()
// Exercise 4: Add a test: confirmOrderSavesWithConfirmedStatus()
// Exercise 5: Use verify() to assert that orderRepository.save() was called exactly once in confirmOrder
@ExtendWith(MockitoExtension.class)
class OrderServiceTest {

    @Mock
    private OrderRepository orderRepository;

    @Mock
    private ProductService productService;

    @InjectMocks
    private OrderService orderService;

    private Product testProduct;

    @BeforeEach
    void setUp() {
        testProduct = new Product("Widget", new BigDecimal("10.00"), 50);
        testProduct.setId(1L);
    }

    @Test
    @DisplayName("getOrderById returns order when found")
    void getOrderByIdReturnsOrderWhenFound() {
        Order order = new Order(1L);
        order.setId(42L);
        when(orderRepository.findById(42L)).thenReturn(Optional.of(order));

        Order result = orderService.getOrderById(42L);

        assertEquals(42L, result.getId());
        verify(orderRepository).findById(42L);
    }

    // TODO Exercise 2: createOrderCallsProductServiceForEachItem()

    // TODO Exercise 3: getOrderByIdThrowsWhenNotFound()

    // TODO Exercise 4: confirmOrderSavesWithConfirmedStatus()

    // TODO Exercise 5: verify() assertion on save() call count
}
