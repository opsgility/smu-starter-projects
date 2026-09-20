package com.skillmeup.ecommerce.repository;

import com.skillmeup.ecommerce.model.ReturnOrder;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface ReturnOrderRepository extends JpaRepository<ReturnOrder, Long> {
    List<ReturnOrder> findByOrderId(Long orderId);
    List<ReturnOrder> findByStatus(ReturnOrder.ReturnStatus status);
}
