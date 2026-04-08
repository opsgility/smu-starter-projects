package com.skillmeup.rideshare;
public class TripDispatcher {
    private PricingStrategy pricingStrategy;

    public TripDispatcher(PricingStrategy pricingStrategy) {
        this.pricingStrategy = pricingStrategy;
    }

    /** Original dispatch: creates and returns a new Trip */
    public Trip dispatchTrip(String tripId, Driver driver, Rider rider, double distanceMiles) {
        double fare = pricingStrategy.calculateFare(distanceMiles, 1);
        return new TripBuilder().id(tripId).driver(driver).rider(rider).withFare(fare).build();
    }

    /**
     * Dispatches an existing Trip object — calculates and sets its fare.
     * availableDrivers and activeRiders influence surge pricing if applicable.
     */
    public void dispatchTrip(Trip trip, int availableDrivers, int activeRiders) {
        double distanceMiles = 5.0; // default — no map service available in this overload
        double fare = pricingStrategy.calculateFare(distanceMiles, activeRiders);
        trip.setFare(fare);
        System.out.printf("[%s] Trip %s | Fare: $%.2f%n",
            pricingStrategy.getClass().getSimpleName().replace("Pricing",""), trip.getTripId(), fare);
    }

    public void setPricingStrategy(PricingStrategy s) { this.pricingStrategy = s; }
}
