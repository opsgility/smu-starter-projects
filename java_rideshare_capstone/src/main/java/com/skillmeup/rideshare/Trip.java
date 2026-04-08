package com.skillmeup.rideshare;
import java.util.ArrayList;
import java.util.List;

public class Trip {
    public enum Status { PENDING, IN_PROGRESS, COMPLETED, CANCELLED }

    private String  tripId;
    private Driver  driver;
    private Rider   rider;
    private Vehicle vehicle;
    private double  fare;
    private Status  status;
    private final List<TripObserver> observers = new ArrayList<>();

    public Trip(String tripId, Driver driver, Rider rider, double fare) {
        this.tripId = tripId; this.driver = driver; this.rider = rider;
        this.fare = fare; this.status = Status.PENDING;
    }

    public Trip(String tripId, Driver driver, Rider rider, Vehicle vehicle, double fare) {
        this(tripId, driver, rider, fare);
        this.vehicle = vehicle;
    }

    public String  getTripId()       { return tripId; }
    public Driver  getDriver()       { return driver; }
    public Rider   getRider()        { return rider; }
    public Vehicle getVehicle()      { return vehicle; }
    public double  getFare()         { return fare; }
    public Status  getStatus()       { return status; }
    public void    setStatus(Status s) { this.status = s; }
    public void    setFare(double f)   { this.fare = f; }

    public void addObserver(TripObserver observer) {
        if (observer != null) observers.add(observer);
    }

    public void complete() {
        this.status = Status.COMPLETED;
        for (TripObserver obs : observers) {
            obs.onTripCompleted(this);
        }
    }

    @Override public String toString() {
        return String.format("Trip[%s | %s -> %s | $%.2f | %s]",
            tripId, driver.getName(), rider.getName(), fare, status);
    }
}
