package com.skillmeup.rideshare;
public class AppContainer {
    private final LegacyMapService legacyMap       = new LegacyMapService();
    private final MapService       mapService      = new MapServiceAdapter(legacyMap);
    private final PricingStrategy  pricing         = new StandardPricing();
    private final TripDispatcher   dispatcher      = new TripDispatcher(pricing);
    private final TripObserver[]   observers       = {
        new ReceiptService(), new EarningsService(), new AnalyticsService()
    };
    public TripDispatcher getDispatcher()  { return dispatcher; }
    public MapService     getMapService()  { return mapService; }
    public TripObserver[] getObservers()   { return observers; }
    public PricingStrategy getPricing()    { return pricing; }
    public void setPricing(PricingStrategy s) { dispatcher.setPricingStrategy(s); }
}
