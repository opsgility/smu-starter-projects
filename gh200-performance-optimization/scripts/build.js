const fs = require('fs');
fs.mkdirSync('dist', { recursive: true });
fs.writeFileSync('dist/app.txt', `Built ${new Date().toISOString()}\n`);
console.log('Build complete');
