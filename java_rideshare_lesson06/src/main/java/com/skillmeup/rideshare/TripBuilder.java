package com.skillmeup.rideshare;
public class TripBuilder {
    private String tripId;
    private Driver driver;
    private Rider  rider;
    private double fare;

    public TripBuilder withTripId(String id) { this.tripId = id; return this; }
    public TripBuilder withDriver(Driver d)  { this.driver = d;  return this; }
    public TripBuilder withRider(Rider r)    { this.rider  = r;  return this; }
    public TripBuilder withFare(double f)    { this.fare   = f;  return this; }

    public Trip build() {
        if (tripId == null || driver == null || rider == null || fare <= 0)
            throw new IllegalStateException("Missing required field");
        return new Trip(tripId, driver, rider, fare);
    }
}
