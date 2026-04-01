const express = require('express');
const app = express();
app.use(express.json());
const tasks = require('./tasks');
app.get('/api/tasks', (req, res) => res.json(tasks.getAll()));
app.get('/api/tasks/:id', (req, res) => {
  const task = tasks.getById(parseInt(req.params.id));
  task ? res.json(task) : res.status(404).json({ error: "Not found" });
});
app.listen(3000, () => console.log('ForgeBoard API on port 3000'));
