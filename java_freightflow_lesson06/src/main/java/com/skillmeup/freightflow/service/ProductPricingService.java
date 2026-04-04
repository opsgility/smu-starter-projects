package com.skillmeup.freightflow.service;

import org.springframework.stereotype.Service;
import java.math.BigDecimal;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

@Service
public class ProductPricingService {
    // Simulate a product price database
    private static final Map<Long, BigDecimal> PRICES = new ConcurrentHashMap<>();
    static {
        for (long i = 1; i <= 1000; i++) {
            PRICES.put(i, BigDecimal.valueOf(10 + (i % 90)));
        }
    }

    /**
     * Get the price for a product.
     * Simulates a slow DB/API lookup with a 5ms delay.
     *
     * TODO Lesson 8 Exercise 4: Add @Cacheable("prices") annotation to cache results
     */
    public BigDecimal getPrice(Long productId) {
        try {
            Thread.sleep(5); // Simulate DB lookup latency
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        return PRICES.getOrDefault(productId, new BigDecimal("9.99"));
    }
}
