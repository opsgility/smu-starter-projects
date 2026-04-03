const express = require('express');
const taskService = require('./task-service');

const app = express();
app.use(express.json());

// GET /api/tasks - list all tasks
app.get('/api/tasks', (req, res) => {
  res.json(taskService.gt());
});

// GET /api/tasks/:id - get task by id
app.get('/api/tasks/:id', (req, res) => {
  const task = taskService.gbi(parseInt(req.params.id));
  if (!task) return res.status(404).json({ error: 'Task not found' });
  res.json(task);
});

// POST /api/tasks - create a task
app.post('/api/tasks', (req, res) => {
  const task = taskService.ct(req.body);
  res.status(201).json(task);
});

// PUT /api/tasks/:id - update a task
app.put('/api/tasks/:id', (req, res) => {
  const task = taskService.ut(parseInt(req.params.id), req.body);
  if (!task) return res.status(404).json({ error: 'Task not found' });
  res.json(task);
});

// DELETE /api/tasks/:id - remove a task
app.delete('/api/tasks/:id', (req, res) => {
  const removed = taskService.dt(parseInt(req.params.id));
  if (!removed) return res.status(404).json({ error: 'Task not found' });
  res.status(204).send();
});

app.listen(3000, () => {
  console.log('ForgeBoard running on port 3000');
});
