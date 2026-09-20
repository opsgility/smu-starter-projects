package com.skillmeup.freightflow.processor;

import com.skillmeup.freightflow.model.Order;
import com.skillmeup.freightflow.service.NotificationService;
import com.skillmeup.freightflow.service.ProductPricingService;
import org.springframework.stereotype.Component;
import java.math.BigDecimal;
import java.util.*;
import java.util.concurrent.*;

/**
 * Processes orders with HikariCP + batch inserts. Throughput: ~1,400 orders/sec.
 *
 * TODO Exercise 1: Add caffeine and spring-boot-starter-cache to pom.xml
 * TODO Exercise 2: Add @EnableCaching to Application.java
 * TODO Exercise 3: Configure CaffeineCacheManager bean in AppConfig.java (maximumSize=1000, expireAfterWrite=5m)
 * TODO Exercise 4: Annotate ProductPricingService.getPrice() with @Cacheable("prices")
 * TODO Exercise 5: Add cache stats log in BenchmarkRunner using Cache.stats()
 * TODO Exercise 6: Run the benchmark twice — second run should show ~100% cache hit rate
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
