package com.skillmeup.rideshare;
public class EarningsService implements TripObserver {
    @Override public void onTripCompleted(Trip trip) {
        System.out.printf("Earnings: %s earned $%.2f%n", trip.getDriver().getName(), trip.getFare() * 0.80);
    }
}
