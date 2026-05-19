const fs = require('fs');
const path = require('path');

const dist = path.join(__dirname, '..', 'dist');
fs.mkdirSync(dist, { recursive: true });

// Bundle minimally — copy src + add a build manifest
const src = path.join(__dirname, '..', 'src');
fs.cpSync(src, path.join(dist, 'src'), { recursive: true });
fs.writeFileSync(
  path.join(dist, 'build.json'),
  JSON.stringify({ builtAt: new Date().toISOString(), commit: process.env.GITHUB_SHA || 'local' }, null, 2)
);

console.log('Build complete — dist/ contains src/ + build.json');
