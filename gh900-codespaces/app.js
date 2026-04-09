// Simple Node.js app — your starting point in the Codespace
// This Codespace is pre-configured with Node.js 18 and the GitHub CLI

const os = require('os');

function getEnvironmentInfo() {
    return {
        platform: os.platform(),
        nodeVersion: process.version,
        hostname: os.hostname(),
        homeDir: os.homedir()
    };
}

const info = getEnvironmentInfo();
console.log('Running in environment:');
console.log(`  Platform:     ${info.platform}`);
console.log(`  Node.js:      ${info.nodeVersion}`);
console.log(`  Hostname:     ${info.hostname}`);
console.log(`  Home dir:     ${info.homeDir}`);
console.log('\nYour Codespace is ready!');
