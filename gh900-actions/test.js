const { add, multiply } = require('./app');

let passed = 0;
let failed = 0;

function test(name, condition) {
    if (condition) {
        console.log(`  PASS: ${name}`);
        passed++;
    } else {
        console.log(`  FAIL: ${name}`);
        failed++;
    }
}

console.log('Running tests...\n');
test('add(2, 3) equals 5', add(2, 3) === 5);
test('add(-1, 1) equals 0', add(-1, 1) === 0);
test('multiply(3, 4) equals 12', multiply(3, 4) === 12);
test('multiply(0, 5) equals 0', multiply(0, 5) === 0);

console.log(`\nResults: ${passed} passed, ${failed} failed`);
process.exit(failed > 0 ? 1 : 0);
