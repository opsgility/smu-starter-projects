package com.skillmeup.rideshare;

/**
 * TODO Exercise 2 (continued): Make AnalyticsService implement TripObserver.
 * onTripCompleted should print:
 *   "Analytics: trip " + trip.getTripId() + " logged"
 */
public class AnalyticsService implements TripObserver {
    @Override
    public void onTripCompleted(Trip trip) {
        // TODO: log the trip
    }
}
