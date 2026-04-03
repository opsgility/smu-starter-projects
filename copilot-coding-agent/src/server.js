const express = require('express');
const app = express();
app.use(express.json());
const tasks = require('./tasks');
app.get('/api/health', (req, res) => res.json({ status: 'ok', timestamp: new Date().toISOString() }));
app.get('/api/tasks', (req, res) => res.json(tasks.getAll()));
app.post('/api/tasks', (req, res) => res.status(201).json(tasks.create(req.body)));
app.listen(3000, () => console.log('ForgeBoard on port 3000'));
