// FleetBoard tracking API — vehicles router
// Student extends this file in the Copilot on GitHub.com exercises.

const express = require('express');
const router = express.Router();

// Seed vehicles for the FleetBoard operator dashboard
const vehicles = [
  { id: 1, plate: 'FB-NR-1001', region: 'us-west',    status: 'active' },
  { id: 2, plate: 'FB-NR-1002', region: 'us-west',    status: 'maintenance' },
  { id: 3, plate: 'FB-NR-1003', region: 'us-east',    status: 'active' },
  { id: 4, plate: 'FB-NR-1004', region: 'eu-central', status: 'active' },
];

// Seed position samples (last 24h), newest first per vehicle
const positionLog = [
  { vehicleId: 1, lat: 47.6062, lng: -122.3321, timestamp: Date.now() -   2 * 60 * 1000 },
  { vehicleId: 1, lat: 47.6050, lng: -122.3300, timestamp: Date.now() -  12 * 60 * 1000 },
  { vehicleId: 1, lat: 47.6039, lng: -122.3285, timestamp: Date.now() -  22 * 60 * 1000 },
  { vehicleId: 2, lat: 47.6097, lng: -122.3331, timestamp: Date.now() -   5 * 60 * 1000 },
  { vehicleId: 2, lat: 47.6100, lng: -122.3340, timestamp: Date.now() -  15 * 60 * 1000 },
  { vehicleId: 3, lat: 40.7128, lng:  -74.0060, timestamp: Date.now() -   7 * 60 * 1000 },
  { vehicleId: 4, lat: 50.1109, lng:    8.6821, timestamp: Date.now() -   3 * 60 * 1000 },
];

// Seed telemetry snapshots (one per vehicle)
const telemetryLog = [
  { vehicleId: 1, batteryLevel: 82, speedKph:  0, lastSeen: Date.now() -   2 * 60 * 1000 },
  { vehicleId: 2, batteryLevel: 41, speedKph:  0, lastSeen: Date.now() -   5 * 60 * 1000 },
  { vehicleId: 3, batteryLevel: 67, speedKph: 32, lastSeen: Date.now() -   7 * 60 * 1000 },
  { vehicleId: 4, batteryLevel: 94, speedKph:  0, lastSeen: Date.now() -   3 * 60 * 1000 },
];

// GET /api/vehicles — list all vehicles
router.get('/', (req, res) => res.json(vehicles));

// GET /api/vehicles/:id — fetch a single vehicle, 404 if missing
router.get('/:id', (req, res) => {
  const id = parseInt(req.params.id, 10);
  const vehicle = vehicles.find(v => v.id === id);
  if (!vehicle) return res.status(404).json({ error: `Vehicle ${id} not found` });
  res.json(vehicle);
});

module.exports = router;
