package com.skillmeup.ecommerce.controller;

import com.skillmeup.ecommerce.model.*;
import com.skillmeup.ecommerce.service.OrderService;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

// Exercise 1: Run this test — observe @WebMvcTest loads only the web layer
// Exercise 2: Add a test: getOrderReturns404WhenNotFound() — stub to throw IllegalArgumentException, expect 400
// Exercise 3: Add a test: createOrderReturns201WithBody()
// Exercise 4: Add a test: confirmOrderReturns200()
// Exercise 5: Add a test: cancelOrderReturns200()
@WebMvcTest(OrderController.class)
class OrderControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private OrderService orderService;

    @Autowired
    private ObjectMapper objectMapper;

    @Test
    @DisplayName("GET /api/orders/{id} returns 200 with order")
    void getOrderReturns200() throws Exception {
        Order order = new Order(1L);
        order.setId(1L);
        when(orderService.getOrderById(1L)).thenReturn(order);

        mockMvc.perform(get("/api/orders/1"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.customerId").value(1));
    }

    // TODO Exercise 2: getOrderReturns400WhenNotFound()

    // TODO Exercise 3: createOrderReturns201WithBody()

    // TODO Exercise 4: confirmOrderReturns200()

    // TODO Exercise 5: cancelOrderReturns200()
}
