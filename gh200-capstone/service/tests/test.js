const { tick, droneState } = require('../src/index');
const { computeBattery } = require('../src/telemetry');

if (typeof droneState.batteryPercent !== 'number') {
  console.error('Expected battery percent to be a number');
  process.exit(1);
}

const afterTick = tick();
if (afterTick.batteryPercent >= 100) {
  console.error('Expected battery to decrease after tick');
  process.exit(1);
}

if (computeBattery(0) !== 0) {
  console.error('Expected battery floor at 0');
  process.exit(1);
}

console.log('All tests passed');
