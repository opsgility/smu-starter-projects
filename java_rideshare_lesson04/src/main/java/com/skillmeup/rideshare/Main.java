package com.skillmeup.rideshare;

public class Main {
    public static void main(String[] args) {
        // Test the factory
        Vehicle car  = VehicleFactory.createVehicle("car",  "C001", "ABC-123");
        Vehicle van  = VehicleFactory.createVehicle("van",  "V001", "GHI-789");
        System.out.println(car);
        System.out.println(van);

        // Test the builder
        Driver driver = new Driver("D001", "Alice", car, 4.9);
        Rider  rider  = new Rider("R001", "Bob", "Main St", "Airport");
        Trip trip = new TripBuilder()
            .withTripId("T001")
            .withDriver(driver)
            .withRider(rider)
            .withFare(25.50)
            .build();
        System.out.println(trip);
    }
}
