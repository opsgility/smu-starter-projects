// ForgeBoard Tasks Module - In-memory task storage

let tasks = [
  { id: 1, title: 'Set up project structure', priority: 'high', status: 'done' },
  { id: 2, title: 'Build API endpoints', priority: 'high', status: 'in-progress' },
  { id: 3, title: 'Write unit tests', priority: 'medium', status: 'todo' },
];

let nextId = 4;

function getAll() {
  return tasks;
}

function getById(id) {
  return tasks.find(t => t.id === id);
}

function create(title, priority) {
  const task = { id: nextId++, title, priority: priority || 'medium', status: 'todo' };
  tasks.push(task);
  return task;
}

function update(id, updates) {
  const task = getById(id);
  if (!task) return null;
  Object.assign(task, updates);
  return task;
}

function remove(id) {
  const idx = tasks.findIndex(t => t.id === id);
  if (idx === -1) return false;
  tasks.splice(idx, 1);
  return true;
}

module.exports = { getAll, getById, create, update, remove };
