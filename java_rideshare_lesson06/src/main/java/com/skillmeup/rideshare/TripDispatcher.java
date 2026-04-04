package com.skillmeup.rideshare;

// This class currently has hardcoded pricing — refactor to use PricingStrategy
public class TripDispatcher {
    // TODO Exercise 3: Replace hardcoded pricing with a PricingStrategy field.
    // Add constructor: TripDispatcher(PricingStrategy pricingStrategy)
    // Change dispatchTrip to call pricingStrategy.calculateFare(distanceMiles, 1) for the fare.

    public Trip dispatchTrip(String tripId, Driver driver, Rider rider, double distanceMiles) {
        // Hardcoded — replace with strategy pattern:
        double fare = 2.50 + distanceMiles * 1.20;
        return new TripBuilder()
            .withTripId(tripId).withDriver(driver).withRider(rider).withFare(fare).build();
    }
}
