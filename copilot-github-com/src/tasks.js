const express = require('express');
const router = express.Router();
let tasks = [
  { id: 1, title: "Implement search", status: "todo", priority: "high" },
  { id: 2, title: "Add pagination", status: "todo", priority: "medium" },
];
let nextId = 3;
router.get('/', (req, res) => res.json(tasks));
router.post('/', (req, res) => {
  const task = { id: nextId++, ...req.body, createdAt: new Date() };
  // BUG: no input validation
  tasks.push(task);
  res.status(201).json(task);
});
router.put('/:id', (req, res) => {
  const idx = tasks.findIndex(t => t.id === parseInt(req.params.id));
  if (idx === -1) return res.status(404).json({ error: "Not found" });
  // BUG: allows overwriting id
  tasks[idx] = { ...tasks[idx], ...req.body };
  res.json(tasks[idx]);
});
module.exports = router;
