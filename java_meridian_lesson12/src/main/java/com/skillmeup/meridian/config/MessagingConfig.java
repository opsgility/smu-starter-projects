package com.skillmeup.meridian.config;

import com.azure.messaging.servicebus.ServiceBusClientBuilder;
import com.azure.messaging.servicebus.ServiceBusSenderClient;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * Azure Service Bus configuration.
 *
 * TODO Capstone Exercise 4: Add ServiceBusProcessorClient bean wired to
 * NotificationProcessor.processMessage(); call .start() in @PostConstruct
 */
@Configuration
public class MessagingConfig {

    @Bean
    public ServiceBusSenderClient serviceBusSenderClient(
            @Value("${azure.servicebus.connection-string}") String connectionString) {
        return new ServiceBusClientBuilder()
            .connectionString(connectionString)
            .sender()
            .queueName("customer-events")
            .buildClient();
    }

    // TODO Capstone Exercise 4: Add ServiceBusProcessorClient bean
    // @Bean
    // public ServiceBusProcessorClient serviceBusProcessorClient(...) { ... }
}
