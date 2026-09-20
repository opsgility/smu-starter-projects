let nextId = 4;
let tasks = [
  { id: 1, title: "Set up CI/CD", description: "Configure GitHub Actions", status: "done", priority: "high", assigneeId: 1, createdAt: new Date("2026-01-15") },
  { id: 2, title: "Database schema", description: "Design the initial schema", status: "in-progress", priority: "high", assigneeId: 2, createdAt: new Date("2026-01-20") },
  { id: 3, title: "User auth", description: "Implement JWT authentication", status: "open", priority: "critical", assigneeId: 1, createdAt: new Date("2026-02-01") },
];
module.exports = {
  getAll: () => tasks,
  getById: (id) => tasks.find(t => t.id === id),
  create: (task) => { task.id = nextId++; task.createdAt = new Date(); tasks.push(task); return task; },
  update: (id, data) => { const t = tasks.find(t => t.id === id); if (t) Object.assign(t, data); return t; },
  remove: (id) => { tasks = tasks.filter(t => t.id !== id); }
};
