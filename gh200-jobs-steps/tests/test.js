const { add } = require('../src/app');
if (add(2, 3) !== 5) { console.error('add failed'); process.exit(1); }
console.log('All tests passed');
