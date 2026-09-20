package com.skillmeup.rideshare;

public class Main {
    public static void main(String[] args) {
        Vehicle car   = VehicleFactory.createVehicle("car", "C001", "ABC-123");
        Driver  alice = new Driver("D001", "Alice", car, 4.9);
        Rider   bob   = new Rider("R001", "Bob", "Main St", "Airport");

        TripDispatcher dispatcher = new TripDispatcher(new StandardPricing());
        Trip trip = dispatcher.dispatchTrip("T001", alice, bob, 5.0);
        trip.setStatus(Trip.Status.COMPLETED);

        // Notify observers
        TripObserver receipt   = new ReceiptService();
        TripObserver earnings  = new EarningsService();
        TripObserver analytics = new AnalyticsService();

        receipt.onTripCompleted(trip);
        earnings.onTripCompleted(trip);
        analytics.onTripCompleted(trip);
    }
}
