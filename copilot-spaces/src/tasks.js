const express = require('express');
const router = express.Router();
let tasks = [
  { id: 1, title: "Set up CI/CD pipeline", status: "done", priority: "high", assigneeId: 1 },
  { id: 2, title: "Design database schema", status: "in-progress", priority: "high", assigneeId: 2 },
  { id: 3, title: "Implement user auth", status: "todo", priority: "critical", assigneeId: 1 },
];
router.get('/', (req, res) => res.json(tasks));
router.get('/:id', (req, res) => {
  const task = tasks.find(t => t.id === parseInt(req.params.id));
  task ? res.json(task) : res.status(404).json({ error: "Task not found" });
});
module.exports = router;
