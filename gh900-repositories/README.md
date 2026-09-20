# Markdown Note Taker

A simple command-line tool for creating and organizing markdown notes.

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Node.js](https://img.shields.io/badge/Node.js-18%2B-green.svg)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)

## Features

- Create notes with titles that auto-generate filenames
- Notes saved in clean Markdown format
- Lightweight with no external dependencies

## Prerequisites

- [Node.js](https://nodejs.org/) version 18 or higher

## Usage

```javascript
const { createNote } = require('./app');
createNote('Meeting Notes', 'Discussed project timeline and deliverables.');
```

## Project Structure

```
markdown-note-taker/
├── app.js              # Main application logic
├── README.md           # Project documentation
├── LICENSE             # MIT License
├── CONTRIBUTING.md     # Contribution guidelines
└── .gitignore          # Git ignore rules
```

## What You Will Do

In the exercises you will build a professional repository structure around this app:
- Write a detailed README with badges and usage examples (this file is your starting point)
- Add an MIT LICENSE file
- Create a CONTRIBUTING.md with guidelines for contributors
- Add a comprehensive `.gitignore` for Node.js projects
- Push to GitHub with `gh repo create`
- Add advanced files: CODEOWNERS, SECURITY.md, and issue templates in `.github/`

## Contributing

Contributions are welcome! Please read CONTRIBUTING.md for guidelines.

## License

This project is licensed under the MIT License — see the LICENSE file for details.
