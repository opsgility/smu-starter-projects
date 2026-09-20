package com.skillmeup.rideshare;
public class AnalyticsService implements TripObserver {
    @Override public void onTripCompleted(Trip trip) {
        System.out.println("Analytics: trip " + trip.getTripId() + " logged");
    }
}
