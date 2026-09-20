package com.skillmeup.rideshare;

public abstract class Vehicle {
    protected String vehicleId;
    protected String licensePlate;
    protected int    capacity;

    public Vehicle(String vehicleId, String licensePlate, int capacity) {
        this.vehicleId = vehicleId; this.licensePlate = licensePlate; this.capacity = capacity;
    }
    public String getVehicleId()    { return vehicleId; }
    public String getLicensePlate() { return licensePlate; }
    public int    getCapacity()     { return capacity; }
    public abstract String getType();

    @Override public String toString() {
        return getType() + "[" + vehicleId + ", plate=" + licensePlate + ", cap=" + capacity + "]";
    }
}
