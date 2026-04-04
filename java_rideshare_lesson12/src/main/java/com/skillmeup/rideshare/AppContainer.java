package com.skillmeup.rideshare;

/**
 * TODO Exercise 1: Implement a manual DI container that wires all services together.
 *
 * The container should create and hold:
 *   - LegacyMapService legacyMap
 *   - MapService mapService = new MapServiceAdapter(legacyMap)
 *   - PricingStrategy pricingStrategy = new StandardPricing()
 *   - TripDispatcher dispatcher = new TripDispatcher(pricingStrategy)
 *   - TripObserver receiptService = new ReceiptService()
 *   - TripObserver earningsService = new EarningsService()
 *   - TripObserver analyticsService = new AnalyticsService()
 *
 * Provide getters for each so Main.java can retrieve them.
 * No business logic should use 'new' except inside this container.
 */
public class AppContainer {
    // TODO: declare fields, instantiate them in constructor, add getters

    // Stub getters so project compiles:
    public TripDispatcher getDispatcher()  { return null; }
    public MapService     getMapService()  { return null; }
    public TripObserver[] getObservers()   { return new TripObserver[0]; }
}
