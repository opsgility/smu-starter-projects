package com.skillmeup.rideshare;
public class Van extends Vehicle {
    public Van(String id, String plate) { super(id, plate, 8); }
    @Override public String getType() { return "Van"; }
}
