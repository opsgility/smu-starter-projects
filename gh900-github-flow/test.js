const { add, subtract } = require('./calculator');

console.log('Testing add:', add(2, 3) === 5 ? 'PASS' : 'FAIL');
console.log('Testing subtract:', subtract(5, 3) === 2 ? 'PASS' : 'FAIL');
