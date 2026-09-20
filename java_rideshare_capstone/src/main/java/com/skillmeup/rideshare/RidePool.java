package com.skillmeup.rideshare;

import java.util.ArrayList;
import java.util.List;

/**
 * A pooled ride where multiple riders share the same vehicle and split the fare.
 *
 * TODO Exercise 1: Implement the static inner Builder class with:
 *   - id(String), driver(Driver), vehicle(Vehicle), addRider(Rider) fluent methods
 *   - build() that validates driver, vehicle, and at least one rider
 *   - build() throws IllegalStateException if requirements not met
 *   - Auto-generates id if not provided (use "RP-" + System.currentTimeMillis())
 *
 * TODO Exercise 1: Add a private constructor that accepts a Builder and sets all fields
 *
 * TODO Exercise 1: Add getters for all fields and getFarePerRider() = totalFare / riders.size()
 *
 * TODO Exercise 2: Add observer support (addObserver, removeObserver, list of TripObserver)
 *
 * TODO Exercise 2: Implement complete(double distanceKm) that:
 *   - Sets status to COMPLETED and calculates totalFare (base fare * 0.70 discount)
 *   - Prints: [RidePool] <id> complete | <count> riders | Total: $X | Per rider: $Y
 *   - For each rider, creates a synthetic Trip and notifies all observers
 */
public class RidePool {

    private String          id;
    private Driver          driver;
    private List<Rider>     riders;
    private Vehicle         vehicle;
    private double          totalFare;
    private Trip.Status     status;

    // TODO Exercise 1: Add private RidePool(Builder builder) constructor

    // TODO Exercise 1: Add getters
    public String       getId()           { return id; }
    public Driver       getDriver()       { return driver; }
    public List<Rider>  getRiders()       { return riders; }
    public Vehicle      getVehicle()      { return vehicle; }
    public double       getTotalFare()    { return totalFare; }
    public Trip.Status  getStatus()       { return status; }
    public int          getRiderCount()   { return riders == null ? 0 : riders.size(); }

    // TODO Exercise 1: Implement getFarePerRider()
    public double getFarePerRider() {
        // TODO: return totalFare / riders.size(), or 0.0 if no riders
        return 0.0;
    }

    public void setTotalFare(double fare)    { this.totalFare = fare; }
    public void setStatus(Trip.Status status) { this.status = status; }

    // TODO Exercise 2: Implement complete(double distanceKm)
    public void complete(double distanceKm) {
        // TODO: calculate fare, set status, print summary, notify observers
        System.out.println("TODO: implement RidePool.complete()");
    }

    // TODO Exercise 1: Implement the static inner Builder class below
    public static class Builder {
        // TODO: fields for id, driver, vehicle, and riders list

        // TODO: fluent methods id(), driver(), vehicle(), addRider()

        // TODO: build() with validation
        public RidePool build() {
            throw new UnsupportedOperationException("TODO: implement Builder.build()");
        }
    }
}
