package com.skillmeup.rideshare;
public class CancellationInsuranceDecorator extends TripDecorator {
    public CancellationInsuranceDecorator(Trip trip) { super(trip); }
    @Override public double getFare() { return wrapped.getFare() + 3.00; }
    @Override public String getDescription() {
        return "Trip[" + getTripId() + "] + CancellationInsurance($3.00)";
    }
}
