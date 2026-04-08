// ForgeBoard Legacy Task Module - Uses callbacks (needs modernization to async/await)
// This module simulates asynchronous operations using setTimeout to mimic real I/O latency.
// The callback convention used here is the Node.js standard: callback(error, result)
// where error is null on success and result is null on failure.

var tasks = [
  { id: 1, title: 'Set up CI/CD',    status: 'done',        priority: 'high',     createdAt: '2026-01-15' },
  { id: 2, title: 'Database schema', status: 'in-progress', priority: 'high',     createdAt: '2026-01-20' },
  { id: 3, title: 'User auth',       status: 'todo',        priority: 'critical', createdAt: '2026-02-01' },
];
var nextId = 4;

function getTask(id, callback) {
  setTimeout(function() {
    var task = tasks.find(function(t) { return t.id === id; }) || null;
    callback(null, task);
  }, 50);
}

function getAllTasks(callback) {
  setTimeout(function() {
    callback(null, tasks.slice());
  }, 50);
}

function createTask(data, callback) {
  setTimeout(function() {
    if (!data || !data.title) {
      callback(new Error('Title is required'), null);
      return;
    }
    var task = {
      id: nextId++,
      title: data.title,
      status: data.status || 'todo',
      priority: data.priority || 'medium',
      createdAt: new Date().toISOString().split('T')[0]
    };
    tasks.push(task);
    callback(null, task);
  }, 50);
}

function updateTask(id, updates, callback) {
  setTimeout(function() {
    var task = tasks.find(function(t) { return t.id === id; });
    if (!task) {
      callback(new Error('Task not found: ' + id), null);
      return;
    }
    if (updates.title !== undefined) task.title = updates.title;
    if (updates.status !== undefined) task.status = updates.status;
    if (updates.priority !== undefined) task.priority = updates.priority;
    callback(null, task);
  }, 50);
}

function deleteTask(id, callback) {
  setTimeout(function() {
    var index = tasks.findIndex(function(t) { return t.id === id; });
    if (index === -1) {
      callback(new Error('Task not found: ' + id), null);
      return;
    }
    tasks.splice(index, 1);
    callback(null, true);
  }, 50);
}

module.exports = { getTask, getAllTasks, createTask, updateTask, deleteTask };
