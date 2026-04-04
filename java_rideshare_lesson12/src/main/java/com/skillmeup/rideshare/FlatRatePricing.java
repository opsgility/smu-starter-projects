package com.skillmeup.rideshare;
public class FlatRatePricing implements PricingStrategy {
    private double rate;
    public FlatRatePricing(double rate) { this.rate = rate; }
    @Override public double calculateFare(double miles, int passengers) { return rate; }
}
