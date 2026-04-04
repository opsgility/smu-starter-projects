package com.skillmeup.rideshare;

public class TripBuilder {
    private String tripId;
    private Driver driver;
    private Rider  rider;
    private double fare;

    // TODO Exercise 2: Implement fluent builder methods:
    //   withTripId(String id)    — sets tripId, returns this
    //   withDriver(Driver d)     — sets driver, returns this
    //   withRider(Rider r)       — sets rider, returns this
    //   withFare(double fare)    — sets fare, returns this
    //   build()                  — validates all fields are set, returns new Trip(tripId, driver, rider, fare)
    //                             throw IllegalStateException("Missing required field") if any is null/0

    // Stubs so project compiles:
    public TripBuilder withTripId(String id)  { return this; }
    public TripBuilder withDriver(Driver d)   { return this; }
    public TripBuilder withRider(Rider r)     { return this; }
    public TripBuilder withFare(double fare)  { return this; }
    public Trip        build()                { return null; }
}
