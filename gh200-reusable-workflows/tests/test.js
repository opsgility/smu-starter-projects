const { compute } = require('../src/app');
if (compute(21) !== 42) { process.exit(1); }
console.log('All tests passed');
