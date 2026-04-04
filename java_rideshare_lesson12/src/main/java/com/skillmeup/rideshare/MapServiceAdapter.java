package com.skillmeup.rideshare;
public class MapServiceAdapter implements MapService {
    private LegacyMapService legacy;
    public MapServiceAdapter(LegacyMapService legacy) { this.legacy = legacy; }
    @Override public double getDistanceMiles(String o, String d) { return legacy.getRouteDistanceKm(o, d) * 0.621371; }
    @Override public String getRouteDescription(String o, String d) { return legacy.getRouteDescription(o, d); }
}
