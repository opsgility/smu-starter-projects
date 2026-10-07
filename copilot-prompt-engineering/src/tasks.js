// FleetBoard Task Management Module — in-memory CRUD + state machine
// Status transitions live in docs/architecture.md and are enforced by updateTaskStatus.

const VALID_STATUSES = ['open', 'in-progress', 'in-review', 'done'];

// Allowed transitions. Any transition not listed here is rejected.
const ALLOWED_TRANSITIONS = {
  'open':        ['in-progress'],
  'in-progress': ['in-review', 'open'],
  'in-review':   ['done', 'in-progress'],
  'done':        ['in-progress'],
};

let nextId = 4;
let tasks = [
  { id: 1, title: 'Fix authentication bug',   priority: 'critical', status: 'done',        createdAt: new Date(Date.now() - 45 * 24 * 60 * 60 * 1000) },
  { id: 2, title: 'Implement task filtering', priority: 'high',     status: 'in-progress', createdAt: new Date(Date.now() - 10 * 24 * 60 * 60 * 1000) },
  { id: 3, title: 'Add user notifications',   priority: 'medium',   status: 'open',        createdAt: new Date() },
];

function getAll() {
  return tasks;
}

function getById(id) {
  return tasks.find(t => t.id === id) || null;
}

function create(title, priority) {
  const task = { id: nextId++, title, priority: priority || 'medium', status: 'open', createdAt: new Date() };
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

// Enforce the FleetBoard task state machine from docs/architecture.md.
// Returns the updated task, or throws if the transition is not allowed.
function updateTaskStatus(id, newStatus) {
  if (!VALID_STATUSES.includes(newStatus)) {
    throw new Error(`Invalid status: ${newStatus}. Valid: ${VALID_STATUSES.join(', ')}`);
  }
  const task = getById(id);
  if (!task) throw new Error(`Task ${id} not found`);
  const allowed = ALLOWED_TRANSITIONS[task.status] || [];
  if (!allowed.includes(newStatus)) {
    throw new Error(`Illegal transition ${task.status} → ${newStatus}. Allowed from ${task.status}: ${allowed.join(', ') || '(none)'}`);
  }
  task.status = newStatus;
  return task;
}

module.exports = { VALID_STATUSES, ALLOWED_TRANSITIONS, getAll, getById, create, update, remove, updateTaskStatus };
