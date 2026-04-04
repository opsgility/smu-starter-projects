package com.skillmeup.rideshare;

public class Main {
    public static void main(String[] args) {
        Vehicle car = VehicleFactory.createVehicle("car", "C001", "ABC-123");
        Driver  alice = new Driver("D001", "Alice", car, 4.9);
        Rider   bob   = new Rider("R001", "Bob", "Main St", "Airport");

        // Test pricing strategies
        PricingStrategy standard = new StandardPricing();
        PricingStrategy surge    = new SurgePricing(1.5);
        PricingStrategy flat     = new FlatRatePricing(15.00);

        System.out.printf("Standard (5 mi): $%.2f%n", standard.calculateFare(5, 1));
        System.out.printf("Surge    (5 mi): $%.2f%n", surge.calculateFare(5, 1));
        System.out.printf("Flat rate:       $%.2f%n", flat.calculateFare(5, 1));

        // Dispatcher uses strategy
        TripDispatcher dispatcher = new TripDispatcher(standard);
        Trip trip = dispatcher.dispatchTrip("T001", alice, bob, 5.0);
        System.out.println(trip);
    }
}
