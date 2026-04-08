const express = require('express');
const app = express();
app.use(express.json());
const tasks = require('./tasks');

// Health check
app.get('/api/health', (req, res) => res.json({ status: 'ok' }));

// GET all tasks
app.get('/api/tasks', (req, res) => res.json(tasks.getAll()));

// POST create task
app.post('/api/tasks', (req, res) => {
  const { title, description, status, priority } = req.body;
  const task = tasks.create({ title, description, status, priority });
  res.status(201).json(task);
});

app.listen(3000, () => console.log('ForgeBoard API running on http://localhost:3000'));
