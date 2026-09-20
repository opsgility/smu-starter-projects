package com.skillmeup.freightflow.repository;

import com.skillmeup.freightflow.model.Order;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface OrderRepository extends JpaRepository<Order, Long> {
    List<Order> findByStatus(com.skillmeup.freightflow.model.OrderStatus status);
}
