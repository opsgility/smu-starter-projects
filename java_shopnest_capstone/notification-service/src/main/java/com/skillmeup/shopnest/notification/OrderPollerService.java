package com.skillmeup.shopnest.notification;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

@Service
public class OrderPollerService {
    private final RestTemplate restTemplate = new RestTemplate();
    private final Set<Object> seenOrders = new HashSet<>();
    private static final String ORDER_URL = "http://order-service:8082/api/orders";

    // TODO Capstone Exercise 1: Implement the polling logic.
    // @Scheduled(fixedDelay = 10000)
    // public void pollOrders() — GET orders from ORDER_URL,
    //   for each order with status PENDING and id not in seenOrders:
    //     log "New order: " + order.id + " for product " + order.productId
    //     add to seenOrders
    @Scheduled(fixedDelay = 10000)
    public void pollOrders() {
        // TODO: implement polling
    }
}
