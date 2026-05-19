const fs = require('fs');
const path = require('path');
const { build, version } = require('../src/app');

const dist = path.join(__dirname, '..', 'dist');
fs.mkdirSync(dist, { recursive: true });

const result = build();
fs.writeFileSync(path.join(dist, 'build.json'), JSON.stringify({ version, ...result }, null, 2));
fs.writeFileSync(path.join(dist, 'build.txt'), `Built ${result.ts}\n`);

console.log(`Build complete: dist/ contains build.json + build.txt (version ${version})`);
