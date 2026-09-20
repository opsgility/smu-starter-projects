// ForgeBoard Task Management Module
// In-memory storage with CRUD operations

let nextId = 4;
let tasks = [
  { id: 1, title: 'Fix authentication bug', priority: 'critical', status: 'done',        createdAt: new Date(Date.now() - 45 * 24 * 60 * 60 * 1000) },
  { id: 2, title: 'Implement task filtering', priority: 'high',     status: 'in-progress', createdAt: new Date(Date.now() - 10 * 24 * 60 * 60 * 1000) },
  { id: 3, title: 'Add user notifications',  priority: 'medium',   status: 'todo',        createdAt: new Date() },
];

function getAll() {
  return tasks;
}

function getById(id) {
  return tasks.find(t => t.id === id) || null;
}

function create(title, priority) {
  const task = { id: nextId++, title, priority: priority || 'medium', status: 'todo', createdAt: new Date() };
  tasks.push(task);
  return task;
}

function update(id, updates) {
  const task = tasks.find(t => t.id === id);
  if (!task) return null;
  Object.assign(task, updates);
  return task;
}

function remove(id) {
  tasks = tasks.filter(t => t.id !== id);
}

module.exports = { getAll, getById, create, update, remove };
