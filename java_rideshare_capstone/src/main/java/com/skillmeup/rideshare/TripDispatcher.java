package com.skillmeup.rideshare;
public class TripDispatcher {
    private PricingStrategy pricingStrategy;
    public TripDispatcher(PricingStrategy pricingStrategy) { this.pricingStrategy = pricingStrategy; }
    public Trip dispatchTrip(String tripId, Driver driver, Rider rider, double distanceMiles) {
        double fare = pricingStrategy.calculateFare(distanceMiles, 1);
        return new TripBuilder().withTripId(tripId).withDriver(driver).withRider(rider).withFare(fare).build();
    }
    public void setPricingStrategy(PricingStrategy s) { this.pricingStrategy = s; }
}
