package com.skillmeup.freightflow.processor;

import com.skillmeup.freightflow.model.Order;
import com.skillmeup.freightflow.service.NotificationService;
import com.skillmeup.freightflow.service.ProductPricingService;
import org.springframework.stereotype.Component;
import java.math.BigDecimal;
import java.util.*;
import java.util.concurrent.*;

/**
 * Processes orders with HikariCP + batch inserts + Caffeine caching. Throughput: ~3,200 orders/sec.
 *
 * Completed from prior lessons:
 *   - spring-boot-starter-cache + caffeine dependencies in pom.xml
 *   - @EnableCaching on Application.java
 *   - CaffeineCacheManager configured in AppConfig.java (maximumSize=1000, expireAfterWrite=5m)
 *   - ProductPricingService.getPrice() annotated with @Cacheable("prices")
 *
 * Lesson 12 exercises focus on GC tuning to reduce pause times.
 */
@Component
public class OrderProcessor {
    private final ProductPricingService pricingService;
    private final NotificationService notificationService;
    private final ExecutorService executor;

    public OrderProcessor(ProductPricingService pricingService,
                         NotificationService notificationService) {
        this.pricingService = pricingService;
        this.notificationService = notificationService;
        int threads = Runtime.getRuntime().availableProcessors();
        this.executor = new ThreadPoolExecutor(
            threads, threads * 2,
            60L, TimeUnit.SECONDS,
            new ArrayBlockingQueue<>(500),
            new ThreadPoolExecutor.CallerRunsPolicy()
        );
    }

    public List<ProcessingResult> processAllOrders(List<Order> orders) {
        List<CompletableFuture<ProcessingResult>> futures = orders.stream()
            .map(order -> CompletableFuture
                .supplyAsync(() -> processOrder(order), executor)
                .exceptionally(ex -> ProcessingResult.failed(order.getId(), ex.getMessage())))
            .toList();

        CompletableFuture.allOf(futures.toArray(new CompletableFuture[0])).join();
        return futures.stream().map(CompletableFuture::join).toList();
    }

    private ProcessingResult processOrder(Order order) {
        try {
            BigDecimal price = pricingService.getPrice(order.getProductId());
            BigDecimal total = price.multiply(BigDecimal.valueOf(order.getQuantity()));
            notificationService.sendEmail(order.getId());
            return ProcessingResult.success(order.getId(), total);
        } catch (Exception e) {
            return ProcessingResult.failed(order.getId(), e.getMessage());
        }
    }
}
