package com.skillmeup.freightflow.service;

import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;
import java.math.BigDecimal;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

@Service
public class ProductPricingService {
    private static final Map<Long, BigDecimal> PRICES = new ConcurrentHashMap<>();
    static {
        for (long i = 1; i <= 1000; i++) {
            PRICES.put(i, BigDecimal.valueOf(10 + (i % 90)));
        }
    }

    @Cacheable("prices")
    public BigDecimal getPrice(Long productId) {
        try {
            Thread.sleep(5);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        return PRICES.getOrDefault(productId, new BigDecimal("9.99"));
    }
}
