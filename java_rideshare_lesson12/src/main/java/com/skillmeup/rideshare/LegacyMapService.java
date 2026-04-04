package com.skillmeup.rideshare;
public class LegacyMapService {
    public double getRouteDistanceKm(String origin, String destination) { return 8.0; }
    public String getRouteDescription(String origin, String destination) {
        return origin + " => " + destination + " via Highway 1";
    }
}
