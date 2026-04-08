package com.skillmeup.rideshare;
public class ReceiptService implements TripObserver {
    @Override public void onTripCompleted(Trip trip) {
        System.out.printf("[Receipt] Sending receipt to %s | Trip: %s | Amount: $%.2f%n",
            trip.getRider().getName(), trip.getTripId(), trip.getFare());
    }
}
