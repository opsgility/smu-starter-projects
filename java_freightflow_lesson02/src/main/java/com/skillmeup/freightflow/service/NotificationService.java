package com.skillmeup.freightflow.service;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import java.util.concurrent.atomic.AtomicLong;

@Service
public class NotificationService {
    private static final Logger log = LoggerFactory.getLogger(NotificationService.class);
    private final AtomicLong notificationsSent = new AtomicLong(0);

    /**
     * Simulates sending an email notification.
     * Takes ~50ms to simulate network latency.
     */
    public void sendEmail(Long orderId) {
        try {
            Thread.sleep(50); // Simulate email API latency
            notificationsSent.incrementAndGet();
            log.debug("Notification sent for order {}", orderId);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new RuntimeException("Notification interrupted", e);
        }
    }

    public long getNotificationsSent() {
        return notificationsSent.get();
    }
}
