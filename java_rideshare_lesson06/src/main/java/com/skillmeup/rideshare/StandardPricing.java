package com.skillmeup.rideshare;

/**
 * TODO Exercise 2: Implement StandardPricing that implements PricingStrategy.
 * Formula: baseFare(2.50) + distanceMiles * 1.20
 * (passengerCount not used in standard pricing)
 */
public class StandardPricing implements PricingStrategy {
    @Override
    public double calculateFare(double distanceMiles, int passengerCount) {
        return 0.0; // TODO: implement
    }
}
