package com.skillmeup.ecommerce.service;

import org.junit.jupiter.api.*;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import java.math.BigDecimal;
import static org.junit.jupiter.api.Assertions.*;

// This test was written FIRST (Red phase) before DiscountService was implemented
// Exercise 1: Run these tests — they should all PASS (DiscountService is now implemented)
// Exercise 2: Add a @ParameterizedTest with @CsvSource to test multiple discount scenarios
// Exercise 3: Add a test: invalidDiscountPercentThrowsException() for values < 0 and > 100
// Exercise 4: Add a test: nullPriceThrowsException()
// Exercise 5: Add a test: qualifiesForBulkDiscountReturnsTrueForHighOrders()
class DiscountServiceTest {

    private DiscountService discountService;

    @BeforeEach
    void setUp() {
        discountService = new DiscountService();
    }

    @Test
    @DisplayName("10% discount on $100.00 returns $90.00")
    void tenPercentDiscountOnOneHundred() {
        BigDecimal result = discountService.applyDiscount(new BigDecimal("100.00"), 10);
        assertEquals(new BigDecimal("90.00"), result);
    }

    @Test
    @DisplayName("0% discount returns original price")
    void zeroDiscountReturnsOriginalPrice() {
        BigDecimal result = discountService.applyDiscount(new BigDecimal("49.99"), 0);
        assertEquals(new BigDecimal("49.99"), result);
    }

    // TODO Exercise 2: @ParameterizedTest with @CsvSource for multiple scenarios

    // TODO Exercise 3: invalidDiscountPercentThrowsException()

    // TODO Exercise 4: nullPriceThrowsException()

    // TODO Exercise 5: qualifiesForBulkDiscountReturnsTrueForHighOrders()
}
