package com.skillmeup.rideshare;
public class ReceiptService implements TripObserver {
    @Override public void onTripCompleted(Trip trip) {
        System.out.printf("Receipt: %s charged $%.2f%n", trip.getRider().getName(), trip.getFare());
    }
}
