package com.skillmeup.rideshare;

// TODO Exercise 1 (SRP): Extract Car, Van, and Motorcycle as separate classes.
// Each should extend a base Vehicle class with vehicleId, licensePlate, capacity fields.
// Move the duplicate printXxxDriver logic into a single printDriver(Driver d) method.

// TODO Exercise 2 (ISP/OCP): Create a Dispatchable interface with:
//   boolean isAvailable();
//   String  getVehicleType();
// Make Vehicle implement Dispatchable. The printDriver method should accept Dispatchable.

// TODO Exercise 3 (DIP): Create a Driver class that holds a Vehicle (not a specific car/van/moto).
// The constructor should accept a Vehicle interface reference, not a concrete type.
// Update main() to use the new Driver and Vehicle classes.

public class Main {
    public static void main(String[] args) {
        // Run the original monolith to see the baseline output
        RideShareApp.main(args);

        // After completing exercises, replace above with your refactored classes:
        // Vehicle car = new Car("C001", "ABC-123");
        // Driver alice = new Driver("D001", "Alice", car, 4.9);
        // System.out.println(alice);
    }
}
