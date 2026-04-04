package com.skillmeup.rideshare;
public class Driver {
    private String driverId;
    private String name;
    private Vehicle vehicle;
    private double rating;

    public Driver(String driverId, String name, Vehicle vehicle, double rating) {
        this.driverId = driverId; this.name = name; this.vehicle = vehicle; this.rating = rating;
    }
    public String  getDriverId() { return driverId; }
    public String  getName()     { return name; }
    public Vehicle getVehicle()  { return vehicle; }
    public double  getRating()   { return rating; }

    @Override public String toString() {
        return "Driver[" + name + ", rating=" + rating + ", vehicle=" + vehicle.getType() + "]";
    }
}
