package com.skillmeup.rideshare;
public class EarningsService implements TripObserver {
    @Override public void onTripCompleted(Trip trip) {
        double driverEarnings = trip.getFare() * 0.80;
        System.out.printf("[Earnings] %s earned $%.2f (80%% of $%.2f)%n",
            trip.getDriver().getName(), driverEarnings, trip.getFare());
    }
}
