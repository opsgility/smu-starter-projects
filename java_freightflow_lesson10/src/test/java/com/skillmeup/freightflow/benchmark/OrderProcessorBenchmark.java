package com.skillmeup.freightflow.benchmark;

import com.skillmeup.freightflow.model.Order;
import com.skillmeup.freightflow.processor.OrderProcessor;
import com.skillmeup.freightflow.processor.ProcessingResult;
import com.skillmeup.freightflow.service.ProductPricingService;
import org.openjdk.jmh.annotations.*;
import org.openjdk.jmh.infra.Blackhole;
import java.math.BigDecimal;
import java.util.List;
import java.util.concurrent.TimeUnit;

/**
 * JMH Benchmark for the FreightFlow Order Processor.
 *
 * TODO Exercise 2: Create this class annotated with @BenchmarkMode, @OutputTimeUnit, @State(Scope.Benchmark)
 * TODO Exercise 3: Write a @Benchmark method calling orderProcessor.processAllOrders(sampleOrders)
 * TODO Exercise 4: Write a second @Benchmark for pricingService.getPrice() — run without cache, then with cache
 * TODO Exercise 5: Run with: mvn verify -Pbenchmark
 * TODO Exercise 6: Re-run with -prof gc and record allocation rate in BenchmarkRunner.java comments
 */
@BenchmarkMode(Mode.Throughput)
@OutputTimeUnit(TimeUnit.SECONDS)
@State(Scope.Benchmark)
@Fork(value = 1)
@Warmup(iterations = 2, time = 1)
@Measurement(iterations = 3, time = 2)
public class OrderProcessorBenchmark {

    private OrderProcessor orderProcessor;
    private ProductPricingService pricingService;
    private List<Order> sampleOrders;

    @Setup(Level.Trial)
    public void setup() {
        // TODO Exercise 3: Initialize orderProcessor with real or stub dependencies
        sampleOrders = BenchmarkRunner.generateSampleOrders(100);
    }

    // TODO Exercise 3: Add @Benchmark method for processAllOrders()
    // @Benchmark
    // public List<ProcessingResult> measureBatchProcessing() {
    //     return orderProcessor.processAllOrders(sampleOrders);
    // }

    // TODO Exercise 4: Add @Benchmark for getPrice() with and without cache
    // @Benchmark
    // public void measurePriceLookup(Blackhole bh) {
    //     bh.consume(pricingService.getPrice(42L));
    // }
}
