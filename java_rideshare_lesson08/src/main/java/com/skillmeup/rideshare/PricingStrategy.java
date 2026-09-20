package com.skillmeup.rideshare;
public interface PricingStrategy {
    double calculateFare(double distanceMiles, int passengerCount);
}
