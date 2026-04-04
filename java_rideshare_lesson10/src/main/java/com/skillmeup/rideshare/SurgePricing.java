package com.skillmeup.rideshare;
public class SurgePricing implements PricingStrategy {
    private double multiplier;
    public SurgePricing(double multiplier) { this.multiplier = multiplier; }
    @Override public double calculateFare(double miles, int passengers) {
        return (2.50 + miles * 1.20) * multiplier;
    }
}
