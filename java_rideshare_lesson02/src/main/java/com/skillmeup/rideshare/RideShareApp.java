package com.skillmeup.rideshare;

// This class violates SOLID principles — your job is to refactor it.
// It handles too many responsibilities (SRP violation), doesn't use interfaces (OCP/ISP violation),
// and instantiates concrete classes everywhere (DIP violation).

public class RideShareApp {

    // All vehicle data baked in — no abstraction
    static String[] carIds      = {"C001", "C002"};
    static String[] carPlates   = {"ABC-123", "DEF-456"};
    static String[] vanIds      = {"V001"};
    static String[] vanPlates   = {"GHI-789"};
    static String[] motoIds     = {"M001"};
    static String[] motoPlates  = {"JKL-012"};

    // All driver data baked in — duplicate code per vehicle type
    static void printCarDriver(String name, String plate, double rating) {
        System.out.println("Car driver: " + name + " plate=" + plate + " rating=" + rating);
    }
    static void printVanDriver(String name, String plate, double rating) {
        System.out.println("Van driver: " + name + " plate=" + plate + " rating=" + rating);
    }
    static void printMotoDriver(String name, String plate, double rating) {
        System.out.println("Motorcycle driver: " + name + " plate=" + plate + " rating=" + rating);
    }

    // Fare calculation duplicated per trip type — no abstraction
    static double calculateStandardFare(double miles) { return 2.50 + miles * 1.20; }
    static double calculateSurgeFare(double miles)    { return 2.50 + miles * 1.20 * 1.5; }
    static double calculateFlatFare()                 { return 15.00; }

    public static void main(String[] args) {
        printCarDriver("Alice",    "ABC-123", 4.9);
        printVanDriver("Bob",      "GHI-789", 4.7);
        printMotoDriver("Charlie", "JKL-012", 4.8);

        System.out.println("Standard fare (5 miles): $" + calculateStandardFare(5));
        System.out.println("Surge fare    (5 miles): $" + calculateSurgeFare(5));
        System.out.println("Flat fare:               $" + calculateFlatFare());
    }
}
