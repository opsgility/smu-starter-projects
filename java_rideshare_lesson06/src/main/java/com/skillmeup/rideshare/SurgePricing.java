package com.skillmeup.rideshare;

/**
 * TODO Exercise 2 (continued): Implement SurgePricing that implements PricingStrategy.
 * Formula: StandardPricing result * surgeMultiplier (default 1.5)
 * Add a constructor that accepts the surge multiplier.
 */
public class SurgePricing implements PricingStrategy {
    private double surgeMultiplier;

    public SurgePricing(double surgeMultiplier) {
        this.surgeMultiplier = surgeMultiplier;
    }

    @Override
    public double calculateFare(double distanceMiles, int passengerCount) {
        return 0.0; // TODO: implement using StandardPricing formula * surgeMultiplier
    }
}
