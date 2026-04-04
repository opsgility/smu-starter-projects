package com.skillmeup.rideshare;
public class Motorcycle extends Vehicle {
    public Motorcycle(String id, String plate) { super(id, plate, 1); }
    @Override public String getType() { return "Motorcycle"; }
}
