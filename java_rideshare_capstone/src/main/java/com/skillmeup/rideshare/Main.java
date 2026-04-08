package com.skillmeup.rideshare;

import java.util.List;

public class Main {
    public static void main(String[] args) {
        System.out.println("========================================");
        System.out.println("  FleetFlow RideShare System — Capstone");
        System.out.println("========================================\n");

        AppContainer container = new AppContainer();

        // ---- Create fleet ----
        Vehicle car1 = VehicleFactory.createVehicle("CAR", "V-001", "Toyota",  "Camry");
        Vehicle car2 = VehicleFactory.createVehicle("CAR", "V-002", "Honda",   "Civic");
        Vehicle van1 = VehicleFactory.createVehicle("VAN", "V-003", "Ford",    "Transit");

        Driver alice  = new Driver("D-001", "Alice",  car1);
        Driver brooke = new Driver("D-002", "Brooke", car2);
        Driver carlos = new Driver("D-003", "Carlos", van1);

        // ---- Trip 1: Regular standard fare ----
        System.out.println("--- Trip 1: Standard fare ---");
        Rider r1 = new Rider("R-001", "Dana", "Airport", "Hotel District");

        // TODO Exercise 3: Build Trip t1 using TripBuilder, dispatch it via container.getRegularDispatcher(),
        //   wire observers, and call t1.complete()
        // Hint: new TripBuilder().id("T-001").driver(alice).rider(r1).vehicle(car1).build()
        // Hint: container.getRegularDispatcher().dispatchTrip(t1, 6, 4)
        // Hint: container.getObservers().forEach(t1::addObserver)
        System.out.println("(TODO: build and complete Trip 1)");

        // ---- Trip 2: Surge fare with decorator ----
        System.out.println("\n--- Trip 2: Surge fare + Cancellation Insurance ---");
        Rider r2 = new Rider("R-002", "Evan", "Stadium", "Downtown");

        // TODO Exercise 3: Build Trip t2, dispatch via container.getSurgeDispatcher(),
        //   apply CancellationInsuranceDecorator, wire observers, complete
        System.out.println("(TODO: build and complete Trip 2 with decorator)");

        // ---- Trip 3: RidePool ----
        System.out.println("\n--- Trip 3: RidePool ---");
        Rider poolR1 = new Rider("R-P1", "Fiona",  "East Side",  "University");
        Rider poolR2 = new Rider("R-P2", "George", "North Park", "University");
        Rider poolR3 = new Rider("R-P3", "Helen",  "West End",   "University");

        // TODO Exercise 1: Build a RidePool using RidePool.Builder
        // Hint: new RidePool.Builder().id("RP-001").driver(carlos).vehicle(van1)
        //         .addRider(poolR1).addRider(poolR2).addRider(poolR3).build()

        // TODO Exercise 2: Wire observers to pool and call pool.complete(15.0)
        System.out.println("(TODO: build RidePool and call complete)");

        // ---- Summary ----
        System.out.println("\n========================================");
        System.out.println("  Session Summary");
        System.out.println("========================================");
        System.out.printf("Total events tracked: %d%n",  container.getAnalytics().getTotalTrips());
        System.out.printf("Total revenue:        $%.2f%n", container.getAnalytics().getTotalRevenue());
    }
}
