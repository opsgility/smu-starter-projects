// FleetBoard shared utilities — house-style reference.
// Exports follow the project's conventions: descriptive verb-noun
// function names, explicit parameter validation, JSDoc on the
// exported surface, consistent `[functionName] failed: ...` error
// wrapping. Study this file for the shape Copilot's refactor of
// task-service should match.

/**
 * Format a FleetBoard internal vehicle identifier for display.
 *
 * @param {string} vehicleId - The internal `fleet-NR-NNNN` identifier.
 * @returns {string} Short display form, e.g. `NR#0417`.
 * @throws {Error} If vehicleId is not a string.
 */
function formatVehicleId(vehicleId) {
  try {
    if (typeof vehicleId !== 'string') {
      throw new Error('vehicleId must be a string');
    }
    return vehicleId.replace('fleet-NR-', 'NR#');
  } catch (err) {
    console.error(err);
    throw new Error(`[formatVehicleId] failed: ${err.message}`, { cause: err });
  }
}

/**
 * Normalize a free-text region label to the canonical set.
 *
 * @param {string} region - Free-text region label (`"west"`, `"us-east-1"`, etc.).
 * @returns {string} One of `"us-west"`, `"us-east"`, `"eu-central"`.
 * @throws {Error} If the region is not recognized.
 */
function normalizeRegion(region) {
  try {
    if (typeof region !== 'string') {
      throw new Error('region must be a string');
    }
    const r = region.trim().toLowerCase();
    if (r.startsWith('us-west') || r === 'west') return 'us-west';
    if (r.startsWith('us-east') || r === 'east') return 'us-east';
    if (r.startsWith('eu') || r === 'europe') return 'eu-central';
    throw new Error(`unknown region "${region}"`);
  } catch (err) {
    console.error(err);
    throw new Error(`[normalizeRegion] failed: ${err.message}`, { cause: err });
  }
}

/**
 * Compute whole days since the given ISO 8601 date string.
 *
 * @param {string} isoDate - ISO 8601 date string.
 * @returns {number} Whole days elapsed since the given date.
 * @throws {Error} If the date string is not parseable.
 */
function daysSince(isoDate) {
  try {
    const then = new Date(isoDate);
    if (Number.isNaN(then.getTime())) {
      throw new Error(`invalid date "${isoDate}"`);
    }
    const ms = Date.now() - then.getTime();
    return Math.floor(ms / (1000 * 60 * 60 * 24));
  } catch (err) {
    console.error(err);
    throw new Error(`[daysSince] failed: ${err.message}`, { cause: err });
  }
}

module.exports = { formatVehicleId, normalizeRegion, daysSince };
