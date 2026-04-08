package com.skillmeup.rideshare;
import java.util.List;

public class AppContainer {
    private final LegacyMapService legacyMap         = new LegacyMapService();
    private final MapService       mapService        = new MapServiceAdapter(legacyMap);
    private final TripDispatcher   regularDispatcher = new TripDispatcher(new StandardPricing());
    private final TripDispatcher   surgeDispatcher   = new TripDispatcher(new SurgePricing(2.0));
    private final AnalyticsService analytics         = new AnalyticsService();
    private final List<TripObserver> observers       = List.of(
        new ReceiptService(), new EarningsService(), analytics
    );

    public TripDispatcher    getDispatcher()        { return regularDispatcher; }
    public TripDispatcher    getRegularDispatcher() { return regularDispatcher; }
    public TripDispatcher    getSurgeDispatcher()   { return surgeDispatcher; }
    public MapService        getMapService()        { return mapService; }
    public List<TripObserver> getObservers()        { return observers; }
    public AnalyticsService  getAnalytics()         { return analytics; }
    public void setPricing(PricingStrategy s)       { regularDispatcher.setPricingStrategy(s); }
}
