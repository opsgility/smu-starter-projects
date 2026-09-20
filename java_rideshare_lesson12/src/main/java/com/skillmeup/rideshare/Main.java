package com.skillmeup.rideshare;

public class Main {
    public static void main(String[] args) {
        // TODO Exercise 2: Replace all direct instantiation below with AppContainer wiring.
        // After this lesson, Main.java should only call AppContainer methods — no 'new' except AppContainer.

        AppContainer container = new AppContainer();
        TripDispatcher dispatcher = container.getDispatcher();
        MapService map = container.getMapService();

        Vehicle car  = VehicleFactory.createVehicle("car", "C001", "ABC-123");
        Driver alice = new Driver("D001", "Alice", car, 4.9);
        Rider  bob   = new Rider("R001", "Bob", "Main St", "Airport");

        if (map != null) {
            double miles = map.getDistanceMiles(bob.getPickup(), bob.getDropoff());
            System.out.printf("Route: %s (%.2f miles)%n", map.getRouteDescription(bob.getPickup(), bob.getDropoff()), miles);
        }

        if (dispatcher != null) {
            Trip trip = dispatcher.dispatchTrip("T001", alice, bob, 5.0);
            trip.setStatus(Trip.Status.COMPLETED);
            System.out.println(trip);
            for (TripObserver obs : container.getObservers()) {
                obs.onTripCompleted(trip);
            }
        }
    }
}
