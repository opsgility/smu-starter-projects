// FleetBoard dispatch — picks the next robot to send based on a short-lived cache.
// The student uses this file for Ask / Edit / Agent-mode practice in exercise 2584
// (lab 1609, "Agent Mode & Developer Productivity").

const { robots } = require('./robots');

const DISPATCH_TTL_SECONDS = 30;

// In-memory cache of recent dispatch snapshots, keyed by warehouseId.
// Entries older than DISPATCH_TTL_SECONDS are considered stale.
const robotCache = new Map();

function cacheEntry(warehouseId) {
  const entry = robotCache.get(warehouseId);
  if (!entry) return null;
  const ageSeconds = (Date.now() - entry.cachedAt) / 1000;
  if (ageSeconds > DISPATCH_TTL_SECONDS) return null;
  return entry;
}

function refreshCache(warehouseId) {
  const snapshot = robots.filter(r => r.warehouseId === warehouseId);
  const entry = { cachedAt: Date.now(), snapshot };
  robotCache.set(warehouseId, entry);
  return entry;
}

// Pick the next robot to dispatch from the given warehouse.
// Only `active` robots are eligible; the pick with the highest batteryLevel wins.
// Returns null when no eligible robot exists in that warehouse.
function dispatchNextRobot(warehouseId) {
  const entry = cacheEntry(warehouseId) || refreshCache(warehouseId);
  const eligible = entry.snapshot
    .filter(r => r.status === 'active')
    .sort((a, b) => b.batteryLevel - a.batteryLevel);
  return eligible[0] || null;
}

module.exports = { dispatchNextRobot, DISPATCH_TTL_SECONDS, robotCache };
