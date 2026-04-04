package com.skillmeup.ecommerce.controller;

import com.skillmeup.ecommerce.model.ReturnOrder;
import com.skillmeup.ecommerce.service.ReturnOrderService;
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

// CAPSTONE EXERCISES — Write MockMvc tests for ReturnOrderController
// Exercise 6: POST /api/returns returns 201 with the created ReturnOrder
//   - Use mockMvc.perform(post(...).contentType(JSON).content(json))
//   - Mock returnOrderService.requestReturn() to return a ReturnOrder
// Exercise 7: POST /api/returns/{id}/approve returns 200
// Exercise 8: GET /api/returns/order/{orderId} returns list of returns
// Exercise 9: POST /api/returns with bad request body returns 400
//   - Stub returnOrderService.requestReturn() to throw IllegalStateException
@WebMvcTest(ReturnOrderController.class)
class ReturnOrderControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private ReturnOrderService returnOrderService;

    @Autowired
    private ObjectMapper objectMapper;

    // TODO Exercise 6: POST /api/returns returns 201

    // TODO Exercise 7: POST /api/returns/{id}/approve returns 200

    // TODO Exercise 8: GET /api/returns/order/{orderId}

    // TODO Exercise 9: bad request returns 422
}
