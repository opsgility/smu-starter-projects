package com.skillmeup.rideshare;

import java.util.ArrayList;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        AppContainer container = new AppContainer();
        TripDispatcher dispatcher = container.getDispatcher();
        MapService map = container.getMapService();

        // Pre-loaded drivers and riders
        List<Driver> drivers = new ArrayList<>();
        drivers.add(new Driver("D001", "Alice", VehicleFactory.createVehicle("car",  "C001", "ABC-123"), 4.9));
        drivers.add(new Driver("D002", "Bob",   VehicleFactory.createVehicle("van",  "V001", "DEF-456"), 4.7));
        drivers.add(new Driver("D003", "Carol", VehicleFactory.createVehicle("motorcycle", "M001", "GHI-789"), 4.8));

        List<Rider> riders = new ArrayList<>();
        riders.add(new Rider("R001", "Dave",    "Main St",    "Airport"));
        riders.add(new Rider("R002", "Eve",     "Park Ave",   "Downtown"));
        riders.add(new Rider("R003", "Frank",   "University", "Mall"));

        // TODO Capstone Exercise 1: Implement dispatch logic.
        // For each rider, find an available driver (simplified: assign in order).
        // Use map.getDistanceMiles() to calculate route distance.
        // Use dispatcher.dispatchTrip() to create the trip.
        // Print each trip.
        System.out.println("=== Dispatch Simulation ===");
        System.out.println("(TODO: implement dispatch loop)");

        // TODO Capstone Exercise 2: Wire surge pricing when fewer than 2 drivers are available.
        // Call container.setPricing(new SurgePricing(1.5)) to switch strategies at runtime.

        // TODO Capstone Exercise 3: After each trip completes, notify all observers.
        // Call trip.setStatus(Trip.Status.COMPLETED) then iterate container.getObservers().
    }
}
