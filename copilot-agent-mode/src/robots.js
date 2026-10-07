// FleetBoard robots — in-memory roster used by the dispatch module.
// The `warehouseId` field name is intentional; the student renames it to `zoneId`
// in Exercise 1 of the Agent Mode & Developer Productivity lab (lab 1609, exercise 2584).

/** @type {{ id: string, warehouseId: string, status: string, batteryLevel: number }[]} */
const robots = [
  { id: 'FB-R-0001', warehouseId: 'wh-nr-01', status: 'active',   batteryLevel: 82 },
  { id: 'FB-R-0002', warehouseId: 'wh-nr-01', status: 'charging', batteryLevel: 24 },
  { id: 'FB-R-0003', warehouseId: 'wh-nr-01', status: 'active',   batteryLevel: 61 },
  { id: 'FB-R-0004', warehouseId: 'wh-nr-02', status: 'active',   batteryLevel: 93 },
  { id: 'FB-R-0005', warehouseId: 'wh-nr-02', status: 'offline',  batteryLevel:  0 },
  { id: 'FB-R-0006', warehouseId: 'wh-nr-02', status: 'active',   batteryLevel: 48 },
  { id: 'FB-R-0007', warehouseId: 'wh-nr-03', status: 'maintenance', batteryLevel: 15 },
  { id: 'FB-R-0008', warehouseId: 'wh-nr-03', status: 'active',   batteryLevel: 71 },
];

function getAll() {
  return robots;
}

function getByWarehouse(warehouseId) {
  return robots.filter(r => r.warehouseId === warehouseId);
}

module.exports = { robots, getAll, getByWarehouse };
