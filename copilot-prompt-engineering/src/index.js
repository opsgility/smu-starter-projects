// FleetBoard prompt-engineering starter — minimal HTTP server over the data modules.
// Boots the three read endpoints the Copilot Space exercise asks the student to call:
//   GET /api/tasks        → tasks.getAll()
//   GET /api/tasks/:id    → tasks.getById(id)
//   GET /api/users        → users.getAll()
// Students extend behaviour (filtering, role-aware responses, state-transition routes)
// inside the Copilot Space; the server itself stays tiny on purpose.

const express = require('express');
const tasks = require('./tasks');
const users = require('./users');

const app = express();
app.use(express.json());

app.get('/api/tasks', (req, res) => res.json(tasks.getAll()));

app.get('/api/tasks/:id', (req, res) => {
  const id = Number.parseInt(req.params.id, 10);
  if (!Number.isInteger(id)) return res.status(400).json({ error: 'id must be an integer' });
  const task = tasks.getById(id);
  if (!task) return res.status(404).json({ error: `Task ${id} not found` });
  res.json(task);
});

app.get('/api/users', (req, res) => res.json(users.getAll()));

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`FleetBoard prompt-engineering API listening on http://localhost:${PORT}`);
  console.log('Try:  curl http://localhost:3000/api/tasks');
});
