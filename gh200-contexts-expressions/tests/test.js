const { greet } = require('../src/app');
const out = greet('world', 'staging');
if (out !== 'Hello world from staging') {
  console.error(`greet failed: ${out}`);
  process.exit(1);
}
console.log('All tests passed');
