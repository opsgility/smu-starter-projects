const { compute } = require('../src/app');
if (compute(5) !== 10) { process.exit(1); }
console.log('All tests passed');
