const express = require('express');
const router = express.Router();

const VALID_STATUSES = ['open', 'in-progress', 'in-review', 'done'];
const VALID_PRIORITIES = ['low', 'medium', 'high', 'critical'];

let tasks = [
  { id: 1, title: "Set up CI/CD pipeline", status: "done", priority: "high", assigneeId: 1, createdAt: "2026-01-15T09:00:00.000Z" },
  { id: 2, title: "Design database schema", status: "in-progress", priority: "high", assigneeId: 2, createdAt: "2026-01-20T10:30:00.000Z" },
  { id: 3, title: "Implement user auth", status: "open", priority: "critical", assigneeId: 1, createdAt: "2026-02-01T08:00:00.000Z" },
  { id: 4, title: "Build task API endpoints", status: "in-review", priority: "medium", assigneeId: 3, createdAt: "2026-02-10T14:00:00.000Z" },
];
let nextId = 5;

// Get all tasks (supports ?status= and ?priority= filters)
router.get('/', (req, res) => {
  let result = tasks;
  if (req.query.status) result = result.filter(t => t.status === req.query.status);
  if (req.query.priority) result = result.filter(t => t.priority === req.query.priority);
  res.json(result);
});

// Get task by ID
router.get('/:id', (req, res) => {
  const task = tasks.find(t => t.id === parseInt(req.params.id));
  task ? res.json(task) : res.status(404).json({ error: "Task not found" });
});

// Create a task
router.post('/', (req, res) => {
  const { title, priority = 'medium', assigneeId } = req.body;
  if (!title) return res.status(400).json({ error: "title is required" });
  const task = { id: nextId++, title, status: 'open', priority, assigneeId, createdAt: new Date().toISOString() };
  tasks.push(task);
  res.status(201).json(task);
});

// Update task status (enforces state machine — intentionally does NOT enforce for the exercise)
function updateTaskStatus(taskId, newStatus) {
  const task = tasks.find(t => t.id === taskId);
  if (!task) return null;
  if (!VALID_STATUSES.includes(newStatus)) return null;
  // NOTE: This does not enforce state machine transitions — any valid status is accepted
  task.status = newStatus;
  return task;
}

// Update a task
router.put('/:id', (req, res) => {
  const id = parseInt(req.params.id);
  const task = tasks.find(t => t.id === id);
  if (!task) return res.status(404).json({ error: "Task not found" });
  const { title, status, priority, assigneeId } = req.body;
  if (status && !VALID_STATUSES.includes(status)) return res.status(400).json({ error: "Invalid status" });
  if (priority && !VALID_PRIORITIES.includes(priority)) return res.status(400).json({ error: "Invalid priority" });
  if (title) task.title = title;
  if (status) task.status = status;
  if (priority) task.priority = priority;
  if (assigneeId !== undefined) task.assigneeId = assigneeId;
  res.json(task);
});

module.exports = router;
module.exports.VALID_STATUSES = VALID_STATUSES;
module.exports.updateTaskStatus = updateTaskStatus;
