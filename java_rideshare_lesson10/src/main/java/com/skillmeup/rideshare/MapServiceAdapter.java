package com.skillmeup.rideshare;

/**
 * TODO Exercise 3: Implement MapServiceAdapter that implements MapService
 * and wraps a LegacyMapService.
 * - Constructor: MapServiceAdapter(LegacyMapService legacy)
 * - getDistanceMiles: call legacy.getRouteDistanceKm() and convert (km * 0.621371)
 * - getRouteDescription: delegate to legacy.getRouteDescription()
 */
public class MapServiceAdapter implements MapService {
    // TODO: implement
    @Override public double getDistanceMiles(String o, String d) { return 0; }
    @Override public String getRouteDescription(String o, String d) { return ""; }
}
