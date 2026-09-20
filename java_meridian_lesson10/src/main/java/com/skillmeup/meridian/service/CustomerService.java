package com.skillmeup.meridian.service;

import com.azure.messaging.servicebus.ServiceBusMessage;
import com.azure.messaging.servicebus.ServiceBusSenderClient;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.skillmeup.meridian.dto.CustomerCreatedEvent;
import com.skillmeup.meridian.model.Customer;
import com.skillmeup.meridian.repository.CustomerRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import java.util.List;
import java.util.UUID;

@Service
public class CustomerService {
    private static final Logger log = LoggerFactory.getLogger(CustomerService.class);
    private final CustomerRepository customerRepository;
    private final ServiceBusSenderClient senderClient;
    private final ObjectMapper objectMapper;

    public CustomerService(CustomerRepository customerRepository,
                           ServiceBusSenderClient senderClient,
                           ObjectMapper objectMapper) {
        this.customerRepository = customerRepository;
        this.senderClient = senderClient;
        this.objectMapper = objectMapper;
    }

    public List<Customer> getAllCustomers() {
        return customerRepository.findAll();
    }

    public Customer getCustomerById(Long id) {
        return customerRepository.findById(id)
            .orElseThrow(() -> new IllegalArgumentException("Customer not found: " + id));
    }

    public Customer createCustomer(Customer customer) {
        if (customerRepository.existsByEmail(customer.getEmail())) {
            throw new IllegalArgumentException("Email already registered: " + customer.getEmail());
        }
        Customer saved = customerRepository.save(customer);

        // TODO Exercise 5: Uncomment to send a CustomerCreatedEvent to Service Bus
        // try {
        //     String json = objectMapper.writeValueAsString(
        //         new CustomerCreatedEvent(saved.getId(), saved.getEmail()));
        //     ServiceBusMessage message = new ServiceBusMessage(json)
        //         .setContentType("application/json")
        //         .setMessageId(UUID.randomUUID().toString());
        //     senderClient.sendMessage(message);
        // } catch (JsonProcessingException e) {
        //     log.warn("Failed to serialize customer event for {}", saved.getId());
        // }

        return saved;
    }

    public void deleteCustomer(Long id) {
        customerRepository.deleteById(id);
    }
}
