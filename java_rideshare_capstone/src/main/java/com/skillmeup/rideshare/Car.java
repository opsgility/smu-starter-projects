package com.skillmeup.rideshare;
public class Car extends Vehicle {
    public Car(String id, String plate) { super(id, plate, 4); }
    @Override public String getType() { return "Car"; }
}
