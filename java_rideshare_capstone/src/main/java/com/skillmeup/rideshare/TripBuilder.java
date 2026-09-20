package com.skillmeup.rideshare;
public class TripBuilder {
    private String  tripId;
    private Driver  driver;
    private Rider   rider;
    private Vehicle vehicle;
    private double  fare;

    // Fluent method aliases
    public TripBuilder id(String id)         { this.tripId  = id; return this; }
    public TripBuilder driver(Driver d)      { this.driver  = d;  return this; }
    public TripBuilder rider(Rider r)        { this.rider   = r;  return this; }
    public TripBuilder vehicle(Vehicle v)    { this.vehicle = v;  return this; }

    // Legacy aliases kept for compatibility
    public TripBuilder withTripId(String id) { return id(id); }
    public TripBuilder withDriver(Driver d)  { return driver(d); }
    public TripBuilder withRider(Rider r)    { return rider(r); }
    public TripBuilder withFare(double f)    { this.fare = f; return this; }

    public Trip build() {
        if (tripId == null || driver == null || rider == null)
            throw new IllegalStateException("Missing required field: id, driver, and rider are required");
        return new Trip(tripId, driver, rider, vehicle, fare);
    }
}
