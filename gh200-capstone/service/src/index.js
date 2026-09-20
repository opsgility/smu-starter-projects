const { computePosition, computeBattery } = require('./telemetry');

const droneState = {
  position: { lat: 47.6062, lng: -122.3321, alt: 120 },
  batteryPercent: 100,
};

function tick() {
  droneState.position = computePosition(droneState.position);
  droneState.batteryPercent = computeBattery(droneState.batteryPercent);
  return droneState;
}

module.exports = { tick, droneState };

if (require.main === module) {
  console.log('Initial state:', JSON.stringify(droneState));
  for (let i = 0; i < 3; i++) console.log('Tick:', JSON.stringify(tick()));
}
