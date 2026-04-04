package com.skillmeup.meridian.model;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "notification_log")
public class NotificationLog {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private Long customerId;

    @Column(nullable = false)
    private String email;

    @Column(nullable = false)
    private LocalDateTime processedAt = LocalDateTime.now();

    @Column(nullable = false)
    private String status;

    public NotificationLog() {}
    public NotificationLog(Long customerId, String email, String status) {
        this.customerId = customerId;
        this.email = email;
        this.status = status;
    }

    public Long getId() { return id; }
    public Long getCustomerId() { return customerId; }
    public String getEmail() { return email; }
    public LocalDateTime getProcessedAt() { return processedAt; }
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
}
