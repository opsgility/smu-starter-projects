package com.skillmeup.rideshare;

/**
 * TODO Exercise 1: Create an abstract TripDecorator that wraps a Trip.
 * - Holds a private final Trip wrapped field, set via constructor.
 * - Provides delegate methods: getTripId(), getDriver(), getRider(), getFare(), getStatus().
 *   Each delegates to wrapped.getXxx().
 * - Declare abstract String getDescription(); for subclasses to override.
 */
public abstract class TripDecorator {
    // TODO: add wrapped field, constructor, delegate methods, and abstract getDescription()
}
