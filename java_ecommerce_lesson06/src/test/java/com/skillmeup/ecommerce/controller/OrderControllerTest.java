package com.skillmeup.ecommerce.controller;

import com.skillmeup.ecommerce.model.Order;
import com.skillmeup.ecommerce.service.OrderService;
import org.junit.jupiter.api.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;
import static org.mockito.Mockito.*;

// Exercise 1: Confirm this test passes as-is.
// Exercise 2: Add getOrderReturns404WhenNotFound() — stub orderService.getOrderById() to throw IllegalArgumentException
// Exercise 3: Add createOrderReturns201() — POST /api/orders with a request body
// Exercise 4: Write ProductController tests in ProductControllerTest.java
@WebMvcTest(OrderController.class)
class OrderControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private OrderService orderService;

    @Test
    @DisplayName("GET /api/orders/{id} returns 200 when order exists")
    void getOrderReturns200() throws Exception {
        Order order = new Order(1L);
        order.setId(1L);
        when(orderService.getOrderById(1L)).thenReturn(order);

        mockMvc.perform(MockMvcRequestBuilders.get("/api/orders/1"))
            .andExpect(MockMvcResultMatchers.status().isOk())
            .andExpect(MockMvcResultMatchers.jsonPath("$.customerId").value(1));
    }

    // TODO Exercise 2: getOrderReturns404WhenNotFound()

    // TODO Exercise 3: createOrderReturns201()
}
