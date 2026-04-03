const express = require('express');
const router = express.Router();

let tasks = [
  { id: 1, title: "Implement search", status: "todo", priority: "high", createdAt: "2026-01-15T09:00:00.000Z" },
  { id: 2, title: "Add pagination", status: "todo", priority: "medium", createdAt: "2026-01-20T10:00:00.000Z" },
  { id: 3, title: "Write API docs", status: "in-progress", priority: "low", createdAt: "2026-02-01T08:00:00.000Z" },
];
let nextId = 4;

// GET all tasks
router.get('/', (req, res) => res.json(tasks));

// GET task by ID
router.get('/:id', (req, res) => {
  const task = tasks.find(t => t.id === parseInt(req.params.id));
  // BUG: returns 200 with empty body instead of 404 when task not found
  res.json(task);
});

// POST create task
router.post('/', (req, res) => {
  // BUG: no input validation — missing title check, status defaults, etc.
  const task = { id: nextId++, ...req.body, createdAt: new Date().toISOString() };
  tasks.push(task);
  // BUG: returns 200 instead of 201 Created
  res.json(task);
});

// PUT update task
router.put('/:id', (req, res) => {
  const idx = tasks.findIndex(t => t.id === parseInt(req.params.id));
  if (idx === -1) return res.status(404).json({ error: "Not found" });
  // BUG: overwrites entire task including id — should merge only changed fields
  tasks[idx] = { ...req.body, id: parseInt(req.params.id) };
  res.json(tasks[idx]);
});

// DELETE task
router.delete('/:id', (req, res) => {
  const idx = tasks.findIndex(t => t.id === parseInt(req.params.id));
  // BUG: returns 200 success even when task was not found
  if (idx !== -1) tasks.splice(idx, 1);
  res.json({ message: "Deleted" });
});

module.exports = router;
