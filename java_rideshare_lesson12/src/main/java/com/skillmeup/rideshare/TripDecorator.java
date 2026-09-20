package com.skillmeup.rideshare;
public abstract class TripDecorator {
    protected final Trip wrapped;
    public TripDecorator(Trip wrapped) { this.wrapped = wrapped; }
    public String getTripId()          { return wrapped.getTripId(); }
    public Driver getDriver()          { return wrapped.getDriver(); }
    public Rider  getRider()           { return wrapped.getRider(); }
    public double getFare()            { return wrapped.getFare(); }
    public Trip.Status getStatus()     { return wrapped.getStatus(); }
    public abstract String getDescription();
}
