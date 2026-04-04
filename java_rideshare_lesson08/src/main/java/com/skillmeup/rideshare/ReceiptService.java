package com.skillmeup.rideshare;

/**
 * TODO Exercise 2: Make ReceiptService implement TripObserver.
 * onTripCompleted should print:
 *   "Receipt: " + trip.getRider().getName() + " charged $" + trip.getFare()
 */
public class ReceiptService implements TripObserver {
    @Override
    public void onTripCompleted(Trip trip) {
        // TODO: print the receipt
    }
}
