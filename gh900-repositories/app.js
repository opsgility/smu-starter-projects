// Markdown Note Taker
// A simple tool for creating and organizing markdown notes
const fs = require('fs');

function createNote(title, content) {
    const filename = title.toLowerCase().replace(/\s+/g, '-') + '.md';
    const markdown = `# ${title}\n\n${content}\n`;
    fs.writeFileSync(filename, markdown);
    console.log(`Note saved: ${filename}`);
}

module.exports = { createNote };
