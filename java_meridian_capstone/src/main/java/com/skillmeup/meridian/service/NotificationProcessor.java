package com.skillmeup.meridian.service;

import com.azure.messaging.servicebus.ServiceBusReceivedMessage;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.skillmeup.meridian.dto.CustomerCreatedEvent;
import com.skillmeup.meridian.model.NotificationLog;
import com.skillmeup.meridian.repository.NotificationLogRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

/**
 * Processes CustomerCreatedEvent messages from Azure Service Bus.
 *
 * TODO Capstone Exercise 3: Implement processMessage() to:
 *   1. Deserialize the message body to CustomerCreatedEvent
 *   2. Save a NotificationLog entry
 *   3. Track a custom telemetry event (optional if TelemetryClient is available)
 */
@Service
public class NotificationProcessor {
    private static final Logger log = LoggerFactory.getLogger(NotificationProcessor.class);
    private final NotificationLogRepository notificationLogRepository;
    private final ObjectMapper objectMapper;

    public NotificationProcessor(NotificationLogRepository notificationLogRepository,
                                  ObjectMapper objectMapper) {
        this.notificationLogRepository = notificationLogRepository;
        this.objectMapper = objectMapper;
    }

    // TODO Exercise 3: Implement processMessage
    public void processMessage(ServiceBusReceivedMessage message) {
        // TODO: Deserialize message.getBody().toString() to CustomerCreatedEvent
        // TODO: Create NotificationLog and save
        // TODO: Log success
        log.info("Received message: {}", message.getMessageId());
    }
}
