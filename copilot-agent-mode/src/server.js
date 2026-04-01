const express = require('express');
const db = require('./database');
const app = express();
app.use(express.json());
app.get('/api/tasks', (req, res) => { const tasks = db.prepare('SELECT * FROM tasks').all(); res.json(tasks); });
app.get('/api/tasks/:id', (req, res) => { const task = db.prepare('SELECT * FROM tasks WHERE id = ?').get(req.params.id); task ? res.json(task) : res.status(404).json({ error: "Not found" }); });
app.post('/api/tasks', (req, res) => { const { title, description, status, priority } = req.body; const result = db.prepare('INSERT INTO tasks (title, description, status, priority) VALUES (?, ?, ?, ?)').run(title, description, status || 'todo', priority || 'medium'); res.status(201).json({ id: result.lastInsertRowid, ...req.body }); });
app.listen(3000, () => console.log('ForgeBoard on port 3000'));
