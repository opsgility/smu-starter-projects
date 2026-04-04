package com.skillmeup.rideshare;

/**
 * TODO Exercise 2 (continued): Implement FlatRatePricing.
 * Always returns a fixed flat fare (e.g. 15.00) regardless of distance or passengers.
 */
public class FlatRatePricing implements PricingStrategy {
    private double flatRate;
    public FlatRatePricing(double flatRate) { this.flatRate = flatRate; }

    @Override
    public double calculateFare(double distanceMiles, int passengerCount) {
        return 0.0; // TODO: implement
    }
}
