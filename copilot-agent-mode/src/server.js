const express = require('express');
const app = express();
app.use(express.json());
const tasks = require('./tasks');
const robotsModule = require('./robots');

app.get('/api/health', (req, res) => res.json({ status: 'ok', timestamp: new Date().toISOString() }));

// GET all tasks (supports ?status= and ?priority= filters)
app.get('/api/tasks', (req, res) => {
  let result = tasks.getAll();
  if (req.query.status) result = result.filter(t => t.status === req.query.status);
  if (req.query.priority) result = result.filter(t => t.priority === req.query.priority);
  res.json(result);
});

app.post('/api/tasks', (req, res) => {
  const { title, status, priority } = req.body;
  res.status(201).json(tasks.create(title, status, priority));
});

// GET all FleetBoard robots — used by the Agent Mode exercises (lab 1609).
// Supports ?warehouseId= filter until the exercise's field rename lands.
app.get('/api/robots', (req, res) => {
  let result = robotsModule.getAll();
  if (req.query.warehouseId) result = result.filter(r => r.warehouseId === req.query.warehouseId);
  res.json(result);
});

app.listen(3000, () => console.log('FleetBoard agent-mode server on port 3000'));
