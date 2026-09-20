package com.skillmeup.rideshare;
public class Trip {
    public enum Status { PENDING, IN_PROGRESS, COMPLETED, CANCELLED }

    private String tripId;
    private Driver driver;
    private Rider  rider;
    private double fare;
    private Status status;

    public Trip(String tripId, Driver driver, Rider rider, double fare) {
        this.tripId = tripId; this.driver = driver; this.rider = rider;
        this.fare = fare; this.status = Status.PENDING;
    }
    public String getTripId()   { return tripId; }
    public Driver getDriver()   { return driver; }
    public Rider  getRider()    { return rider; }
    public double getFare()     { return fare; }
    public Status getStatus()   { return status; }
    public void   setStatus(Status s) { this.status = s; }

    @Override public String toString() {
        return String.format("Trip[%s | %s -> %s | $%.2f | %s]",
            tripId, driver.getName(), rider.getName(), fare, status);
    }
}
