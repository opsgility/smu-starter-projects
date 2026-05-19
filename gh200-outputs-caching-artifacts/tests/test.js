const { build, version } = require('../src/app');
if (version !== '1.0.0') { process.exit(1); }
const result = build();
if (!result.ok) { process.exit(1); }
console.log('All tests passed');
