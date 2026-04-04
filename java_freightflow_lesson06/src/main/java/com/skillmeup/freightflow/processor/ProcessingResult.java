package com.skillmeup.freightflow.processor;

import com.skillmeup.freightflow.model.OrderStatus;
import java.math.BigDecimal;
import java.time.Instant;

public record ProcessingResult(
    Long orderId,
    BigDecimal total,
    OrderStatus status,
    String errorMessage,
    Instant processedAt
) {
    public static ProcessingResult success(Long orderId, BigDecimal total) {
        return new ProcessingResult(orderId, total, OrderStatus.COMPLETED, null, Instant.now());
    }

    public static ProcessingResult failed(Long orderId, String error) {
        return new ProcessingResult(orderId, null, OrderStatus.FAILED, error, Instant.now());
    }

    public boolean isSuccess() {
        return status == OrderStatus.COMPLETED;
    }
}
