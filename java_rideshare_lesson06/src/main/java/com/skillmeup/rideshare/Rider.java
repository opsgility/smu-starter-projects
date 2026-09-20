package com.skillmeup.rideshare;
public class Rider {
    private String riderId;
    private String name;
    private String pickup;
    private String dropoff;

    public Rider(String riderId, String name, String pickup, String dropoff) {
        this.riderId = riderId; this.name = name; this.pickup = pickup; this.dropoff = dropoff;
    }
    public String getRiderId() { return riderId; }
    public String getName()    { return name; }
    public String getPickup()  { return pickup; }
    public String getDropoff() { return dropoff; }

    @Override public String toString() {
        return "Rider[" + name + ", " + pickup + " -> " + dropoff + "]";
    }
}
