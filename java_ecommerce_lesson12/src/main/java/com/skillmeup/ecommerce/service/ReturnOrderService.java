package com.skillmeup.ecommerce.service;

import com.skillmeup.ecommerce.model.Order;
import com.skillmeup.ecommerce.model.OrderStatus;
import com.skillmeup.ecommerce.model.ReturnOrder;
import com.skillmeup.ecommerce.repository.OrderRepository;
import com.skillmeup.ecommerce.repository.ReturnOrderRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;

@Service
public class ReturnOrderService {
    private final ReturnOrderRepository returnOrderRepository;
    private final OrderRepository orderRepository;

    public ReturnOrderService(ReturnOrderRepository returnOrderRepository,
                              OrderRepository orderRepository) {
        this.returnOrderRepository = returnOrderRepository;
        this.orderRepository = orderRepository;
    }

    public ReturnOrder getReturnById(Long id) {
        return returnOrderRepository.findById(id)
            .orElseThrow(() -> new IllegalArgumentException("Return not found: " + id));
    }

    public List<ReturnOrder> getReturnsByOrder(Long orderId) {
        return returnOrderRepository.findByOrderId(orderId);
    }

    @Transactional
    public ReturnOrder requestReturn(Long orderId, String reason) {
        Order order = orderRepository.findById(orderId)
            .orElseThrow(() -> new IllegalArgumentException("Order not found: " + orderId));
        if (order.getStatus() != OrderStatus.DELIVERED) {
            throw new IllegalStateException("Only DELIVERED orders can be returned");
        }
        ReturnOrder returnOrder = new ReturnOrder(orderId, reason);
        return returnOrderRepository.save(returnOrder);
    }

    @Transactional
    public ReturnOrder approveReturn(Long returnId) {
        ReturnOrder returnOrder = getReturnById(returnId);
        returnOrder.approve();
        // Update original order status
        Order order = orderRepository.findById(returnOrder.getOrderId()).orElseThrow();
        order.setStatus(OrderStatus.RETURNED);
        orderRepository.save(order);
        return returnOrderRepository.save(returnOrder);
    }

    @Transactional
    public ReturnOrder rejectReturn(Long returnId, String reason) {
        ReturnOrder returnOrder = getReturnById(returnId);
        returnOrder.reject(reason);
        return returnOrderRepository.save(returnOrder);
    }
}
