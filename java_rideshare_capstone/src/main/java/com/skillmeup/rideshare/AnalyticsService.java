package com.skillmeup.rideshare;
public class AnalyticsService implements TripObserver {
    private int    totalTrips   = 0;
    private double totalRevenue = 0.0;

    @Override public void onTripCompleted(Trip trip) {
        totalTrips++;
        totalRevenue += trip.getFare();
        System.out.printf("[Analytics] Trip #%d complete | Trip fare: $%.2f | Total revenue: $%.2f%n",
            totalTrips, trip.getFare(), totalRevenue);
    }

    public int    getTotalTrips()   { return totalTrips; }
    public double getTotalRevenue() { return totalRevenue; }
}
