package com.skillmeup.rideshare;

/**
 * Our expected interface for mapping (distance in miles, not km).
 */
public interface MapService {
    double getDistanceMiles(String origin, String destination);
    String getRouteDescription(String origin, String destination);
}
