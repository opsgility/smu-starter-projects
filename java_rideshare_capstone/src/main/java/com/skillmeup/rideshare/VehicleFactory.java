package com.skillmeup.rideshare;
public class VehicleFactory {
    public static Vehicle createVehicle(String type, String id, String plate) {
        return switch (type.toUpperCase()) {
            case "CAR"        -> new Car(id, plate);
            case "VAN"        -> new Van(id, plate);
            case "MOTORCYCLE" -> new Motorcycle(id, plate);
            default           -> throw new IllegalArgumentException("Unknown vehicle type: " + type);
        };
    }

    /** Overload accepting make and model (make/model stored in plate field as combined label) */
    public static Vehicle createVehicle(String type, String id, String make, String model) {
        return createVehicle(type, id, make + " " + model);
    }
}
