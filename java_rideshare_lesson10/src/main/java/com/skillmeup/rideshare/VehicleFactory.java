package com.skillmeup.rideshare;
public class VehicleFactory {
    public static Vehicle createVehicle(String type, String id, String plate) {
        return switch (type.toLowerCase()) {
            case "car"        -> new Car(id, plate);
            case "van"        -> new Van(id, plate);
            case "motorcycle" -> new Motorcycle(id, plate);
            default           -> throw new IllegalArgumentException("Unknown vehicle type: " + type);
        };
    }
}
