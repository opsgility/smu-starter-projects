// FleetBoard productivity service — Express entry point.
// Legacy wiring: every call site hits the cryptic function names
// exported from task-service. Refactor target for Copilot practice:
// rename the calls after task-service exports change in Exercise 3.

const express = require('express');
const taskService = require('./task-service');

const app = express();
app.use(express.json());
const port = 3000;

app.get('/api/tasks', (req, res) => {
  res.json(taskService.gt());
});

app.get('/api/tasks/:id', (req, res) => {
  try {
    const task = taskService.gbi(parseInt(req.params.id, 10));
    res.json(task);
  } catch (err) {
    res.status(404).json({ error: err.message });
  }
});

app.post('/api/tasks', (req, res) => {
  const task = taskService.ct(req.body);
  res.status(201).json(task);
});

app.put('/api/tasks/:id', (req, res) => {
  try {
    const task = taskService.ut(parseInt(req.params.id, 10), req.body);
    res.json(task);
  } catch (err) {
    res.status(404).json({ error: err.message });
  }
});

app.delete('/api/tasks/:id', (req, res) => {
  try {
    taskService.dt(parseInt(req.params.id, 10));
    res.status(204).end();
  } catch (err) {
    res.status(404).json({ error: err.message });
  }
});

app.get('/api/tasks/status/:status', (req, res) => {
  res.json(taskService.fbs(req.params.status));
});

app.get('/api/tasks/priority/:priority', (req, res) => {
  res.json(taskService.fbp(req.params.priority));
});

app.listen(port, () => {
  console.log(`FleetBoard productivity service listening on port ${port}`);
});
