package com.skillmeup.rideshare;

/**
 * TODO Exercise 2 (continued): Make EarningsService implement TripObserver.
 * onTripCompleted should print:
 *   "Earnings: driver " + trip.getDriver().getName() + " earned $" + (trip.getFare() * 0.80)
 */
public class EarningsService implements TripObserver {
    @Override
    public void onTripCompleted(Trip trip) {
        // TODO: print driver earnings (80% of fare)
    }
}
