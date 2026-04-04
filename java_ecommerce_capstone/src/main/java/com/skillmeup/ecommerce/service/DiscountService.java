package com.skillmeup.ecommerce.service;

import org.springframework.stereotype.Service;
import java.math.BigDecimal;
import java.math.RoundingMode;

@Service
public class DiscountService {

    /**
     * Apply a percentage discount to a price.
     * @param price the original price
     * @param discountPercent the discount percentage (0-100)
     * @return discounted price
     */
    public BigDecimal applyDiscount(BigDecimal price, int discountPercent) {
        if (price == null || price.compareTo(BigDecimal.ZERO) < 0) {
            throw new IllegalArgumentException("Price must be non-negative");
        }
        if (discountPercent < 0 || discountPercent > 100) {
            throw new IllegalArgumentException("Discount percent must be between 0 and 100");
        }
        BigDecimal factor = BigDecimal.ONE.subtract(
            BigDecimal.valueOf(discountPercent).divide(BigDecimal.valueOf(100))
        );
        return price.multiply(factor).setScale(2, RoundingMode.HALF_UP);
    }

    /**
     * Determine if an order qualifies for a bulk discount.
     * Orders over $500 qualify for 10% discount.
     */
    public boolean qualifiesForBulkDiscount(BigDecimal orderTotal) {
        return orderTotal.compareTo(new BigDecimal("500.00")) > 0;
    }
}
