package com.skillmeup.rideshare;
public class StandardPricing implements PricingStrategy {
    @Override public double calculateFare(double miles, int passengers) { return 2.50 + miles * 1.20; }
}
