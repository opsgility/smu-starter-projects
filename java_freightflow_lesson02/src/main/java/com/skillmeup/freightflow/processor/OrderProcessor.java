package com.skillmeup.freightflow.processor;

import com.skillmeup.freightflow.model.Order;
import com.skillmeup.freightflow.service.NotificationService;
import com.skillmeup.freightflow.service.ProductPricingService;
import org.springframework.stereotype.Component;
import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;

/**
 * Processes orders sequentially.
 * This is the BASELINE implementation — every optimization starts here.
 *
 * TODO Exercise 2: Create a ThreadPoolExecutor with Runtime.getRuntime().availableProcessors() threads
 * TODO Exercise 3: Submit each order as a Callable<ProcessingResult> to the executor
 * TODO Exercise 4: Collect all Future<ProcessingResult> objects and call .get() to gather results
 * TODO Exercise 5: Shut down the executor with shutdown() and awaitTermination()
 * TODO Exercise 6: Run BenchmarkRunner before and after — record throughput improvement above
 */
@Component
public class OrderProcessor {
    private final ProductPricingService pricingService;
    private final NotificationService notificationService;

    public OrderProcessor(ProductPricingService pricingService,
                         NotificationService notificationService) {
        this.pricingService = pricingService;
        this.notificationService = notificationService;
    }

    public List<ProcessingResult> processAllOrders(List<Order> orders) {
        List<ProcessingResult> results = new ArrayList<>();

        // TODO Exercise 2-5: Replace this sequential loop with ThreadPoolExecutor
        for (Order order : orders) {
            results.add(processOrder(order));
        }

        return results;
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
