package com.skillmeup.rideshare;

public class Main {
    public static void main(String[] args) {
        Vehicle car   = VehicleFactory.createVehicle("car", "C001", "ABC-123");
        Driver  alice = new Driver("D001", "Alice", car, 4.9);
        Rider   bob   = new Rider("R001", "Bob", "Main St", "Airport");

        // Test the adapter
        MapService map = new MapServiceAdapter(new LegacyMapService());
        double miles = map.getDistanceMiles("Main St", "Airport");
        System.out.printf("Distance: %.2f miles%n", miles);
        System.out.println(map.getRouteDescription("Main St", "Airport"));

        // Create a trip and decorate it
        Trip base = new TripBuilder().withTripId("T001").withDriver(alice)
            .withRider(bob).withFare(new StandardPricing().calculateFare(miles, 1)).build();
        System.out.println("Base fare: $" + base.getFare());

        // Add cancellation insurance decorator
        // CancellationInsuranceDecorator insured = new CancellationInsuranceDecorator(base);
        // System.out.println("Insured fare: $" + insured.getFare());
    }
}
