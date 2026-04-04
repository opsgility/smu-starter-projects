package com.skillmeup.rideshare;

// This is a legacy class we cannot modify — it uses a different interface.
public class LegacyMapService {
    public double getRouteDistanceKm(String origin, String destination) {
        // Simulated — returns 8 km for any route
        return 8.0;
    }
    public String getRouteDescription(String origin, String destination) {
        return origin + " => " + destination + " via Highway 1";
    }
}
