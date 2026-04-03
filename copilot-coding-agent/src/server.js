const express = require('express');
const app = express();
app.use(express.json());
const tasks = require('./tasks');

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

app.listen(3000, () => console.log('ForgeBoard on port 3000'));
