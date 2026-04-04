package com.skillmeup.ecommerce.model;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "return_orders")
public class ReturnOrder {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private Long orderId;

    @Column(nullable = false)
    private String reason;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private ReturnStatus status = ReturnStatus.REQUESTED;

    @Column(nullable = false)
    private LocalDateTime requestedAt = LocalDateTime.now();

    public enum ReturnStatus {
        REQUESTED, APPROVED, REJECTED, COMPLETED
    }

    public ReturnOrder() {}

    public ReturnOrder(Long orderId, String reason) {
        if (reason == null || reason.isBlank()) {
            throw new IllegalArgumentException("Return reason cannot be blank");
        }
        this.orderId = orderId;
        this.reason = reason;
    }

    public void approve() {
        if (status != ReturnStatus.REQUESTED) {
            throw new IllegalStateException("Only REQUESTED returns can be approved");
        }
        this.status = ReturnStatus.APPROVED;
    }

    public void reject(String rejectionReason) {
        if (status != ReturnStatus.REQUESTED) {
            throw new IllegalStateException("Only REQUESTED returns can be rejected");
        }
        this.status = ReturnStatus.REJECTED;
    }

    // Getters and setters
    public Long getId() { return id; }
    public Long getOrderId() { return orderId; }
    public String getReason() { return reason; }
    public ReturnStatus getStatus() { return status; }
    public void setStatus(ReturnStatus status) { this.status = status; }
    public LocalDateTime getRequestedAt() { return requestedAt; }
}
