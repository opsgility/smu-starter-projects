const VALID_STATUSES = ['open', 'in-progress', 'in-review', 'done'];

let nextId = 4;
let tasks = [
  { id: 1, title: 'Set up CI/CD',    status: 'done',        priority: 'high',     createdAt: new Date('2026-01-10T09:00:00Z'), comments: [] },
  { id: 2, title: 'Database schema', status: 'in-progress', priority: 'high',     createdAt: new Date('2026-01-12T14:30:00Z'), comments: [] },
  { id: 3, title: 'User auth',       status: 'open',        priority: 'critical', createdAt: new Date('2026-01-15T08:00:00Z'), comments: [] },
];

// BUG: returns undefined instead of null when task not found (should return null, not undefined)
function getAll() {
  return tasks;
}

function getById(id) {
  const task = tasks.find(t => t.id === id);
  return task; // BUG: when task is not found, find() returns undefined — caller gets undefined instead of null
}

// BUG: missing input validation — title is not checked for empty/null before creating the task
function create(title, status, priority) {
  // BUG: no check that title is a non-empty string; null/undefined titles are silently accepted
  const task = {
    id: nextId++,
    title,
    status: status || 'open',
    priority: priority || 'medium',
    createdAt: new Date(),
    comments: [],
  };
  tasks.push(task);
  return task;
}

// BUG: overwrites the entire task object instead of merging updates (loses fields not present in updates)
function update(id, updates) {
  const index = tasks.findIndex(t => t.id === id);
  if (index === -1) return null;
  // BUG: replaces the task entirely instead of merging; fields omitted from updates are lost
  tasks[index] = { id, ...updates };
  return tasks[index];
}

// BUG: silently succeeds even when the task ID doesn't exist
function remove(id) {
  const index = tasks.findIndex(t => t.id === id);
  // BUG: when index is -1, splice(-1, 1) removes the last element instead of detecting a missing task
  tasks.splice(index, 1);
  return true;
}

// updateTask validates status against VALID_STATUSES but intentionally allows any valid
// status → any valid status transition (no state machine enforcement).
function updateTask(id, status) {
  if (!VALID_STATUSES.includes(status)) {
    return { error: `Invalid status. Must be one of: ${VALID_STATUSES.join(', ')}` };
  }
  const task = tasks.find(t => t.id === id);
  if (!task) return null;
  task.status = status;
  return task;
}

module.exports = { VALID_STATUSES, getAll, getById, create, update, remove, updateTask };
