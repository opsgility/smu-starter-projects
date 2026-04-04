package com.skillmeup.ecommerce.service;

import com.skillmeup.ecommerce.model.*;
import com.skillmeup.ecommerce.repository.OrderRepository;
import com.skillmeup.ecommerce.repository.ReturnOrderRepository;
import org.junit.jupiter.api.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.*;
import org.mockito.junit.jupiter.MockitoExtension;
import java.util.Optional;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

// CAPSTONE EXERCISES — Write all tests in this class
// Exercise 1: requestReturnSucceedsForDeliveredOrder()
//   - Mock orderRepository.findById() to return an Order with status DELIVERED
//   - Mock returnOrderRepository.save() to return a ReturnOrder
//   - Call returnOrderService.requestReturn(orderId, reason)
//   - Verify the saved ReturnOrder has status REQUESTED
// Exercise 2: requestReturnThrowsForNonDeliveredOrder()
//   - Mock order with status CONFIRMED
//   - Assert requestReturn() throws IllegalStateException
// Exercise 3: approveReturnChangesOrderStatusToReturned()
//   - Mock returnRepository to return a REQUESTED ReturnOrder
//   - Call approveReturn()
//   - Verify orderRepository.save() was called with order status RETURNED
// Exercise 4: rejectReturnChangesStatusToRejected()
//   - Mock returnRepository to return a REQUESTED ReturnOrder
//   - Call rejectReturn()
//   - Verify status is REJECTED
// Exercise 5: blankReturnReasonThrowsException()
//   - Mock order with DELIVERED status
//   - Call requestReturn(orderId, "") — assert IllegalArgumentException
@ExtendWith(MockitoExtension.class)
class ReturnOrderServiceTest {

    @Mock
    private ReturnOrderRepository returnOrderRepository;

    @Mock
    private OrderRepository orderRepository;

    @InjectMocks
    private ReturnOrderService returnOrderService;

    // TODO Exercise 1: requestReturnSucceedsForDeliveredOrder()

    // TODO Exercise 2: requestReturnThrowsForNonDeliveredOrder()

    // TODO Exercise 3: approveReturnChangesOrderStatusToReturned()

    // TODO Exercise 4: rejectReturnChangesStatusToRejected()

    // TODO Exercise 5: blankReturnReasonThrowsException()
}
