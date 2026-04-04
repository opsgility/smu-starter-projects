package com.skillmeup.rideshare;

/**
 * TODO Exercise 2: Extend TripDecorator to add cancellation insurance.
 * - Adds $3.00 to the fare (override getFare() to return wrapped.getFare() + 3.00).
 * - getDescription() returns wrapped description + " + CancellationInsurance($3.00)"
 *   (hint: for the base Trip, just use "Trip[" + tripId + "]")
 */
public class CancellationInsuranceDecorator extends TripDecorator {
    // TODO: implement
}
